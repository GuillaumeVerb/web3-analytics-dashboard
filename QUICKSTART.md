# Quick Start Guide

## Installation & Running (2 minutes)

### Step 1: Install Dependencies
Open your terminal and navigate to this directory, then run:

```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## Test with Sample Data

A sample CSV file (`sample_data.csv`) is included in this directory with 50 blockchain transactions.

To test the app:
1. Click **"Browse files"** in the sidebar
2. Select `sample_data.csv`
3. The app will auto-detect columns:
   - **Date Column**: `block_time`
   - **Address Column**: `from_address`
   - **Value Column**: `amount_usd`
4. Explore the dashboard!

## Using Your Own Data

### Supported CSV Format
Your CSV should have columns like:
- A date/time column (e.g., `block_time`, `timestamp`, `date`)
- An address column (e.g., `from_address`, `wallet`, `user_address`)
- A numeric value column in USD (e.g., `amount_usd`, `value_usd`)

### Example Sources
- **Dune Analytics**: Export any query results as CSV
- **Etherscan**: Export transaction history
- **Custom blockchain data**: Any CSV with the columns above

## Features Overview

### 📊 KPI Cards
View 8 key metrics instantly:
- Total Volume
- Transaction Count
- Unique Addresses
- Active Days
- Average Transaction Value
- Date Range
- Average Daily Volume
- Average Daily Transactions

### 📈 Charts
- **Daily Volume**: Area chart showing transaction volume over time
- **Daily Transactions**: Bar chart of transaction count
- **Top Addresses**: Ranked by total volume (adjust N with slider)
- **Cohort Retention**: Weekly user retention heatmap

### ⚙️ Customization
- Adjust **Top N Addresses** slider (5-50)
- Select different columns from your CSV
- Expand data preview to see raw data

## Troubleshooting

**App won't start?**
- Make sure Python 3.11+ is installed: `python --version`
- Try: `pip install -r requirements.txt --upgrade`

**CSV upload fails?**
- Check file is valid CSV format
- Ensure file size < 200MB
- Verify no special characters in column names

**Charts not showing?**
- Verify selected columns contain valid data
- Check for null values in key columns
- Ensure date column can be parsed as datetime

## Next Steps

1. Upload your own blockchain data CSV
2. Experiment with different column selections
3. Use the insights for your Web3 analytics!

---

**Built by WDI – Web3 Data Intelligence**


