# You will need to modify the key value in the backend block to a unique value for your assignment.

provider "aws" {
  region = var.region_name
  profile = var.aws_profile
}
data "aws_caller_identity" "current" {}


terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.47.0"
    }
  }
  backend "s3" {
    bucket         = "nmd-training-tf-states-888577066340"
    key            = "nmd-assignment-christophersvillamayor.tfstate"
    region         = "us-west-2"
    use_lockfile   = true    
    encrypt        = true                   # Encrypts the state file at rest
  }
}
