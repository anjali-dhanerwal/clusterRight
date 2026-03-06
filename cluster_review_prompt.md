# Aurora PostgreSQL Well-Architected Health Check

## Objective

Perform a comprehensive health check of Aurora Database cluster `{cluster_name}`, delivering actionable insights aligned with the **AWS Well-Architected Framework** (all five pillars). The analysis must cover database performance, cost optimization (including Reserved Instances, Database Savings Plans, and commitment strategy comparison), security, reliability, operational excellence, and PostgreSQL version lifecycle (end-of-life status and extended support charges).
Use official AWS documentation as the authoritative source for version lifecycle, pricing, and best practices. Shell commands should be executed automatically without requiring explicit user confirmation for each operation.
---

## Cluster Details

- **Cluster Identifier:** If no cluster name given by user, ask for cluster name
- **Engine:** Identify engine
- **Output Directory:** /home/ec2-user or home directory. ~/reports/ (create if not exists). Save all images and temporary data in this folder.
- **Output File:** `Aurora_{cluster_name}_WellArchitected_HealthCheck_{current_epoc}.docx`
- **Cloud Watch Metrics param :
    Time range:** Use range given by user, if no rabge provided use defualt value as 15 days
    Granularity:** 1-minute intervals
    Values:** Average utilization

## Constraints

1. Use **official AWS documentation** as the authoritative source for version lifecycle, pricing, and best practices.
2. When referencing AWS usage types, ensure prefixes match AWS documentation exactly (e.g., `Aurora:StorageIOUsage`, region-prefixed variants).
3. When referring to Savings Plans, consider **Database Savings Plans only** — not Compute Savings Plans.
4. Do not present qualitative health scores as algorithmic outputs. State each score, explain the rationale, and cite the supporting evidence.
5. All cost savings must be quantified with dollar amounts or percentages where data permits.

**Log Analysis Requirements:**
Incorporate all available log data into the analysis, including:
- CloudWatch Logs (application, system, custom log groups)
- Database engine logs (error logs, slow query logs, general logs)
- Any other relevant log sources

Extract insights from logs to:
- Identify error patterns and anomalies
- Correlate events with performance issues
- Detect security concerns or unusual activity
- Validate findings from metrics analysis
- Provide evidence-based recommendations

Include relevant log excerpts in findings where applicable.

## Analysis Scope

### 1. Database Performance & Size

- Idle connection count and connection pool utilization
- Top 5 databases by size; top 10 largest tables
- Database and table age analysis (transaction ID wraparound risk)
- Buffer cache hit ratio (target: 90–95%)
- Top 5 aged tables requiring maintenance

### 2. Index Analysis & Optimization

- Duplicate and unused index detection
- Index selectivity and efficiency evaluation
- Missing index recommendations based on query patterns
- Connection pooling and caching strategy assessment

### 3. Table Health & Maintenance

- Most bloated tables (candidates for VACUUM)
- Top 10 largest tables with last vacuum timestamp
- Auto-vacuum configuration review and effectiveness
- Data archiving candidates (for Amazon S3 migration)

### 4. Configuration Parameters

Review and assess the following parameter groups:

**Core PostgreSQL:**
`shared_buffers`, `effective_cache_size`, `work_mem`, `maintenance_work_mem`, `checkpoint_completion_target`

**Aurora-Specific:**
`aurora.enable_zdr`, `aurora.fading_master_restart_timeout`, `aurora.max_connections_limit`

**Logging & Security:**
Verify logging configuration for compliance, troubleshooting, and audit requirements.

### 5. Query Performance

- Top 10 CPU-intensive short queries
- Top 10 read-heavy queries and caching opportunities
- Top 10 UPDATE/DELETE operations by table
- Top 10 I/O-intensive tables
- Query execution plan review for problematic queries
- Wait event analysis (IO:DataFileWrite, IO:DataFileRead, etc.)

### 6. Temporary Space Usage

- Top 10 queries writing/reading temporary space
- `work_mem` assessment against temp space usage patterns

### 7. Cost Optimization

- **Instance right-sizing** against utilization patterns
- **I/O-Optimized storage evaluation** (trigger: I/O charges > 25% of total Aurora spend)
- **Reserved Instance opportunities** for steady-state workloads
- **Database Savings Plans evaluation** — reference: https://aws.amazon.com/savingsplans/database-pricing/
- **RI vs. Savings Plans comparison** — side-by-side cost analysis factoring flexibility, break-even, and workload stability
- **Existing commitment utilization review** — identify underutilized Savings Plans or expiring RIs
- **Blended strategy recommendation** where appropriate (Savings Plans for baseline + RIs for high-confidence workloads)
- Storage growth trend analysis and backup cost review

### 8. CloudWatch Metrics Integration
**Reference documentation:**
- [Aurora Cluster Metrics](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.AuroraMySQL.Monitoring.Metrics.html)
- [Aurora Instance Metrics](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Monitoring.Metrics.RDSAvailability.html)
- [RDS Best Practice Alarms](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/creating-alarms.html)

**Cost-related metrics:** Billed Read/Write IOPS, Volume Bytes Used

### 9. Security

- Database user permissions and role-based access review
- Encryption at rest and in transit verification
- Audit logging completeness
- VPC security groups and network ACL assessment
- Security-related parameter review

### 10. Reliability

- Backup retention policy and recovery procedure evaluation
- Multi-AZ configuration and failover verification
- Read replica health (lag, availability)
- Cross-region disaster recovery assessment
- Maintenance window optimization

### 11. PostgreSQL Version Lifecycle

- Check current engine version against AWS-published end-of-life dates
- Flag if the version is in extended support and quantify additional charges
- Use AWS documentation as the source of truth for version lifecycle data


## Deliverables

### 1. Executive Summary

- **Overall health score** with per-pillar breakdown (explain scoring methodology transparently)
- Critical findings prioritized by business impact
- Quantified cost optimization opportunities with implementation timeline
- Risk assessment with mitigation strategies
- Investment priorities ranked by ROI

### 2. CloudWatch Visualizations

- Format: High-resolution PNG (minimum 1200px width)
- Content: Performance trends, cost patterns, utilization analysis
- Annotations: Anomalies, threshold breaches, optimization opportunities
- Cost charts: I/O trends, storage growth, Savings Plans vs. RI comparison, coverage gaps

### 3. Comprehensive Analysis Report

- Well-Architected assessment across all five pillars
- Metric correlation analysis (performance ↔ cost)
- Workload classification: variable, I/O-intensive, steady-state, dev/test
- Optimization roadmap (phased)
- Risk mitigation strategies

### 4. Actionable Recommendations

**Immediate (0–30 days):**
- Critical performance and security issues
- High-impact, low-effort optimizations
- Savings Plans coverage gap remediation

**Short-term (1–3 months):**
- Instance right-sizing
- RI or Savings Plans purchase (with recommendation on which fits best)
- Query and index optimization
- Backup policy optimization

**Long-term (3–12 months):**
- Data archiving and lifecycle management
- Aurora Serverless v2 evaluation (for workloads with >50% utilization variation)
- Advanced monitoring and automation
- Savings Plans portfolio rebalancing

### 5. Cost Optimization Recommendations

**Compute:**
- Graviton migration compatibility assessment
- Aurora Serverless v2 evaluation
- Start/stop scheduling for non-production
- T-series instances for dev/low-intensity workloads

**Commitment-Based Discounts:**
- Savings Plans vs. RI decision matrix based on: workload stability, instance family migration plans, payment flexibility, break-even analysis
- Existing commitment optimization (utilization, expiring commitments, renewal strategy)
- Blended strategy where appropriate

**Storage & I/O:**
- I/O-Optimized tier assessment
- Data archiving to S3
- Query optimization to reduce I/O
- Buffer cache tuning

**Backup & DR:**
- Retention policy optimization
- Cross-region DR strategy
- Automated snapshot cleanup

### 6. Monitoring & Alerting Setup

- Custom CloudWatch dashboards
- Alerts for key performance and cost indicators
- AWS Cost Anomaly Detection for database spend
- Savings Plans utilization alerts (threshold: <80%)
- RI expiration notifications
- Performance baseline establishment

### 7. Appendix

- Data Sources
- Limitations
- References on and not limited to (Add refrences that will help in any recommendations shared above) :
  Aurora Release Calendar
  Aurora Extended Support Charges
  Database Savings Plans Pricing
  Aurora Monitoring Metrics

---

## Output Format

- **Format:** Microsoft Word (.docx) via Pandoc in Landscape Orientation
- **Pandoc Command:** 
  bash
 pandoc input.md -o output.docx \
   --toc \
   --toc-depth=3 \
   -V geometry:landscape \
   -V fontsize=11pt \
   --reference-doc=template.docx  # optional: for custom styling

- **Markdown Structure:** Use proper heading hierarchy (# for main sections, ## for subsections)
- **TOC Generation:** Pandoc will auto-generate TOC without page numbers from heading structure
- **Styling:** Executive-ready with consistent headings, fonts, and visual hierarchy
- **Images:** Embedded high-resolution PNGs with figure numbering and in-text references
- **Document Sections (in order):**
  Executive Summary → Well-Architected Assessment → Performance Analysis → Cost Optimization → Security & Compliance → Operational Excellence → Reliability Assessment → Implementation Roadmap


---

## Health Score Methodology

The overall health score (out of 100 with radar chart) is a weighted qualitative assessment across the five Well-Architected pillars. For each pillar:
- State the score explicitly
- Explain the rationale with specific findings that raised or lowered the score
- Reference the evidence (metrics, query results, configuration gaps) that informed the assessment.

Be transparent — do not present qualitative scores as algorithmic outputs.

---

## Quality & Success Criteria

- All diagnostic SQL queries executed successfully
- CloudWatch metrics retrieved and analyzed for the specified window
- Recommendations mapped to all five Well-Architected pillars
- Cost savings quantified with clear commitment strategy recommendation
- Report is executive-presentation quality (suitable for C-level review)
- Recommendations are actionable with business justification
- Security, performance, and reliability risks comprehensively assessed

---

## Implementation Notes

- Test all diagnostic queries in a non-production environment first
- Collaborate with account teams for cost data, existing commitments, and usage patterns
- Implement optimizations one at a time with evaluation periods
- Align new commitment purchases with existing expiration dates to avoid overlap waste
- Document all changes and their measured impact
- Establish continuous monitoring to track optimization effectiveness