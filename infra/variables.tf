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
