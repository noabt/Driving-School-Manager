terraform {
  backend "s3" {
    bucket         = "dsm-bucket"
    key            = "eks/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "dsm-table"
  }
}
