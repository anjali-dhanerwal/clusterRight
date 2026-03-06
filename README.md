# EC2 Instance Setup Requirements

## Prerequisites

- AWS EC2 instance (Amazon Linux 2023 or RHEL-based distribution)
- SSH access to the instance
- Sudo privileges

### Database Connectivity Requirement

The Aurora PostgreSQL cluster being reviewed must be accessible from the system where the agent is running. The agent connects to the cluster using the [AWS RDS Data API / PostgreSQL MCP Server](https://github.com/awslabs/mcp) and supports the following connection methods:

- **RDS Data API** (recommended) — requires the Data API to be enabled on the Aurora cluster and the execution role to have `rds-data:ExecuteStatement` permissions.
- **IAM Database Authentication** — requires IAM auth enabled on the cluster and the `rds-db:connect` permission for the target DB user.
- **Native PostgreSQL credentials (pgwire)** — requires network connectivity (VPC/security group access) from the agent host to the cluster endpoint on port 5432, along with valid database credentials.

If the cluster is not reachable via any of these methods (e.g., the agent runs outside the VPC with no Data API enabled, or credentials are unavailable), the analysis will still run but will **exclude all database-level diagnostics**, including:

- Table size, bloat, and vacuum analysis
- Index usage and duplicate index detection
- Query performance analysis (pg_stat_statements)
- Configuration parameter review (pg_settings)
- Connection pool utilization and idle connection counts
- Transaction ID wraparound risk assessment

The report will still include CloudWatch metrics analysis, cost optimization, version lifecycle assessment, and Well-Architected recommendations based on externally available data.

> **Note — Aurora MySQL:** Database-level diagnostics are currently supported for Aurora PostgreSQL only. For Aurora MySQL clusters, the agent does not connect to the database and the analysis will be limited to CloudWatch metrics, cost optimization, version lifecycle assessment, and Well-Architected recommendations based on externally available data. MySQL support for in-database diagnostics is planned for a future release.

### Required IAM Roles

1. **EC2 Instance Role**
   - Attached to the EC2 instance
   - Permissions: S3 write access to `s3://<Bucket Name>` bucket
   - Example policy:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:PutObject",
           "s3:PutObjectAcl"
         ],
         "Resource": "arn:aws:s3:::<Bucket Name>/*"
       }
     ]
   }
   ```

2. **Application Execution Role**
   - Used by the application for Aurora cluster analysis
   - Required permissions include:
     - **RDS**: Read-only access to describe DB clusters, instances, parameters, snapshots, logs, and recommendations
     - **CloudWatch**: Read access to metrics, logs, alarms, and anomaly detection
     - **Cost Explorer & Billing**: Access to cost data, budgets, savings plans, and optimization recommendations
     - **Compute Optimizer**: Access to EC2, RDS, Lambda, and ECS recommendations
   
   The role requires four managed policies:
   
   **Policy 1: clusterRightRDSMCP** (50+ read-only RDS actions including):
   - `rds:Describe*` - All describe operations for clusters, instances, parameters
   - `rds:DownloadDBLogFilePortion` - Log file access
   - `rds:ListTagsForResource` - Resource tagging information
   - `rds-db:connect` - Database connection capability
   
   **Policy 2: clusterRightCloudWatchMCP** (60+ read-only actions including):
   - `cloudwatch:GetMetric*` - Metric data retrieval
   - `cloudwatch:DescribeAlarms` - Alarm configuration
   - `logs:DescribeLogGroups` - Log group discovery
   - `logs:FilterLogEvents` - Log analysis
   - `logs:StartQuery` / `logs:GetQueryResults` - CloudWatch Insights queries
   
   **Policy 3: clusterRightPricingMCP** (80+ read-only actions including):
   - `ce:GetCostAndUsage*` - Cost Explorer data
   - `ce:GetSavingsPlans*` - Savings Plans analysis
   - `ce:GetReservation*` - Reserved Instance data
   - `compute-optimizer:Get*Recommendations` - Optimization recommendations
   - `budgets:ViewBudget` - Budget information
   - `cost-optimization-hub:*` - Cost optimization insights
   
   **Policy 4: cloudControlMCP** (CloudFormation resource access):
   - `cloudformation:ListResources` - List CloudFormation resources
   - `cloudformation:GetResource` - Get resource details
   - `cloudformation:GetResourceRequestStatus` - Check resource request status
   - `cloudformation:ListResourceRequests` - List resource requests
Refer : user-policy.json and update resources to limit the access.

## Installation Steps

### 1. Install Python 3.11
```bash
sudo yum install python3.11 -y
```

### 2. Install Git
```bash
sudo yum install git -y
```

### 3. Install Pandoc
```bash
sudo yum install pandoc -y
```

### 4. Install GitHub CLI
```bash
sudo dnf install 'dnf-command(config-manager)' -y
sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install gh --repo gh-cli -y
```

### 5. Configure Git
```bash
git config --global user.name "Your Name"
git config --global user.email "youremail@domain.com"
```

### 6. Authenticate GitHub CLI
```bash
gh auth login
```
Follow the interactive prompts to complete authentication.

## Verification

Verify installations:
```bash
python3.11 --version
git --version
pandoc --version
gh --version
```

## Notes

- Replace `"Your Name"` and `"youremail@domain.com"` with your actual Git credentials
- GitHub CLI authentication requires a GitHub account and personal access token or browser-based OAuth flow

---

## Project Setup

### 7. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 8. Set Up Python Virtual Environment
```bash
python3.11 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

### 9. Configure Environment Variables
```bash
cp .env.example .env
vim .env
```
Update the `.env` file with your configuration values.

---

## Running the Application

### Execute the Health Check
```bash
source ./venv/bin/activate
python3.11 aurora_cluster_operational_review.py
sample api call "curl http://<IP>:8085/invocations  -H "Content-Type: application/json" -d '{"prompt": "Give me the name of Aurora cluster in my account"}'"
```


### Upload Output to S3
```bash
aws s3 cp <Output Files> s3://<Bucket Name>/reports --recursive 
```
