terraform {
  backend "gcs" {
    bucket = "monta-gpt-terraform-state"
    prefix = "terraform/state"
  }

  required_version = ">= 1.0.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  }
}
