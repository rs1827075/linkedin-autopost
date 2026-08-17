---
source_title: Extending Agentforce with External MCP Tools via MuleSoft
source_link: https://developer.salesforce.com/blogs/2026/08/extending-agentforce-with-external-mcp-tools-via-mulesoft
status: pending-review
---

## Post text (edit freely, this is what gets published)

Integrating external capabilities into autonomous agents usually means writing custom wrapper code and managing brittle endpoints. Recently, Salesforce highlighted an approach using Model Context Protocol servers deployed on MuleSoft CloudHub.

What changed is that you can now secure these connections with OAuth and register them directly in Salesforce. This lets your autonomous agents execute external tools without requiring custom Apex classes for every integration.

Picture a case where an advisor's agent needs to pull real-time loan status from an external legacy core during a client call. Instead of building a bespoke REST integration in Apex, the agent calls the registered MuleSoft MCP tool directly to fetch the required data securely.

For enterprise Financial Services Cloud environments, this pattern reduces technical debt significantly. We deal with numerous external data silos, and keeping integration logic outside of Salesforce keeps our core org cleaner and easier to maintain.

How are you currently handling external tool execution for your autonomous agents? I am curious about the patterns others are testing.

#Salesforce #MuleSoft #Agentforce #Apex #Integration

## Image brief (for your own reference / manual image creation)

A clean architectural diagram showing data flow from Salesforce Agentforce through an OAuth-secured MuleSoft CloudHub MCP server to an external system.

## Reviewer checklist before merging this PR

- [ ] Every claim in the post text is actually true - check the source link
- [ ] The example paragraph reflects something real, not vague filler
- [ ] Tone sounds like you, not like a template
- [ ] An image is attached or linked below (optional)

## Image

<!-- paste an image URL or leave blank -->
