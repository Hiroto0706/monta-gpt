variable "project_id" {
  description = "GCPプロジェクトID"
  type        = string
  default     = "monta-gpt" # ユーザーのプロジェクトID
}

variable "region" {
  description = "GCPリージョン"
  type        = string
  default     = "asia-northeast1"
}

variable "zone" {
  description = "GCPゾーン"
  type        = string
  default     = "asia-northeast1-a"
}

variable "cluster_name" {
  description = "GKEクラスタ名"
  type        = string
  default     = "monta-gpt-cluster"
}

variable "db_instance_name" {
  description = "Cloud SQLインスタンス名"
  type        = string
  default     = "monta-gpt-db"
}
