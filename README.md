# Cloud Fortress Prime — Enterprise Cloud Security & AI-Driven Architecture Initiative 🚀
[ Status: Work In Progress](https://img.shields.io/badge/status-WIP-yellow)

**Organization:** U.S. Department of Veterans Affairs (VA)  
**Duration:** July 28 – August 12, 2025 (resumed August 19, 2025)  
**Scope:** Design, implement, and validate a secure, automated AWS cloud environment integrating **enterprise firewalls, AI/ML monitoring, DLP, and CI/CD automation**.

## **Mission**
Cloud Fortress Prime delivers a **fully architected, enterprise-grade AWS cloud environment** integrating:

- Palo Alto NGFW for perimeter security  
- Netskope-style DLP for sensitive data protection  
- AI/ML monitoring with AWS Macie and Detective  
- Automated CI/CD pipelines and SOAR workflows (Lambda + EventBridge)  
- Compliance alignment (HIPAA, SOC 2, GDPR)  

The initiative demonstrates **scalable, secure, auditable cloud deployments** aligned with VA IT security and operational objectives.

---

## Project Progress

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 0 – Project Setup & AWS Account | ✅ Completed | AWS account, IAM users with MFA, Git repo, local dev environment |
| Phase 1 – Terraform Backend | ✅ Completed | S3 bucket & DynamoDB lock table for Terraform state |
| Phase 2 – Core Infrastructure (Parts 1 & 2) | ✅ Completed | Multi-tier VPC, public/private subnets, NAT gateways, EC2 instances, ALB, ECR, KMS, Secrets Manager |
| Phase 3 – Application Deployment & CI/CD | ✅ Completed | Containerized Flask application, Jenkins & GitHub Actions pipelines |
| **Phase 4 – Security Services (Part 1)** | ⚙ **In Progress** | CloudTrail audit logging, AWS Macie data classification, DLP simulation, compliance mapping |
| Phase 4 – Security Services (Part 2) | ⏳ Planned | GuardDuty, Security Hub, CSPM, automated security playbooks |
| Phase 4 – Security Services (Part 3) | ⏳ Planned | AWS Detective, EventBridge + Lambda, SOAR workflows |
| Phase 5 – SOAR Testing | ⏳ Planned | Incident simulation, workflow validation, automated response testing |
| Phase 6 – Demo & Documentation | ⏳ Planned | Architecture diagrams, full documentation, demo script |
| Phase 7 – Project Reflection & Branding | ⏳ Planned | Lessons learned, resume update, career prep |

---

## Key Highlights (Completed So Far)
- Integrated **Palo Alto NGFW** for enterprise perimeter protection  
- Implemented **multi-tier VPC architecture** with public/private subnets and NAT gateways  
- Automated **CI/CD pipelines** and **incident response workflows** with Jenkins, GitHub Actions, and Lambda  
- Leveraged **AI/ML monitoring** for threat detection and data classification (Macie, Detective)  
- Produced **enterprise-grade architecture diagrams, playbooks, and documentation**  
- Established **repeatable, scalable, and auditable cloud security framework**

---

## Current Focus**
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

---

## Architecture Overview

Core Flow:

📊 [Architecture  Diagram (WIP)] 
<img width="2630" height="780" alt="image" src="https://github.com/user-attachments/assets/f70f58b5-c811-46cc-986d-a2ba4bd8fa82" />

**Flow Description:**  

Inbound Traffic → Palo Alto NGFW → ALB → EC2 → CloudTrail/GuardDuty → Macie → Security Hub → EventBridge/Lambda → Falcon SIEM → Audit Dashboard

**Data & Security Flow Mapping:**
1. **Inbound Traffic → Palo Alto Firewall:** perimeter filtering and rule enforcement  
2. **Allowed Traffic → ALB → EC2:** application layer deployment  
3. **App Activity → CloudTrail + GuardDuty:** auditing & threat detection  
4. **Sensitive Data → Macie → Security Hub:** classification & centralized findings  
5. **Incidents → EventBridge → Lambda:** automated SOAR responses  


