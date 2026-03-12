# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Tutorial materials for an AI-assisted development workflow course. Students fork this repo and use it to build and deploy an e-commerce sales dashboard. The repo contains documentation only — no application code. Students create their own application code (`app.py`, `requirements.txt`) during the workshop.

## Repository structure

```
README.md                      # Overview and getting started
v2/                            # Current version of the tutorial
  pre-work-setup.md            # Account creation, tool installation, repo setup (async pre-work)
  workshop-build-deploy.md     # Full workshop: MCP, spec-kit, build, deploy (~3 hours)
  README.md                    # v2 overview
v1/                            # Original multi-session tutorial (reference)
prd/ecommerce-analytics.md     # Product requirements document for the dashboard
data/sales-data.csv            # Sample dataset (~1000 transaction records)
```

## What students build

A Streamlit dashboard (`app.py`) reading from `data/sales-data.csv` with:
- KPI cards: Total Sales (~$650-700K), Total Orders (482)
- Sales trend line chart (monthly)
- Sales by category bar chart (Electronics, Accessories, Audio, Wearables, Smart Home)
- Sales by region bar chart (North, South, East, West)

Tech stack: Python 3.11+, Streamlit, Plotly, Pandas. Package manager: `uv`.

## Key commands

```bash
# Run the dashboard locally (once app.py is created)
streamlit run app.py

# Install dependencies (once requirements.txt is created)
uv pip install -r requirements.txt

# spec-kit workflow (run before coding)
specify init
specify constitution
specify spec
specify plan
specify tasks

# Claude Code
claude                          # Start a session
claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse  # Add Jira MCP (once)
```

Inside a Claude Code session:
```
/init                           # Scan repo and create/update CLAUDE.md
/mcp                            # Check MCP server status, authenticate Atlassian
/output-style explanatory       # Enable detailed explanations (recommended for learners)
/exit                           # Quit session
```

## The development workflow

```
PRD -> spec-kit -> Jira -> Code -> Commit -> Push -> Deploy
```

1. Read `prd/ecommerce-analytics.md`
2. Run spec-kit to generate: constitution → specification → plan → tasks
3. Create Jira issues from tasks (project key: `ECOM`)
4. Build each feature in its own branch, with commits referencing the Jira key (e.g., `ECOM-1: Add KPI cards`)
5. Push to GitHub, merge to main
6. Deploy to Streamlit Community Cloud

## Traceability convention

Every commit message must include the Jira issue key: `ECOM-N: description`. This links code to requirements — a core concept the tutorial teaches.

## Jira setup

Project name: **E-Commerce Analytics**, key: **ECOM**, board: Scrum with columns To Do / In Progress / Done. Connected to Claude Code via the Atlassian MCP server (`--transport sse`).

## Deployment

Students deploy to [Streamlit Community Cloud](https://streamlit.io/cloud) by connecting their GitHub fork. The `main` branch should contain a working `app.py` and `requirements.txt`. Reference deployment: https://sales-dashboard-greg-lontok.streamlit.app/
