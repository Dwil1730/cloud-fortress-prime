# Cloud Fortress Prime — Enterprise Cloud Security & AI-Driven Architecture Initiative 

Organization: U.S. Department of Veterans Affairs (VA)  
Duration: July 28 – August 12, 2025 (resumed August 19, 2025)  
Scope: Design, implement, and validate a secure, automated AWS cloud environment integrating enterprise firewalls, AI/ML monitoring, DLP, and CI/CD automation.

![Status: Work In Progress](https://img.shields.io/badge/status-WIP-yellow)

## Executive Summary
Cloud Fortress Prime is an initiative aimed at fortifying the U.S. Department of Veterans Affairs' cloud infrastructure by integrating advanced security measures, ensuring compliance with federal standards, and enhancing operational resilience.

## Mission
Deliver a fully architected, enterprise-grade AWS cloud environment integrating:

- Palo Alto NGFW for perimeter security  
- Netskope-style DLP for sensitive data protection  
- AI/ML monitoring with AWS Macie and Detective  
- Automated CI/CD pipelines and SOAR workflows (Lambda + EventBridge)  
- Compliance alignment (HIPAA, SOC 2, GDPR)  

The initiative demonstrates **scalable, secure, auditable cloud deployments** aligned with VA IT security and operational objectives.

## Project Progress

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 0 – Project Setup & AWS Account | ✅ Completed | AWS account, IAM users with MFA, Git repo, local dev environment |
| Phase 1 – Terraform Backend | ✅ Completed | S3 bucket & DynamoDB lock table for Terraform state |
| Phase 2 – Core Infrastructure (Parts 1 & 2) | ✅ Completed | Multi-tier VPC, public/private subnets, NAT gateways, EC2 instances, ALB, ECR, KMS, Secrets Manager |
| Phase 3 – Application Deployment & CI/CD | ✅ Completed | Containerized Flask application, Jenkins & GitHub Actions pipelines |
| **Phase 4 – Security Services (Part 1)** | **🔄 In Progress** | CloudTrail audit logging, AWS Macie data classification, DLP simulation, compliance mapping |
| Phase 4 – Security Services (Part 2) | 📋 Planned | GuardDuty, Security Hub, CSPM, automated security playbooks |
| Phase 4 – Security Services (Part 3) | 📋 Planned | AWS Detective, EventBridge + Lambda, SOAR workflows |
| Phase 5 – SOAR Testing | 📋 Planned | Incident simulation, workflow validation, automated response testing |
| Phase 6 – Demo & Documentation | 📋 Planned | Architecture diagrams, full documentation, demo script |
| Phase 7 – Project Reflection & Branding | 📋 Planned | Lessons learned, resume update, career prep |

---

## Key Highlights (Completed So Far)
- Integrated **Palo Alto NGFW** for enterprise perimeter protection  
- Implemented **multi-tier VPC architecture** with public/private subnets and NAT gateways  
- Automated **CI/CD pipelines** and **incident response workflows** with Jenkins, GitHub Actions, and Lambda  
- Leveraged **AI/ML monitoring** for threat detection and data classification (Macie, Detective)  
- Produced **enterprise-grade architecture diagrams, playbooks, and documentation**  
- Established **repeatable, scalable, and auditable cloud security framework**

---

## Architecture Overview

**Core Flow:**

Inbound Traffic → Palo Alto NGFW → ALB → EC2 → CloudTrail/GuardDuty → Macie → Security Hub → EventBridge/Lambda → Falcon SIEM → Audit Dashboard

**Data & Security Flow Mapping:**
1. **Inbound Traffic → Palo Alto Firewall:** perimeter filtering and rule enforcement  
2. **Allowed Traffic → ALB → EC2:** application layer deployment  
3. **App Activity → CloudTrail + GuardDuty:** auditing & threat detection  
4. **Sensitive Data → Macie → Security Hub:** classification & centralized findings  
5. **Incidents → EventBridge → Lambda:** automated SOAR responses  

![Architecture Diagram (WIP)]
<img width="2630" height="780" alt="image" src="https://github.com/user-attachments/assets/f70f58b5-c811-46cc-986d-a2ba4bd8fa82" />

---

## IAM Policies & Zero Trust Identity Controls

Zero Trust architecture places identity and access management at the center of the security model. This implementation enforces least-privilege access through layered IAM controls:

### IAM Policy Framework
- **Service Control Policies (SCPs)**: Organization-level guardrails preventing privilege escalation and restricting cross-account resource access
- **IAM Roles with Session Policies**: Dynamic, time-bound access for workloads using assumed roles with MFA enforcement
- **Resource-Based Policies**: S3 bucket policies, KMS key policies, and Security Group rules enforcing encryption-in-transit and data sovereignty
- **Permission Boundaries**: Applied to developer and application roles to prevent privilege creep beyond approved service actions

### Key IAM Enforcement Mechanisms
- **Conditional Access**: IAM policies using condition keys (aws:SourceIp, aws:SecureTransport, aws:MultiFactorAuthPresent) to enforce context-aware authentication
- **Cross-Account Access**: IAM roles with external ID validation and trust policies limiting AssumeRole actions to specific principals
- **Secrets Rotation**: AWS Secrets Manager automated rotation for RDS credentials, API keys, and service account passwords (90-day max lifetime)
- **Audit Logging**: CloudTrail and AWS Security Lake capturing all IAM API calls for insider threat detection and compliance validation

### Python Automation for IAM Governance
Custom Python scripts integrated into CI/CD pipelines perform:
- **Overpermissioned Role Detection**: Analyzing CloudTrail logs to identify unused IAM permissions and recommend least-privilege policies
- **Policy Drift Detection**: Comparing deployed IAM policies against approved baselines stored in Git, alerting on unauthorized changes
- **Anomaly Scoring**: Machine learning-based detection of unusual IAM activity (e.g., credential access from new geolocations, bulk data exfiltration attempts)

---

## EC2 Launch Templates & Hardened Configuration

EC2 Launch Templates enforce immutable security baselines for compute workloads:

### Launch Template Security Controls
- **AMI Hardening**: CIS Benchmark Level 1-compliant Amazon Linux 2023 images with automated patching via Systems Manager Patch Manager
- **Instance Metadata Service v2 (IMDSv2)**: Enforced via launch template metadata options (HttpTokens: required, HttpPutResponseHopLimit: 1) to prevent SSRF attacks
- **Encrypted EBS Volumes**: All volumes encrypted at rest using customer-managed KMS keys with automatic key rotation
- **Security Group Enforcement**: Launch templates reference Security Groups with zero ingress from 0.0.0.0/0, allowing only application-tier traffic from ALB security groups
- **IAM Instance Profiles**: Attached roles limited to specific S3 buckets, RDS instances, and Secrets Manager entries—no AdministratorAccess or PowerUser policies

### User Data Scripts & Configuration Management
- **Automated Hardening**: User data scripts deploy AIDE (file integrity monitoring), fail2ban (brute-force protection), and auditd (system call logging)
- **Secrets Injection**: Systems Manager Parameter Store integration retrieves database credentials at boot without hardcoding in launch templates
- **Version Control**: Launch template versions tracked in Git with approval workflows for configuration changes

---

## Beyond Configuration: Runtime Enforcement & Continuous Validation

Zero Trust requires ongoing verification, not one-time configuration. This architecture implements multiple layers of runtime checks:

### Security Automation & Policy Enforcement
- **AWS Config Rules**: Custom and managed rules continuously monitor IAM policy changes, S3 public access, Security Group drift, and encryption compliance—non-compliant resources trigger automatic Lambda remediation
- **GuardDuty Threat Detection**: Real-time monitoring for compromised credentials, cryptocurrency mining, unusual API call patterns, and reconnaissance activity
- **Security Hub Automated Response**: Lambda functions automatically isolate compromised EC2 instances, rotate exposed credentials, and revoke overpermissioned IAM sessions based on Security Hub findings
- **Network Traffic Analysis**: VPC Flow Logs analyzed by Python scripts to detect lateral movement, data exfiltration to unknown IPs, and unauthorized cross-subnet communication

### Python-Based Insider Threat Detection
Custom Python automation feeds CloudTrail, GuardDuty, and VPC Flow Logs into anomaly detection models:
- **Behavioral Analytics**: Baseline user/service behavior established over 30-day windows; deviations (e.g., 10x increase in S3 GetObject calls) trigger alerts
- **Multi-Cloud Correlation**: Aggregates AWS CloudTrail and Azure Activity Logs to detect coordinated attacks across cloud environments
- **CI/CD Security Gates**: Pre-deployment scripts scan Terraform plans for overpermissioned IAM policies, public S3 buckets, or Security Groups allowing 0.0.0.0/0—blocking deployments until remediated

### Compliance & Audit Trail
- **Immutable Logging**: CloudTrail logs stored in S3 with Object Lock (WORM) enabled, preventing tampering for HIPAA/FedRAMP audit requirements
- **Quarterly Access Reviews**: Python scripts generate IAM access reports showing last-used permissions, flagging dormant roles for deprovisioning
- **Incident Response Playbooks**: Automated playbooks using AWS Systems Manager Automation Documents for credential rotation, instance isolation, and forensic snapshot creation

---

## What Lives Outside Terraform

While Terraform deploys infrastructure baselines, several Zero Trust controls exist outside IaC for security and operational reasons:

- **IAM Policies**: Stored in AWS Organizations Service Control Policies (SCPs) and applied via AWS Control Tower—managed separately to prevent Terraform state file exposure of sensitive policies
- **Secrets & Credentials**: Managed exclusively in AWS Secrets Manager and Systems Manager Parameter Store with automated rotation—never stored in Terraform state
- **Runtime Security Rules**: AWS Config Rules, GuardDuty detectors, and Security Hub standards deployed via AWS APIs to avoid Terraform drift on managed rulesets
- **Python Security Automation**: CI/CD pipeline scripts, Lambda functions, and insider threat detection models maintained in separate Git repositories with their own deployment pipelines

---

## Current Focus
**Phase 4 – Security Services (Part 1)**  

- Audit logging via **CloudTrail**  
- Sensitive data discovery & classification via **AWS Macie**  
- DLP simulations and compliance validation  
- Documenting **security controls, audit trails, and remediation guidance**

---

## Next Steps
1. Complete Security Services phases (GuardDuty, Security Hub, Detective, SOAR automation)  
2. Integrate logs and findings into **Falcon SIEM** for central correlation and analyst triage  
3. Conduct **SOAR testing and incident simulations**  
4. Finalize **architecture diagrams, documentation, and executive demo**

