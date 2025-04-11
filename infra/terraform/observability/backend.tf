
terraform {
  backend "s3" {
    bucket         = "kubeobserve360-tfstate"
    key            = "global/s3/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "kubeobserve360-tfstate-lock"
    encrypt        = true
  }
}
