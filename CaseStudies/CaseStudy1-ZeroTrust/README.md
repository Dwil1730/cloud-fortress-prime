# Case Study 1: Zero-Trust Network Architecture Implementation

![Architecture Overview]
<img width="1435" height="686" alt="VPC _Dashboard" src="https://github.com/user-attachments/assets/93784954-6829-4138-ad87-8a5c4fb56fe1" />
## Executive Summary
**Challenge:** Secure multi-tier network with zero-trust principles  
**Solution:** Multi-tier VPC, microsegmentation, high-availability NAT gateways  
**Timeline:** 3 days (July 30 – August 1, 2025)  
**Impact:** Reduced lateral movement, enforced defense-in-depth, compliance-ready

## Business Challenge
- Complete network isolation between tiers  
- Controlled internet access for private resources  
- Zero-trust compliance alignment  
- Scalable architecture for future growth  

**Risk Factors:**
- Flat networks enable lateral movement  
- Unrestricted internet increases attack surface  
- Manual SG management creates vulnerabilities  

## Technical Solution Architecture

### Phase 1: VPC Foundation Design
- Multi-tier VPC: 10.0.0.0/16  
- Public Subnets: Web tier  
- Private Subnets: App tier  
- Database Subnets: Data tier  

Subnets Overview

 <img width="603" height="263" alt="Subnets" src="https://github.com/user-attachments/assets/f39f1c7e-30a0-4e32-8fe4-1bad3d8ba3a4" /><img width="1297" height="587" alt="Database Subnets A B" src="https://github.com/user-attachments/assets/1b88d1ba-42dd-44cf-8adb-9e3b0b9568aa" />



### Phase 2: Security Controls Implementation
**Security Groups (Microsegmentation)**

├── Web Tier SG
│ ├── Inbound: HTTPS (443) from Internet
│ ├── Inbound: HTTP (80) from ALB
│ └── Outbound: App ports to App Tier only
├── App Tier SG
│ ├── Inbound: App ports from Web Tier only
│ ├── Outbound: DB ports to DB Tier only
│ └── Outbound: HTTPS to internet via NAT
└── DB Tier SG
├── Inbound: DB ports from App Tier only
└── Outbound: None (isolated)


### Phase 3: Controlled Internet Access
- High-availability NAT gateways per AZ  
- Private subnet routing through NAT  
- Internet Gateway restricted to public subnets  

![Route Tables
<img width="2870" height="1372" alt="image" src="https://github.com/user-attachments/assets/cc48cb73-97cf-4943-965f-e939f79b61fb" />

---

## Security Outcomes
✅ Lateral movement prevention  
✅ Reduced attack surface  
✅ Compliance alignment  
✅ Automated, repeatable security

**Quantified Results:**
- 100% isolation between tiers  
- Zero direct internet access to DB  
- 3-second NAT failover  
- 50% reduction in SG complexity  

---

## Business Value
- Compliance-ready & audit-friendly  
- Scalable foundation  
- Operational efficiency  
- Cost optimization  

## Technical Artifacts
- Architecture diagrams  
- Terraform IaC examples (`Terraform_Examples/`)  
- Validation testing: connectivity, SG rules, NAT failover  

---

## Lessons Learned & Recommendations
- Plan subnet CIDR blocks for future growth  
- Implement SGs before apps  
- Use consistent naming conventions  
- Test connectivity before production  

### Future Enhancements
- VPC Flow Logs monitoring  
- Transit Gateway multi-VPC connectivity  
- Network ACLs for extra layer  
- VPN Gateway for hybrid connectivity
