---
source_title: Advanced Code Extension PySpark Examples for Batch Data Transforms
source_link: https://developer.salesforce.com/blogs/2026/10/advanced-code-extension-pyspark-examples-for-batch-data-transforms
status: pending-review
---

## Post text (edit freely, this is what gets published)

Processing massive volumes of client financial data often hits walls when standard transforms are not enough. We need custom logic to shape lake objects without bogging down the main org.

Salesforce recently highlighted advanced PySpark examples for code extension scripts in batch data transforms. This capability lets you run custom Python logic directly against data lake objects and data model objects within an isolated compute environment inside Data 360.

Picture a case where you need to run complex rolling calculations across millions of historical transaction records before loading them into financial services cloud. Instead of pulling everything into Apex and risking governor limits, you execute a custom batch transform script that processes the data natively in that isolated environment.

For enterprise Salesforce work, this changes how we handle heavy data ingestion pipelines for wealth management or retail banking clients. It keeps heavy computation away from transactional processing while still letting us prepare clean, unified data models.

How are you currently handling heavy batch transformations for your data lake objects? I would love to hear your approaches.

#Salesforce #Data360 #Python #FinancialServicesCloud #DataEngineering

## Image brief (for your own reference / manual image creation)

A simple conceptual diagram showing raw data lake objects flowing into an isolated PySpark compute box and outputting transformed data model objects.

## Reviewer checklist before merging this PR

- [ ] Every claim in the post text is actually true - check the source link
- [ ] The example paragraph reflects something real, not vague filler
- [ ] Tone sounds like you, not like a template
- [ ] An image is attached or linked below (optional)

## Image

<!-- paste an image URL or leave blank -->
