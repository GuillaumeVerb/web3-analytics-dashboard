# WDI – Web3 Analytics Dashboard

A production-quality Streamlit application for analyzing Web3 and on-chain data from CSV exports.

![Dashboard Preview](https://img.shields.io/badge/Status-Production--Ready-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red)

## 🎯 Features

### Core Functionality
- **CSV Upload**: Import data from Dune Analytics or any on-chain dataset
- **Dynamic Column Selection**: Automatically detect and select date, address, and value columns
- **Real-time Data Preview**: View your uploaded data instantly

### Analytics & Visualizations
- **Key Performance Indicators (KPIs)**:
  - Total Volume
  - Number of Transactions
  - Unique Addresses
  - Active Days
  - Average Transaction Value
  - Daily Averages

- **Interactive Charts**:
  - Daily Volume Time Series (Area Chart)
  - Daily Transaction Count (Bar Chart)
  - Top N Addresses by Volume (Horizontal Bar Chart)
  - Cohort Retention Analysis (Heatmap)

### Design
- Dark, minimalistic, premium crypto/fintech aesthetic
- Responsive layout optimized for wide screens
- Interactive Plotly charts with hover details
- Clean, professional UI components

## 🚀 Quick Start

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

The app will open automatically in your default browser at `http://localhost:8501`

## 📊 Usage Guide

### Step 1: Upload Your Data
- Click the file uploader in the left sidebar
- Select a CSV file containing blockchain/on-chain data
- The app accepts exports from Dune Analytics or any similar data source

### Step 2: Configure Columns
The app will automatically detect potential columns, but you can adjust:
- **Date Column**: Select the column containing timestamps or dates
- **Address Column**: Select the column with wallet addresses or user IDs
- **Value Column**: Select the column with transaction values in USD

### Step 3: Explore Analytics
- View KPIs at the top of the dashboard
- Scroll through interactive charts
- Adjust the "Top N Addresses" slider to customize the leaderboard
- Examine cohort retention patterns

### Supported Data Formats

Your CSV should contain columns similar to:
- Date/timestamp (e.g., `block_time`, `timestamp`, `date`)
- Address/wallet (e.g., `user_address`, `from_address`, `wallet`)
- Value in USD (e.g., `amount_usd`, `value_usd`, `volume`)

Example CSV structure:
```csv
block_time,from_address,to_address,amount_usd
2024-01-01 10:30:00,0x1234...,0x5678...,1500.50
2024-01-01 11:45:00,0xabcd...,0xef01...,2300.75
...
```

## 🏗️ Project Structure

```
Web3 Analytics Dashboard/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Technical Details

### Tech Stack
- **Python**: 3.11+
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical computations

### Code Organization
The `app.py` file is organized into clear sections:
1. **Configuration**: Page setup and custom CSS
2. **Helper Functions**: Modular functions for data processing
3. **Main App**: Application logic and UI components

### Key Helper Functions
- `load_data()`: Load CSV into DataFrame
- `detect_date_columns()`: Auto-detect date columns
- `detect_numeric_columns()`: Auto-detect numeric columns
- `detect_address_columns()`: Auto-detect address columns
- `compute_kpis()`: Calculate all KPIs
- `build_timeseries()`: Create time series aggregations
- `build_top_addresses()`: Generate top addresses ranking
- `build_cohort_retention()`: Compute retention analysis
- `format_number()`: Format numbers with K/M/B suffixes

## 🎨 Customization

### Changing Colors
Edit the custom CSS in the `st.markdown()` section of `app.py`:
- Main accent color: `#00d4ff` (cyan)
- Secondary color: `#00ff88` (green)
- Background: `#0e1117` (dark)

### Adding New Charts
Add new visualization functions following the pattern:
```python
def build_new_chart(df, ...):
    # Your logic here
    return chart_data
```

### Modifying KPIs
Edit the `compute_kpis()` function to add new metrics.

## 📝 Data Privacy

- **No data is stored**: All analysis happens in-memory
- **No external API calls**: Data stays on your local machine
- **No database required**: Pure CSV-based analysis

## 🤝 Contributing

This is a demo application built by WDI – Web3 Data Intelligence. For enterprise features or customization requests, please contact WDI.

## 📄 License

Built for demonstration purposes by WDI – Web3 Data Intelligence.

## 🐛 Troubleshooting

### App won't start
- Ensure Python 3.11+ is installed: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### CSV upload fails
- Check that your file is valid CSV format
- Ensure the file isn't corrupted
- Try with a smaller sample first

### Charts not displaying
- Verify your selected columns contain valid data
- Check for null/missing values in key columns
- Ensure date column can be parsed as datetime

### Performance issues
- Limit CSV size to < 1M rows for optimal performance
- Close other browser tabs
- Use more recent data or aggregate before uploading

## 📧 Support

For questions, issues, or feature requests related to this demo, please contact **WDI – Web3 Data Intelligence**.

---

**Built with ❤️ by WDI – Web3 Data Intelligence**


