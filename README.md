# Puddle DevOps Infrastructure

Complete CI/CD pipeline for the [Puddle Django marketplace](https://github.com/mohamedmostafa33/puddle) with automated testing, Docker builds, and ECR deployment.

## 🏗️ Architecture

```
GitHub Push → CI Pipeline → Infrastructure Job → Terraform (ECR)
                         ↓
                    Build Job → Django Tests
                         ↓
                    Docker Job → Build & Push to ECR
```

## 🛠️ Technologies

**CI/CD**: GitHub Actions  
**IaC**: Terraform + Terraform Cloud  
**Testing**: Django Test Framework (14 tests)  
**Container**: Docker + AWS ECR  
**Orchestration**: Kubernetes  
**Automation**: Ansible  

## 📁 Project Structure

```
├── .github/workflows/
│   ├── ci.yaml           # Main CI/CD pipeline
│   └── infra.yaml        # Infrastructure provisioning
├── terraform/
│   ├── ecr.tf            # ECR repository
│   ├── versions.tf       # Terraform Cloud config
│   ├── provider.tf
│   └── outputs.tf
├── docker/
│   ├── Dockerfile        # Production image
│   └── .dockerignore
├── k8s/                  # Kubernetes manifests
│   ├── deployment.yaml   # 3 replicas + health checks
│   ├── service.yaml
│   ├── namespace.yaml
│   ├── configmap.yaml
│   └── secret.yaml
├── ansible/              # Alternative deployment
│   └── playbooks/
│       └── ecr-deploy.yaml
└── puddle/               # Django application
    ├── core/tests.py     # 7 tests
    └── item/tests.py     # 7 tests
```

## 🚀 CI/CD Pipeline

### Workflow Triggers

**Push to `feature/pipeline-setup`** → Runs complete pipeline

### Pipeline Jobs

1. **Infrastructure** (Reusable workflow)
   - Provisions AWS ECR via Terraform
   - Stores state in Terraform Cloud
   - Outputs ECR URL

2. **Build** (Tests)
   - Python 3.12 setup
   - Install dependencies
   - Run 14 Django unit tests
   - Generate coverage report

3. **Docker** (Build & Push)
   - Build image with commit SHA tag
   - Login to ECR
   - Push `:v{SHA}` and `:latest` tags

### Required Secrets

```
AWS_ACCESS_KEY_ID         # AWS credentials
AWS_SECRET_ACCESS_KEY     # AWS credentials
TF_API_TOKEN              # Terraform Cloud token
```

## 📦 Local Deployment

### 1. Provision ECR

```bash
cd terraform/
terraform init
terraform apply
```

### 2. Build & Push (Manual)

```bash
# Get ECR URL
ECR_URL=$(cd terraform && terraform output -raw ecr_repository_url)

# Build
docker build -t puddle-app:latest -f docker/Dockerfile ./puddle

# Login & Push
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_URL
docker tag puddle-app:latest $ECR_URL:latest
docker push $ECR_URL:latest
```

### 3. Deploy to Kubernetes

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## 🧪 Testing

```bash
cd puddle/
python manage.py test --verbosity=2
```

**Test Coverage:**
- Core app: Authentication, views, user management (7 tests)
- Item app: Models, CRUD operations, permissions (7 tests)

## ⚙️ Configuration

### Terraform Cloud

State managed in Terraform Cloud workspace:
- Organization: `puddle-devops`
- Workspace: `puddle-infra`

### ECR Repository

```hcl
name = "puddle-app-repo"
region = "us-east-1"
image_tag_mutability = "MUTABLE"
```

### Kubernetes

- **Replicas**: 3
- **Resources**: 256Mi RAM, 0.25 CPU
- **Health Probes**: `/` endpoint check
- **Service**: LoadBalancer on port 80

## 🔍 Troubleshooting

**Pipeline fails on terraform:**
- Check `TF_API_TOKEN` secret
- Verify Terraform Cloud workspace exists

**Tests failing:**
- Run locally: `python manage.py test`
- Check database migrations

**ECR push fails:**
- Verify AWS credentials
- Check ECR repository exists

## ✨ Key Features

✅ Automated CI/CD with GitHub Actions  
✅ Sequential job execution (infra → test → build)  
✅ Terraform Cloud state management  
✅ Reusable workflow architecture  
✅ Git SHA-based image tagging  
✅ 14 unit tests with coverage  
✅ Production-ready Kubernetes manifests  
✅ Health monitoring & auto-restart  

## 🔗 Links

- [Puddle App Repo](https://github.com/mohamedmostafa33/puddle)
- [GitHub Actions Docs](https://docs.github.com/actions)
- [Terraform Cloud](https://app.terraform.io)
- [AWS ECR](https://aws.amazon.com/ecr/)

---

**Built for DevOps portfolio** 🚀