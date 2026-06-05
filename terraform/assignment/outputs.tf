output "lambda_function_name" {
    value = module.lambda_function.lambda_function_name
} 

output "ecr_repository_name" {
    value = module.ecr_repo.ecr_repository_name
}

output "ecr_repository_url" {
    value = module.ecr_repo.ecr_repository_url
}