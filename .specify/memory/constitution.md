<!--
SYNC IMPACT REPORT
Version change: 0.0.0 → 1.0.0
Modified principles:
- [PRINCIPLE_1_NAME] → Technical Accuracy & Validation
- [PRINCIPLE_2_NAME] → Clarity & Accessibility
- [PRINCIPLE_3_NAME] → Spec-First AI-Assisted Authoring
- [PRINCIPLE_4_NAME] → Reproducibility
- [PRINCIPLE_5_NAME] → Practical Implementation Focus
- [PRINCIPLE_6_NAME] → Architecture Decision Justification
Added sections: Book Standards, RAG Chatbot Standards
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ✅ Constitution Check section should align with new principles
Follow-up TODOs: None
-->

# Unified AI/Spec-Driven Book with Embedded RAG Chatbot Constitution

## Core Principles

### Technical Accuracy & Validation
All technical claims must reference official docs, specs, or verified repositories and be validated against official documentation and primary sources. This ensures that all content maintains the highest standard of technical accuracy and reliability.
<!-- Rationale: Technical accuracy is fundamental to the credibility and utility of the book -->

### Clarity & Accessibility
Content must be clear for developers, educators, and advanced learners. All explanations, code examples, and architectural decisions must be presented with sufficient context and clarity to be understood by the target audience.
<!-- Rationale: Clear communication enables effective learning and implementation -->

### Spec-First AI-Assisted Authoring
Use Claude Code + Spec-Kit Plus for spec-first, AI-assisted authoring. All features and content must begin with a clear specification before implementation, leveraging AI tools for efficiency and consistency.
<!-- Rationale: A spec-first approach ensures well-considered, consistent, and maintainable content -->

### Reproducibility
Setup, code, and deployment steps must be reproducible. All examples, configurations, and procedures must work consistently across different environments and by different users.
<!-- Rationale: Reproducibility is essential for the practical value of the book -->

### Practical Implementation Focus
Content must be practical and implementation-focused with runnable, minimal code examples. All code examples must be tested and functional, providing immediate value to readers.
<!-- Rationale: Practical examples ensure readers can immediately apply what they learn -->

### Architecture Decision Justification
Architecture decisions must be explicitly justified with clear reasoning, trade-offs, and alternatives considered. This ensures all technical choices are well-informed and defensible.
<!-- Rationale: Explicit justification leads to better architectural decisions and learning outcomes -->

## Book Standards

Framework: Docusaurus, Deployment: GitHub Pages, Structure: Modular chapters aligned with Spec-Kit Plus phases, Content type: Concept → Spec → Implementation → Validation, Markdown only, repo-ready. All book content must follow these standards to ensure consistency and maintainability.
<!-- Rationale: Standardized book structure ensures consistent experience and maintainable content -->

## RAG Chatbot Standards

Embedded within published book UI, Stack: OpenAI Agent. The RAG chatbot must be seamlessly integrated into the book interface and leverage OpenAI's agent framework for intelligent responses to user queries about the book content.
<!-- Rationale: A well-integrated chatbot enhances the learning experience by providing immediate, contextual assistance -->

## Governance

All changes to this constitution require explicit documentation of the amendment, approval process, and migration plan if applicable. The constitution supersedes all other practices and must be referenced during all significant architectural decisions and implementation planning. All PRs and reviews must verify compliance with these principles. Complexity must be justified against these principles. Use `.specify/memory/constitution.md` for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date unknown | **Last Amended**: 2025-12-24