# Outputs
output "lambda_arn" {
  value = aws_lambda_function.lambda_function.arn
}

output "lambda_role_name" {
  description = "The name of the IAM role created for the Lambda function"
  value       = aws_iam_role.lambda_exec_role.name 
}

output "lambda_function_name" {
  value = aws_lambda_function.lambda_function.function_name
}
