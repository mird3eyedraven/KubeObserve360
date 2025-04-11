
provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "tfstate" {
  bucket = "kubeobserve360-tfstate"
  versioning {
    enabled = true
  }
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_dynamodb_table" "tfstate_lock" {
  name           = "kubeobserve360-tfstate-lock"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Environment = "dev"
    Name        = "kubeobserve360-tfstate-lock"
  }
}
