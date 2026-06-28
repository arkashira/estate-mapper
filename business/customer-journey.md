<think>
Okay, I need to create a customer journey map for the estate-mapper product. The user provided the product hypothesis, BD rationale, and some context. Let me start by understanding each phase: Aware, Consider, Try, Adopt, Expand. 

First, the Aware phase. The trigger event here is probably when the customer faces an issue with legacy systems. Maybe they have an audit or compliance issue. The friction points could be the complexity of their environment and lack of visibility. Emotions might be frustration and anxiety. Opportunities to delight could be highlighting the ease of discovery. The metric could be website visits or demo sign-ups.

Next, the Consider phase. The trigger here is the evaluation of solutions. Friction points might be comparing with existing tools and budget constraints. Emotions could be skepticism and cautious optimism. Delight opportunities could be clear ROI examples and case studies. Metrics might be whitepaper downloads or consultations booked.

For the Try phase, the trigger is a trial or pilot. Friction could be integration with existing systems and time to see results. Emotions might be hope and impatience. Delight could come from quick setup and accurate reports. Metrics could be trial sign-ups and trial-to-purchase rate.

Adopt phase: Trigger is full deployment. Friction might be training and change management. Emotions are relief and confidence. Delight points could be automated reports and cost savings. Metrics like active users and retention rate.

Expand phase: Trigger is successful adoption leading to upselling. Friction is maybe scaling the solution. Emotions are loyalty and advocacy. Delight through advanced features. Metrics like upsell rate and referrals.

I need to make sure each phase is specific, with clear triggers, friction points, emotions, opportunities, and metrics. Also, check if the market data provided has any info, but it's empty here. Use the product's unique value in legacy environments. Avoid duplication with existing products mentioned in the portfolio. Make sure the metrics are numerical where possible.
</think>

# customer-journey.md

## **Aware**  
**Trigger event**: IT audit failure, compliance breach, or unplanned downtime due to undocumented legacy VMs/SANs/AD objects.  
**Friction points**:  
- Legacy estate complexity (hybrid on-prem/cloud, SAN sprawl, AD drift).  
- Manual discovery tools miss ephemeral workloads or misattribute ownership.  
- Fear of decommissioning "unknown" assets (risk of breaking critical systems).  
**User emotions**: Frustration, anxiety, urgency.  
**Opportunities to delight**:  
- Highlight 1-click discovery of *all* assets (VMs, containers, AD groups) in <24h.  
- Show risk scores for each asset (e.g., "92% safe-to-decommission" with owner attribution).  
**Metric**: # of demo sign-ups (target: 150/month).  

---

## **Consider**  
**Trigger event**: Evaluation of asset discovery tools vs. homegrown scripts or CSPM solutions.  
**Friction points**:  
- "Shadow IT" blind spots in legacy environments (e.g., SAN-attached VMs without cloud tags).  
- Budget constraints vs. vendor lock-in (e.g., Splunk, ServiceNow).  
- Skepticism about AI accuracy in messy telemetry logs.  
**User emotions**: Skepticism, cautious optimism.  
**Opportunities to delight**:  
- Publish case study: "Saved $2.1M/year by decommissioning 412 unused VMs in 3 weeks."  
- Offer free risk assessment (crawl public logs for known legacy assets).  
**Metric**: # of whitepaper downloads ("The $1.2T Cost of Ghost Assets") → target: 800/month.  

---

## **Try**  
**Trigger event**: Pilot approval for estate-mapper in a single business unit.  
**Friction points**:  
- Integration with legacy SIEMs (Splunk, QRadar) or log aggregators.  
- Time-to-value: "How soon can we get a decommission plan?"  
- Data privacy concerns (exposing AD logs to third-party AI).  
**User emotions**: Hope, impatience.  
**Opportunities to delight**:  
- Auto-generate a "Top 10 Assets to Decommission" report in 72h.  
- Embed risk scores in Jira/ServiceNow tickets for workflow alignment.  
**Metric**: Trial-to-purchase conversion rate (target: 40% within 30 days).  

---

## **Adopt**  
**Trigger event**: Full deployment across estate with recurring usage for quarterly audits.  
**Friction points**:  
- Training IT teams to interpret risk scores (e.g., "Why is this VM 83% safe?").  
- Change management: Convincing business units to act on recommendations.  
**User emotions**: Relief, confidence.  
**Opportunities to delight**:  
- Auto-generate compliance reports for ISO 27001, SOC 2.  
- Alert on "zombie" assets reappearing post-decommission (e.g., accidental re-provisioning).  
**Metric**: Monthly active users (target: 95% retention at 6 months).  

---

## **Expand**  
**Trigger event**: Success in legacy estate management → interest in adjacent use cases.  
**Friction points**:  
- Scaling to multi-cloud estates (AWS, Azure, GCP) with hybrid workloads.  
- Upsell resistance: "Why pay for more when our current plan works?"  
**User emotions**: Loyalty, advocacy.  
**Opportunities to delight**:  
- Add "migration risk" module for cloud lift-and-shift projects.  
- Partner with CSPs to bundle estate-mapper with migration services.  
**Metric**: Upsell rate to premium tier (target: 30% within 12 months).