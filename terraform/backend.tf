terraform {
  backend "gcs" {
    bucket = "terraform-state-sevenl33-v2-25"
    prefix = "terraform/state"
  }
}