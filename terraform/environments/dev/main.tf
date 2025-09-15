provider "aws" {
  region = "us-east-1"
}

############################
# 1. VPC
############################
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
}

############################
# 2. Public Subnets
############################
resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true
}

############################
# 3. Internet Gateway
############################
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "cloud-fortress-igw"
  }
}

############################
# 4. Public Route Table
############################
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "cloud-fortress-public-rt"
  }
}

############################
# 5. Route Table Associations
############################
resource "aws_route_table_association" "public_1" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_2" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public.id
}

############################
# 6. Security Group for ALB
############################
resource "aws_security_group" "alb" {
  name        = "alb-sg"
  description = "Security group for ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

############################
# 7. Application Load Balancer
############################
resource "aws_lb" "main" {
  name               = "cloud-fortress-prime-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = [aws_subnet.public_1.id, aws_subnet.public_2.id]

  enable_deletion_protection = false

  tags = {
    Name = "cloud-fortress-prime-alb"
  }
}

############################
# 8. ALB Target Group
############################
resource "aws_lb_target_group" "app" {
  name     = "cloud-fortress-app-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }

  tags = {
    Name = "cloud-fortress-app-tg"
  }
}

############################
# 9. ALB Listener
############################
resource "aws_lb_listener" "app" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

############################
# 10. EC2 Instance
############################
resource "aws_instance" "app" {
  ami           = "ami-0ad253013fad0a42a"  # Example Amazon Linux 2 AMI
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public_1.id
  security_groups = [aws_security_group.alb.id]

  tags = {
    Name = "cloud-fortress-app-instance"
  }
}

############################
# 11. Target Group Attachment
############################
resource "aws_lb_target_group_attachment" "app" {
  target_group_arn = aws_lb_target_group.app.arn
  target_id        = aws_instance.app.id
  port             = 80
}

############################
# 12. ECR Repository
############################
resource "aws_ecr_repository" "app" {
  name                 = "cloud-fortress-app"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
    kms_key        = aws_kms_key.secrets.arn
  }

  tags = {
    Name = "cloud-fortress-app"
  }
}

############################
# 13. KMS Key for Encryption
############################
resource "aws_kms_key" "secrets" {
  description             = "KMS key for Cloud Fortress Prime secrets and encryption"
  deletion_window_in_days = 7

  tags = {
    Name = "cloud-fortress-prime-secrets-key"
  }
}

############################
# 14. KMS Key Alias
############################
resource "aws_kms_alias" "secrets" {
  name          = "alias/cloud-fortress-prime-secrets"
  target_key_id = aws_kms_key.secrets.key_id
}

############################
# 15. Secrets Manager Secret
############################
resource "aws_secretsmanager_secret" "database_password" {
  name        = "cloud-fortress-prime/database-password"
  description = "Database password for Cloud Fortress Prime application"
  kms_key_id  = aws_kms_key.secrets.arn

  tags = {
    Name = "cloud-fortress-prime-database-password"
  }
}

resource "aws_secretsmanager_secret_version" "database_password" {
  secret_id     = aws_secretsmanager_secret.database_password.id
  secret_string = jsonencode({
    username = "admin"
    password = "temporary-password-123"
    engine   = "mysql"
    host     = "localhost"
    port     = 3306
    dbname   = "cloudfortress"
  })
}

############################
# 16. Outputs
############################
output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.app.repository_url
}

output "kms_key_id" {
  description = "ID of the KMS key"
  value       = aws_kms_key.secrets.key_id
}

output "secrets_manager_arn" {
  description = "ARN of the secrets manager secret"
  value       = aws_secretsmanager_secret.database_password.arn
}
