---
source_title: Salesforce Microfrontend (UI Embedding) で React アプリの埋め込みを試す
source_link: https://developer.salesforce.com/blogs/2026/09/salesforce-microfrontend-ui-embedding-jp
status: pending-review
---

## Post text (edit freely, this is what gets published)

Integrating external JavaScript applications into Salesforce layouts has traditionally meant dealing with rigid iframe wrappers or heavy custom wrappers. We need cleaner ways to blend custom web apps right into standard record pages without losing context.

Salesforce Microfrontend UI Embedding introduces the lightning-ui-embedding capability for bringing external apps directly into Lightning pages. It allows developers to mount React applications natively while passing contextual data like the current recordId right through.

Picture a case where an advisor viewing a client account record in Financial Services Cloud needs a custom React-based portfolio visualizer embedded seamlessly right into the layout. Instead of navigating away or opening a separate tab, the component loads inline and automatically receives the active record identifier to fetch relevant financial holdings.

For enterprise Salesforce architectures, this approach helps bridge the gap between custom web development and the native platform UI. It keeps user context intact while expanding what we can build beyond standard Lightning web components.

How are you currently handling custom frontend embedding in your Salesforce implementations?

#Salesforce #React #LightningWebComponents #WebDevelopment

## Image brief (for your own reference / manual image creation)

A clean architectural diagram illustrating an external React application being embedded into a Salesforce Lightning record page via lightning-ui-embedding.

## Reviewer checklist before merging this PR

- [ ] Every claim in the post text is actually true - check the source link
- [ ] The example paragraph reflects something real, not vague filler
- [ ] Tone sounds like you, not like a template
- [ ] An image is attached or linked below (optional)

## Image

<!-- paste an image URL or leave blank -->
