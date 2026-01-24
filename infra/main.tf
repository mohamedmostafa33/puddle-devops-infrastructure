module "ecr" {
  source   = "./modules/ecr"
  ecr_name = var.ecr_name
}

module "s3" {
  source         = "./modules/s3"
  s3_bucket_name = var.s3_bucket_name
}

module "vpc" {
  source                      = "./modules/vpc"
  vpc_cidr_block              = var.vpc_cidr_block
  public_subnet_cidr_block_a  = var.public_subnet_cidr_block_a
  public_subnet_cidr_block_b  = var.public_subnet_cidr_block_b
  private_subnet_cidr_block_a = var.private_subnet_cidr_block_a
  private_subnet_cidr_block_b = var.private_subnet_cidr_block_b
}

module "eks" {
  source             = "./modules/eks"
  cluster_name       = var.cluster_name
  vpc_id             = module.vpc.vpc_id
  public_subnet_ids  = module.vpc.public_subnet_ids
  private_subnet_ids = module.vpc.private_subnet_ids
  eks_version        = var.eks_version
  node_instance_type = var.node_instance_type
  node_min_size      = var.node_min_size
  node_max_size      = var.node_max_size
  tags               = var.tags
}