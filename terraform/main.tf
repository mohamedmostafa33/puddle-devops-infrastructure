resource "aws_ecr_repository" "my_ecr_repo" {
name = var.ecr-name
image_tag_mutability = "MUTABLE"
}

