Cloud Fortress Prime — AWS Security & CrowdStrike Falcon SIEM Integration 🚀

- Enterprise-grade AWS security environment with centralized SIEM, automated response, AI/ML threat detection, and compliance alignment (GDPR, HIPAA, SOC 2).

- Includes Palo Alto firewall and Netskope policy simulation for advanced network and DLP security.

🏗️ Project Overview
Cloud Fortress Prime is a secure, production-ready AWS environment designed to:

- Centralize threat detection and accelerate incident response.

- Maintain regulatory compliance across federal and enterprise frameworks.

- Integrate multiple log sources into CrowdStrike Falcon SIEM.

- Use Infrastructure as Code (Terraform) for automated, repeatable deployments.

- Incorporate AI/ML-powered AWS services for advanced monitoring and automated remediation.

- Simulate enterprise firewall rules (Palo Alto) and DLP policies (Netskope/Defender/Purview).

📊 Architecture Overview

AWS Infrastructure
- Multi-tier VPCs with public/private subnets, NAT gateways, route tables
- IAM least privilege enforcement
- Encrypted storage with KMS, Secrets Manager

Log Sources
- GitHub, AWS CloudTrail, Google Workspace, JumpCloud SSO
- Sophos Firewall, HP Switches & Access Points
- Centralized ingestion into CrowdStrike Falcon SIEM
- Automated response workflows via AWS Lambda + EventBridge
Security & Automation
- Centralized ingestion into CrowdStrike Falcon SIEM
- Automated response workflows with AWS Lambda + EventBridge

AI/ML Security
- Amazon Macie: sensitive data discovery & classification.
- AWS Detective:  ML driven investigation of incidents.
- AWS Security Hub: centralized posture dashboard with automated playbooks.

📊 [Architecture Diagram ]
<img width="1470" height="982" alt="image" src="https://github.com/user-attachments/assets/99a2875c-3098-45bc-9576-455f9fad4ab7" />


🔑 Key Features

- Secure Cloud Segmentation: Multi-tier VPC + IAM least privilege → reduced lateral movement
- Automated Deployments: CI/CD pipelines with Terraform, GitHub Actions, Docker, Amazon ECR
- Unified Threat Detection: GuardDuty, CloudTrail, Security Hub, Detective
- SIEM Integration: CrowdStrike Falcon ingestion from seven critical log sources
- SOAR Workflows: Lambda + EventBridge → automated remediation and faster incident response
- Infrastructure as Code: Terraform → scalable, consistent deployments
- Advanced AI/ML Security: Macie & Detective → proactive threat detection and classification
- Compliance Ready: GDPR, HIPAA, SOC 2 → audit-ready posture
- Enterprise Firewall & DLP Simulation: Palo Alto rule enforcement and Netskope-style data security controls
- Advanced AI/ML Security: Macie & Detective → proactive detection, classification, and investigation of threats
- Compliance Ready: Controls aligned with GDPR, HIPAA, SOC 2 → audit-ready documentation and posture

🤖 AI/ML & Advanced Security Enhancements

- Amazon Macie: Sensitive data discovery → mitigates exposure and regulatory risk
- AWS Detective: ML-powered insights → reduces time to identify root causes
- AWS Security Hub: Centralized dashboard → automated playbooks for continuous monitoring
- Future Enhancements: AI-driven anomaly detection and predictive threat modeling

📁 Project Structure
<img width="1078" height="276" alt="image" src="https://github.com/user-attachments/assets/d54d3d83-9f11-4daa-ae17-0bd53b288cba" />

📅 Project Progress & Milestones

✅ Phase 1 – Core Infrastructure Completed
- Multi-tier VPC, public/private subnets, NAT gateways, route tables.
- EC2 instances deployed, security groups configured.
- Baseline network connectivity established.

⚙ Phase 2 – Firewall & Network Security Simulation (Current)
- AWS Network Firewall deployed.
- Stateless/stateful rule groups simulating Palo Alto & Netskope policies:
- Stateless: IP/protocol block/allow rules.
- Stateful: session tracking, HTTP/HTTPS rules.
- Firewall attached to VPC subnets.
- GuardDuty, CloudTrail, Security Hub integration for automated alerts.
- Blocker: Terraform error (Reference to undeclared resource aws_networkfirewall_rule_group.cfp_stateful_rg) → planned rewrite
⬜ Phase 3 – DLP & Data Security (Upcoming)
- Simulation of DLP with AWS Macie / Netskope-style rules.
- Data classification, audit, and compliance integration.
  
📝 Daily Logs / Notes
- Documented firewall rules, session tracking, and protocol flows.
- Visual VPC & firewall diagrams recommended for GitHub and interviews.
- Current milestone: Phase 2 – Firewall rules partially deployed.

  Sample Daily Log
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
<img width="1114" height="222" alt="image" src="https://github.com/user-attachments/assets/e3c6179b-23b7-4177-80e6-40c8adc41c8c" />
🖼️ Screenshots
[Terraform Apply Success] 
<img width="1510" height="548" alt="image" src="https://github.com/user-attachments/assets/022b4319-4cfc-4b1e-a975-b6d967f0efab" />
[S3 Bucket Configuration]
<img width="1046" height="890" alt="image" src="https://github.com/user-attachments/assets/115d846e-9dc5-43fe-bede-f2023db97b09" />

[DynamoDB Lock Table]
<img width="876" height="612" alt="image" src="https://github.com/user-attachments/assets/cf1ee7d0-3cdd-41a7-a73c-ca6ff6c19100" />


✅ Next Steps
1. Fix Terraform errors with cfp_stateful_rg.
2. Finalize stateless/stateful firewall rule groups.
3. Begin Phase 3 – DLP & Data Security simulation.


