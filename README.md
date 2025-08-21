Cloud Fortress Prime — AWS Security & CrowdStrike Falcon SIEM Integration 
🚀

Enterprise-grade AWS security environment with centralized SIEM, automated response, AI/ML threat detection, and compliance alignment (GDPR, HIPAA, SOC 2).

🏗️ Project Overview

Cloud Fortress Prime is a secure, production-ready AWS environment designed to centralize threat detection, accelerate incident response, and maintain compliance. It integrates multiple log sources into CrowdStrike Falcon SIEM, leverages Infrastructure as Code (IaC), and incorporates AI/ML-powered AWS services for advanced monitoring, automation, and security insights.

📊 Architecture Overview

AWS Infrastructure
- Multi-tier VPCs, IAM least privilege
- Encrypted storage with KMS, Secrets Manager

Log Sources
- GitHub, AWS CloudTrail, Google Workspace, JumpCloud SSO
- Sophos Firewall, HP Switches & Access Points
Security & Automation
- Centralized ingestion into CrowdStrike Falcon SIEM
- Automated response workflows with AWS Lambda + EventBridge

AI/ML Security
- Amazon Macie — automated discovery/classification of sensitive data → reduces exposure risks, supports GDPR/HIPAA compliance
- AWS Detective — ML-driven investigation → faster root cause analysis of incidents
- AWS Security Hub — unified posture dashboard with automated playbooks

📊 [Architecture Diagram ]
<img width="1144" height="552" alt="image" src="https://github.com/user-attachments/assets/fb85f804-da2e-493a-a7aa-ec28dcde2b4c" />

🔑 Key Features

Secure Cloud Segmentation: Multi-tier VPC + IAM least privilege → reduced lateral movement and stronger network isolation
Automated Deployments: CI/CD pipelines with Docker, GitHub Actions, and Amazon ECR → streamlined, repeatable infrastructure deployment
Unified Threat Detection: GuardDuty, CloudTrail, Security Hub, Detective → centralized visibility and faster threat identification
SIEM Integration: CrowdStrike Falcon ingestion from seven critical log sources → enterprise-level security monitoring
SOAR Workflows: Lambda + EventBridge → automated remediation, faster incident response
Infrastructure as Code: Terraform → scalable, consistent, repeatable deployments

Advanced AI/ML Security: Macie & Detective → proactive detection, classification, and investigation of threats

Compliance Ready: Controls aligned with GDPR, HIPAA, SOC 2 → audit-ready documentation and posture

🤖 AI/ML & Advanced Security Enhancements

Amazon Macie: Sensitive data discovery → mitigates exposure and regulatory risk
AWS Detective: ML-powered insights → reduces time to identify root causes
AWS Security Hub: Centralized dashboard → automated playbooks for continuous monitoring
Future Enhancements: AI-driven anomaly detection and predictive threat modeling

📁 Project Structure
cloud-fortress-prime/
├── terraform/     ← Infrastructure as Code
├── docs/          ← Daily logs & notes
├── screenshots/   ← Infrastructure proofs
└── app-code/      ← Optional automation/app code

📅 Project Progress & Milestones

✅ Day 1 — Setup: IAM, CloudWatch, Billing, CLI/tools installation

✅ Day 2 — Terraform Backend: Remote state with S3 & DynamoDB (encrypted, secure)

🔜 Day 3+: Core infrastructure deployment (VPC, networking, compute), advanced security integration, Falcon dashboard setup, AI/ML enhancements

- Full daily logs 
# Day 1 - Project Setup and AWS Account Configuration
 **Date:** July 28, 2025
 **Start Time:** 9:10 AM
 **End Time:** [11:29 AM PST AT WORK ]
 **Duration:** [2 HOURS ]
 ## Objectives Completed
 - [✅] AWS account creation and security setup
 - [✅] IAM user configuration with MFA
 - [✅] Billing alerts configured
 - [✅] Local development environment setup
 - [✅] Project structure created
 - [✅] Git repository initialized
 ## Commands Executed

🖼️ Screenshots
[Terraform Apply Success] 
<img width="1510" height="548" alt="image" src="https://github.com/user-attachments/assets/022b4319-4cfc-4b1e-a975-b6d967f0efab" />
[S3 Bucket Configuration]
<img width="1046" height="890" alt="image" src="https://github.com/user-attachments/assets/115d846e-9dc5-43fe-bede-f2023db97b09" />

[DynamoDB Lock Table]
<img width="876" height="612" alt="image" src="https://github.com/user-attachments/assets/cf1ee7d0-3cdd-41a7-a73c-ca6ff6c19100" />


Quick Start
git clone https://github.com/Dwil1730/cloud-fortress-prime.git
cd cloud-fortress-prime
terraform init
terraform apply
