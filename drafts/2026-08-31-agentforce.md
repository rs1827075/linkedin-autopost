---
source_title: 新しいAgentforceメタデータと開発ライフサイクル
source_link: https://developer.salesforce.com/blogs/2026/08/new-agentforce-metadata-and-development-lifecycle-jp
status: pending-review
---

## Post text (edit freely, this is what gets published)

managing agent configurations across multiple sandboxes and production environments often feels unnecessarily fragile. teams frequently struggle with tracking changes and maintaining smooth delivery pipelines for autonomous features.

salesforce recently introduced new version-managed metadata models alongside a human-readable agent script format. this update aims to streamline ci/cd pipelines and simplify peer reviews for intelligent automation assets.

picture a case where your deployment process relies on these new readable scripts instead of bundled assets that cause widespread side effects. by isolating changes, your team can review updates faster and push agent improvements with greater confidence.

for financial services cloud implementations, this matters because we handle sensitive client data and complex compliance workflows. keeping deployment steps reliable and transparent helps maintain strict governance over customer-facing logic.

how is your team currently handling version control and metadata deployment for autonomous agents in your org?

#salesforce #agentforce #cicd #devops #salesforcedevelopers

## Image brief (for your own reference / manual image creation)

a minimalist diagram showing a ci/cd pipeline branching into clean code review steps for metadata models.

## Reviewer checklist before merging this PR

- [ ] Every claim in the post text is actually true - check the source link
- [ ] The example paragraph reflects something real, not vague filler
- [ ] Tone sounds like you, not like a template
- [ ] An image is attached or linked below (optional)

## Image

<!-- paste an image URL or leave blank -->
