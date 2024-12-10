provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# ネットワークの作成 (GKE用)
resource "google_compute_network" "vpc_network" {
  name                    = "monta-gpt-vpc"
  auto_create_subnetworks = false
}

# サブネットの作成 (GKE用)
resource "google_compute_subnetwork" "subnetwork" {
  name          = "monta-gpt-subnetwork"
  ip_cidr_range = "10.0.0.0/16"
  region        = var.region
  network       = google_compute_network.vpc_network.name
}

# GKEクラスタ作成
resource "google_container_cluster" "primary" {
  name             = var.cluster_name
  location         = var.region
  enable_autopilot = true

  deletion_protection = false

  # VPC接続設定
  network    = google_compute_network.vpc_network.self_link
  subnetwork = google_compute_subnetwork.subnetwork.self_link

  ip_allocation_policy {}

  master_auth {
    client_certificate_config {
      issue_client_certificate = false
    }
  }
}

# Cloud SQLインスタンス (Public IP有効化)
resource "google_sql_database_instance" "default" {
  name             = var.db_instance_name
  database_version = "POSTGRES_14"
  region           = var.region

  settings {
    tier = "db-f1-micro" # 最小構成でコストを抑える
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

# データベース作成
resource "google_sql_database" "default" {
  name     = "monta-gpt"
  instance = google_sql_database_instance.default.name
}

# DBユーザー用のパスワード生成
resource "random_password" "db_password" {
  length  = 16
  special = true
}

# DBユーザー作成 (cloud_sql_proxy経由でアクセス想定)
resource "google_sql_user" "default" {
  name     = "monta_user"
  instance = google_sql_database_instance.default.name
  password = random_password.db_password.result
}

# Kubernetesへの認証設定
data "google_client_config" "default" {}

provider "kubernetes" {
  host  = "https://34.85.17.84"
  token = data.google_client_config.default.access_token

  cluster_ca_certificate = base64decode(
    google_container_cluster.primary.master_auth[0].cluster_ca_certificate
  )
}

# アプリ用のNamespace作成
resource "kubernetes_namespace" "app_namespace" {
  metadata {
    name = "monta-gpt"
  }
}

# Cloud SQL接続用パスワードを格納するSecret
resource "kubernetes_secret" "cloud_sql_password" {
  depends_on = [google_sql_user.default]

  metadata {
    name      = "cloud-sql-password"
    namespace = kubernetes_namespace.app_namespace.metadata[0].name
  }

  data = {
    # base64エンコードはTerraformが自動で行う
    "password" = random_password.db_password.result
    # ユーザー名やDB名も必要ならここに格納可能
    "username" = "monta_user"
    "database" = "monta-gpt"
  }
}

