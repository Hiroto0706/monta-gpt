###############################################################################
# Provider定義
###############################################################################
# Google Cloud用プロバイダ設定
# プロジェクトとリージョンを指定（GKEやCloud SQL、Redisなどで使用）
provider "google" {
  project = var.project_id
  region  = var.region
}


###############################################################################
# ネットワーク設定(VPC/Subnet)
###############################################################################
# VPC作成
resource "google_compute_network" "vpc_network" {
  name                    = "monta-gpt-vpc"
  auto_create_subnetworks = false
}

# サブネット作成 (GKE等で使用)
resource "google_compute_subnetwork" "subnetwork" {
  name          = "monta-gpt-subnetwork"
  ip_cidr_range = "10.0.0.0/16"
  region        = var.region
  network       = google_compute_network.vpc_network.name
}


###############################################################################
# GKE(Autopilot) クラスタ設定
###############################################################################
resource "google_container_cluster" "primary" {
  name             = var.cluster_name
  location         = var.region
  enable_autopilot = true

  deletion_protection = false

  # ネットワーク設定
  network    = google_compute_network.vpc_network.self_link
  subnetwork = google_compute_subnetwork.subnetwork.self_link

  # Pod/Service IPの自動割当ポリシー(必須)
  ip_allocation_policy {}

  # Master Auth設定(クライアント証明書は発行しない)
  master_auth {
    client_certificate_config {
      issue_client_certificate = false
    }
  }
}

# GKEクラスターへの認証情報取得
data "google_client_config" "default" {}

# Kubernetesプロバイダ設定
provider "kubernetes" {
  host  = "https://${google_container_cluster.primary.endpoint}"
  token = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(
    google_container_cluster.primary.master_auth[0].cluster_ca_certificate
  )
}


###############################################################################
# Cloud SQL(PostgreSQL) 設定
###############################################################################
resource "google_sql_database_instance" "default" {
  name             = var.db_instance_name
  database_version = "POSTGRES_14"
  region           = var.region

  settings {
    # 最小構成tier (db-f1-micro)でコスト削減
    tier = "db-f1-micro"

    # パスワードポリシー設定 (強度確保)
    password_validation_policy {
      enable_password_policy = true
      min_length             = 12
      complexity             = "COMPLEXITY_DEFAULT"
    }
    ip_configuration {
      ipv4_enabled = true
    }
  }

  deletion_protection = false
}

# 使用するDBを1つ作成
resource "google_sql_database" "default" {
  name     = "monta-gpt"
  instance = google_sql_database_instance.default.name
}


###############################################################################
# DBユーザー/パスワード管理
###############################################################################
resource "random_password" "db_password" {
  length  = 16
  special = true
}

resource "google_sql_user" "default" {
  name     = "monta_user"
  instance = google_sql_database_instance.default.name
  password = random_password.db_password.result
}


###############################################################################
# Kubernetes上にアプリ用NamespaceとSecretを作成
###############################################################################
resource "kubernetes_namespace" "app_namespace" {
  metadata {
    name = "monta-gpt"
  }
}

# Cloud SQL接続情報をSecretとして格納
resource "kubernetes_secret" "cloud_sql_password" {
  depends_on = [google_sql_user.default]

  metadata {
    name      = "cloud-sql-password"
    namespace = kubernetes_namespace.app_namespace.metadata[0].name
  }

  data = {
    POSTGRES_PASSWORD = random_password.db_password.result
    POSTGRES_USERNAME = "monta_user"
    POSTGRES_DATABASE = "monta-gpt"
    POSTGRES_PORT     = 5432
    POSTGRES_HOST     = google_sql_database_instance.default.public_ip_address
  }
}


###############################################################################
# Redis (MemoryStore)設定
###############################################################################
resource "google_redis_instance" "cache" {
  name               = "monta-gpt-redis"
  tier               = "BASIC"
  memory_size_gb     = 1
  region             = var.region
  authorized_network = google_compute_network.vpc_network.id

  redis_version = "REDIS_6_X"
  display_name  = "Monta GPT Redis Cache"

  auth_enabled = true

  redis_configs = {
    maxmemory-policy = "allkeys-lru"
  }
}

# Redis用パスワード生成
resource "random_password" "redis_password" {
  length  = 16
  special = true
}

# Redis接続情報をKubernetes Secretに格納
resource "kubernetes_secret" "redis_config" {
  metadata {
    name      = "redis-config"
    namespace = kubernetes_namespace.app_namespace.metadata[0].name
  }

  data = {
    REDIS_HOST     = google_redis_instance.cache.host
    REDIS_PORT     = google_redis_instance.cache.port
    REDIS_PASSWORD = random_password.redis_password.result
  }
}

