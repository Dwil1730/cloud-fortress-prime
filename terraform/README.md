
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

