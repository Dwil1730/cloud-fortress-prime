terraform {
  backend "s3" {
<<<<<<< HEAD
    bucket = "cloud-fortress-prime-terraform-state-2025"  # your backend bucket name
    key    = "terraform.tfstate"
    region = "us-east-1"  # bucket region
=======
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
>>>>>>> 7881a9c80684aaaff865289c8f14a63885e34508
  }
}
