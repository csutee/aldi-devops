output "namespace" {
	description = "Namespace containing the application."
	value       = kubernetes_namespace.homework.metadata[0].name
}

output "release_name" {
	description = "Name of the Helm release."
	value       = helm_release.homework.name
}
