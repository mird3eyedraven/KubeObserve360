
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
