resource "aws_ecr_repository" "my_ecr_repo" {
name = "puddle-app-repo"
image_tag_mutability = "MUTABLE"
}