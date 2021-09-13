resource "kubernetes_deployment" "word-counter" {
  metadata {
    name = "word-counter"
    labels = {
      App = "WordCounter"
    }
  }

  spec {
    replicas = 2
    selector {
      match_labels = {
        App = "WordCounter"
      }
    }
    template {
      metadata {
        labels = {
          App = "WordCounter"
        }
      }
      spec {
        container {
          env {
            name = "DATABASE_URL"
            value = join("", [
              "postgresql://",
              var.database_username,
              ":",
              var.database_password,
              "@",
              aws_db_instance.default.endpoint,
              "/",
              aws_db_instance.default.name
            ])
          }
          image = "julianaklulo/word-counter:v1"
          name  = "word-counter"

          port {
            container_port = 80
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "word-counter" {
  metadata {
    name = "word-counter"
  }
  spec {
    selector = {
      App = kubernetes_deployment.word-counter.spec.0.template.0.metadata[0].labels.App
    }
    port {
      port        = 80
      target_port = 80
    }

    type = "LoadBalancer"
  }
}

output "application_ip" {
  value = kubernetes_service.word-counter.status.0.load_balancer.0.ingress.0.hostname
}