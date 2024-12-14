output "kubernetes_cluster_name" {
  value = google_container_cluster.primary.name
}

output "kubernetes_cluster_endpoint" {
  value = google_container_cluster.primary.endpoint
}

output "kubernetes_cluster_ca_certificate" {
  value = google_container_cluster.primary.master_auth[0].cluster_ca_certificate
}

output "cloud_sql_instance_connection_name" {
  value = google_sql_database_instance.default.connection_name
}

output "db_password" {
  value     = random_password.db_password.result
  sensitive = true
}

output "db_host" {
  value = google_sql_database_instance.default.private_ip_address
}

output "db_url" {
  value     = "postgresql://monta_user:${random_password.db_password.result}@${google_sql_database_instance.default.private_ip_address}:5432/monta-gpt"
  sensitive = true
}

output "redis_host" {
  value = google_redis_instance.cache.host
}

output "redis_port" {
  value = google_redis_instance.cache.port
}

output "redis_password" {
  value     = random_password.redis_password.result
  sensitive = true
}