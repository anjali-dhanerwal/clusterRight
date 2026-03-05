# PostgreSQL Health Check Analysis Prompt

## Objective
Perform a comprehensive PostgreSQL health check analysis for Aurora cluster **{cluster_name}** using predefined SQL queries and CloudWatch metrics to provide actionable insights and recommendations.
current_date is system date

## Analysis Scope

### 1. Database Performance & Size Analysis
- **Idle Connections Count**: Monitor connection pool efficiency
- **Top 5 Databases by Size**: Identify storage consumption patterns
- **Top 10 Biggest Tables**: Analyze table growth and storage usage
- **Database Age Analysis**: Check transaction ID wraparound risks
- **Top 5 Aged Tables**: Identify tables requiring maintenance attention

### 2. Index Analysis
- **Duplicate Indexes Identification**: Find redundant indexes consuming storage
- **Unused Indexes Detection**: Locate indexes that are never accessed

### 3. Table Health & Maintenance
- **Most Bloated Tables**: Identify tables requiring VACUUM operations
- **Top 10 Biggest Tables with Last Vacuum Information**: Track maintenance schedules

### 4. Configuration Parameters
- **Key PostgreSQL Parameters**: Review core database settings
- **Key Performance Parameters**: Analyze performance-related configurations
- **Logging Parameters Settings**: Verify logging configuration
- **Aurora-Specific Parameters**: Check Aurora PostgreSQL specific settings

### 5. Query Performance Analysis
- **Top 10 Short Queries Consuming CPU**: Identify high-impact queries
- **Top 10 Read Queries**: Analyze read-heavy operations
- **Top 10 UPDATE/DELETE Operations by Table**: Monitor write operations
- **Top 10 Read I/O Tables**: Identify I/O intensive tables

### 6. Temporary Space Usage
- **Top 10 Queries Writing to Temporary Space**: Monitor temp space writers
- **Top 10 Queries Reading from Temporary Space**: Monitor temp space readers

### CloudWatch Metrics
Leverage CloudWatch metrics for operational analysis with the following specifications:
- **Time Range**: **{date_range}**
- **Data Granularity**: 5-minute intervals
- **Metric Values**: Include average utilization values

#### Reference Documentation
- [Aurora Cluster Metrics](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.AuroraMonitoring.Metrics.html#Aurora.AuroraMySQL.Monitoring.Metrics.clusters)
- [Aurora Instance Metrics](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.AuroraMonitoring.Metrics.html#Aurora.AuroraMySQL.Monitoring.Metrics.instances)
- [RDS Best Practice Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html#RDS)

## Deliverables

### 1. Executive Summary
- Key performance insights highlighting critical findings
- Overall health assessment of the PostgreSQL cluster
- Priority recommendations for immediate action

### 2. Data Visualizations
- **Format**: PNG images exported directly from CloudWatch
- **Resolution**: Minimum 1200px width for high-quality output
- **Content**: Utilization trends and performance patterns
- **Annotations**: Mark performance anomalies and threshold breaches

### 3. Comprehensive Analysis Report
- **Metric Correlation**: Identify patterns and relationships between multiple metrics
- **Holistic Performance Insights**: Provide integrated view of database health
- **Pattern Analysis**: Detect trends, anomalies, and performance bottlenecks

### 4. Actionable Recommendations
- **Optimization Opportunities**: Based on observed patterns and metrics
- **Performance Tuning**: Configuration and query optimization suggestions
- **Maintenance Actions**: Required database maintenance tasks
- **Monitoring Improvements**: Enhanced alerting and monitoring recommendations

### 5. Future Projections
- **Performance Trends**: Predict future performance patterns
- **Maintenance Schedules**: Estimated maintenance schedules based on observed patterns

## Output Format

Generate a professional Word document (.docx) using Pandoc with executive-ready formatting and embedded CloudWatch visualizations.

### Output File Location

**CRITICAL: Save the generated report to the user-specified location:**
- **Output Directory**: **{output_location}**
- **File Name**: Aurora_{cluster_name}_OperationalReview_{current_date}.docx
- **Full Path**: {output_location}/Aurora_{cluster_name}_OperationalReview_{current_date}.docx

### Document Requirements
- **Format**: Microsoft Word (.docx) created via Pandoc conversion
- **Styling**: Professional formatting with consistent headings, fonts, and layout
- **Structure**: Executive-optimized with proper pagination and section breaks
- **Table of Contents**: Auto-generated with page numbers and navigation links

### CloudWatch Integration
- **Image Format**: High-resolution PNG exports directly from CloudWatch console
- **Resolution Standard**: Minimum 1200px width for crisp document display
- **Embedding Method**: Direct image insertion (not external links)
- **Image Presentation**: Proper sizing, positioning, and captioning with figure references
- **Annotations**: Clear marking of performance anomalies and threshold breaches

### Content Structure
The document must deliver a comprehensive analysis including:

1. **Executive Summary**: Key performance insights and critical findings overview
2. **Detailed Metric Analysis**: In-depth examination with embedded CloudWatch visualizations
3. **Database-CloudWatch Correlation**: Analysis connecting SQL query performance with operational metrics
4. **Prioritized Recommendations**: Implementation-ready guidance with clear action items
5. **Performance Trend Analysis**: Future projections and capacity planning insights

### Quality Standards
- Executive presentation quality suitable for C-level review
- Technical depth appropriate for database administrators and DevOps teams
- Clear visual hierarchy with professional document flow
- All CloudWatch images properly referenced and integrated into narrative text

## Success Criteria
- All predefined SQL queries executed successfully
- CloudWatch metrics retrieved and analyzed for the specified time range
- High-resolution visualizations generated and annotated
- Actionable recommendations provided based on data-driven insights
- Professional report format suitable for technical and executive audiences