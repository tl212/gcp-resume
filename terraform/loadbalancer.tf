# Backend bucket pointing to your storage bucket
resource "google_compute_backend_bucket" "resume_backend" {
  name        = "resume-backend-bucket"
  bucket_name = google_storage_bucket.resume_site.name
  enable_cdn  = true
}

# URL map to route requests
resource "google_compute_url_map" "resume_url_map" {
  name            = "resume-url-map"
  default_service = google_compute_backend_bucket.resume_backend.id
}

# Managed SSL certificate for both root and www
resource "google_compute_managed_ssl_certificate" "resume_ssl" {
  name = "resume-ssl-cert"
  
  managed {
    domains = ["7l33.dev", "www.7l33.dev"]  # Both root and www
  }
}

# HTTPS proxy
resource "google_compute_target_https_proxy" "resume_https_proxy" {
  name             = "resume-https-proxy"
  url_map          = google_compute_url_map.resume_url_map.id
  ssl_certificates = [google_compute_managed_ssl_certificate.resume_ssl.id]
}

# Reserve the static IP
resource "google_compute_global_address" "resume_lb_ip" {
  name = "resume-lb-ip"
}

# Global forwarding rule (connects IP to proxy)
resource "google_compute_global_forwarding_rule" "resume_forwarding_rule" {
  name       = "resume-forwarding-rule"
  target     = google_compute_target_https_proxy.resume_https_proxy.id
  port_range = "443"
  ip_address = google_compute_global_address.resume_lb_ip.address
}

# HTTP to HTTPS redirect
resource "google_compute_url_map" "http_redirect" {
  name = "http-redirect"
  
  default_url_redirect {
    https_redirect         = true
    strip_query            = false
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
  }
}

resource "google_compute_target_http_proxy" "http_proxy" {
  name    = "http-proxy"
  url_map = google_compute_url_map.http_redirect.id
}

resource "google_compute_global_forwarding_rule" "http_forwarding_rule" {
  name       = "http-forwarding-rule"
  target     = google_compute_target_http_proxy.http_proxy.id
  port_range = "80"
  ip_address = google_compute_global_address.resume_lb_ip.address
}

# Output the IP address and domain
output "load_balancer_ip" {
  value = google_compute_global_address.resume_lb_ip.address
  description = "The IP address to point your DNS A records to"
}

output "domain_url" {
  value = "https://7l33.dev"
}