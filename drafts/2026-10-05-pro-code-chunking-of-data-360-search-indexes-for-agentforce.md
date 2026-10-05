---
source_title: Pro-Code Chunking of Data 360 Search Indexes for Agentforce
source_link: https://developer.salesforce.com/blogs/2026/09/pro-code-chunking-of-data-360-search-indexes-for-agentforce
status: pending-review
---

## Post text (edit freely, this is what gets published)

Giving Agentforce the right context for complex financial data is tough, especially when standard search indexes break apart detailed tables and long client conversations.

Salesforce recently highlighted pro-code chunking with Data 360 Code Extension functions, giving developers more control over how documents are split before indexing.

Picture a case where an advisor uploads a multi-page wealth management review containing nested fee schedules and sensitive client identifiers. Instead of letting automated splitting chop up a table mid-row, you can write custom logic to preserve the entire fee structure while masking specific PII before it hits the search index.

In enterprise financial services, retrieval accuracy directly impacts advisor trust. When an autonomous agent pulls up retirement account details or compliance disclosures, the underlying chunks need to retain their original context without leaking sensitive data.

How are you currently handling document parsing and data preparation for your agent implementations?

#Salesforce #Agentforce #Data360 #Apex #FinancialServicesCloud

## Image brief (for your own reference / manual image creation)

A simple conceptual diagram showing a raw financial document splitting into masked, structured chunks before entering a search index.

## Reviewer checklist before merging this PR

- [ ] Every claim in the post text is actually true - check the source link
- [ ] The example paragraph reflects something real, not vague filler
- [ ] Tone sounds like you, not like a template
- [ ] An image is attached or linked below (optional)

## Image

<!-- paste an image URL or leave blank -->
