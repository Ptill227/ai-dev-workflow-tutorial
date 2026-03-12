<!--
SYNC IMPACT REPORT
==================
Version change: (unversioned template) → 1.0.0
Reason for bump: Initial ratification — all sections populated from scratch (MINOR baseline).

Modified principles: N/A (first version)

Added sections:
  - Core Principles (I–IV)
  - Technology Stack
  - Development Workflow
  - Governance

Removed sections: N/A

Templates requiring updates:
  ✅ .specify/memory/constitution.md — this file
  ✅ .specify/templates/plan-template.md — "Constitution Check" gates align with
     Principles I–IV (no structural change needed; gates are derived at plan-time)
  ✅ .specify/templates/spec-template.md — no constitution-specific tokens; compatible
  ✅ .specify/templates/tasks-template.md — task types (setup, foundational, story
     phases) compatible with all four principles; no changes required

Follow-up TODOs: None — all placeholders resolved.
-->

# E-Commerce Analytics Dashboard Constitution

## Core Principles

### I. Simplicity and Readability (NON-NEGOTIABLE)

All code MUST be written to be understood by a developer reading it for the first
time without needing to consult the author.

- Functions MUST do one thing and be named to reflect that one thing.
- No function body MAY exceed 30 lines; extract helpers when this limit is
  approached.
- Magic numbers and string literals MUST be assigned to named constants.
- Comments are required only where the *why* is non-obvious; avoid restating *what*
  the code does.
- Complexity MUST be justified in writing before it is introduced (see Governance).

**Rationale**: The dashboard is tutorial material. Readable code is the primary
learning artifact students take away. Clever or dense code defeats the educational
purpose and creates maintenance burden.

### II. User-Friendly Interactive Visualizations

Every chart or metric surface MUST meet the following standards before it is
considered complete:

- All axes, legends, and KPI labels MUST carry human-readable titles and units.
- Interactive tooltips MUST display exact values on hover for every chart.
- Charts MUST be sorted in a meaningful order (e.g., highest-to-lowest for bar
  charts) unless chronological ordering applies.
- Currency MUST be formatted as `$X,XXX` (or `$X,XXX,XXX`); counts as plain
  integers with thousands separators.
- Color choices MUST maintain sufficient contrast for accessibility and MUST be
  consistent across charts that share a dimension (e.g., the same category always
  uses the same color).
- Dashboard load time MUST remain under 5 seconds; individual chart render time
  MUST remain under 2 seconds after data is loaded.

**Rationale**: The dashboard serves non-technical executives. Visual clarity and
interactivity directly determine whether stakeholders trust and adopt the tool.

### III. Python Best Practices

All Python code in this project MUST conform to the following standards:

- Style MUST follow PEP 8; line length MUST NOT exceed 88 characters (Black
  formatter default).
- Imports MUST be grouped and ordered: standard library → third-party → local,
  each group separated by a blank line.
- Data loading MUST use `@st.cache_data` (or the appropriate Streamlit caching
  decorator) to avoid redundant file reads on re-renders.
- Pandas operations MUST prefer vectorised expressions over row-by-row iteration.
- All file paths MUST be constructed with `pathlib.Path`; hard-coded string paths
  are not permitted.
- The application MUST be runnable with a single command: `streamlit run app.py`.

**Rationale**: Consistent, idiomatic Python reduces cognitive overhead, makes the
codebase approachable for students at different experience levels, and ensures the
app performs well with the ~1 000-row dataset.

### IV. Environment Isolation

The project runtime environment MUST be fully reproducible and isolated:

- All dependencies MUST be declared in `requirements.txt` (pinned to compatible
  version ranges, e.g., `streamlit>=1.30,<2`).
- A Python virtual environment MUST be used for local development; no global
  package installations are permitted as part of the setup instructions.
- The package manager for installation is `uv` (`uv pip install -r
  requirements.txt`).
- No dependency MAY be added to the application without a corresponding entry in
  `requirements.txt`.
- Streamlit Community Cloud deployment MUST succeed using only `requirements.txt`
  at the repository root; no `setup.py` or `pyproject.toml` is required for Phase 1.

**Rationale**: Reproducible environments prevent "works on my machine" failures
during the workshop and ensure clean deployments to Streamlit Community Cloud.

## Technology Stack

The following stack is mandatory for Phase 1. Substitutions require a constitution
amendment (see Governance).

| Layer | Technology | Minimum Version |
|-------|------------|-----------------|
| Language | Python | 3.11 |
| Dashboard framework | Streamlit | 1.30 |
| Visualization | Plotly Express | 5.0 |
| Data processing | Pandas | 2.0 |
| Package manager | uv | latest stable |

**Data source**: `data/sales-data.csv` (approximately 1 000 transaction records,
12 months, 5 categories, 4 regions). No database or external API is permitted in
Phase 1.

**Deployment target**: Streamlit Community Cloud, connected to the `main` branch of
the student's GitHub fork.

**Out of scope for Phase 1**: authentication, real-time data, export, email alerts,
date-range filtering, drill-down views, mobile-responsive design.

## Development Workflow

All implementation work MUST follow this sequence:

1. **Read the PRD** — `prd/ecommerce-analytics.md` is the source of truth for
   requirements. No feature may be built that contradicts it.
2. **Run spec-kit** — `specify init → specify constitution → specify spec →
   specify plan → specify tasks` before writing any application code.
3. **Branch per feature** — each Jira task is worked on its own Git branch.
4. **Commit traceability** — every commit message MUST include the Jira issue key
   in the format `ECOM-N: description` (e.g., `ECOM-3: Add KPI cards`).
5. **Merge to main** — merge only when the feature is complete and the dashboard
   runs without errors locally.
6. **Deploy** — push to `main` triggers a Streamlit Community Cloud redeploy.

Code review checklist (applied to every PR / self-review):

- [ ] Principle I: no function exceeds 30 lines; code is self-explanatory.
- [ ] Principle II: all charts have labels, tooltips, and correct sort order.
- [ ] Principle III: PEP 8 compliant; caching applied; pathlib used for paths.
- [ ] Principle IV: `requirements.txt` updated if any dependency was added.
- [ ] Acceptance criteria from the relevant Jira issue are met.

## Governance

This constitution supersedes all other development practices, conventions, and
verbal agreements within this project.

**Amendment procedure**:
1. Propose the change in writing, stating which principle is affected and why the
   amendment is needed.
2. Record the decision and rationale in this file under the amended section.
3. Increment `CONSTITUTION_VERSION` according to semantic versioning:
   - **MAJOR** — removal or incompatible redefinition of an existing principle.
   - **MINOR** — new principle or section added; material expansion of guidance.
   - **PATCH** — clarification, wording fix, or non-semantic refinement.
4. Update `LAST_AMENDED_DATE` to the date of the change.
5. Run the consistency propagation checklist (templates and CLAUDE.md) and note
   results in the Sync Impact Report.

**Complexity justification**: Any deviation from Principle I simplicity rules MUST
be documented in the plan's Complexity Tracking table with the rationale and
alternatives considered.

**Compliance reviews**: Constitution compliance MUST be verified at each PR review
and at each checkpoint defined in `tasks.md`. Non-compliant code MUST be corrected
before merge.

**Runtime guidance**: Refer to `CLAUDE.md` for Claude Code session commands and
project-specific development guidance.

---

**Version**: 1.0.0 | **Ratified**: 2026-03-11 | **Last Amended**: 2026-03-11
