# Tasks: E-Commerce Sales Analytics Dashboard

**Input**: Design documents from `/specs/002-ecommerce-dashboard/`
**Prerequisites**: plan.md ✅ · spec.md ✅ · research.md ✅ · data-model.md ✅ · quickstart.md ✅

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (independent — no dependency on an incomplete task in the same phase)
- **[Story]**: Which user story this task belongs to (US1–US4 map to spec.md priorities P1–P4)
- No test tasks — not requested in this spec

## Path Convention

Single-file application at repository root:

```text
app.py           ← all application code lives here
requirements.txt ← dependency declarations
data/
└── sales-data.csv  ← source data (already present, do not modify)
```

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the deployable project skeleton — virtual environment, declared dependencies, and the app.py file with all constants and page configuration in place.

- [x] T001 Create `requirements.txt` at repo root with pinned version ranges: `streamlit>=1.30,<2`, `plotly>=5.0,<6`, `pandas>=2.0,<3`
- [x] T002 Create Python virtual environment using `uv venv` and install dependencies with `uv pip install -r requirements.txt`
- [x] T003 Create `app.py` at repo root with: grouped imports (stdlib → third-party → local), module-level constants (`DATA_FILE`, `DASHBOARD_TITLE`, `CURRENCY_FORMAT`, `CHART_HEIGHT`), and `st.set_page_config(page_title=DASHBOARD_TITLE, layout="wide")` call

**Checkpoint**: `streamlit run app.py` launches without import errors (blank page is fine at this stage)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: CSV data loading with caching and error handling — every user story depends on this working correctly.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T004 Implement `load_data() -> pd.DataFrame` in `app.py`: use `@st.cache_data`, read `DATA_FILE` with `pd.read_csv(..., parse_dates=["date"])`, return the DataFrame
- [x] T005 Add startup error handling in `app.py` main flow: if `DATA_FILE` does not exist, call `st.error("Data file not found: data/sales-data.csv")` then `st.stop()`; otherwise call `df = load_data()`

**Checkpoint**: `streamlit run app.py` loads the CSV, prints `len(df)` to terminal (should be ~1,000), and stops cleanly with a user-friendly error if the file is missing

---

## Phase 3: User Story 1 — Executive KPI Review (Priority: P1) 🎯 MVP

**Goal**: Display Total Sales and Total Orders as prominent KPI cards visible immediately on page load — no interaction required.

**Independent Test**: Load the dashboard, confirm `Total Sales` shows ~$650,000–$700,000 formatted as `$XXX,XXX` and `Total Orders` shows `482` as a plain integer. Both cards visible without scrolling.

### Implementation

- [ ] T006 [US1] Implement `show_kpis(df: pd.DataFrame)` in `app.py`: compute `total_sales = df["total_amount"].sum()` and `total_orders = len(df)`; render using `col1, col2 = st.columns(2)` with `col1.metric("Total Sales", f"${total_sales:,.0f}")` and `col2.metric("Total Orders", f"{total_orders:,}")`
- [ ] T007 [US1] Add KPI section to `app.py` main layout: render `st.title(DASHBOARD_TITLE)`, then call `show_kpis(df)`, followed by `st.divider()`

**Checkpoint**: Dashboard shows the title and two KPI metric cards with correct values. This is the MVP — deployable independently.

---

## Phase 4: User Story 2 — Sales Growth Trend Analysis (Priority: P2)

**Goal**: Display a monthly sales line chart with interactive tooltips, enabling the CEO to assess business growth over time.

**Independent Test**: Chart renders with 12 monthly data points, x-axis shows "Jan 2024" style labels, y-axis shows `$XXX,XXX` currency format, hovering any point shows exact month + sales value.

### Implementation

- [ ] T008 [US2] Implement `make_trend_chart(df: pd.DataFrame)` in `app.py`: group by month using `df.assign(month=df["date"].dt.to_period("M")).groupby("month")["total_amount"].sum().reset_index()`, convert Period to timestamp with `.dt.to_timestamp()`, call `px.line(df_trend, x="month", y="total_amount", title="Sales Trend Over Time", labels={"month": "Month", "total_amount": "Sales ($)"}, markers=True)`, apply `fig.update_xaxes(tickformat="%b %Y")` and `fig.update_yaxes(tickformat=CURRENCY_FORMAT)`, return the figure
- [ ] T009 [US2] Add trend section to `app.py` main layout: call `st.plotly_chart(make_trend_chart(df), use_container_width=True)` followed by `st.divider()`

**Checkpoint**: Dashboard shows KPI cards (US1) + trend chart (US2). Hover over any point to confirm tooltip shows month and exact sales value.

---

## Phase 5: User Story 3 — Product Category Performance Analysis (Priority: P3)

**Goal**: Display a sales-by-category bar chart sorted highest to lowest with interactive tooltips, enabling marketing budget allocation decisions.

**Independent Test**: Chart shows 5 bars (Electronics, Accessories, Audio, Wearables, Smart Home) sorted highest → lowest. Hovering a bar shows category name + exact `$XXX,XXX` sales value.

### Implementation

- [ ] T010 [P] [US3] Implement `make_category_chart(df: pd.DataFrame)` in `app.py`: group by category using `df.groupby("category")["total_amount"].sum().reset_index().sort_values("total_amount", ascending=False)`, call `px.bar(df_cat, x="category", y="total_amount", title="Sales by Category", labels={"category": "Category", "total_amount": "Sales ($)"})`, apply `fig.update_traces(hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>")` and `fig.update_yaxes(tickformat=CURRENCY_FORMAT)`, return the figure
- [ ] T011 [US3] Reserve left column slot in `app.py` two-column chart layout: create `col_cat, col_reg = st.columns(2)` and render `col_cat.plotly_chart(make_category_chart(df), use_container_width=True)` (leave `col_reg` placeholder for US4)

**Checkpoint**: Category bar chart visible in left column. Bars sorted correctly with 5 categories and currency-formatted tooltips.

---

## Phase 6: User Story 4 — Regional Sales Performance Review (Priority: P4)

**Goal**: Display a sales-by-region bar chart sorted highest to lowest with interactive tooltips, enabling regional managers to identify underperforming territories.

**Independent Test**: Chart shows 4 bars (North, South, East, West) sorted highest → lowest. Hovering a bar shows region name + exact `$XXX,XXX` sales value.

### Implementation

- [ ] T012 [P] [US4] Implement `make_region_chart(df: pd.DataFrame)` in `app.py`: group by region using `df.groupby("region")["total_amount"].sum().reset_index().sort_values("total_amount", ascending=False)`, call `px.bar(df_reg, x="region", y="total_amount", title="Sales by Region", labels={"region": "Region", "total_amount": "Sales ($)"})`, apply `fig.update_traces(hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>")` and `fig.update_yaxes(tickformat=CURRENCY_FORMAT)`, return the figure
- [ ] T013 [US4] Complete two-column layout in `app.py`: render `col_reg.plotly_chart(make_region_chart(df), use_container_width=True)` in the right column created in T011

**Checkpoint**: All 5 visualizations present — 2 KPI cards + trend chart + category chart (left) + region chart (right). All charts interactive with correct tooltips and formatting.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final layout verification, constitution compliance check, and deployment.

- [ ] T014 Verify constitution compliance in `app.py`: confirm no function exceeds 30 lines; all magic strings/numbers are referenced from constants; imports are grouped (stdlib → third-party); PEP 8 line length ≤ 88 chars
- [ ] T015 [P] Verify all 5 visualizations meet Principle II requirements: all axes have labels, all charts have titles, all bar charts sorted highest → lowest, all currency values use `$X,XXX` format, load time under 5 seconds measured manually
- [ ] T016 Push `app.py` and `requirements.txt` to the `main` branch of your GitHub fork (commit message format: `ECOM-N: Add sales dashboard`)
- [ ] T017 Connect GitHub fork to Streamlit Community Cloud at share.streamlit.io; set **Main file path** to `app.py`; confirm public URL loads all 5 visualizations within 5 seconds

**Checkpoint**: Dashboard is live at a public URL, all acceptance criteria from spec.md are met, and CLAUDE.md code review checklist passes.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion — **BLOCKS all user stories**
- **User Stories (Phases 3–6)**: All depend on Phase 2 completion; can proceed in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all user story phases complete

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2. No dependency on other stories. ← Start here for MVP
- **US2 (P2)**: Can start after Phase 2. No dependency on US1 (adds a new section).
- **US3 (P3)**: Can start after Phase 2. Creates `col_cat` column slot (T011); US4 fills `col_reg` in T013.
- **US4 (P4)**: Depends on T011 (column layout created by US3). Must follow US3.

### Within Each User Story

- Function implementation task before rendering/integration task
- T010 [P] and T012 [P] are marked parallel — logically independent functions, no shared state

### Parallel Opportunities Within Stories

- **T010 + T012**: `make_category_chart()` and `make_region_chart()` are independent functions — can be implemented in either order
- **T014 + T015**: Constitution compliance check and visualization audit have no dependency on each other

---

## Parallel Example: Category + Region Charts

```text
# T010 and T012 can be done in either order (both are independent function implementations):
Task T010: Implement make_category_chart(df) in app.py
Task T012: Implement make_region_chart(df) in app.py

# Then integrate both into the two-column layout:
Task T011: Reserve col_cat in st.columns(2), render category chart
Task T013: Render region chart in col_reg (depends on T011)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T003)
2. Complete Phase 2: Foundational (T004–T005) — **critical blocker**
3. Complete Phase 3: US1 KPI Cards (T006–T007)
4. **STOP and VALIDATE**: `streamlit run app.py` shows title + 2 KPI cards with correct values
5. Deploy to Streamlit Community Cloud — this is a working MVP

### Incremental Delivery

1. Phase 1 + 2 → Foundation ready
2. Phase 3 (US1) → KPI cards → deploy (MVP!)
3. Phase 4 (US2) → Add trend chart → deploy
4. Phase 5 (US3) → Add category chart → deploy
5. Phase 6 (US4) → Add region chart → deploy (full feature complete)
6. Phase 7 → Polish + final deployment

### Commit Traceability (per constitution)

Every commit must include the Jira issue key:

```bash
git commit -m "ECOM-1: Add project setup and requirements.txt"
git commit -m "ECOM-2: Add CSV data loader with caching"
git commit -m "ECOM-3: Add KPI cards for total sales and orders"
git commit -m "ECOM-4: Add monthly sales trend chart"
git commit -m "ECOM-5: Add sales by category chart"
git commit -m "ECOM-6: Add sales by region chart"
git commit -m "ECOM-7: Polish layout and deploy to Streamlit Cloud"
```

---

## Notes

- [P] tasks = logically independent, no unresolved prerequisites — can be done in either order
- [Story] label maps each task to its user story for Jira traceability
- Each user story adds a new, independently testable section to `app.py`
- US4 is the only story with a dependency on another story (T011 from US3 creates the column layout)
- Verify KPI values against PRD expected output before committing: Total Sales ~$650K–$700K, Total Orders = 482
- Suggested MVP scope: Phase 1 + Phase 2 + Phase 3 (US1) — deployable in under an hour
