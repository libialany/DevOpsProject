import pulumi
import pulumi_aws as aws
import pulumi_aws.route53 as route53
import pulumi_aws.s3 as s3
import json
import os

# Cambia esto a tu dominio real, EJEMPLO: "midominio.com"
domain_name = "xyz.mlibia.xyz"

# 1. Obtener la zona de Route 53 (ya existente)
#    Pulumi buscará una zona que coincida con domain_name
zone = route53.get_zone(name=domain_name)

# 2. Crear el bucket S3 con habilitación de "website"
bucket = s3.Bucket(
    "staticWebsiteBucket",
    bucket=domain_name,  # El bucket debe coincidir con tu dominio
    website=s3.BucketWebsiteArgs(
        index_document="index.html",
        error_document=None,  # O puedes usar 'error.html' si lo deseas
    ),
)
public_access_block = s3.BucketPublicAccessBlock(
    "publicAccessBlock",
    bucket=bucket.id,
    block_public_acls=False,
    block_public_policy=False,
    ignore_public_acls=False,
    restrict_public_buckets=False,
)
# 3. Política para permitir lectura pública
#    (Omitir si prefieres políticas más restringidas, o si usarás CloudFront + OAC)
public_read_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": "*",
        "Action": ["s3:GetObject"],
        "Resource": [f"arn:aws:s3:::{domain_name}/*"]
    }]
}

bucket_policy = s3.BucketPolicy(
    "bucketPolicy",
    bucket=bucket.bucket,
    policy=bucket.bucket.apply(
        lambda bucket_name: json.dumps(public_read_policy)
    ),
)

# 4. Subir el archivo "index.html" al bucket
index_object = s3.BucketObject(
    "indexObject",
    bucket=bucket.bucket,
    source=pulumi.FileAsset("site/index.html"),  # Ruta local a tu archivo
    key="index.html",
    content_type="text/html"
)

# 5. Crear registro DNS de tipo A (Alias) a S3 Website
#    IMPORTANTE: Ajustar la Hosted Zone ID según tu región S3
#    Por ejemplo, "Z3AQBSTGFYJSTF" es para us-east-1
#
#    Para encontrar la tuya, revisa la doc oficial: 
#    https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_website_region_endpoints
# s3_website_hosted_zone_id = "Z3AQBSTGFYJSTF"  # Ajusta a la región de tu bucket

# record = route53.Record(
#     "staticWebsiteAliasRecord",
#     name=domain_name,          # "midominio.com"
#     zone_id=zone.zone_id,      # Zone ID obtenida de get_zone
#     type="A",
#     aliases=[
#         route53.RecordAliasArgs(
#             name=bucket.website_endpoint,  # El endpoint del sitio en S3
#             zone_id=s3_website_hosted_zone_id,
#             evaluate_target_health=False
#         )
#     ]http://test.mlibia.xyz.s3-website-us-east-1.amazonaws.com
# )

# # 6. Exportar la URL de S3 por si quieres probar directamente
# pulumi.export("s3_website_endpoint", bucket.website_endpoint)
pulumi.export("domain_alias_url", pulumi.Output.concat("http://", domain_name))
