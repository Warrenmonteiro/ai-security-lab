# AI Security Lab

I'm a cloud and security engineer (Azure, Entra ID, Microsoft Sentinel) building toward a role in **AI security and AI infrastructure**: designing, deploying and securing AI systems on Azure.

This repo is where that work happens in public. Each project gets its own folder, its own README, and real results: tests, evaluation scores, costs and security findings.

## What's here and what's coming

| Folder | Project | Status |
|---|---|---|
| `pdf-tools/` | Tested Python command-line tool, with CI | In progress |
| `api/` | FastAPI service deployed to Azure Container Apps with Terraform | Planned |
| `sharecipes-ai/` | **Project 1:** an AI recipe assistant (RAG) for [Sharecipes](https://sharecipes.ca), a live app with 100+ users. Azure AI Search and Microsoft Foundry, with evaluations and locked-down infrastructure | Planned |
| `security/` | Red-teaming my own AI app with PyRIT against the OWASP Top 10 for LLM Applications, then fixing what I find | Planned |
| `sentinel-triage/` | **Project 2:** an AI agent that triages Microsoft Sentinel incidents, hardened against prompt injection in alert data | Planned |

## Principles

- **Identity over secrets.** Managed identities and Entra ID instead of API keys.
- **Infrastructure as code.** Everything deploys and tears down with Terraform.
- **Measure it.** Every AI feature ships with an evaluation and a cost figure.
- **Lab data only.** Everything runs in my own Azure tenant. No client or employer data is ever used.

## Certifications

AZ-104 · AWS Solutions Architect Associate · CISA