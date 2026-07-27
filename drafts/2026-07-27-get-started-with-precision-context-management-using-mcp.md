---
source_title: Get Started with Precision Context Management Using MCP+
source_link: https://developer.salesforce.com/blogs/2026/07/get-started-with-precision-context-management-using-mcp
status: pending-review
---

## Post text (edit freely, this is what gets published)

Agents often pull back too much data, driving up token costs and cluttering the context window. It is a common challenge when integrating large language models with enterprise systems.

Salesforce recently introduced MCP+, a post-processing layer designed to sit between your agent and its tools. It intercepts tool responses and filters them down so the agent receives only the relevant details, all without requiring a rewrite of your existing tools or agent logic.

Picture a case where an autonomous agent queries a wealth management service for a client portfolio history. Instead of dumping the entire transaction ledger into the prompt, MCP+ strips out the noise and passes just the recent holdings needed for the next reasoning step.

For Financial Services Cloud implementations dealing with complex, deeply nested financial accounts, reducing payload size directly impacts API limits and operational costs. It helps maintain performance without sacrificing the depth of data available in the background.

How are you currently managing context windows and token consumption in your Agentforce deployments? I would be interested in hearing what approaches have worked for your teams.

#Salesforce #Agentforce #Apex #FinancialServicesCloud #ArtificialIntelligence

## Image brief (for your own reference / manual image creation)

A simple conceptual diagram showing an agent querying a tool, intercepted by a filtering layer labeled MCP+, and passing a smaller data payload downstream.

## Reviewer checklist before merging this PR

- [ ] Every claim in the post text is actually true - check the source link
- [ ] The example paragraph reflects something real, not vague filler
- [ ] Tone sounds like you, not like a template
- [ ] An image is attached or linked below (optional)

## Image

<!-- paste an image URL or leave blank -->
