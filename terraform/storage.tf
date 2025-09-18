# cloud storage bucket static website
resource "google_storage_bucket" "resume_site" {
  name          = "resume-sevenl33-v2-25"
  location      = "US"
  force_destroy = true

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

# Make bucket publicly readable
resource "google_storage_bucket_iam_binding" "public_read" {
  bucket = google_storage_bucket.resume_site.name
  role   = "roles/storage.objectViewer"
  members = [
    "allUsers",
  ]
}

# Upload website files
resource "google_storage_bucket_object" "website_files" {
  for_each = fileset("../frontend/website", "**/*")
  
  bucket = google_storage_bucket.resume_site.name
  name   = each.value
  source = "../frontend/website/${each.value}"
}
