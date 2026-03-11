# Research: E-Commerce Sales Analytics Dashboard

**Feature Branch**: `002-ecommerce-dashboard`
**Created**: 2026-03-11
**Status**: Complete — all NEEDS CLARIFICATION resolved

---

## Decision 1: App Structure (single-file vs. multi-module)

**Decision**: Single `app.py` at the repository root.

**Rationale**: The application is ~150–200 lines. Splitting into modules adds file-navigation overhead with no benefit at this scale. Constitution Principle I (simplicity) and the `streamlit run app.py` mandate both point to a flat structure. The internal code organization (constants → loader → chart builders → layout) provides logical separation without filesystem fragmentation.

**Alternatives considered**:
- `src/` package with separate modules for charts, data loading: Rejected — premature for this scope; adds `__init__.py` boilerplate, import complexity, and no payoff.
- `pages/` multi-page Streamlit app: Rejected — all content fits a single page; multi-page navigation would confuse non-technical users.

---

## Decision 2: Streamlit Caching Strategy

**Decision**: `@st.cache_data` for the CSV loading function.

**Rationale**: `@st.cache_data` (introduced in Streamlit 1.18, stable in 1.30+) is the correct decorator for functions that return serializable data like DataFrames. It caches by function arguments and returns a copy, preventing mutation bugs. `@st.cache_resource` is for global stateful resources (DB connections, ML models) — not applicable here.

**Pattern**:
```python
@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_FILE, parse_dates=["date"])
```

**Alternatives considered**:
- `@st.cache_resource`: Rejected — returns the same object reference (not a copy), risks accidental DataFrame mutation across renders.
- No caching: Rejected — violates Constitution Principle III; causes redundant disk reads on every Streamlit re-render (e.g., widget interaction).

---

## Decision 3: KPI Card Layout

**Decision**: `st.columns(2)` with `st.metric()` in each column.

**Rationale**: `st.metric(label, value)` renders a visually prominent card with a large number and label — exactly the "KPI card" pattern. `st.columns(2)` places them side-by-side. This is the idiomatic Streamlit pattern used in thousands of dashboards.

**Pattern**:
```python
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
```

**Alternatives considered**:
- Custom HTML/CSS cards: Rejected — violates Principle I (unnecessary complexity), breaks hot-reload, harder to maintain.
- `st.info()` boxes: Rejected — not visually distinct enough for KPI prominence.

---

## Decision 4: Monthly Sales Trend Chart

**Decision**: `plotly.express.line()` on a DataFrame with a string month column derived via `dt.to_period("M")`.

**Rationale**: Plotly Express provides interactive tooltips out of the box. Converting dates to `Period` then to string (e.g., `"2024-01"`) ensures clean x-axis month labels without Plotly auto-formatting issues with raw datetime values.

**Pattern**:
```python
df_trend = (
    df.assign(month=df["date"].dt.to_period("M"))
    .groupby("month")["total_amount"]
    .sum()
    .reset_index()
)
df_trend["month"] = df_trend["month"].dt.to_timestamp()  # Period → datetime for Plotly
fig = px.line(
    df_trend, x="month", y="total_amount",
    title="Sales Trend Over Time",
    labels={"month": "Month", "total_amount": "Sales ($)"},
    markers=True,
)
fig.update_xaxes(tickformat="%b %Y")   # "Jan 2024", "Feb 2024" …
fig.update_yaxes(tickformat="$,.0f")
```

**Alternatives considered**:
- `.astype(str)` string month labels: Axis ordering is correct for `YYYY-MM` format but Plotly loses date-type axis intelligence (auto tick density, zoom behaviour). Rejected in favour of `.dt.to_timestamp()`.
- `px.line` with raw datetime x-axis: Tick labels default to day-level granularity with no month grouping. Rejected.
- `st.line_chart()`: Rejected — no tooltip customization, no axis label control; violates Principle II.

---

## Decision 5: Category and Region Bar Charts

**Decision**: `plotly.express.bar()` with `color_discrete_sequence` and `tickformat` for currency.

**Rationale**: `px.bar` supports interactive tooltips, axis formatting, and horizontal/vertical orientation. Vertical bars are more familiar to business users for categorical comparisons. Pre-sorting the DataFrame descending before passing to Plotly ensures correct bar order (Plotly respects row order).

**Pattern**:
```python
df_cat = (
    df.groupby("category")["total_amount"]
    .sum()
    .reset_index()
    .sort_values("total_amount", ascending=False)
)
fig = px.bar(
    df_cat, x="category", y="total_amount",
    title="Sales by Category",
    labels={"category": "Category", "total_amount": "Sales ($)"},
)
fig.update_yaxes(tickformat="$,.0f")
fig.update_traces(hovertemplate="%{x}: $%{y:,.0f}<extra></extra>")
```

**Alternatives considered**:
- Horizontal bar (`orientation="h"`): Valid alternative; vertical chosen because chart width accommodates 4–5 category names without overlap.
- `st.bar_chart()`: Rejected — no tooltip or sort control; violates Principle II.

---

## Decision 6: Pandas Aggregation Patterns

**Decision**: Vectorized groupby + sum + sort_values for all aggregations. No `apply()` or row iteration.

**Rationale**: Vectorized operations on a ~1,000-row DataFrame complete in milliseconds. `iterrows()` / `apply()` are 10–100× slower and violate Constitution Principle III.

**Patterns**:
```python
# Monthly trend (chronological)
df.assign(month=df["date"].dt.to_period("M").astype(str)) \
  .groupby("month")["total_amount"].sum().reset_index()
# Sort is implicit (period strings "2024-01", "2024-02" sort lexicographically == chronologically)

# Category totals (descending)
df.groupby("category")["total_amount"].sum() \
  .reset_index() \
  .sort_values("total_amount", ascending=False)

# Region totals (descending)
df.groupby("region")["total_amount"].sum() \
  .reset_index() \
  .sort_values("total_amount", ascending=False)
```

---

## Decision 7: File Path Handling

**Decision**: `pathlib.Path(__file__).parent / "data" / "sales-data.csv"` as a module-level constant.

**Rationale**: Constitution Principle III explicitly requires `pathlib.Path` for all file paths. Using `__file__` makes the path relative to `app.py`, which works regardless of the working directory from which `streamlit run app.py` is invoked.

**Pattern**:
```python
from pathlib import Path
DATA_FILE = Path(__file__).parent / "data" / "sales-data.csv"
```

**Alternatives considered**:
- `"data/sales-data.csv"` string: Rejected — hard-coded string; violates Principle III; breaks if run from a different directory.
- `os.path.join()`: Rejected — less readable than pathlib; Principle III explicitly names pathlib.

---

## Decision 8: Dependency Versions (`requirements.txt`)

**Decision**: Compatible version ranges pinned to current stable releases (early 2026).

```
streamlit>=1.30,<2
plotly>=5.0,<6
pandas>=2.0,<3
```

**Rationale**: Lower bounds ensure the features used (e.g., `@st.cache_data`, `px.line`) are available. Upper bounds prevent breaking changes from major version upgrades from silently breaking the app on Streamlit Community Cloud. No patch-level pinning — allows security patches without manual updates.

**Alternatives considered**:
- Exact version pinning (`streamlit==1.32.0`): Rejected — creates deployment friction when minor updates are needed; security patches require manual PRs.
- No upper bound: Rejected — risks Streamlit 2.x or Pandas 3.x breaking changes.

---

## Resolved Clarifications

No `[NEEDS CLARIFICATION]` markers were present in the spec. All technical choices align directly with the constitution and user input. No external research was required beyond confirming the decisions above.
