# Puddle E-commerce Platform - DevOps Infrastructure

Production-grade DevOps infrastructure for Django e-commerce platform on AWS using Infrastructure as Code, CI/CD, GitOps, and observability.

## 🎯 Overview

Enterprise-level deployment of Django application (Puddle) on AWS with complete automation from code to production. Features Infrastructure as Code (Terraform), containerization (Docker), Kubernetes orchestration (EKS), and GitOps deployment (ArgoCD).

![Architecture](docs/Puddle%20e-commerce%20platform%20architecture.png)

### Key Features
- ☁️ **AWS Infrastructure**: VPC, EKS, RDS, S3, ECR via Terraform
- 🚀 **CI/CD**: GitHub Actions with conditional execution
- 📦 **GitOps**: ArgoCD for declarative deployments
- 📊 **Monitoring**: Prometheus + Grafana with custom dashboards
- 🔒 **Security**: Network isolation, IAM policies, secrets management
- 🔍 **Code Quality**: SonarQube integration

---

## 🛠️ Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Infrastructure** | Terraform 1.6.0, AWS (VPC, EKS 1.33, RDS PostgreSQL 17.6, S3, ECR) |
| **Application** | Django 4.1.5, Python 3.12, Gunicorn 20.1.0 |
| **Orchestration** | Kubernetes (EKS), Helm 3.x |
| **CI/CD** | GitHub Actions, ArgoCD, SonarQube |
| **Monitoring** | Prometheus (kube-prometheus-stack 56.6.2), Grafana 7.3.7 |
| **Container** | Docker, AWS ECR |

---

## 📂 Project Structure

```
puddle-devops-infrastructure/
├── .github/workflows/      # CI/CD pipelines (ci-cd.yaml, infra.yaml)
├── infra/                  # Terraform modules (vpc, eks, rds, s3, ecr)
├── helm/                   # Helm chart for application
├── argocd/                 # ArgoCD application manifests
├── monitoring/grafana/dashboards/  # Custom Grafana dashboards
├── src/                    # Django application source
├── k8s/                    # Kubernetes manifests (legacy)
└── docs/                   # Screenshots and diagrams
```

---

## 🏗️ Infrastructure Components

### AWS VPC
- CIDR: `10.0.0.0/16`
- 2 Public + 2 Private Subnets (Multi-AZ)
- Internet Gateway + NAT Gateway

### Amazon EKS
- Kubernetes 1.33
- 3x t3.small nodes (2 vCPU, 2GB RAM each)
- Capacity: ~33 pods across cluster

### Amazon RDS
- PostgreSQL 17.6 (db.t3.micro)
- 20GB storage, 7-day backup
- Private subnet deployment

### Amazon S3
- Bucket: `puddle-s3-media-nti`
- Django media storage (images, uploads)

### Amazon ECR
- Repository: `puddle-app-repo`
- Tagging: Git commit SHA
- Scan on push enabled

---

## 🔄 CI/CD Pipeline

### Infrastructure Pipeline (`.github/workflows/infra.yaml`)
**Triggers**: Push/PR to `main` or manual

1. **Detect Changes** → Only runs if `infra/**/*.tf` or `*.tfvars` changed
2. **Terraform** → Init, Validate, Plan, Apply
3. **Kubernetes Setup** → Configure kubectl, install ArgoCD
4. **Secrets** → Create database and app secrets
5. **Deploy** → Apply ArgoCD applications (app, prometheus, grafana)

### Application Pipeline (`.github/workflows/ci-cd.yaml`)
**Triggers**: Push/PR to `main` or manual

1. **Detect Changes** → Only runs if `src/**` changed
2. **Build & Test** → Python tests with coverage
3. **SonarQube** → Code quality scan
4. **Docker** → Build image, tag with commit SHA, push to ECR
5. **Update Manifest** → Update Helm values with new image tag
6. **Deploy** → Trigger ArgoCD sync

**Quality Gates**: All tests pass, coverage threshold met, SonarQube quality gate passed

---

## 📊 Monitoring & Observability

### Prometheus
- **Stack**: kube-prometheus-stack (Prometheus, Alertmanager, Node Exporter, Kube State Metrics)
- **Retention**: 7 days (emptyDir storage)
- **Scrapes**: Django app metrics every 30s via ServiceMonitor

### Grafana
- **Access**: LoadBalancer (admin/Admin@123)
- **Pre-configured Dashboards**:
  - Django Application (HTTP requests, latency, errors, Gunicorn workers)
  - PostgreSQL Database (connections, queries, transactions, cache hits)
  - Kubernetes Cluster (nodes, pods, resources, network)
  - ArgoCD Application Health

![Grafana Dashboard 1](docs/grafana1.PNG)
![Grafana Dashboard 2](docs/grafana2.PNG)

### ArgoCD
All applications synchronized and healthy:

![ArgoCD Applications](docs/argocd1.PNG)
![ArgoCD Health Status](docs/argocd2.PNG)

---

## 🚀 Quick Start

### Prerequisites
- AWS CLI v2.x, Terraform 1.6.0, kubectl 1.28+, Helm 3.x, Docker 20+
- AWS account with IAM permissions (EC2, EKS, RDS, S3, ECR)
- Terraform Cloud account and API token
- GitHub account with Secrets configured

### GitHub Secrets Required
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
TF_API_TOKEN
DJANGO_SECRET_KEY
DATABASE_URL
ECR_URL
EKS_CLUSTER_NAME
SONAR_TOKEN (optional)
SONAR_HOST_URL (optional)
```

### Deployment Steps

#### Option A: Automated (GitHub Actions)
1. Push to `main` branch
2. Monitor workflows in GitHub Actions
3. Wait ~15-20 minutes
4. Access services via LoadBalancer URLs

#### Option B: Manual
```bash
# 1. Provision infrastructure
cd infra
terraform init
terraform apply
aws eks update-kubeconfig --name puddle-eks-cluster --region us-east-1

# 2. Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'

# 3. Create secrets
kubectl create secret generic puddle-db-secret \
  --from-literal=DATABASE_URL="postgresql://user:pass@host:5432/db" \
  --namespace=puddle-production

kubectl create secret generic puddle-app-secret \
  --from-literal=DJANGO_SECRET_KEY="key" \
  --from-literal=AWS_ACCESS_KEY_ID="key" \
  --from-literal=AWS_SECRET_ACCESS_KEY="secret" \
  --namespace=puddle-production

# 4. Deploy applications
kubectl apply -f argocd/application.yaml
kubectl apply -f argocd/prometheus-application.yaml
kubectl apply -f argocd/grafana-application.yaml

# 5. Verify
kubectl get applications -n argocd
kubectl get pods -A
```

### Access Services
```bash
# Application
kubectl get svc puddle-app-service -n puddle-production

# Grafana (admin/Admin@123)
kubectl get svc grafana -n monitoring

# ArgoCD (admin/<get-password>)
kubectl get svc argocd-server -n argocd
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Live Application

![Puddle Application](docs/puddle.PNG)

---

## ⚙️ Configuration

### Environment Variables (ConfigMap)
```yaml
DJANGO_DEBUG: "False"
DJANGO_ALLOWED_HOSTS: "*"
USE_S3: "True"
AWS_BUCKET_NAME: "puddle-s3-media-nti"
AWS_S3_REGION_NAME: "us-east-1"
```

### Resource Limits
**Application Pod**: 100m CPU / 128Mi RAM (requests), 250m CPU / 256Mi RAM (limits)  
**Prometheus**: 200m CPU / 512Mi RAM (requests), 500m CPU / 1Gi RAM (limits)

### Health Probes
- **Liveness**: `/health/` endpoint, 60s initial delay, 10s period
- **Readiness**: `/health/` endpoint, 30s initial delay, 10s period

---

## 🔒 Security

### Network
- Private subnets for EKS nodes and RDS
- Security groups restrict traffic (RDS only from EKS, LoadBalancer only HTTP)
- No direct internet access to application pods

### Application
- `DEBUG=False` in production
- Secrets in Kubernetes Secrets (never in Git)
- Non-root container user
- SSL database connections

### Container
- Minimal base image (python:3.12-slim)
- ECR image scanning enabled
- Regular dependency updates

---

## 🐛 Troubleshooting

### Pod CrashLoopBackOff
```bash
# Check logs
kubectl logs -n puddle-production <pod-name>

# Verify secrets
kubectl get secret puddle-db-secret -n puddle-production -o yaml

# Test database connection
kubectl exec -n puddle-production <pod-name> -- python manage.py dbshell
```

### ArgoCD Sync Failures
```bash
# Force sync
argocd app sync puddle-app --force

# Check application status
kubectl get applications -n argocd
argocd app get puddle-app
```

### LoadBalancer Pending
```bash
# Check service
kubectl describe svc puddle-app-service -n puddle-production

# Verify subnet tags
kubernetes.io/cluster/<cluster-name> = shared
kubernetes.io/role/elb = 1
```

### Prometheus Not Scraping
```bash
# Check targets
kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090
# Visit http://localhost:9090/targets

# Verify metrics endpoint
kubectl exec -n puddle-production <pod-name> -- curl localhost:8000/metrics
```

### Useful Commands
```bash
# Get all resources
kubectl get all -n puddle-production

# View logs with follow
kubectl logs -f -n puddle-production -l app=puddle-app

# Port forward for local access
kubectl port-forward -n puddle-production svc/puddle-app-service 8000:80

# Restart deployment
kubectl rollout restart deployment/puddle-app-deployment -n puddle-production

# Scale deployment
kubectl scale deployment/puddle-app-deployment --replicas=3 -n puddle-production
```

---
