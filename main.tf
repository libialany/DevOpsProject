###############################################################################
# Gallery App – Infrastructure as Code
# AWS Modules: terraform-aws-modules (v6.33 compatible)
###############################################################################

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

###############################################################################
# 1. S3 BUCKET  (terraform-aws-modules/s3-bucket/aws  v4.x)
###############################################################################

module "gallery_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 4.0"

  bucket = var.bucket_name

  # Block ALL public access – images are served exclusively via CloudFront OAC
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  object_ownership = "BucketOwnerEnforced"

  versioning = {
    enabled = false
  }

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = local.tags
}

###############################################################################
# 2. BUCKET POLICY – allow CloudFront OAC + Lambda role
###############################################################################

data "aws_iam_policy_document" "gallery_bucket_policy" {
  statement {
    sid    = "AllowCloudFrontOAC"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    actions   = ["s3:GetObject"]
    resources = ["${module.gallery_bucket.s3_bucket_arn}/*"]

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [module.cloudfront.cloudfront_distribution_arn]
    }
  }

  statement {
    sid    = "AllowLambdaListObjects"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = [module.lambda_function.lambda_role_arn]
    }

    actions   = ["s3:ListBucket"]
    resources = [module.gallery_bucket.s3_bucket_arn]
  }

  statement {
    sid    = "AllowLambdaGetObject"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = [module.lambda_function.lambda_role_arn]
    }

    actions   = ["s3:GetObject"]
    resources = ["${module.gallery_bucket.s3_bucket_arn}/*"]
  }
}

resource "aws_s3_bucket_policy" "gallery" {
  bucket = module.gallery_bucket.s3_bucket_id
  policy = data.aws_iam_policy_document.gallery_bucket_policy.json

  depends_on = [
    module.cloudfront,
    module.lambda_function,
  ]
}

###############################################################################
# 3a. CLOUDFRONT OAC – native resource so we hold the concrete ID
#     Using the module's internal OAC map can leave origins unsigned (→ 403)
###############################################################################

resource "aws_cloudfront_origin_access_control" "gallery" {
  name                              = "${var.project_name}-gallery-oac"
  description                       = "Gallery S3 OAC – sigv4 signed"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

###############################################################################
# 3b. CLOUDFRONT DISTRIBUTION  (terraform-aws-modules/cloudfront/aws  v3.x)
###############################################################################

module "cloudfront" {
  source  = "terraform-aws-modules/cloudfront/aws"
  version = "~> 3.0"

  comment             = "Gallery App CDN"
  enabled             = true
  is_ipv6_enabled     = true
  price_class         = "PriceClass_100"
  wait_for_deployment = false

  # Pass the concrete OAC ID – avoids the module's internal name-lookup ambiguity
  origin = {
    gallery_s3 = {
      domain_name              = module.gallery_bucket.s3_bucket_bucket_regional_domain_name
      origin_id                = local.s3_origin_id
      origin_access_control_id = aws_cloudfront_origin_access_control.gallery.id
    }
  }

  default_cache_behavior = {
    target_origin_id       = local.s3_origin_id
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]

    use_forwarded_values = false
    cache_policy_id      = "658327ea-f89d-4fab-a63d-7e88639e58f6" # Managed-CachingOptimized

    compress = true
  }

  # No WAF as per requirements
  web_acl_id = null

  tags = local.tags
}

###############################################################################
# 4. LAMBDA FUNCTION  (terraform-aws-modules/lambda/aws  v7.x)
###############################################################################

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/handler.py"
  output_path = "${path.module}/lambda/handler.zip"
}

module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 7.0"

  function_name = "${var.project_name}-gallery-handler"
  description   = "Returns a list of CloudFront image URLs from S3"
  handler       = "handler.lambda_handler"
  runtime       = "python3.12"
  publish       = true

  source_path            = null
  create_package         = false
  local_existing_package = data.archive_file.lambda_zip.output_path

  environment_variables = {
    BUCKET_NAME       = module.gallery_bucket.s3_bucket_id
    CLOUDFRONT_DOMAIN = module.cloudfront.cloudfront_distribution_domain_name
    IMAGE_EXTENSIONS  = "jpg,jpeg,png,gif,webp,svg"
  }

  attach_policies   = true
  policies          = ["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"]
  number_of_policies = 1

  attach_policy_statements = true
  policy_statements = {
    list_bucket = {
      effect    = "Allow"
      actions   = ["s3:ListBucket"]
      resources = [module.gallery_bucket.s3_bucket_arn]
    }
    cloudfront_read = {
      effect  = "Allow"
      actions = [
        "cloudfront:GetDistribution",
        "cloudfront:ListDistributions",
      ]
      resources = ["*"]
    }
  }

  allowed_triggers = {
    APIGateway = {
      service    = "apigateway"
      source_arn = "${module.api_gateway.api_execution_arn}/*/*"
    }
  }

  tags = local.tags
}

###############################################################################
# 5. API GATEWAY (HTTP)  (terraform-aws-modules/apigateway-v2/aws  v5.x)
###############################################################################

module "api_gateway" {
  source  = "terraform-aws-modules/apigateway-v2/aws"
  version = "~> 5.0"

  name          = "${var.project_name}-gallery-api"
  description   = "Gallery App – HTTP API"
  protocol_type = "HTTP"

  cors_configuration = {
    allow_headers = ["Content-Type", "Authorization"]
    allow_methods = ["GET", "OPTIONS"]
    allow_origins = ["*"]
    max_age       = 300
  }

  # No custom domain – use the default execute-api endpoint only
  create_domain_name = false

  create_stage = true
  stage_name   = "$default"
#   auto_deploy  = true

  routes = {
    "GET /images" = {
      integration = {
        uri                    = module.lambda_function.lambda_function_invoke_arn
        type                   = "AWS_PROXY"
        payload_format_version = "2.0"
      }
    }
  }

  tags = local.tags
}

###############################################################################
# 6. WAF – Web ACL with rate-based rule, associated to API Gateway stage
#
# IMPORTANT NOTES:
#   • scope must be REGIONAL for API Gateway (CLOUDFRONT is only for CF distros)
#   • aws_wafv2_web_acl_association takes the stage ARN, not the API id
#   • AWS WAF minimum rate limit is 100 req / evaluation window – values below
#     100 are rejected by the API; 100 is used here as the closest valid value
#     to the desired 20 req/min intent.
#   • Evaluation window: 120 seconds (2 minutes) as requested.
###############################################################################

resource "aws_wafv2_web_acl" "gallery_api" {
  name        = "${var.project_name}-api-web-acl"
  description = "Rate-based protection for the Gallery API Gateway stage"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  rule {
    name     = "GalleryRateLimit"
    priority = 1

    action {
      block {}
    }

    statement {
      rate_based_statement {
        # Minimum accepted by AWS WAF; set as close to intent (20/min) as allowed
        limit                 = 100
        # evaluation_window_sec: 120 = 2 minutes (matches requirement)
        evaluation_window_sec = 120

        # Aggregate by originating IP address
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "GalleryRateLimit"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "${var.project_name}-api-web-acl"
    sampled_requests_enabled   = true
  }

  tags = local.tags
}

# Associate the Web ACL with the API Gateway $default stage
# Stage ARN format: arn:aws:apigateway:{region}::/apis/{api-id}/stages/{stage-name}
resource "aws_wafv2_web_acl_association" "gallery_api" {
  resource_arn = "arn:aws:apigateway:${var.aws_region}::/apis/${module.api_gateway.api_id}/stages/$default"
  web_acl_arn  = aws_wafv2_web_acl.gallery_api.arn

  depends_on = [module.api_gateway]
}
