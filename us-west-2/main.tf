data "aws_vpc" "default" {
  default = true
  provider = aws.west
}

data "aws_subnets" "default" {
  provider = aws.west
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_security_group" "alb_sg" {
  provider = aws.west
  name   = "alb-sg"
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "ec2_sg" {
  name   = "ec2-sg"
  provider = aws.west
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_instance" "web" {
  count                       = 2
  provider               = aws.west
  ami                         = "ami-XXX" # Replace with a valid AMI ID for us-west-2
  key_name                    = "demo"
  instance_type               = "t3.micro"
  subnet_id                   = data.aws_subnets.default.ids[count.index]
  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  associate_public_ip_address = true
  user_data = templatefile("${path.module}/user_data.sh", {
    nginx_conf  = file("${path.module}/nginx.conf")
    instance_id = count.index
    region_name = "WEST"
  })


  tags = {
    Name = "web-${count.index}"
  }
}

resource "aws_lb" "alb" {
  provider           = aws.west
  name               = "example-alb"
  load_balancer_type = "application"
  internal           = false
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = data.aws_subnets.default.ids
}

resource "aws_lb_target_group" "tg" {
  provider    = aws.west
  name        = "web-tg"
  port        = 80
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = data.aws_vpc.default.id

  health_check {
    path                = "/"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_target_group_attachment" "web" {
  provider        = aws.west
  count            = length(aws_instance.web)
  target_group_arn = aws_lb_target_group.tg.arn
  target_id        = aws_instance.web[count.index].id
  port             = 80
}

resource "aws_lb_listener" "http" {
  provider          = aws.west
  load_balancer_arn = aws_lb.alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.arn
  }
}


resource "aws_route53_health_check" "secondary_health_check" {
  fqdn = aws_lb.alb.dns_name
  type = "HTTP"
  resource_path = "/health"
  failure_threshold = 3
  request_interval  = 30
  port = 80
}

resource "aws_route53_record" "secondary_failover_record" {
  zone_id = "XXX" # Replace with your Route 53 zone ID
  name    = "demo"
  type    = "A"
  set_identifier = "secondary-alb"
  failover_routing_policy {
    type = "SECONDARY"
  }
  alias {
    name                   = aws_lb.alb.dns_name
    zone_id                = aws_lb.alb.zone_id
    evaluate_target_health = true
  }
  health_check_id = aws_route53_health_check.secondary_health_check.id
}
