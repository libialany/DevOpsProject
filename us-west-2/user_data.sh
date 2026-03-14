#!/bin/bash
yum update -y
yum install -y nginx

cat <<HTML > /usr/share/nginx/html/index.html
<html>
    <h1>NGINX OK</h1>
    <p>Region: ${region_name}</p>
    <p>Instance: ${instance_id}</p>
</html>
HTML

cat > /etc/nginx/nginx.conf <<'EOF'
${nginx_conf}
EOF

systemctl enable nginx
systemctl restart nginx

