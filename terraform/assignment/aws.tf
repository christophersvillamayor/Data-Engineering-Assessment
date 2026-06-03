# You will need to modify the key value in the backend block to a unique value for your assignment.

# FIXME: probably should add required_providers
provider "aws" {
  region = var.region_name
  profile = var.aws_profile
}
data "aws_caller_identity" "current" {}


terraform {
  backend "s3" {
    bucket         = "nmd-training-tf-states-888577066340"
    key            = "nmd-assignment-christophersvillamayor.tfstate"
    region         = "us-west-2"
    use_lockfile   = true    
    encrypt        = true                   # Encrypts the state file at rest
  }
}
