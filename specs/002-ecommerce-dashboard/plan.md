# Implementation Plan: E-Commerce Sales Analytics Dashboard

**Branch**: `002-ecommerce-dashboard` | **Date**: 2026-03-11 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-ecommerce-dashboard/spec.md`

## Summary

Build a single-page Streamlit dashboard (`app.py`) that reads ~1,000 transaction records from `data/sales-data.csv` and displays five visualizations: two KPI metric cards (Total Sales, Total Orders), a monthly sales trend line chart, a sales-by-category bar chart, and a sales-by-region bar chart. All charts are interactive (hover tooltips), currency-formatted, and sorted by value. The app is deployed to Streamlit Community Cloud via the `main` branch of the student's GitHub fork.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit ≥1.30,<2 · Plotly Express ≥5.0,<6 · Pandas ≥2.0,<3
**Storage**: CSV file — `data/sales-data.csv` (read-only, no database)
**Testing**: Manual visual verification against expected values from PRD; no automated test suite in Phase 1
**Target Platform**: Web browser (local dev) + Streamlit Community Cloud (deployment)
**Project Type**: Single-file web application
**Performance Goals**: Dashboard load < 5 seconds; individual chart render < 2 seconds after data load
**Constraints**: Single command launch (`streamlit run app.py`); no authentication; read-only data; no row-by-row pandas iteration; no hard-coded string paths
**Scale/Scope**: ~1,000 CSV rows; 5 product categories; 4 geographic regions; 1 developer (student)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status | Notes |
|-----------|------|--------|-------|
| I. Simplicity | No function exceeds 30 lines; named constants for magic values | ✅ PASS | Single-file app; each chart builder is a focused helper; all strings/numbers assigned to constants |
| I. Simplicity | Complexity justified in writing before introduction | ✅ PASS | No complexity deviations; tracked in Complexity Tracking section |
| II. Visualizations | All axes, legends, KPI labels carry human-readable titles | ✅ PASS | Every `px.line`/`px.bar` call includes explicit `labels={}` and `title=` |
| II. Visualizations | Interactive tooltips on every chart | ✅ PASS | Plotly Express provides tooltips by default; `hovertemplate` customized for currency |
| II. Visualizations | Bar charts sorted highest → lowest | ✅ PASS | `.sort_values("total_amount", ascending=False)` before every chart call |
| II. Visualizations | Currency formatted as `$X,XXX` | ✅ PASS | `tickformat="$,.0f"` on all y-axes; `st.metric()` uses f-string format |
| II. Visualizations | Load < 5s; chart render < 2s | ✅ PASS | `@st.cache_data` prevents redundant CSV reads; ~1,000 rows render in <100ms |
| III. Python | PEP 8; max 88-char line length | ✅ PASS | Enforced in code review checklist |
| III. Python | `@st.cache_data` for CSV loading | ✅ PASS | Applied to `load_data()` function |
| III. Python | Vectorized Pandas (no `iterrows`) | ✅ PASS | All aggregations use `.groupby().sum()` |
| III. Python | `pathlib.Path` for all file paths | ✅ PASS | `DATA_FILE = Path(__file__).parent / "data" / "sales-data.csv"` |
| III. Python | `streamlit run app.py` single command | ✅ PASS | Flat structure at repo root |
| IV. Isolation | All deps in `requirements.txt` with version ranges | ✅ PASS | `streamlit>=1.30,<2`, `plotly>=5.0,<6`, `pandas>=2.0,<3` |
| IV. Isolation | `uv` as package manager | ✅ PASS | Documented in quickstart.md |
| IV. Isolation | No `setup.py` or `pyproject.toml` needed | ✅ PASS | `requirements.txt` at repo root is sufficient for Streamlit Community Cloud |

**Gate result**: ALL PASS — proceed to design.

## Project Structure

### Documentation (this feature)

```text
specs/002-ecommerce-dashboard/
├── plan.md              # This file (/speckit.plan output)
├── research.md          # Phase 0 output — technology decisions
├── data-model.md        # Phase 1 output — entities, schema, constants
├── quickstart.md        # Phase 1 output — setup and run instructions
└── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
```

### Source Code (repository root)

```text
app.py                   # Single-entry Streamlit application
requirements.txt         # Pinned dependency version ranges

data/
└── sales-data.csv       # Source dataset (~1,000 transaction records)
```

**Structure Decision**: Single-file layout at the repository root. Constitution Principle I mandates simplicity and the `streamlit run app.py` requirement makes any subdirectory structure unnecessary. Internal code is organized by logical sections (constants → data loading → chart builders → page layout) within `app.py`.

## Complexity Tracking

No complexity violations. All design decisions conform to Constitution Principles I–IV without exception. No entries required.

---

## Phase 0: Research Summary

See [research.md](research.md) for full decision rationale. Key resolved decisions:

| Decision | Choice | Key Reason |
|----------|--------|------------|
| App structure | Single `app.py` | Principle I; 150–200 line scope doesn't warrant modules |
| Caching | `@st.cache_data` | Correct decorator for serializable DataFrames in Streamlit 1.30+ |
| KPI cards | `st.metric()` in `st.columns(2)` | Idiomatic Streamlit; visually prominent |
| Trend chart | `px.line` with `dt.to_period("M")` | Clean month labels; interactive tooltips |
| Bar charts | `px.bar` pre-sorted descending | Constitution Principle II; Plotly respects row order |
| Aggregations | `groupby().sum().sort_values()` | Vectorized; Principle III |
| File paths | `pathlib.Path(__file__).parent / ...` | Principle III; works from any working directory |
| Dependencies | Compatible ranges (`>=X,<Y`) | Security patches without breaking changes |

---

## Phase 1: Design Artifacts

### Data Model

See [data-model.md](data-model.md) for full schema and derivation rules.

**Key constants to define in `app.py`**:

```python
DATA_FILE      = Path(__file__).parent / "data" / "sales-data.csv"
DASHBOARD_TITLE = "ShopSmart Sales Dashboard"
CURRENCY_FORMAT = "$,.0f"          # Plotly tickformat / hovertemplate
CHART_HEIGHT    = 400              # Consistent height across all charts
```

**Core data transformations**:

```python
# Load (cached)
df = load_data()                   # pd.DataFrame, ~1,000 rows

# KPIs
total_sales  = df["total_amount"].sum()
total_orders = len(df)

# Trend
df_trend = (df.assign(month=df["date"].dt.to_period("M").astype(str))
              .groupby("month")["total_amount"].sum()
              .reset_index())

# Category
df_category = (df.groupby("category")["total_amount"].sum()
                 .reset_index()
                 .sort_values("total_amount", ascending=False))

# Region
df_region = (df.groupby("region")["total_amount"].sum()
               .reset_index()
               .sort_values("total_amount", ascending=False))
```

### Interface Contracts

Not applicable. This is a read-only, single-page web application with no external API, no user-facing endpoints, and no data writes. The CSV schema (documented in `data-model.md`) is the only contract, and it is consumed internally.

### Quickstart

See [quickstart.md](quickstart.md) for full setup, run, and deployment instructions.

**TL;DR**:
```bash
uv venv && source .venv/bin/activate  # (Windows: .venv\Scripts\Activate.ps1)
uv pip install -r requirements.txt
streamlit run app.py
```

---

## Implementation Guidance (for `/speckit.tasks`)

The following logical units map to individual Jira tasks. Each is independently testable per the spec's user story priorities.

### Unit 1 — Environment & Data Foundation (maps to FR-006, FR-010)
- Create `requirements.txt` with pinned version ranges
- Create `app.py` skeleton: imports, constants, `load_data()` with `@st.cache_data`
- Verify CSV loads correctly with expected row count (~1,000) and column types
- **Test**: `streamlit run app.py` launches without errors; `len(df)` prints 482 in terminal

### Unit 2 — KPI Cards (maps to FR-001, FR-002, SC-003)
- Implement `show_kpis(df)`: compute total_sales and total_orders; render with `st.metric()` in `st.columns(2)`
- Verify values match PRD expectations (~$650K–$700K, 482 orders)
- **Test**: KPI cards visible on page load, correctly formatted

### Unit 3 — Sales Trend Chart (maps to FR-003, FR-007, SC-002)
- Implement `make_trend_chart(df)`: monthly groupby, `px.line`, axis labels, currency y-axis
- **Test**: 12 data points visible, hover tooltips show month + sales amount

### Unit 4 — Category Bar Chart (maps to FR-004, FR-007, SC-004)
- Implement `make_category_chart(df)`: category groupby descending sort, `px.bar`, labels, tooltips
- **Test**: 5 bars visible, sorted highest → lowest, tooltips show exact $ values

### Unit 5 — Region Bar Chart (maps to FR-005, FR-007, SC-004)
- Implement `make_region_chart(df)`: region groupby descending sort, `px.bar`, labels, tooltips
- **Test**: 4 bars visible, sorted highest → lowest, tooltips show exact $ values

### Unit 6 — Layout & Polish (maps to FR-009, FR-011, FR-012, SC-005)
- Add `st.title(DASHBOARD_TITLE)`, arrange charts in a two-column grid (category + region side by side)
- Verify professional appearance; check all axis labels, chart titles, and formatting
- **Test**: Non-technical colleague can identify all metrics without explanation

### Unit 7 — Deployment (maps to FR-010, SC-006)
- Push `app.py` + `requirements.txt` to `main` branch
- Connect GitHub fork to Streamlit Community Cloud; verify public URL loads correctly
- **Test**: Dashboard accessible at public URL; all 5 visualizations render in < 5 seconds
