
resource "aws_s3_bucket" "logs" {
  bucket = "kubeobserve360-logs"
  force_destroy = true
}

resource "aws_iam_policy" "s3_access" {
  name        = "S3AccessPolicy"
  description = "Allow access to S3 logging bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["s3:*"],
        Effect = "Allow",
        Resource = [
          "arn:aws:s3:::kubeobserve360-logs",
          "arn:aws:s3:::kubeobserve360-logs/*"
        ]
      }
    ]
  })
}
