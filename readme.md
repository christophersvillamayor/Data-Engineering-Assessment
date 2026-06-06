# Data-Engineering-Assessment

## Dependencies
- Terraform
- Docker
- AWS Cli
- Python

## Setup

In a Terminal (Git Bash for Windows), run:
```bash
./scripts/task setup
```
This will configure and export an AWS profile for the current task session.

If you already have an AWS profile configured, you can use either:
```bash
export AWS_PROFILE=<your_profile>
./scripts/task setup
```
or
```bash
./scripts/task setup <your_profile>
```

You can verify your AWS identity with:
```bash
aws sts get-caller-identity
```

## Initial Deployment / Bootstrap

For a fresh environment, run:
```bash
./scripts/task bootstrap
```
This will:

1. Initialize Terraform
2. Create the required infrastructure
3. Create the ECR repository
4. Build and push a bootstrap container image
5. Create the Lambda function and related resources

The bootstrap image is only used to allow Lambda to be created. Future deployments will use commit-based image tags.

## Deploy

To deploy an updated Lambda image, run:
```bash
./scripts/task deploy
```

This will:

1. Build the Docker image
2. Tag the image using the current Git commit SHA
3. Push the image to ECR
4. Apply Terraform with the new image tag
5. Update the Lambda function to the new image

Each deployment creates an immutable image version based on the Git commit.

## Terraform Commands

You can run Terraform operations directly through the task script.

Initialize Terraform:
```bash
./scripts/task tf_init
```

Create a Terraform plan:
```bash
./scripts/task tf_plan
```

Apply Terraform changes:
```bash
./scripts/task tf_apply
```

Destroy all Terraform-managed resources:
```bash
./scripts/task tf_destroy
```

## Testing

After deployment, you can test the Lambda through the following command:
```bash
./scripts/task test
```

This will:
1. Upload ./assessment_assets/sample_orders.csv to the Input S3
2. Tail the CloudWatch logs for the Lambda function

If you would like to test `app/orders_analytics.py` locally, run:
```
./scripts/task local_test
```

## Troubleshooting

Check the current AWS profile:
```bash
echo $AWS_PROFILE
```

Check Terraform outputs:
```bash
terraform -chdir=terraform/assignment output
```

Check ECR images:
```bash
aws ecr describe-images \
  --repository-name <repository_name>
```

Check Lambda deployment status:
```bash
aws lambda get-function \
  --function-name <lambda_name>
```

View output s3:
```bash
output_bucket_name=$(terraform -chdir=terraform/assignment output -raw output_s3_name)
aws s3 ls s3://$output_bucket_name/results/
```