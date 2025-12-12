# Case Study 1: Zero-Trust Network Architecture for VA EHRM

**Timeline**: 3 days (July 30 – August 1, 2025)
**Status**: Destroyed (cost control), fully reproducible via Terraform
**Code**: [terraform/](./terraform/)
## Why I built this
I worked on cloud and infrastructure security for the VA EHRM project. One of the recurring issues we had was a flat network for PHI data that was too manual to manage: editing security groups by hand, figuring out where the paths to the internet were, and proving network isolation for audits was painful. This project pulls together a Zero Trust VPC design I used there, but I rebuilt it in my own account using Terraform so I could get hands-on practice turning the network into code and have something concrete I could discuss and share.

## What this project does

- Builds a multi-tier VPC in AWS (web, app, data) spread across two AZs for extra reliability.  
- Enforces strict traffic flows using security groups: web can only talk to app, app can only talk to db, with no direct internet access from the db tier.  
- Sends all outbound traffic from the private tiers through HA NAT gateways to keep egress controlled.  
- Runs Checkov against the Terraform and a small pipeline to catch misconfigurations (like accidentally allowing 0.0.0.0/0) before applying the changes. The project files are kept so this environment can be easily rebuilt.

## Issues I ran into

- It took a few tries to get the security group rules right. Early versions were either too open (I didn’t notice I had 0.0.0.0/0 in some places) or too restrictive and broke traffic between web, app, and db.  
- I initially left a back door to the internet from the database subnets through a route I missed the first time around. That forced me to go back through each route table and double-check that the db tier had no internet paths.  
- I started out configuring everything in the AWS console, made small mistakes, and got frustrated. Moving the design into Terraform, plus Checkov and a validation script, made it much easier to see and repeat the configuration.

## What I’d do differently next time

- Plan for multi-account and logging from the start instead of trying to bolt them on afterwards.  
- Add VPC Flow Logs and a basic check for unusual patterns in those logs as part of the initial design.  
- Use Terraform modules from the beginning, with separate folders for dev, test, and prod, instead of refactoring later.

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

## Security Groups Architecture

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
### Screenshots

VPC Architecture
<img width="1435" height="686" alt="VPC _Dashboard" src="https://github.com/user-attachments/assets/13f3f261-f026-474a-89e9-a478bcbf1b31" />

Complete VPC setup showing multi-tier architecture

Security Groups Configuration
<img width="1435" height="686" alt="SecurityGroups_ Inbound" src="https://github.com/user-attachments/assets/9b134817-b356-440c-9636-225288caf70e" />
<img width="1435" height="686" alt="SecurityGroups_ Outbound" src="https://github.com/user-attachments/assets/661afcd8-cf24-4b8b-9438-551b7bb7c437" />

Microsegmentation rules enforcing zero-trust principles

Route Tables
<img width="1435" height="686" alt="RouteTables" src="https://github.com/user-attachments/assets/3a04828c-b8ea-4018-b800-834bc8fd5cc1"/>

Controlled internet access through NAT gateways

  NAT Gateways
<img width="687" height="347" alt="nat-gateways" src="https://github.com/user-attachments/assets/2f4ed3a8-4604-4ab4-954e-68a2c4392ac0"/>

High-availability NAT gateway deployment

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
## Cost

Running this setup costs about $65/month for the two NAT gateways ($0.045/hour each). Everything else (VPC, subnets, security groups, route tables) is free. For this demo, I destroyed everything to avoid the monthly cost, but the Terraform code makes it easy to spin back up in about 10 minutes. 

## Code structure

terraform/
├── main.tf # Provider configuration
├── vpc.tf # VPC and subnets
├── security-groups.tf # All security group rules
├── nat-gateways.tf # NAT gateway and EIP setup
├── route-tables.tf # Routing configuration
├── variables.tf # Input variables
└── outputs.tf # Output values


The Terraform is straightforward—no fancy modules yet, just basic resource definitions. I kept it simple because I wanted to understand exactly what each resource does before abstracting things into modules. 

## What I learned

- Security groups are easy to mess up: when you're clicking through the AWS console, it's easy to add a rule you didn't mean to or forget to restrict something properly. Having everything in code made it much easier to review and catch mistakes.  
- Route tables need careful review: I thought I had the database tier isolated, but I'd accidentally left a route to the internet gateway in one of the route table associations. Only caught it when I went through the Terraform line by line.  
- Testing is essential: I initially thought "it's just networking, if it deploys it works." I had to actually test connectivity between tiers to make sure the security groups were doing what I thought they were doing. 
- High availability costs money: two NAT gateways double the cost compared to one, but it's worth it to avoid having a single point of failure. In a real production environment, the extra cost is small compared to downtime. 
- IaC makes iteration faster: once I had the basic Terraform working, it was much faster to make changes, destroy, and rebuild than clicking through the console. Plus I have a record of exactly what I built. 
