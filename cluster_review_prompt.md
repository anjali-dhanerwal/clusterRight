# Aurora Well-Architected Health Check

## Objective

Perform a comprehensive health check of Aurora Database cluster `{cluster_name}`, delivering actionable insights aligned with the **AWS Well-Architected Framework** (all five pillars). The analysis must cover database performance, cost optimization (including Reserved Instances, Database Savings Plans, and commitment strategy comparison), security, reliability, operational excellence, and version lifecycle (end-of-life status and extended support charges).
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
- **PostgreSQL-specific:**
  - Database and table age analysis (transaction ID wraparound risk)
  - Top 5 aged tables requiring maintenance (autovacuum assessment)
- Buffer cache hit ratio (target: 90–95%)
  *PostgreSQL:* pg_stat_bgwriter / shared buffer stats
  *MySQL:* InnoDB buffer pool hit ratio (Innodb_buffer_pool_read_requests vs Innodb_buffer_pool_reads)
- **MySQL-specific:**
  - InnoDB buffer pool utilization (Innodb_buffer_pool_pages_free vs Innodb_buffer_pool_pages_total)
  - Table fragmentation analysis (data length vs index length vs data free)
  - Thread cache efficiency (Threads_created vs Connections)


### 2. Index Analysis & Optimization

- Duplicate and unused index detection
  *PostgreSQL:* via pg_stat_user_indexes (index scan counts)
  *MySQL:* via sys.schema_unused_indexes and sys.schema_redundant_indexes
- Index selectivity and efficiency evaluation
- Missing index recommendations based on query patterns
  *PostgreSQL:* sequential scan analysis via pg_stat_user_tables
  *MySQL:* performance_schema statement analysis and sys.statements_with_full_table_scans
- Connection pooling and caching strategy assessment
- **MySQL-specific:**
  - Index cardinality accuracy (ANALYZE TABLE recency)
  - Adaptive hash index effectiveness (Innodb_adaptive_hash_searches vs Innodb_adaptive_hash_searches_btree)
  - Full-text index and spatial index review (if applicable)

### 3. Table Health & Maintenance

- **PostgreSQL-specific:**
  - Most bloated tables (candidates for VACUUM)
  - Top 10 largest tables with last vacuum/autovacuum timestamp
  - Autovacuum configuration review and effectiveness
  - Dead tuple ratio analysis
- **MySQL-specific:**
  - Table fragmentation detection (DATA_FREE from information_schema.TABLES)
  - Tables requiring OPTIMIZE TABLE (high free space ratio)
  - InnoDB row format review (COMPACT vs DYNAMIC vs COMPRESSED)
  - Auto-increment capacity usage (current value vs max for column type)
  - information_schema.TABLES staleness — UPDATE_TIME review for maintenance recency
- Data archiving candidates (for Amazon S3 migration)

### 4. Configuration Parameters

Review and assess the following parameter groups (not limited to these — refer to the official [PostgreSQL documentation](https://www.postgresql.org/docs/) and [
MySQL documentation](https://dev.mysql.com/doc/) for the specific engine version in use to identify additional relevant parameters):

**Core PostgreSQL:**
`shared_buffers`, `effective_cache_size`, `work_mem`, `maintenance_work_mem`, `checkpoint_completion_target`

**Core MySQL:**
innodb_buffer_pool_size, innodb_log_file_size, innodb_flush_log_at_trx_commit, max_connections, table_open_cache, tmp_table_size

**Aurora PostgreSQL-Specific:**
`aurora.enable_zdr`, `aurora.fading_master_restart_timeout`, `aurora.max_connections_limit`

**Aurora MySQL-Specific:**
aurora_disable_hash_join, aurora_parallel_query, aurora_read_replica_read_committed, aurora_binlog_replication_max_yield_seconds, aurora_lab_mode

**Logging & Security:**
Verify logging configuration for compliance, troubleshooting, and audit requirements.

### 5. Query Performance

- Top 10 CPU-intensive short queries
- Top 10 read-heavy queries and caching opportunities
- Top 10 UPDATE/DELETE operations by table
- Top 10 I/O-intensive tables
- Query execution plan review for problematic queries
- Wait event analysis
  - *PostgreSQL:* IO:DataFileWrite, IO:DataFileRead, etc. via pg_stat_activity
  - *MySQL:* performance_schema.events_waits_summary_global_by_event_name (e.g., io/file/innodb/*, synch/mutex/*)
- **MySQL-specific:**
  - Slow query log analysis (queries exceeding long_query_time)
  - Full table scan frequency (Select_scan, Select_full_join status counters)
  - Sort and temp table spill-to-disk rates (Sort_merge_passes, Created_tmp_disk_tables)
  - Prepared statement usage and efficiency (Com_stmt_* counters)
  - Locking contention analysis (Innodb_row_lock_waits, Innodb_row_lock_time_avg)

### 5a. Performance Insights Analysis

**Reference documentation:**
- [Performance Insights Overview](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_PerfInsights.html)
- [Performance Insights API](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_PerfInsights.API.html)

**Prerequisites:**
- Verify Performance Insights is enabled on the cluster instances
- Check retention period (free tier: 7 days; paid: up to 2 years)

**DB Load Analysis:**
- Average DB load vs. vCPU count (identify saturation)
- DB load breakdown by wait events (top 10 wait states)
- DB load breakdown by SQL (top 10 queries by load)
- DB load breakdown by user/host/database
- Peak load periods and correlation with application events

**Top SQL Analysis (via Performance Insights):**
- Top 10 SQL statements by DB load (AAS)
- Top 10 SQL by average latency
- Top 10 SQL by calls per second
- SQL statements with highest wait time contribution
- Digest-level query grouping for pattern identification

**Wait Event Deep Dive:**
- Top wait events by category (CPU, IO, Lock, Network, Memory)
- *PostgreSQL:* Client:ClientRead, IO:DataFileRead, Lock:transactionid, LWLock:buffer_mapping
- *MySQL:* io/file/innodb/innodb_data_file, synch/mutex/innodb/buf_pool_mutex, io/table/sql/handler
- Wait event trends over the analysis window (identify emerging bottlenecks)

**Counter Metrics (via Performance Insights):**
- Active sessions over time
- Transactions per second (TPS) trends
- Rows examined vs. rows returned ratio
- Temp bytes usage trends

**Recommendations:**
- Correlate Performance Insights findings with CloudWatch metrics and query analysis (Sections 5, 6)
- Identify queries that are candidates for optimization based on combined DB load and wait event data
- Recommend Performance Insights retention upgrade if current retention is insufficient for trend analysis

### 6. Temporary Space Usage

- Top 10 queries writing/reading temporary space
  *PostgreSQL:* via pg_stat_statements (temp_blks_read, temp_blks_written)
  *MySQL:* via performance_schema.events_statements_summary_by_digest (SUM_CREATED_TMP_DISK_TABLES, SUM_CREATED_TMP_TABLES)
- **PostgreSQL-specific:**
  - work_mem assessment against temp space usage patterns
- **MySQL-specific:**
  - tmp_table_size and max_heap_table_size assessment against disk-based temp table creation rates
  - Internal temp table engine usage review (internal_tmp_mem_storage_engine — TempTable vs MEMORY)
  - InnoDB temp tablespace usage (innodb_temp_data_file_path sizing)

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

### 11.Version Lifecycle

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
  Performance Insights User Guide
  Performance Insights Counter Metrics

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