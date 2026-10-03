resource "kubernetes_namespace" "homework" {
  metadata {
    name = var.namespace
  }
}

resource "helm_release" "homework" {
  name      = "myapp"
  chart     = "${path.module}/../helm"
  namespace = kubernetes_namespace.homework.metadata[0].name
  wait      = true
  timeout   = 300

  values = [
    yamlencode({
      environment  = var.environment
      replicaCount = var.replica_count
      image = {
        repository = var.image_repository
        tag        = var.image_tag
      }
    })
  ]
}
