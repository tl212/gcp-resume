# Create a zip file for the Cloud Function source code
data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "../backend"
  output_path = "visitor_counter.zip"
}

# Google Cloud Storage bucket for storing function source code
resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project_id}-function-source"
  location = "US"
}

# Upload the function source code to the bucket
resource "google_storage_bucket_object" "function_archive" {
  name   = "visitor_counter-${data.archive_file.function_zip.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.function_zip.output_path
}

# Cloud Function (2nd gen)
resource "google_cloudfunctions2_function" "visitor_counter" {
  name        = "visitor-counter"
  location    = var.region
  description = "Visitor counter function for resume site"

  build_config {
    runtime     = "python311"
    entry_point = "visitor_counter"
    source {
      storage_source {
        bucket = google_storage_bucket.function_bucket.name
        object = google_storage_bucket_object.function_archive.name
      }
    }
  }

  service_config {
    max_instance_count = 10
    available_memory   = "256M"
    timeout_seconds    = 60
    ingress_settings   = "ALLOW_ALL"
    all_traffic_on_latest_revision = true
  }
}

# IAM binding to make the function publicly accessible
resource "google_cloud_run_service_iam_binding" "function_invoker" {
  location = google_cloudfunctions2_function.visitor_counter.location
  service  = google_cloudfunctions2_function.visitor_counter.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}

# Firestore database
resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"
  location_id = "us-central1"
  type        = "FIRESTORE_NATIVE"

  # Delete protection disabled for development
  delete_protection_state = "DELETE_PROTECTION_DISABLED"
}
