<think>
Okay, I need to create a REQUIREMENTS.md for the estate-mapper project. Let me start by understanding the context provided. The project is an agent that auto-discovers VMs and services in mixed legacy estates, infers usage and owners from logs, and ranks them for decommissioning or migration risk. 

First, I should outline the functional requirements. The main functions would be discovery, analysis, ranking, and reporting. So FR-1 would be about discovering VMs and services. I need to specify the protocols and data sources it should support, like SSH, SMB, SNMP, and logs from auth systems. 

Next, FR-2 is analyzing usage and ownership. The agent needs to process network traffic, telemetry, and auth logs to determine usage patterns and infer owners. Maybe using ML models for that. 

FR-3 is ranking assets based on risk and decommissioning potential. The criteria should include usage frequency, criticality, dependencies, and owner engagement. 

FR-4 is generating reports. The output should be in formats like JSON, CSV, and HTML with visualizations. 

Now non-functional requirements. Performance: it should handle large estates efficiently. Let's say process 10,000 assets in under an hour. Security is important since it deals with logs and credentials. Need encryption at rest and in transit, role-based access, and secure credential storage. 

Reliability: high availability, maybe 99.9% uptime, and fault tolerance. Scalability to handle up to 100,000 assets. 

Constraints: must work with existing tools like Ansible and Terraform. Compatibility with Linux and Windows. No need for agent installation on hosts. 

Assumptions: access to necessary logs and telemetry, existing infrastructure for data collection, and that users have permissions. 

I should structure all this into the markdown document with appropriate sections. Make sure each requirement is clear and shippable. Check for any missing points, like data sources or specific protocols. Also, ensure that the constraints and assumptions are realistic based on the provided context.
</think>

# REQUIREMENTS.md

## Functional Requirements

**FR-1: Asset Discovery**  
- Automatically discover VMs and services across mixed estates (Linux/Windows, cloud/on-prem)  
- Support discovery via:  
  - SSH/SFTP (Linux)  
  - SMB/WinRM (Windows)  
  - SNMP (network devices)  
  - Cloud provider APIs (AWS, Azure, GCP)  
- Map discovered assets to IP addresses, hostnames, and service ports  

**FR-2: Usage Analysis**  
- Analyze network traffic patterns (firewall logs, NetFlow) to identify active/passive usage  
- Process telemetry data (CPU/RAM/disk metrics) from monitoring systems (Prometheus, Datadog)  
- Parse authentication logs (LDAP, Active Directory, SSO) to identify user access patterns  
- Use ML models to detect anomalous usage patterns (e.g., seasonal vs. continuous)  

**FR-3: Ownership Inference**  
- Correlate service usage with:  
  - Email headers from automated alerts  
  - Git commit history for associated codebases  
  - Jira/ServiceNow tickets referencing the asset  
  - LDAP group memberships  
- Rank confidence scores for inferred ownership (0-100%)  

**FR-4: Risk Ranking**  
- Calculate decommission risk score based on:  
  - Usage frequency (last 90 days)  
  - Criticality (number of dependent services)  
  - Security posture (CVEs, patch status)  
  - Owner engagement (ticket activity, SLAs)  
- Generate migration risk matrix with color-coded tiers (Green/Yellow/Red)  

**FR-5: Output Generation**  
- Export structured reports in:  
  - JSON (for automation pipelines)  
  - CSV (for spreadsheet analysis)  
  - HTML (interactive dashboards with D3.js visualizations)  
- Include:  
  - Asset inventory with metadata  
  - Risk scores and confidence metrics  
  - Recommended decommission/migration order  

## Non-Functional Requirements

**Performance**  
- Process 10,000+ assets in <1 hour (95th percentile)  
- Maintain <500ms latency for API queries during analysis  
- Support parallel processing of 10+ discovery channels  

**Security**  
- Encrypt all credentials in transit (TLS 1.3+) and at rest (AES-256)  
- Implement RBAC with 3 distinct user roles (Viewer/Analyst/Admin)  
- Store secrets in HashiCorp Vault or AWS Secrets Manager  
- Comply with SOC 2 Type II standards  

**Reliability**  
- 99.9% SLA for continuous discovery pipelines  
- Auto-retry failed discovery attempts (exponential backoff)  
- Maintain 7-day history of analysis results for audit trails  

**Scalability**  
- Support estates with up to 100,000+ assets  
- Horizontal scaling via Kubernetes (Helm charts provided)  
- Stateless architecture for load-balanced deployment  

## Constraints

- Must integrate with existing tooling:  
  - Ansible for configuration discovery  
  - Terraform for cloud resource mapping  
  - ELK stack for log analysis  
- No agent installation required on target hosts  
- Must work with legacy systems (Windows Server 2008 R2+)  
- Output format must be compatible with Axentx's BRAIN (pgvector) schema  

## Assumptions

- Access to:  
  - Centralized log aggregation system  
  - CMDB (Configuration Management Database)  
  - Service ticketing system API  
- Users have:  
  - Read access to network telemetry  
  - Read-only credentials for discovery  
  - Permission to analyze non-sensitive logs  
- Existing infrastructure for:  
  - Container orchestration (Kubernetes)  
  - Secret management  
  - High-availability storage (S3-compatible)
