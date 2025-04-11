import os
from pathlib import Path

# Define base project path
base_path = Path("./infra/terraform")

# Define Terraform service directories and main.tf placeholders
terraform_services = {
    "eks": """
provider "aws" {
  region = var.region
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.18.1"

  name = "kubeobserve360-vpc"
  cidr = var.vpc_cidr

  azs             = var.azs
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets

  enable_nat_gateway = true
  single_nat_gateway = true
  enable_dns_hostnames = true
  tags = var.tags
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = "1.29"
  subnets         = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  enable_irsa = true

  eks_managed_node_groups = {
    default = {
      desired_capacity = 2
      max_capacity     = 3
      min_capacity     = 1

      instance_types = ["t3.medium"]
    }
  }

  tags = var.tags
}
""",
    "observability": """
provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

resource "helm_release" "prometheus" {
  name       = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "prometheus"
  version    = "25.11.0"
  namespace  = "observability"
  create_namespace = true
}

resource "helm_release" "grafana" {
  name       = "grafana"
  repository = "https://grafana.github.io/helm-charts"
  chart      = "grafana"
  version    = "7.3.9"
  namespace  = "observability"
  create_namespace = true

  set {
    name  = "adminPassword"
    value = "admin123"
  }
}

resource "helm_release" "loki" {
  name       = "loki"
  repository = "https://grafana.github.io/helm-charts"
  chart      = "loki"
  version    = "5.41.5"
  namespace  = "observability"
  create_namespace = true
}
""",
    "kafka-flink": """
resource "helm_release" "kafka" {
  name       = "kafka"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "kafka"
  version    = "26.3.2"
  namespace  = "data-pipeline"
  create_namespace = true
}

resource "helm_release" "flink" {
  name       = "flink"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "flink"
  version    = "0.3.4"
  namespace  = "data-pipeline"
  create_namespace = true
}
""",
    "storage": """
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
"""
}

# Write each main.tf file
for service, content in terraform_services.items():
    service_dir = base_path / service
    service_dir.mkdir(parents=True, exist_ok=True)
    with open(service_dir / "main.tf", "w") as f:
        f.write(content)

import shutil
shutil.make_archive("./kubeobserve360-infra", 'zip', base_path)

