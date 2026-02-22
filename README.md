# Gallery App – IaC with Terraform AWS Modules

A serverless photo gallery on AWS, fully managed with Terraform using the official `terraform-aws-modules` collection.

## Architecture

```
Browser / app.py
      │
      ▼
┌─────────────────┐        ┌──────────────────┐
│  API Gateway    │──────▶│  Lambda (Python) │
│  (HTTP API)     │        │  handler.py       │
└─────────────────┘        └────────┬─────────┘
                                    │ s3:ListBucket
                                    ▼
                           ┌──────────────────┐
                           │    S3 Bucket     │  (private)
                           │  gallery images  │
                           └──────────────────┘
                                    ▲
                           OAC (sigv4)
                                    │
Browser ──────────────────▶ CloudFront CDN
                            (image delivery)
```

## Module Versions Used

| Module | Version |
|--------|---------|
| `terraform-aws-modules/s3-bucket/aws` | ~> 4.0 |
| `terraform-aws-modules/cloudfront/aws` | ~> 3.0 |
| `terraform-aws-modules/lambda/aws` | ~> 7.0 |
| `terraform-aws-modules/apigateway-v2/aws` | ~> 5.0 |

## Project Layout

```
gallery-app-terraform/
├── main.tf                   # All AWS resources
├── variables.tf              # Input variables
├── locals.tf                 # Shared locals / tags
├── outputs.tf                # Key resource outputs
├── terraform.tfvars.example  # Copy → terraform.tfvars and fill in
├── lambda/
│   └── handler.py            # Lambda: lists S3 keys, returns CF URLs
└── app.py                    # Python frontend (local dev server)
```

## Quick Start

### 1. Prerequisites

- Terraform >= 1.5
- AWS CLI configured (`aws configure`)
- Python >= 3.10 (for the frontend)

### 2. Deploy Infrastructure

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars – set bucket_name to something globally unique

terraform init
terraform plan
terraform apply
```

### 3. Upload Sample Images

```bash
aws s3 cp ./photos/ s3://<your-bucket-name>/ --recursive \
  --include "*.jpg" --include "*.png" --include "*.webp"
```

### 4. Run the Frontend

```bash
export GALLERY_API_ENDPOINT=$(terraform output -raw api_gateway_endpoint)
python app.py
# Open http://localhost:8080
```

## Security Posture

| Control | Setting |
|---------|---------|
| S3 public access | ❌ Fully blocked |
| S3 → CloudFront | ✅ Origin Access Control (OAC) with SigV4 |
| Lambda S3 access | ✅ AmazonS3ReadOnlyAccess + explicit ListBucket |
| API Gateway | ✅ CORS restricted to GET/OPTIONS |
| WAF | ➖ Disabled (per requirements) |
| Encryption at rest | ✅ AES-256 SSE-S3 |
| HTTPS | ✅ CloudFront enforces redirect-to-https |

## Environment Variables (Lambda)

| Variable | Description |
|----------|-------------|
| `BUCKET_NAME` | S3 bucket name (set by Terraform) |
| `CLOUDFRONT_DOMAIN` | CF distribution domain (set by Terraform) |
| `IMAGE_EXTENSIONS` | Comma-separated list, default `jpg,jpeg,png,gif,webp,svg` |

## API Reference

### `GET /images`

Returns a JSON list of all images in the bucket.

**Response**
```json
{
  "count": 3,
  "images": [
    {
      "key": "photos/beach.jpg",
      "url": "https://d1234abcd.cloudfront.net/photos/beach.jpg",
      "size": 204800,
      "last_modified": "2024-06-01T12:00:00+00:00"
    }
  ]
}
```

## Teardown

```bash
terraform destroy
```
