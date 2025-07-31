terraform {
  backend "s3" {
    bucket = "cloud-fortress-prime-terraform-state-2025"  # your backend bucket name
    key    = "terraform.tfstate"
    region = "us-east-1"  # bucket region
  }
}
