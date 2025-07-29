terraform {
  backend "s3" {
    bucket = "cloud-fortress-prime-terraform-state-2025"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "cloud-fortress-prime-terraform-state-2025"
  acl    = "private"

  versioning {
    enabled = true
  }
}
