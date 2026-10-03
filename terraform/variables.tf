variable "namespace" {
  description = "Kubernetes namespace for the application."
  type        = string
  default     = "devops-homework"
}

variable "environment" {
  description = "Environment value exposed by the application."
  type        = string
  default     = "dev"
}

variable "image_repository" {
  description = "Container image repository."
  type        = string
  default     = "myapp"
}

variable "image_tag" {
  description = "Container image tag to deploy."
  type        = string
  default     = "1.0.0"
}

variable "kubeconfig_path" {
  description = "Path to the kubeconfig used by the Kubernetes and Helm providers."
  type        = string
  default     = "~/.kube/config"
}

variable "replica_count" {
  description = "Number of application pods."
  type        = number
  default     = 1
}
