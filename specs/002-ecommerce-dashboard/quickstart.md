# Quickstart: E-Commerce Sales Analytics Dashboard

**Branch**: `002-ecommerce-dashboard` | **Last Updated**: 2026-03-11

## Prerequisites

- Python 3.11 or higher
- `uv` package manager ([install guide](https://github.com/astral-sh/uv))
- Git

## Setup (First Time)

### 1. Clone and enter the repository

```bash
# In your terminal
git clone <your-fork-url>
cd ai-dev-workflow-tutorial
```

### 2. Create a virtual environment

```bash
# In your terminal
uv venv
```

This creates a `.venv/` folder in the project root.

### 3. Activate the virtual environment

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
# In your terminal (with venv activated)
uv pip install -r requirements.txt
```

### 5. Run the dashboard

```bash
# In your terminal (with venv activated)
streamlit run app.py
```

The dashboard opens automatically in your default browser at `http://localhost:8501`.

---

## Daily Development Workflow

```bash
# Activate environment (each new terminal session)
source .venv/bin/activate       # macOS/Linux
.venv\Scripts\Activate.ps1      # Windows PowerShell

# Run the app
streamlit run app.py

# The app hot-reloads on file save — no restart needed
```

---

## Adding a Dependency

```bash
# 1. Install it
uv pip install <package-name>

# 2. Update requirements.txt (REQUIRED — Principle IV)
uv pip freeze > requirements.txt
# Or manually add the package with a version range
```

---

## Deployment (Streamlit Community Cloud)

1. Push `app.py` and `requirements.txt` to the `main` branch of your GitHub fork
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repository
3. Set **Main file path** to `app.py`
4. Click **Deploy**

The app deploys automatically on every push to `main`.

---

## Expected Output

When running with `data/sales-data.csv`, you should see:

| Metric        | Expected Value      |
|---------------|---------------------|
| Total Sales   | ~$650,000–$700,000  |
| Total Orders  | 482                 |
| Categories    | 5 bars (Electronics highest) |
| Regions       | 4 bars              |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Ensure your venv is activated and `uv pip install -r requirements.txt` was run |
| `FileNotFoundError: sales-data.csv` | Confirm `data/sales-data.csv` exists in the repository root |
| Port 8501 already in use | Run `streamlit run app.py --server.port 8502` |
| Dashboard shows no data | Check the CSV structure matches the schema in `data-model.md` |
