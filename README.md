<<<<<<< HEAD
# cloud-fortress-prime
# Cloud Fortress Prime: AWS Security & CrowdStrike Falcon SIEM Integration

## Project Overview
Cloud Fortress Prime is a secure, production-ready AWS environment designed to integrate multiple log sources into CrowdStrike Falcon SIEM for centralized threat detection and automated incident response. This project demonstrates infrastructure as code, security automation, compliance best practices, and leverages advanced AWS security services and AI/ML capabilities to enhance threat intelligence and response.

## Architecture Overview
![Cloud Fortress Prime Architecture](./docs/cloud-fortress-prime-architecture.png)

The architecture diagram illustrates the AWS infrastructure components, log sources (GitHub, AWS CloudTrail, Google Workspace, JumpCloud SSO, Sophos Firewall, HP Switches & Access Points), CrowdStrike Falcon SIEM ingestion, and SOAR automation workflows using AWS Lambda and EventBridge.

## Key Features
- Multi-tier VPC with secure subnetting and IAM roles following least privilege principles
- CI/CD pipeline with Docker, GitHub Actions, and Amazon ECR for streamlined deployments
- Integration of AWS GuardDuty, CloudTrail, Security Hub, and AWS Detective for comprehensive threat detection and investigation
- CrowdStrike Falcon SIEM log ingestion from seven critical sources for centralized security monitoring
- Automated SOAR workflows leveraging AWS Lambda and EventBridge to accelerate incident response
- Infrastructure as code using Terraform for repeatable, scalable deployments
- Incorporation of AI/ML-powered services such as Amazon Macie for automated sensitive data discovery and classification
- Use of AWS Security Hub integrated with GuardDuty and CloudTrail to provide a unified security posture dashboard
- Secrets management and encryption using AWS Secrets Manager and AWS KMS to safeguard credentials and sensitive data

## AI/ML and Advanced Security Integration
This project embraces AWS’s AI/ML capabilities to enhance security operations:
- **Amazon Macie** automatically discovers and classifies sensitive data, reducing risk of data exposure.
- **AWS Detective** provides machine learning-driven insights to accelerate root cause analysis of security findings.
- **AWS Security Hub** aggregates findings from multiple services, enabling automated security response playbooks.
- Planned integration with AI-powered automation and anomaly detection to continuously improve threat detection accuracy.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Dwil1730/cloud-fortress-prime.git
   cd cloud-fortress-prime

---

## 📁 Project Structure

```
cloud-fortress-prime/
├── README.md
├── .gitignore
├── terraform/                ← Terraform codebase
│   ├── main.tf
│   ├── backend.tf
│   └── .terraform.lock.hcl
├── docs/
│   └── daily-logs/
│       ├── day-01-setup.md
│       └── day-02-terraform-backend.md
├── screenshots/
│   └── day-02/
│       ├── terraform-apply-success.png
│       ├── s3-bucket-config.png
│       └── dynamodb-status.png
└── app-code/ (optional)      ← Any app or automation code
```

## 📌 Daily Logs

- [Day 01 – Setup](docs/daily-logs/day-01-setup.md)
- [Day 02 – Terraform Backend](docs/daily-logs/day-02-terraform-backend.md)

## 🛠️ Terraform Details

Remote state stored in:

```
s3://cloud-fortress-prime-terraform-state-2025/dev/terraform.tfstate
```

Locking table:

```
cloud-fortress-terraform-locks
```

## 🖼️ Screenshots

Visual evidence of working infrastructure is in [screenshots/day-02/](screenshots/day-02/)

=======
Day 1 Completion Certificate
When finished, add this to your daily log:

✅ Day 1 Complete
Duration: 1 hours
AWS Services Configured: IAM, CloudWatch, Billing
Tools Installed: AWS CLI, Terraform, Docker, Git
Documentation: Started daily logging process
Next: Ready for Terraform backend setup on Day 2

Total Project Progress: 6.25% (1/16 days)
## 📅 Project Progress & Milestones

### Day 2 Completion Certificate

✅ **Day 2 Complete - Terraform Backend Mastery**  
**Duration:** 2 hours  
**Infrastructure Focus:** Remote state management with AWS S3 and DynamoDB  
**Security:** Encrypted state storage with public access blocked  
**Skills Gained:**  
- Terraform backend configuration  
- State management best practices  
- AWS S3 and DynamoDB usage for infrastructure as code  

**Next Steps:** Prepare for core infrastructure deployment including VPC, networking, and compute resources
>>>>>>> 7881a9c80684aaaff865289c8f14a63885e34508
