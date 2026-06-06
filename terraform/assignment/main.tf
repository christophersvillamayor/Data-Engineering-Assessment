## Update the following terraform code to meet the project requirements
## We have provided some sample code to help you get started

resource "aws_s3_bucket" "input_s3" {
  bucket = "${local.app_name}-input-bucket"
  tags = merge({
        Name        = "${local.app_name}-input-bucket"
        Environment = "${var.env}"
    }, local.default_tags
  )
  force_destroy = true
}

resource "aws_s3_bucket" "output_s3" {
  bucket = "${local.app_name}-output-bucket"

  tags = merge({
      Name        = "${local.app_name}-output-bucket"
      Environment = "${var.env}"
    }, local.default_tags
  )
  force_destroy = true
}

module "lambda_function" {
  source                  = "../modules/lambda"
  lambda_name             = "${local.app_name}-file-processor"
  role_name               = "${local.app_name}-file-processor-role"
  log_retention_in_days   = 14
  image_uri               = "${module.ecr_repo.repository_url}:${var.image_tag}"
  timeout                 = 15
  memory_size             = 256
  environment_variables   = {
    LOG_LEVEL = "DEBUG"
    OUTPUT_BUCKET = aws_s3_bucket.output_s3.bucket
  }

  default_tags = local.default_tags
}

module "ecr_repo" {
  source    = "../modules/ecr-repo"
  repo_name = "${local.app_name}-ecr"
  default_tags = local.default_tags
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_function.lambda_arn
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${aws_s3_bucket.input_s3.bucket}"
}

resource "aws_iam_role_policy" "lambda_s3" {
  name = "lambda-s3-read-permissions"
  
  role = module.lambda_function.lambda_role_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject"]
        Resource = ["arn:aws:s3:::${aws_s3_bucket.input_s3.bucket}/*"]
      },
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject"]
        Resource = ["arn:aws:s3:::${aws_s3_bucket.output_s3.bucket}/*"]
      }
    ]
  })
}

resource "aws_iam_user_policy" "cloudwatch_logs_read" {
  name = "CloudWatchLogsRead"
  user = var.aws_profile

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:FilterLogEvents",
          "logs:GetLogEvents",
          "logs:DescribeLogStreams",
          "logs:DescribeLogGroups"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_s3_bucket_notification" "s3_notification" {
  bucket = aws_s3_bucket.input_s3.id
  lambda_function {
    lambda_function_arn = module.lambda_function.lambda_arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".csv"
  }
}
