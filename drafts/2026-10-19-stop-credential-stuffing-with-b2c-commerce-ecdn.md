---
source_title: Stop Credential Stuffing with B2C Commerce eCDN
source_link: https://developer.salesforce.com/blogs/2026/10/stop-credential-stuffing-with-b2c-commerce-ecdn
status: pending-review
---

## Post text (edit freely, this is what gets published)

Credential stuffing attacks continue to plague retail and financial platforms, draining resources and frustrating legitimate users. Attackers rely on automated scripts to test stolen username and password combinations across login endpoints.

Salesforce has addressed this by introducing eCDN leaked-credential detection for B2C Commerce storefronts. This feature helps identify suspicious authentication attempts and prompts shoppers to reset exposed passwords before unauthorized access occurs.

Picture a case where an automated botnet targets your customer portal with thousands of leaked credentials per minute. Instead of letting those requests hit your backend apex controllers, the edge content delivery network intercepts them using configured firewall and rate-limiting rules.

For enterprise systems handling sensitive client data, mitigating automated credential abuse is critical for maintaining security compliance. Stopping these requests at the edge also preserves backend capacity for genuine customer traffic.

How is your team currently handling credential stuffing and bot mitigation on your storefronts?

#Salesforce #B2CCommerce #CyberSecurity #Cloudflare #WebSecurity

## Image brief (for your own reference / manual image creation)

A simple network diagram showing incoming bot traffic being blocked at the eCDN edge layer before reaching the commerce backend.

## Reviewer checklist before merging this PR

- [ ] Every claim in the post text is actually true - check the source link
- [ ] The example paragraph reflects something real, not vague filler
- [ ] Tone sounds like you, not like a template
- [ ] An image is attached or linked below (optional)

## Image

<!-- paste an image URL or leave blank -->
