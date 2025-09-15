# ------------------------
# 1. Provider
# ------------------------
# ------------------------
# 2. VPC & Subnets
# ------------------------
resource "aws_vpc" "cfp_vpc" {
  cidr_block = "10.0.0.0/16"
  tags       = { Name = "CFP-VPC" }
}

# Public Subnets
resource "aws_subnet" "public1" {
  vpc_id                  = aws_vpc.cfp_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"
  tags                    = { Name = "Public-Subnet-1" }
}

resource "aws_subnet" "public2" {
  vpc_id                  = aws_vpc.cfp_vpc.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1b"
  tags                    = { Name = "Public-Subnet-2" }
}

# Private Subnets
resource "aws_subnet" "private1" {
  vpc_id            = aws_vpc.cfp_vpc.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1a"
  tags              = { Name = "Private-Subnet-1" }
}

resource "aws_subnet" "private2" {
  vpc_id            = aws_vpc.cfp_vpc.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "us-east-1b"
  tags              = { Name = "Private-Subnet-2" }
}

# ------------------------
# 3. Internet Gateway & Route Tables
# ------------------------
resource "aws_internet_gateway" "cfp_igw" {
  vpc_id = aws_vpc.cfp_vpc.id
  tags   = { Name = "CFP-IGW" }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.cfp_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.cfp_igw.id
  }

  tags = { Name = "Public-RT" }
}

resource "aws_route_table_association" "public1_assoc" {
  subnet_id      = aws_subnet.public1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public2_assoc" {
  subnet_id      = aws_subnet.public2.id
  route_table_id = aws_route_table.public_rt.id
}

# ------------------------
# 4. Security Groups
# ------------------------
resource "aws_security_group" "public_sg" {
  name   = "Public-SG"
  vpc_id = aws_vpc.cfp_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "Public-SG" }
}

resource "aws_security_group" "private_sg" {
  name   = "Private-SG"
  vpc_id = aws_vpc.cfp_vpc.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_subnet.public1.cidr_block, aws_subnet.public2.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "Private-SG" }
}

# EC2 Security Group (SSH + HTTP/HTTPS)
resource "aws_security_group" "cfp_ec2_sg" {
  name   = "CFP-EC2-SG"
  vpc_id = aws_vpc.cfp_vpc.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "CFP-EC2-SG" }
}

# ------------------------
# 5. EC2 Instance
# ------------------------
resource "aws_instance" "cfp_ec2" {
  ami           = "ami-0ad253013fad0a42a" # Replace with valid AMI
  instance_type = "t3.micro"
  key_name      = "cloud-fortress-key"

  subnet_id              = aws_subnet.public1.id
  vpc_security_group_ids = [aws_security_group.cfp_ec2_sg.id]

  associate_public_ip_address = true

  tags = { Name = "CFP-EC2-Instance" }
}
# ------------------------
# 6. AWS Network Firewall
# ------------------------
resource "aws_networkfirewall_firewall_policy" "cfp_fw_policy" {
  name = "cfp-fw-policy"

  firewall_policy {
    # Stateful rule group reference
    stateful_rule_group_reference {
      resource_arn = aws_networkfirewall_rule_group.cfp_stateful_rg.arn
    }
    # Stateless rule group reference
    stateless_rule_group_reference {
      priority     = 1
      resource_arn = aws_networkfirewall_rule_group.cfp_stateless_rg.arn
    }

    # Default actions for stateless engine
    stateless_default_actions          = ["aws:pass"]
    stateless_fragment_default_actions = ["aws:pass"]
  }
}
  # ❌ Remove tags here — not supported on firewall_policy
  # tags = { Name = "CFP-Firewall-Policy"} 

resource "aws_networkfirewall_firewall" "cfp_fw" {
  name                = "CFP-Firewall"
  firewall_policy_arn = aws_networkfirewall_firewall_policy.cfp_fw_policy.arn
  vpc_id              = aws_vpc.cfp_vpc.id

  subnet_mapping { subnet_id = aws_subnet.public1.id }
  subnet_mapping { subnet_id = aws_subnet.public2.id }

  # ✅ Tags are allowed here
  tags = { Name = "CFP-Firewall" }
}

# ------------------------
# ------------------------
# ------------------------
# 1. Stateless Rule Group
# ------------------------
resource "aws_networkfirewall_rule_group" "cfp_stateless_rg" {
  name     = "CFP-Stateless-RG"
  type     = "STATELESS"
  capacity = 100

  rule_group {
    rules_source {
      stateless_rules_and_custom_actions {
        stateless_rule {
          priority = 1

          rule_definition {
            actions = ["aws:pass"]
            match_attributes {
              source {
                address_definition = "0.0.0.0/0"
              }
              destination {
                address_definition = "10.0.3.0/24"
              }
              protocols = [6] # TCP
              destination_port {
                from_port = 80
                to_port   = 80
              }
            }
          }
        }
      }
    }
  }
}

# ------------------------
# 2. Stateful Rule Group
# ------------------------
resource "aws_networkfirewall_rule_group" "cfp_stateful_rg" {
  name     = "cfp-stateful-rg"
  type     = "STATEFUL"
  capacity = 100

  rule_group {
    rules_source {
      rules_string = <<EOT
pass tcp any any -> any any (msg: "Allow all TCP traffic"; sid:1; rev:1;)
EOT
    }
  }
}

# ------------------------
# 3. Firewall Policy
# Now you can reference it safely
# ------------------------
# 7. S3 Bucket
# ------------------------
resource "aws_s3_bucket" "ml_data" {
  bucket = "cloud-fortress-ml-data-20250814"
}

# ------------------------
# 8. Outputs
# ------------------------
output "vpc_id" { value = aws_vpc.cfp_vpc.id }
output "public_subnets" { value = [aws_subnet.public1.id, aws_subnet.public2.id] }
output "private_subnets" { value = [aws_subnet.private1.id, aws_subnet.private2.id] }
output "firewall_arn" { value = aws_networkfirewall_firewall.cfp_fw.arn }
output "ec2_id" { value = aws_instance.cfp_ec2.id }
output "s3_bucket" { value = aws_s3_bucket.ml_data.id }
