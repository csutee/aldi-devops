terraform {
	required_version = ">= 1.5"

	required_providers {
		helm = {
			source  = "hashicorp/helm"
			version = "~> 2.13"
		}
		kubernetes = {
			source  = "hashicorp/kubernetes"
			version = "~> 2.30"
		}
	}
}

provider "kubernetes" {
	config_path = pathexpand(var.kubeconfig_path)
}

provider "helm" {
	kubernetes {
		config_path = pathexpand(var.kubeconfig_path)
	}
}