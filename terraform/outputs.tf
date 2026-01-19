output "ecr_repository_url" {
  value = aws_ecr_repository.my_ecr_repo.repository_url
}

output "s3_bucket_name" {
  value = aws_s3_bucket.puddle_app_bucket.bucket
}