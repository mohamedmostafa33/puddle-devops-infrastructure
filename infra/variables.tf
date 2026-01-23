variable "ecr_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "puddle-app-repo"
}

variable "s3_bucket_name" {
  description = "Name of the s3 bucket"
  type        = string
  default     = "puddle-s3-media-nti"
}

variable "vpc_cidr_block" {
  description = "The cidr for the vpc"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr_block" {
  description = "The cidr for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidr_block" {
  description = "The cidr for the private subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
  default     = "puddle-eks-cluster"
}

variable "vpc_id" {
  description = "VPC ID where the EKS cluster will be deployed"
  type        = string
}

variable "public_subnet_ids" {
  description = "Public subnet IDs"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "Private subnet IDs"
  type        = list(string)
}

variable "eks_version" {
  description = "The Kubernetes version for the EKS cluster"
  type        = string
  default     = "1.28"
}

variable "node_instance_type" {
  description = "Instance type for the node group"
  type        = string
  default     = "t3.medium"
}

variable "node_min_size" {
  description = "Minimum number of nodes"
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Maximum number of nodes"
  type        = number
  default     = 2
}

variable "tags" {
  description = "Tags for all resources"
  type        = map(string)
  default = {
    Environment = "Dev"
    Project     = "Puddle"
  }
}