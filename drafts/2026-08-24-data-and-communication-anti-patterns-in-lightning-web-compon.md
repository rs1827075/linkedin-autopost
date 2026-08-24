---
source_title: Data and Communication Anti-Patterns in Lightning Web Components
source_link: https://developer.salesforce.com/blogs/2026/08/data-and-communication-anti-patterns-in-lightning-web-components
status: pending-review
---

## Post text (edit freely, this is what gets published)

Building robust Lightning web components gets tricky when data starts flowing unpredictably between parent and child elements. Stale user interfaces and lost events often stem from subtle reactivity mistakes that are tough to track down.

Salesforce recently highlighted common data and communication anti-patterns involving the wire service, public properties, and custom events. Understanding these pitfalls helps keep state predictable across your component hierarchy.

Picture a case where a child component mutates a public property directly instead of dispatching an event upward. That hidden mutation creates tightly coupled code and causes the parent component to lose track of the actual state changes.

In enterprise implementations, keeping data flow clean prevents cascading bugs that plague complex user interfaces. Clean boundaries between components make your codebase far easier to maintain over time.

How do you typically structure communication between deeply nested components in your projects?

#Salesforce #LWC #LightningWebComponents #SalesforceDeveloper

## Image brief (for your own reference / manual image creation)

A clean architecture diagram illustrating parent-child data flow and event dispatching in a component hierarchy.

## Reviewer checklist before merging this PR

- [ ] Every claim in the post text is actually true - check the source link
- [ ] The example paragraph reflects something real, not vague filler
- [ ] Tone sounds like you, not like a template
- [ ] An image is attached or linked below (optional)

## Image

<!-- paste an image URL or leave blank -->
