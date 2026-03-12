# Data Model: E-Commerce Sales Analytics Dashboard

**Feature Branch**: `002-ecommerce-dashboard`
**Created**: 2026-03-11

## Source: `data/sales-data.csv`

This is the single data source for Phase 1. No database or external API is used.

### Raw Transaction Schema

| Column         | Python Type | Description                        | Example            |
|----------------|-------------|------------------------------------|--------------------|
| `date`         | `datetime`  | Transaction date (parsed on load)  | `2024-01-15`       |
| `order_id`     | `str`       | Unique order identifier            | `ORD-001234`       |
| `product`      | `str`       | Product name                       | `Wireless Headphones` |
| `category`     | `str`       | Product category (5 values)        | `Electronics`      |
| `region`       | `str`       | Geographic region (4 values)       | `North`            |
| `quantity`     | `int`       | Units sold per transaction         | `2`                |
| `unit_price`   | `float`     | Price per unit                     | `49.99`            |
| `total_amount` | `float`     | Total transaction value            | `99.98`            |

### Validation Rules

- `total_amount` must be numeric and non-negative; rows with missing or invalid values are excluded from all calculations
- `date` must be parseable as a date; rows with invalid dates are excluded from trend calculations
- `category` must be one of: Electronics, Accessories, Audio, Wearables, Smart Home
- `region` must be one of: North, South, East, West
- The file must exist at `data/sales-data.csv` relative to the repository root; if absent, the app displays a user-friendly error

---

## Derived Aggregates (computed at runtime)

### KPI Metrics

| Metric          | Derivation                            | Display Format   |
|-----------------|---------------------------------------|------------------|
| `total_sales`   | `df["total_amount"].sum()`            | `$XXX,XXX`       |
| `total_orders`  | `len(df)` (count of rows)             | `XXX`            |

### Monthly Sales Trend

| Field         | Derivation                                                  |
|---------------|-------------------------------------------------------------|
| `month`       | `df["date"].dt.to_period("M").dt.to_timestamp()` — Period converted to timestamp for Plotly date axis |
| `sales`       | `df.groupby("month")["total_amount"].sum()` — sorted chronologically |

Chart type: line chart. X-axis: month label via `tickformat="%b %Y"` (e.g., "Jan 2024"). Y-axis: sales amount ($).

### Sales by Category

| Field      | Derivation                                                        |
|------------|-------------------------------------------------------------------|
| `category` | `df["category"]`                                                  |
| `sales`    | `df.groupby("category")["total_amount"].sum()` — sorted descending |

Chart type: bar chart. X-axis: category name. Y-axis: sales amount ($). Sorted highest → lowest.

### Sales by Region

| Field    | Derivation                                                      |
|----------|-----------------------------------------------------------------|
| `region` | `df["region"]`                                                  |
| `sales`  | `df.groupby("region")["total_amount"].sum()` — sorted descending |

Chart type: bar chart. X-axis: region name. Y-axis: sales amount ($). Sorted highest → lowest.

---

## State Transitions

This is a read-only, stateless application. There are no user-driven state changes. Data is loaded once on startup (cached) and displayed. No write operations are performed.

---

## Constants

The following values are defined as named constants (Principle I — no magic strings):

| Constant              | Value                                                  | Used In                |
|-----------------------|--------------------------------------------------------|------------------------|
| `DATA_FILE`           | `Path(__file__).parent / "data" / "sales-data.csv"`   | Data loader function   |
| `DASHBOARD_TITLE`     | `"ShopSmart Sales Dashboard"`                          | Page title             |
| `CURRENCY_FORMAT`     | `"$,.0f"` (Plotly format string)                       | All currency axes/tooltips |
| `CHART_HEIGHT`        | `400` (pixels)                                         | All chart figures      |
