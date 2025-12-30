# Puddle DevOps Infrastructure

A complete DevOps project showcasing Docker containerization, Ansible automation, and Kubernetes orchestration for the [Puddle Django web application](https://github.com/mohamedmostafa33/puddle).

## 🏗️ Architecture

```
Django App → Docker Image → AWS ECR → Kubernetes Deployment
```

## 🛠️ Technologies

- **Docker**: Container packaging
- **Ansible**: Infrastructure automation
- **Kubernetes**: Container orchestration
- **AWS ECR**: Container registry
- **Django**: Web application

## 📁 Project Structure

```
├── ansible/               # Ansible automation
│   ├── ansible.cfg
│   ├── inventory/
│   │   ├── hosts.yaml
│   │   └── group_vars/
│   │       └── all.yaml
│   └── playbooks/
│       └── ecr-deploy.yaml
├── docker/               # Docker configuration
│   ├── Dockerfile
│   └── .dockerignore
├── k8s/                  # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── puddle/               # Django application
```

## 📋 Prerequisites

- Docker 20.10+
- Python 3.10+
- Ansible 2.15+
- kubectl
- AWS CLI v2
- Minikube (for local testing)
- AWS account with ECR access

## 🚀 Installation

### 1. Python Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install boto3 botocore requests
```

### 2. Ansible Collections

```bash
ansible-galaxy collection install community.aws
ansible-galaxy collection install community.docker
```

### 3. AWS Configuration

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: us-east-1
# Default output format: json
```

### 4. ECR Authentication

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
```

## 📦 Deployment

### Deploy to AWS ECR

```bash
cd ansible
ansible-playbook playbooks/ecr-deploy.yaml
```

This will:
- Create ECR repository (if not exists)
- Build Docker image
- Push image to ECR

### Deploy to Kubernetes

```bash
# Start Minikube (for local testing)
minikube start

# Apply manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Verify deployment
kubectl get pods -n puddle-app-namespace
kubectl get svc -n puddle-app-namespace
```

## ⚙️ Configuration

### Ansible Variables

Edit [ansible/inventory/group_vars/all.yaml](ansible/inventory/group_vars/all.yaml):

```yaml
aws_region: "us-east-1"
ecr_repository_name: "puddle-app"
image_tag: "latest"
```

### Kubernetes ConfigMap

Non-sensitive Django settings in [k8s/configmap.yaml](k8s/configmap.yaml):

- `DJANGO_DEBUG`: Set to "False" for production
- `DJANGO_ALLOWED_HOSTS`: Configure allowed hosts
- `DJANGO_SECURE`: Security settings
- `DJANGO_EMAIL_BACKEND`: Email configuration

### Kubernetes Secret

Sensitive credentials in [k8s/secret.yaml](k8s/secret.yaml):

- `DJANGO_SECRET_KEY`: Django secret key (base64 encoded)
- `DATABASE_URL`: Database connection string (optional, defaults to SQLite)

**⚠️ Note**: The included secret.yaml contains demo credentials for portfolio purposes only. Update with your own secrets for production use.

## 🧪 Testing

```bash
# Check pod status
kubectl get pods -n puddle-app-namespace

# View logs
kubectl logs -n puddle-app-namespace -l app=puddle-app

# Test service
kubectl get svc -n puddle-app-namespace
# Access via LoadBalancer IP or use port-forward for local testing
kubectl port-forward -n puddle-app-namespace svc/puddle-app-service 8080:80
```

## 🔍 Troubleshooting

**Pods not starting:**
```bash
kubectl describe pod -n puddle-app-namespace <pod-name>
kubectl logs -n puddle-app-namespace <pod-name>
```

**ECR authentication issues:**
- Verify AWS credentials: `aws sts get-caller-identity`
- Re-authenticate with ECR
- Check IAM permissions for ECR operations

**Service not accessible:**
- For Minikube: Use `minikube service puddle-app-service -n puddle-app-namespace`
- For cloud: Check LoadBalancer provisioning status

## ✨ Key Features

- ✅ Automated Docker image builds with Ansible
- ✅ AWS ECR integration for container registry
- ✅ Kubernetes deployment with 3 replicas
- ✅ Health monitoring (liveness/readiness probes)
- ✅ Resource management (CPU/memory limits)
- ✅ ConfigMap and Secret for configuration management
- ✅ Production-ready Kubernetes manifests

## 🔗 Related Links

- [Puddle Django App Repository](https://github.com/mohamedmostafa33/puddle)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Ansible Documentation](https://docs.ansible.com/)

---

Built for DevOps portfolio and learning purposes 🚀