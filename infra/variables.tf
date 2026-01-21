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