# resource "helm_release" "argocd" {
#   count            = var.create_eks_cluster ? 1 : 0
#   name             = "argocd"
#   repository       = "https://argoproj.github.io/argo-helm"
#   chart            = "argo-cd"
#   namespace        = "argocd"
#   version          = "5.31.0"
#   create_namespace = true

#   # set {
#   #   name  = "controller.adminPassword"
#   #   value = "admin"
#   # }

#   # set {
#   #   name  = "controller.adminUser"
#   #   value = "admin"
#   # }

#   set {
#     name  = "server.ingress.enabled"
#     value = "true"
#   }


#   # values = [
#   #   file("argocd-values.yml"),
#   # ]
# }



resource "helm_release" "argocd" {
  name            = "argocd"
  repository      = "https://argoproj.github.io/argo-helm"
  chart           = "argo-cd"
  namespace       = "argocd"
  create_namespace = true

  set {
    name  = "server.service.type"
    value = "LoadBalancer"
  }

  # In case you want to override other values, you can use additional set blocks
  set {
    name  = "server.ingress.enabled"
    value = "true"
  }

  # If you want to completely replace the values, use values block
  # values = [
  #   "${file("values.yaml")}"
  # ]

  # Resetting values to default might not be necessary, as you are explicitly setting values
  reset_values = true
}
