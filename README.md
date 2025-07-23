# AutoAgent QA

## Overview

AutoAgent QA is an internal AI-powered helpdesk agent designed to assist employees in quickly finding answers to their questions based on internal company knowledge. This includes documents, policies, onboarding guides, and past support tickets. The assistant interacts with users through Slack, delivering fast, accurate, and context-aware responses directly in their workflow.

This solution reduces dependency on human support teams for repetitive questions and enhances productivity by making institutional knowledge instantly accessible.

## Purpose & Goals

*   Reduce time spent by employees searching for internal information.
*   Minimize human support workload by automatically handling frequently asked questions.
*   Ensure knowledge continuity by leveraging past tickets and documentation.
*   Provide seamless Slack integration, where most internal collaboration already occurs.
*   Escalate edge cases to human agents when needed, maintaining reliability and trust.

## Key Features

*   **Instant Answers:** Employees can ask questions directly in Slack. The agent replies with relevant answers drawn from company documents, guides, and prior conversations.
*   **Context-Aware Help:** The assistant uses retrieval-augmented generation (RAG) to ground its answers in your actual documentation, increasing accuracy and trust.
*   **Human Escalation:** If the agent is unsure or the answer requires judgment, the conversation is escalated to a human support agent.
*   **Feedback Collection:** Users can rate responses (e.g., 👍 / 👎), helping improve the assistant over time.
*   **Performance Monitoring:** Usage, feedback, and escalation metrics are tracked to continuously improve service quality and understand employee needs.

## Who Is It For?

*   **HR Teams** – To automate responses related to benefits, leave, and onboarding.
*   **IT Departments** – To reduce tickets about tools, access, and troubleshooting.
*   **Operations Teams** – To streamline internal process-related inquiries.
*   **All Employees** – To promote self-service and reduce waiting times.

## Status

**Progress: 20%**

### Document Ingestion
- [x] Load documents from local source
- [ ] Load documents from remote sources
- [x] Split documents into chunks
- [x] Generate embeddings for document chunks
- [x] Build/rebuild Chroma index
 
### RAG-based Question Answering
- [x] Implement RAG pipeline via LangChain
- [x] Retrieve relevant documents from Chroma
- [x] Generate answers using OpenAI GPT-4o

### Slack Integration
- [x] Handle Slack events/webhooks
- [x] Send answers to Slack
- [ ] Collect user feedback in Slack

### Human Escalation
- [ ] Implement escalation logic 
- [ ] Implement routing to real human

### Feedback Collection (Supabase)
- [ ] Store feedback
- [ ] Store and metadata in Supabase

### CMS Backend (Supabase)
- [ ] Implement login system
- [ ] Custom chroma DB
- [ ] View Currently Embedded Documents
- [ ] Delete Embedded Documents
- [ ] View Currently Embedded Documents
- [ ] Allow users to add new documents

### Logging (OpenTelemetry)
- [ ] Integrate OpenTelemetry
- [ ] Send Data to Backend for analytics.


## Tech Stack

*   Python – Core logic and integrations
*   LangChain – Language model orchestration and RAG
*   OpenAI – Language model for generating responses
*   Chroma – Local vector database for document retrieval
*   Supabase – Stores usage logs, feedback, and metadata
*   Slack API – User interface via internal Slack workspace
*   OpenTelemetry – Monitors usage and performance
