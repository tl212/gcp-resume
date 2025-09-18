output "resume_url" {
  value = "https://storage.googleapis.com/${google_storage_bucket.resume_site.name}/index.html"
}

output "function_url" {
  value = google_cloudfunctions2_function.visitor_counter.service_config[0].uri
}