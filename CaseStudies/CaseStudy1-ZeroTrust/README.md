# Case Study 1: Zero-Trust Network Architecture Implementation

Architecture Overview
<img width="2630" height="780" alt="image" src="https://github.com/user-attachments/assets/f70f58b5-c811-46cc-986d-a2ba4bd8fa82" />

 📋 Executive Summary

| Aspect | Details |
|--------|---------|
| Challenge | Secure multi-tier network with zero-trust principles |
| Solution | Multi-tier VPC, microsegmentation, high-availability NAT gateways |
| Timeline| 3 days (July 30 – August 1, 2025) |
| Impact | 100% tier isolation, reduced attack surface, compliance-ready architecture |


 🎯 Business Challenge

Modern enterprise applications face significant security challenges:

- Lateral Movement Risk: Flat networks enable attackers to move freely between systems
- Attack Surface Exposure: Unrestricted internet access increases vulnerability
- Compliance Gaps**: Manual security group management creates audit findings
- Scalability Constraints: Legacy architectures don't scale with business growth

 🏗️ Technical Architecture
 Network Design
 
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

Security Groups Architecture

 - Web Tier SG:
   - Inbound: HTTPS (443) from Internet
   - Inbound: HTTP (80) from ALB
   - Outbound: App ports to App Tier only
- App Tier SG
   - Inbound: App ports from Web Tier only
   - Outbound: DB ports to DB Tier only
   - Outbound: HTTPS to internet via NAT
- DB Tier SG
    - Inbound: DB ports from App Tier only
    - Outbound: None (isolated)
    - 
📊 Screenshots

VPC Architecture
<img width="1435" height="686" alt="VPC _Dashboard" src="https://github.com/user-attachments/assets/13f3f261-f026-474a-89e9-a478bcbf1b31" />

Complete VPC setup showing multi-tier architecture
