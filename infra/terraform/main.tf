provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone

  # credentials = file("/monta-gpt-credentials.json")yes
}

# ネットワークの作成
resource "google_compute_network" "vpc_network" {
  name                    = "monta-gpt-network"
  auto_create_subnetworks = false
}

# サブネットの作成
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

# Cloud SQLインスタンス作成
resource "google_sql_database_instance" "default" {
  depends_on = [google_service_networking_connection.private_vpc_connection]

  name             = var.db_instance_name
  database_version = "POSTGRES_14"
  region           = var.region

  settings {
    tier = "db-f1-micro" # 最小構成でコストを抑える
    ip_configuration {
      private_network = google_compute_network.vpc_network.self_link
    }
  }

  deletion_protection = false
}

# データベース作成
resource "google_sql_database" "default" {
  name     = "monta-gpt"
  instance = google_sql_database_instance.default.name
}

resource "google_compute_global_address" "private_service_connection" {
  name          = "psc-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vpc_network.self_link
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vpc_network.self_link
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_service_connection.name]
}


# Cloud SQL用のサービスアカウントを作成
resource "google_service_account" "cloud_sql_sa" {
  account_id   = "cloud-sql-client-sa"
  display_name = "Cloud SQL Client Service Account"
}

# サービスアカウントにCloud SQL Clientロールを付与
resource "google_project_iam_member" "cloud_sql_sa_role" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloud_sql_sa.email}"
}

# サービスアカウントのキーを作成
resource "google_service_account_key" "cloud_sql_sa_key" {
  service_account_id = google_service_account.cloud_sql_sa.name
  public_key_type    = "TYPE_X509_PEM_FILE"
  private_key_type   = "TYPE_GOOGLE_CREDENTIALS_FILE"
}

# サービスアカウントのキーをローカルに保存
resource "local_file" "cloud_sql_sa_key" {
  content  = google_service_account_key.cloud_sql_sa_key.private_key
  filename = "${path.module}/credentials/cloud-sql-sa-key.json"
}

# Kubernetesへの認証設定
provider "kubernetes" {
  host  = "https://34.85.17.84"
  token = data.google_client_config.default.access_token

  cluster_ca_certificate = base64decode(
    google_container_cluster.primary.master_auth[0].cluster_ca_certificate,
  )
}

data "google_client_config" "default" {}

# Cloud SQL用のKubernetes Secretを作成
resource "kubernetes_secret" "cloud_sql_sa" {
  depends_on = [google_sql_database_instance.default]

  metadata {
    name      = "cloud-sql-sa"
    namespace = "monta-gpt"
  }

  data = {
    "credentials.json" = filebase64("${path.module}/credentials/cloud-sql-sa-key.json")
  }
}

resource "kubernetes_namespace" "app_namespace" {
  metadata {
    name = "monta-gpt"
  }
}
