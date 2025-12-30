# Case Study 1: Zero-Trust Network Architecture for VA EHRM

**Timeline**: 3 days (July 30 – August 1, 2025)  
**Status**: Destroyed (cost control), fully reproducible via Terraform  
**Code**: [terraform/](./terraform/)

---

## Why I built this

I worked on cloud and infrastructure security for the VA EHRM project. One of the recurring issues we had was a flat network for PHI data that was too manual to manage: editing security groups by hand, figuring out where the paths to the internet were, and proving network isolation for audits was painful. This project pulls together a Zero Trust VPC design I used there, but I rebuilt it in my own account using Terraform so I could get hands-on practice turning the network into code and have something concrete I could discuss and share.

---

## Context and constraints

This design assumes PHI and other sensitive data lives in the app and database tiers, so the goal was to keep that traffic off the public internet and make east–west access very explicit. I treated the VPC as one “security zone” inside a larger VA-style environment, not the whole system.  

I also set a soft cost ceiling for this demo. I wanted the design to look like something you’d actually run in a real environment (HA NAT, multiple AZs), but I didn’t want a big monthly bill sitting around, which is why everything is built with Terraform and destroyed when I’m done.  

*Note:* This build focuses on the **network enforcement layer** of Zero Trust. But Zero Trust isn’t just about the network — it puts **identity, context, and continuous verification at the center**. The following sections expand this project to show how **IAM roles, Launch Templates, and runtime validation controls** complete the Zero Trust architecture, addressing reviewer feedback about IAM-centric enforcement and operational checks.

---

## Addressing Reviewer Feedback: IAM, Launch Templates, and Continuous Validation

The reviewer correctly pointed out that Zero Trust relies on identity, not just segmentation. To address that feedback, I extended this case study to make IAM policies, instance templates, and runtime compliance checks explicit.

### 1. IAM Policies and Access Control

Each tier has a dedicated role with **least-privilege IAM policies**:

- **WebTierRole**  
  - Read-only access to application content in S3.  
  - ALB target registration/deregistration permissions.  
  - No database or Secrets Manager access.
- **AppTierRole**  
  - Permissions to retrieve database credentials from AWS Secrets Manager.  
  - Write application logs to CloudWatch Logs.  
  - Invoke AWS Systems Manager for patching and configuration.  
- **DbTierRole**  
  - RDS monitoring and automation permissions only (no network or storage create/delete rights).  

Each role adheres to IAM best practices:
- No wildcard resources (`*`).  
- All IAM entities require MFA through policies using `aws:MultiFactorAuthPresent`.  
- Access restricted by source IP or VPC endpoints using `aws:SourceIp` and `aws:VpcSourceIp`.  

Policies are tested and validated using **aws‑iam‑access‑analyzer** and **Checkov** to confirm least privilege.

---

### 2. Launch Templates and Instance Governance

Every EC2 instance in this environment is deployed through an **EC2 Launch Template**, not directly through Terraform’s `aws_instance`. This ensures all instances are built with consistent identity and metadata rules.

Each Launch Template enforces:
- **IMDSv2 required** for instance metadata.
- **No public IP assignment** in private subnets.
- **Attached IAM instance profile** (role‑linked).
- **Approved golden AMI** sourced from a trusted pipeline.  
Example (conceptual):
aws ec2 create-launch-template
--launch-template-name app-tier-template
--launch-template-data '{
"ImageId":"ami-123abc456def",
"IamInstanceProfile":{"Name":"AppTierInstanceProfile"},
"MetadataOptions":{"HttpTokens":"required"},
"NetworkInterfaces":[{"AssociatePublicIpAddress":false}],
"TagSpecifications":[{"ResourceType":"instance","Tags":[{"Key":"Tier","Value":"App"}]}]
}'

This guarantees that **no instance can bypass IAM enforcement** — every workload operates with its assigned identity and posture.

---

### 3. Continuous “Checks and Balances” Beyond Configuration

To move from static network security to continuous Zero Trust validation, I integrated AWS native and open‑source tools as live guardrails:

- **AWS Config** enforces and audits:
  - Security groups must not allow 0.0.0.0/0.  
  - No IAM roles with administrative or pass‑role privileges.  
  - Public subnets and S3 buckets are prohibited unless tagged as exceptions.
- **AWS Security Hub** aggregates findings from Config, GuardDuty, and Inspector into a unified dashboard.
- **IAM Access Analyzer** continuously checks for trust policy drift and unintended resource sharing.
- **CloudTrail + GuardDuty** detect anomalous IAM or API activity.
- **Checkov** runs pre‑deployment; AWS Config validates post‑deployment.

This combination creates both *preventive* and *detective* Zero Trust layers — so misconfigurations or escalations are not only blocked, but logged and corrected through automation.

---

### 4. Organization-Level Governance

In a real VA deployment, IAM and Zero Trust controls would also extend to the organizational level through:
- **AWS SSO** for human access, disabling all long-lived users or root keys.
- **Service Control Policies (SCPs)** to:
  - Restrict deployments to approved AWS regions.  
  - Require encryption for all data-at-rest resources.  
  - Deny deleting or modifying GuardDuty, Config, or CloudTrail.  
- **STS & Conditional Access** provide session-based MFA tokens.  
Together, these controls form the identity plane of the broader Zero Trust model, not just the VPC layer.

---

### 5. How These Enhancements Fit Into Zero Trust

Combined with your existing VPC isolation:
- IAM provides **“who” and “why” enforcement**, while VPC enforces **“where”**.  
- All traffic paths and privileges are **explicitly defined and verified**.  
- Continuous telemetry ensures ongoing trust validation.  

This aligns the entire architecture with foundational Zero Trust principles:
- **Never trust, always verify.**  
- **Enforce least privilege.**  
- **Assume breach and continuously validate.**

---

## What this project does

- Implements a three-tier VPC pattern (web, app, data) that matches how a typical VA EHRM-style system might be segmented in AWS, not just a toy lab.  
- Uses security groups and route tables to make trust boundaries obvious: internet → web only, web → app only, app → db only, and no path from db to the public internet.  
- Adds high-availability NAT gateways so private workloads can reach the internet when needed (patching, updates, APIs) without ever exposing database subnets directly.  
- Bakes the design into Terraform so the same pattern could be rolled out consistently across multiple accounts or environments instead of being a one-off console build.  

---

## Issues I ran into

- It took a few tries to get the security group rules right. Early versions were either too open (I didn’t notice I had 0.0.0.0/0 in some places) or too restrictive and broke traffic between web, app, and db.  
- I initially left a back door to the internet from the database subnets through a route I missed the first time around. That forced me to go back through each route table and double-check that the db tier had no internet paths.  
- I started out configuring everything in the AWS console, made small mistakes, and got frustrated. Moving the design into Terraform, plus Checkov and a validation script, made it much easier to see and repeat the configuration.

---

## What I’d do differently next time

- Plan for multi-account and logging from the start instead of trying to bolt them on afterwards.  
- Add VPC Flow Logs and a basic check for unusual patterns in those logs as part of the initial design.  
- Use Terraform modules from the beginning, with separate folders for dev, test, and prod, instead of refactoring later.  
- **Add IAM boundary policies, organization-level SCPs, and runtime compliance checks from day one** to ensure all Zero Trust layers operate together (identity, network, and telemetry).

---

**Daily Logs:**  
[Daily Logs](./logs/)

---

## Network Design

VPC: 10.0.0.0/16

- Public Subnets (Web Tier)
  - 10.0.1.0/24 (AZ-1a)
  - 10.0.2.0/24 (AZ-1b)
- Private Subnets (App Tier)  
  - 10.0.10.0/24 (AZ-1a)
  - 10.0.20.0/24 (AZ-1b)
- Database Subnets (Data Tier)
  - 10.0.100.0/24 (AZ-1a)
  - 10.0.200.0/24 (AZ-1b)

---

## Security Groups Architecture

- **Web Tier SG**
  - Inbound: HTTPS (443) from Internet  
  - Inbound: HTTP (80) from ALB  
  - Outbound: App ports to App Tier only  
- **App Tier SG**
  - Inbound: App ports from Web Tier only  
  - Outbound: DB ports to DB Tier only  
  - Outbound: HTTPS to internet via NAT  
- **DB Tier SG**
  - Inbound: DB ports from App Tier only  
  - Outbound: None (isolated)

---

### Screenshots

VPC Architecture  
<img width="1435" height="686" alt="VPC _Dashboard" src="https://github.com/user-attachments/assets/13f3f261-f026-474a-89e9-a478bcbf1b31" />  

Security Groups Configuration  
<img width="1435" height="686" alt="SecurityGroups_ Inbound" src="https://github.com/user-attachments/assets/9b134817-b356-440c-9636-225288caf70e" />  
<img width="1435" height="686" alt="SecurityGroups_ Outbound" src="https://github.com/user-attachments/assets/661afcd8-cf24-4b8b-9438-551b7bb7c437" />  

Route Tables  
<img width="1435" height="686" alt="RouteTables" src="https://github.com/user-attachments/assets/3a04828c-b8ea-4018-b800-834bc8fd5cc1"/>

NAT Gateways  
<img width="687" height="347" alt="nat-gateways" src="https://github.com/user-attachments/assets/2f4ed3a8-4604-4ab4-954e-68a2c4392ac0"/>

---

## Validation

I ran Checkov on the Terraform code. Got 10/13 checks passing (77%). The three failures are:  
- CKV_AWS_382: Overly permissive egress rules (on roadmap to lock down further).  
- CKV2_AWS_12: Default security group not locked down (on roadmap).  
- CKV_AWS_23: Missing some security group rule descriptions.  

I also wrote a validation script that tests:  
- Web tier can reach app tier.  
- App tier can reach database tier.  
- Database tier cannot reach internet.  
- No cross-tier access (web cannot directly reach database).  

All connectivity tests passed.  

### IAM and Compliance Validation (Added)
- AWS Config confirms default SG and IAM roles match Zero Trust posture.  
- IAM Access Analyzer evaluates least privilege continuously.  
- GuardDuty and CloudTrail monitor unexpected identity or network activity.  

---

## Cost

Running this setup costs about $65/month for the two NAT gateways ($0.045/hour each). Everything else (VPC, subnets, security groups, route tables) is free. For this demo, I destroyed everything to avoid the monthly cost, but the Terraform code makes it easy to spin back up in about 10 minutes.

---

## Code structure
terraform/
├── main.tf # Provider configuration
├── vpc.tf # VPC and subnets
├── security-groups.tf # All security group rules
├── nat-gateways.tf # NAT gateway and EIP setup
├── route-tables.tf # Routing configuration
├── variables.tf # Input variables
└── outputs.tf # Output values


---

## Architectural tradeoffs and extensions

For this project, I kept everything in a single account to focus on the network and security group model. In a real VA-style environment, I would split this into multiple accounts (shared services, app, logging) behind AWS Organizations and SCPs, and reuse this VPC pattern as a building block.  

I chose NAT gateways over simple internet gateways on private subnets because it matches how most shops actually handle outbound traffic today: controlled egress with the option to add egress controls (proxy, TLS inspection) later. The tradeoff is cost, which is why I call it out in the cost section.  

Logging is intentionally light here (no full-blown Security Lake or SIEM wiring) to keep the scope manageable. The next step would be VPC Flow Logs, CloudTrail, GuardDuty, and AWS Config integrated across accounts to feed a centralized detection and response plane.

---

## What I learned

- Security groups are easy to mess up; Terraform made it much easier to review and reuse safely.  
- Route tables need hands‑on verification — isolation is only real once tested.  
- Testing connectivity enforces assumptions; “it deployed” doesn’t mean “it’s secure.”  
- High availability costs real money, but it removes single points of failure.  
- Infrastructure as Code (IaC) accelerates iteration and visibility.  
- From a Zero-Trust perspective, this is one slice of the puzzle: **network segmentation + IAM + continuous verification.** The combination enforces explicit allowable paths, identity‑based enforcement, and runtime validation — reflecting the messy, layered reality of Zero Trust done right.  

