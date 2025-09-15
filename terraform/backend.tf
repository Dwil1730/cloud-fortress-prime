terraform {
  backend "s3" {
    bucket         = "cloud-fortress-prime-terraform-state-2025"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "cloud-fortress-terraform-locks"
    encrypt        = true
  }
}
