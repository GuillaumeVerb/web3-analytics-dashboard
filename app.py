"""
WDI – Web3 Analytics Dashboard
A production-quality Streamlit app for analyzing Web3/on-chain data from CSV exports.
Built by WDI – Web3 Data Intelligence
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import io
import base64

# Optional protocol templates - import in main() to avoid silent failures
try:
    from protocol_templates import detect_protocol, suggest_columns, format_protocol_info, get_protocol_template
    PROTOCOL_TEMPLATES_AVAILABLE = True
except ImportError:
    PROTOCOL_TEMPLATES_AVAILABLE = False
    # Define dummy functions if module not available
    def detect_protocol(df): return None, {}
    def suggest_columns(df): return {}, 'generic'
    def format_protocol_info(protocol): return f"**{protocol}**"
    def get_protocol_template(protocol): return {}


# ============================================================================
# CONFIGURATION
# ============================================================================

# Page config MUST be first Streamlit command and at module level
st.set_page_config(
    page_title="WDI – Web3 Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark, minimalistic, premium style
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1a1d29;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 600;
        color: #00d4ff;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #b0b3c1;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Headers */
    h1 {
        color: #ffffff;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    h2, h3 {
        color: #e0e3f0;
        font-weight: 600;
    }
    
    /* Cards/containers */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #1a1d29;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1a1d29;
        color: #ffffff;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data
def load_data(file):
    """
    Load CSV file into a pandas DataFrame.
    
    Args:
        file: Uploaded file object from Streamlit
    
    Returns:
        pd.DataFrame: Loaded dataframe
    """
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def detect_date_columns(df):
    """
    Detect potential date columns in the dataframe.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        list: Column names that might contain dates
    """
    date_cols = []
    
    for col in df.columns:
        # Check by name
        if any(keyword in col.lower() for keyword in ['date', 'time', 'timestamp', 'day', 'created']):
            date_cols.append(col)
        # Check by dtype
        elif df[col].dtype == 'object':
            # Try to parse a sample
            try:
                sample = df[col].dropna().head(100)
                if len(sample) > 0:
                    pd.to_datetime(sample, errors='coerce')
                    if pd.to_datetime(sample, errors='coerce').notna().sum() > len(sample) * 0.8:
                        date_cols.append(col)
            except:
                pass
    
    return date_cols


def detect_numeric_columns(df):
    """
    Detect numeric columns in the dataframe.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        list: Column names with numeric data
    """
    return [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]


def detect_address_columns(df):
    """
    Detect potential address/wallet columns.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        list: Column names that might contain addresses
    """
    address_keywords = ['address', 'wallet', 'user', 'account', 'from', 'to', 'sender', 'receiver']
    address_cols = [col for col in df.columns if any(kw in col.lower() for kw in address_keywords)]
    
    # If no matches, return all string columns
    if not address_cols:
        address_cols = [col for col in df.columns if df[col].dtype == 'object']
    
    return address_cols


def prepare_dataframe(df, date_col, date_start=None, date_end=None):
    """
    Prepare dataframe by converting date column to datetime and applying time filters.
    
    Args:
        df: pandas DataFrame
        date_col: Name of the date column
        date_start: Optional start date filter
        date_end: Optional end date filter
    
    Returns:
        pd.DataFrame: Prepared and filtered dataframe
    """
    df_copy = df.copy()
    try:
        df_copy[date_col] = pd.to_datetime(df_copy[date_col])
        
        # Apply time filters if provided
        if date_start is not None:
            df_copy = df_copy[df_copy[date_col].dt.date >= date_start]
        if date_end is not None:
            df_copy = df_copy[df_copy[date_col].dt.date <= date_end]
        
        df_copy = df_copy.sort_values(date_col)
    except Exception as e:
        st.error(f"Error converting date column: {e}")
    
    return df_copy


def format_number(num):
    """
    Format large numbers with K, M, B suffixes.
    
    Args:
        num: Number to format
    
    Returns:
        str: Formatted number
    """
    if pd.isna(num):
        return "N/A"
    
    if abs(num) >= 1e9:
        return f"${num/1e9:.2f}B"
    elif abs(num) >= 1e6:
        return f"${num/1e6:.2f}M"
    elif abs(num) >= 1e3:
        return f"${num/1e3:.2f}K"
    else:
        return f"${num:.2f}"


def compute_kpis(df, date_col, address_col, value_col):
    """
    Compute key performance indicators from the dataframe.
    
    Args:
        df: pandas DataFrame
        date_col: Name of date column
        address_col: Name of address/user column
        value_col: Name of value column (in USD)
    
    Returns:
        dict: Dictionary containing KPI values
    """
    kpis = {}
    
    try:
        # Total volume
        kpis['total_volume'] = df[value_col].sum() if value_col in df.columns else 0
        
        # Number of transactions
        kpis['num_transactions'] = len(df)
        
        # Unique addresses
        kpis['unique_addresses'] = df[address_col].nunique() if address_col in df.columns else 0
        
        # Active days
        if date_col in df.columns:
            df_dates = df[date_col].dropna()
            if len(df_dates) > 0:
                kpis['active_days'] = df_dates.dt.date.nunique()
                kpis['date_range'] = (df_dates.max() - df_dates.min()).days + 1
            else:
                kpis['active_days'] = 0
                kpis['date_range'] = 0
        else:
            kpis['active_days'] = 0
            kpis['date_range'] = 0
        
        # Average transaction value
        kpis['avg_tx_value'] = kpis['total_volume'] / kpis['num_transactions'] if kpis['num_transactions'] > 0 else 0
        
    except Exception as e:
        st.error(f"Error computing KPIs: {e}")
        return {}
    
    return kpis


def build_timeseries(df, date_col, value_col, freq='D'):
    """
    Build time series aggregation of volume per period.
    
    Args:
        df: pandas DataFrame
        date_col: Name of date column
        value_col: Name of value column
        freq: Frequency for aggregation ('D' for day, 'W' for week)
    
    Returns:
        pd.DataFrame: Time series dataframe
    """
    try:
        df_ts = df.copy()
        df_ts['date'] = df_ts[date_col].dt.date
        
        ts = df_ts.groupby('date').agg({
            value_col: 'sum',
            date_col: 'count'
        }).reset_index()
        
        ts.columns = ['date', 'volume', 'tx_count']
        ts['date'] = pd.to_datetime(ts['date'])
        
        # Add moving averages
        ts['volume_ma7'] = ts['volume'].rolling(window=7, min_periods=1).mean()
        ts['tx_count_ma7'] = ts['tx_count'].rolling(window=7, min_periods=1).mean()
        
        # Add cumulative volume
        ts['cumulative_volume'] = ts['volume'].cumsum()
        
        return ts
    except Exception as e:
        st.error(f"Error building time series: {e}")
        return pd.DataFrame()


def build_top_addresses(df, address_col, value_col, top_n=10):
    """
    Build top N addresses by total volume.
    
    Args:
        df: pandas DataFrame
        address_col: Name of address column
        value_col: Name of value column
        top_n: Number of top addresses to return
    
    Returns:
        pd.DataFrame: Top addresses dataframe
    """
    try:
        top = df.groupby(address_col)[value_col].agg(['sum', 'count']).reset_index()
        top.columns = [address_col, 'total_volume', 'tx_count']
        top = top.sort_values('total_volume', ascending=False).head(top_n)
        
        # Truncate long addresses for display
        top['address_display'] = top[address_col].apply(
            lambda x: f"{str(x)[:6]}...{str(x)[-4:]}" if len(str(x)) > 12 else str(x)
        )
        
        return top
    except Exception as e:
        st.error(f"Error building top addresses: {e}")
        return pd.DataFrame()


def export_chart_png(fig, filename="chart.png"):
    """
    Export Plotly chart to PNG format.
    
    Args:
        fig: Plotly figure object
        filename: Output filename
    
    Returns:
        bytes: PNG image data, or None if export fails
    """
    try:
        # Try using kaleido (recommended)
        import plotly.io as pio
        img_bytes = pio.to_image(fig, format="png", width=1200, height=600, scale=2)
        return img_bytes
    except Exception as e:
        try:
            # Fallback: try orca
            img_bytes = fig.to_image(format="png", width=1200, height=600, scale=2)
            return img_bytes
        except Exception as e2:
            st.warning(f"⚠️ PNG export requires 'kaleido'. Install with: pip install kaleido")
            return None


def create_download_button_png(fig, filename, button_text="📥 Download PNG"):
    """
    Create a download button for Plotly chart as PNG.
    
    Args:
        fig: Plotly figure object
        filename: Filename for download
        button_text: Button label
    
    Returns:
        Streamlit download button component
    """
    img_bytes = export_chart_png(fig, filename)
    if img_bytes:
        return st.download_button(
            label=button_text,
            data=img_bytes,
            file_name=filename,
            mime="image/png"
        )
    return None


def build_cohort_retention(df, date_col, address_col):
    """
    Build a simplified cohort retention analysis.
    Groups users by their first activity week and tracks return in subsequent weeks.
    
    Args:
        df: pandas DataFrame
        date_col: Name of date column
        address_col: Name of address column
    
    Returns:
        pd.DataFrame: Cohort retention dataframe
    """
    try:
        df_cohort = df.copy()
        df_cohort['date'] = df_cohort[date_col].dt.date
        df_cohort['week'] = df_cohort[date_col].dt.to_period('W')
        
        # Get first activity week for each address
        first_activity = df_cohort.groupby(address_col)['week'].min().reset_index()
        first_activity.columns = [address_col, 'cohort_week']
        
        # Merge back
        df_cohort = df_cohort.merge(first_activity, on=address_col)
        
        # Calculate weeks since first activity
        df_cohort['weeks_since_first'] = (df_cohort['week'] - df_cohort['cohort_week']).apply(lambda x: x.n)
        
        # Aggregate: count unique users per cohort per week
        cohort_data = df_cohort.groupby(['cohort_week', 'weeks_since_first'])[address_col].nunique().reset_index()
        cohort_data.columns = ['cohort_week', 'weeks_since_first', 'active_users']
        
        # Pivot for heatmap
        cohort_pivot = cohort_data.pivot(index='cohort_week', columns='weeks_since_first', values='active_users')
        
        # Calculate retention percentages
        cohort_size = cohort_pivot.iloc[:, 0]
        cohort_retention = cohort_pivot.divide(cohort_size, axis=0) * 100
        
        return cohort_retention
    except Exception as e:
        st.error(f"Error building cohort retention: {e}")
        return pd.DataFrame()


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application logic."""
    
    # ========================================================================
    # SIDEBAR
    # ========================================================================
    
    with st.sidebar:
        st.markdown("# 📊 WDI")
        st.markdown("### Web3 Data Intelligence")
        st.markdown("---")
        
        # File uploader
        st.markdown("### 📁 Data Upload")
        uploaded_file = st.file_uploader(
            "Upload your CSV file",
            type=['csv'],
            help="Upload a CSV file exported from Dune Analytics or any on-chain dataset"
        )
        
        st.markdown("---")
        
        # Column selectors (shown only after file upload)
        if uploaded_file is not None:
            df = load_data(uploaded_file)
            
            if df is not None:
                # Auto-detect protocol
                suggestions, detected_protocol = suggest_columns(df)
                
                st.markdown("### ⚙️ Configuration")
                
                # Show detected protocol
                if detected_protocol and detected_protocol != 'generic':
                    protocol_info = format_protocol_info(detected_protocol)
                    st.success(f"🔍 Auto-detected: {protocol_info}")
                    st.caption("Column mappings suggested automatically")
                
                # Date column selector
                date_cols = detect_date_columns(df)
                if not date_cols:
                    date_cols = list(df.columns)
                
                # Helper to get index for selectbox
                def get_index(suggested_col, available_cols):
                    if suggested_col and suggested_col in available_cols:
                        return available_cols.index(suggested_col)
                    return 0
                
                date_col = st.selectbox(
                    "Date Column",
                    options=date_cols,
                    index=get_index(suggestions.get('date_col'), date_cols),
                    help="Select the column containing timestamps/dates"
                )
                
                # Address column selector
                address_cols = detect_address_columns(df)
                if not address_cols:
                    address_cols = list(df.columns)
                
                address_col = st.selectbox(
                    "Address Column",
                    options=address_cols,
                    index=get_index(suggestions.get('address_col'), address_cols),
                    help="Select the column containing wallet addresses or user IDs"
                )
                
                # Value column selector
                numeric_cols = detect_numeric_columns(df)
                if not numeric_cols:
                    numeric_cols = list(df.columns)
                
                value_col = st.selectbox(
                    "Value Column (USD)",
                    options=numeric_cols,
                    index=get_index(suggestions.get('value_col'), numeric_cols),
                    help="Select the column containing transaction values in USD"
                )
                
                st.markdown("---")
                
                # Chart Settings
                st.markdown("### 📊 Chart Settings")
                
                top_n = st.slider(
                    "Top N Addresses",
                    min_value=5,
                    max_value=50,
                    value=10,
                    step=5,
                    help="Number of top addresses to display"
                )
                
                show_moving_avg = st.checkbox(
                    "Show Moving Averages",
                    value=True,
                    help="Display 7-day moving average on time series charts"
                )
                
                show_cumulative = st.checkbox(
                    "Show Cumulative Chart",
                    value=True,
                    help="Display cumulative volume growth chart"
                )
                
                st.markdown("---")
                
                # Time Filters
                st.markdown("### 📅 Time Filters")
                
                # Prepare date column for filtering
                df_dates = prepare_dataframe(df, date_col)
                if not df_dates.empty and date_col in df_dates.columns:
                    min_date = df_dates[date_col].min().date()
                    max_date = df_dates[date_col].max().date()
                    
                    # Quick filters
                    time_filter = st.radio(
                        "Period",
                        options=["All Time", "Last 7 Days", "Last 30 Days", "Last 90 Days", "Custom Range"],
                        horizontal=False
                    )
                    
                    date_start = None
                    date_end = None
                    
                    if time_filter == "Last 7 Days":
                        date_end = max_date
                        date_start = (pd.Timestamp(max_date) - pd.Timedelta(days=7)).date()
                    elif time_filter == "Last 30 Days":
                        date_end = max_date
                        date_start = (pd.Timestamp(max_date) - pd.Timedelta(days=30)).date()
                    elif time_filter == "Last 90 Days":
                        date_end = max_date
                        date_start = (pd.Timestamp(max_date) - pd.Timedelta(days=90)).date()
                    elif time_filter == "Custom Range":
                        col1, col2 = st.columns(2)
                        with col1:
                            date_start = st.date_input(
                                "Start Date",
                                value=min_date,
                                min_value=min_date,
                                max_value=max_date
                            )
                        with col2:
                            date_end = st.date_input(
                                "End Date",
                                value=max_date,
                                min_value=min_date,
                                max_value=max_date
                            )
                    
                    # Store in session state
                    st.session_state['date_start'] = date_start
                    st.session_state['date_end'] = date_end
                    st.session_state['time_filter'] = time_filter
                else:
                    st.session_state['date_start'] = None
                    st.session_state['date_end'] = None
                    st.session_state['time_filter'] = "All Time"
                
                # Store in session state
                st.session_state['date_col'] = date_col
                st.session_state['address_col'] = address_col
                st.session_state['value_col'] = value_col
                st.session_state['top_n'] = top_n
                st.session_state['show_moving_avg'] = show_moving_avg
                st.session_state['show_cumulative'] = show_cumulative
                st.session_state['df'] = df
        
        st.markdown("---")
        st.markdown("**Version:** 1.0.0")
    
    # ========================================================================
    # MAIN CONTENT
    # ========================================================================
    
    # Header
    st.markdown("# 📊 WDI – Web3 Analytics Dashboard")
    st.markdown(
        "**Analyze on-chain data with interactive visualizations and key metrics.** "
        "Upload your CSV export from Dune Analytics or any blockchain data source to get started."
    )
    st.markdown("---")
    
    # Check if file is uploaded
    if uploaded_file is None:
        st.info("👈 Please upload a CSV file in the sidebar to begin analysis.")
        
        # Show example/instructions
        st.markdown("### 📋 How to Use")
        st.markdown("""
        1. **Upload your CSV file** containing on-chain data (e.g., from Dune Analytics)
        2. **Select the relevant columns**:
           - Date/Timestamp column
           - Address/Wallet column
           - Value column (in USD)
        3. **Explore the analytics**: KPIs, time series charts, top addresses, and retention analysis
        
        ### 📊 Supported Data
        - Transaction data from any blockchain
        - DEX swap data
        - Protocol activity logs
        - NFT sales data
        - Any CSV with date, address, and value columns
        """)
        
        return
    
    # Get data from session state
    df = st.session_state.get('df')
    date_col = st.session_state.get('date_col')
    address_col = st.session_state.get('address_col')
    value_col = st.session_state.get('value_col')
    top_n = st.session_state.get('top_n', 10)
    show_moving_avg = st.session_state.get('show_moving_avg', True)
    show_cumulative = st.session_state.get('show_cumulative', True)
    date_start = st.session_state.get('date_start')
    date_end = st.session_state.get('date_end')
    time_filter = st.session_state.get('time_filter', 'All Time')
    
    if df is None:
        st.error("Error loading data. Please try uploading the file again.")
        return
    
    # Prepare dataframe with time filters
    df_prepared = prepare_dataframe(df, date_col, date_start, date_end)
    
    # Show filter info if active
    if time_filter != "All Time" and date_start and date_end:
        st.info(f"📅 Filtered to: {time_filter} ({date_start} to {date_end}) - {len(df_prepared):,} rows")
    
    # Show data preview
    with st.expander("🔍 Data Preview", expanded=False):
        st.markdown(f"**Shape:** {df.shape[0]:,} rows × {df.shape[1]} columns")
        st.dataframe(df.head(100), use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # KPI SECTION
    # ========================================================================
    
    st.markdown("## 📈 Key Performance Indicators")
    
    # Compute KPIs
    kpis = compute_kpis(df_prepared, date_col, address_col, value_col)
    
    if kpis:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Volume",
                value=format_number(kpis['total_volume']),
                help="Sum of all transaction values"
            )
        
        with col2:
            st.metric(
                label="Transactions",
                value=f"{kpis['num_transactions']:,}",
                help="Total number of transactions"
            )
        
        with col3:
            st.metric(
                label="Unique Addresses",
                value=f"{kpis['unique_addresses']:,}",
                help="Number of unique wallet addresses"
            )
        
        with col4:
            st.metric(
                label="Active Days",
                value=f"{kpis['active_days']:,}",
                help="Number of days with activity"
            )
        
        # Second row of KPIs
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            st.metric(
                label="Avg Transaction",
                value=format_number(kpis['avg_tx_value']),
                help="Average transaction value"
            )
        
        with col6:
            st.metric(
                label="Date Range",
                value=f"{kpis['date_range']} days",
                help="Total days from first to last transaction"
            )
        
        with col7:
            avg_daily_volume = kpis['total_volume'] / kpis['active_days'] if kpis['active_days'] > 0 else 0
            st.metric(
                label="Avg Daily Volume",
                value=format_number(avg_daily_volume),
                help="Average volume per active day"
            )
        
        with col8:
            avg_daily_txs = kpis['num_transactions'] / kpis['active_days'] if kpis['active_days'] > 0 else 0
            st.metric(
                label="Avg Daily Txs",
                value=f"{avg_daily_txs:.1f}",
                help="Average transactions per active day"
            )
    
    st.markdown("---")
    
    # ========================================================================
    # TIME SERIES CHARTS
    # ========================================================================
    
    st.markdown("## 📅 Time Series Analysis")
    
    # Build time series data
    ts_data = build_timeseries(df_prepared, date_col, value_col)
    
    if not ts_data.empty:
        # Volume over time with MA
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("### 💰 Daily Volume")
            fig_volume = go.Figure()
            
            # Add daily volume area
            fig_volume.add_trace(go.Scatter(
                x=ts_data['date'],
                y=ts_data['volume'],
                mode='lines',
                name='Daily Volume',
                fill='tozeroy',
                line=dict(color='#00d4ff', width=1),
                fillcolor='rgba(0, 212, 255, 0.3)'
            ))
            
            # Add 7-day moving average if enough data and enabled
            if len(ts_data) >= 7 and show_moving_avg:
                fig_volume.add_trace(go.Scatter(
                    x=ts_data['date'],
                    y=ts_data['volume_ma7'],
                    mode='lines',
                    name='7-Day MA',
                    line=dict(color='#ff00ff', width=2, dash='dash')
                ))
            
            fig_volume.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e3f0'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#2a2d3a', title='Volume (USD)'),
                hovermode='x unified',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
            )
            st.plotly_chart(fig_volume, use_container_width=True)
            st.caption("📊 Daily aggregated transaction volume with 7-day moving average")
            create_download_button_png(fig_volume, "daily_volume.png", "📥 Export PNG")
        
        with col_chart2:
            st.markdown("### 📊 Daily Transactions")
            fig_tx = go.Figure()
            
            # Add daily tx count
            fig_tx.add_trace(go.Bar(
                x=ts_data['date'],
                y=ts_data['tx_count'],
                name='Daily Txs',
                marker_color='#00ff88'
            ))
            
            # Add 7-day moving average if enough data and enabled
            if len(ts_data) >= 7 and show_moving_avg:
                fig_tx.add_trace(go.Scatter(
                    x=ts_data['date'],
                    y=ts_data['tx_count_ma7'],
                    mode='lines',
                    name='7-Day MA',
                    line=dict(color='#ff6b00', width=2, dash='dash'),
                    yaxis='y'
                ))
            
            fig_tx.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e3f0'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#2a2d3a', title='Transactions'),
                hovermode='x unified',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
            )
            st.plotly_chart(fig_tx, use_container_width=True)
            st.caption("📊 Daily transaction count with 7-day moving average")
            create_download_button_png(fig_tx, "daily_transactions.png", "📥 Export PNG")
        
        # Add cumulative volume chart if enabled
        if show_cumulative:
            st.markdown("### 📈 Cumulative Volume Growth")
            fig_cumulative = px.area(
                ts_data,
                x='date',
                y='cumulative_volume',
                labels={'date': 'Date', 'cumulative_volume': 'Cumulative Volume (USD)'},
                color_discrete_sequence=['#8b00ff']
            )
            fig_cumulative.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e3f0'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#2a2d3a'),
                hovermode='x unified'
            )
            st.plotly_chart(fig_cumulative, use_container_width=True)
            st.caption("📈 Total cumulative volume over time - shows overall growth trajectory")
            create_download_button_png(fig_cumulative, "cumulative_volume.png", "📥 Export PNG")
        
        # Transaction Size Distribution
        st.markdown("### 📊 Transaction Size Distribution")
        col_hist1, col_hist2 = st.columns(2)
        
        with col_hist1:
            # Histogram of transaction values
            fig_hist = px.histogram(
                df_prepared,
                x=value_col,
                nbins=50,
                labels={value_col: 'Transaction Value (USD)', 'count': 'Frequency'},
                color_discrete_sequence=['#00d4ff']
            )
            fig_hist.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e3f0'),
                xaxis=dict(showgrid=True, gridcolor='#2a2d3a', title='Transaction Value (USD)'),
                yaxis=dict(showgrid=True, gridcolor='#2a2d3a', title='Number of Transactions'),
                showlegend=False
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            st.caption("Distribution of transaction sizes - shows volume concentration")
            create_download_button_png(fig_hist, "tx_distribution.png", "📥 Export PNG")
        
        with col_hist2:
            # Log scale histogram for better visualization
            df_log = df_prepared[df_prepared[value_col] > 0].copy()
            if not df_log.empty:
                fig_hist_log = px.histogram(
                    df_log,
                    x=value_col,
                    nbins=50,
                    labels={value_col: 'Transaction Value (USD)', 'count': 'Frequency'},
                    color_discrete_sequence=['#00ff88']
                )
                fig_hist_log.update_layout(
                    xaxis_type="log",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e3f0'),
                    xaxis=dict(showgrid=True, gridcolor='#2a2d3a', title='Transaction Value (USD, Log Scale)'),
                    yaxis=dict(showgrid=True, gridcolor='#2a2d3a', title='Number of Transactions'),
                    showlegend=False
                )
                st.plotly_chart(fig_hist_log, use_container_width=True)
                st.caption("Log-scale distribution - better view of all transaction sizes")
                create_download_button_png(fig_hist_log, "tx_distribution_log.png", "📥 Export PNG")
            else:
                st.info("No positive values to display in log scale")
    
    st.markdown("---")
    
    # ========================================================================
    # TOP ADDRESSES
    # ========================================================================
    
    st.markdown("## 🏆 Top Addresses by Volume")
    
    top_addresses = build_top_addresses(df_prepared, address_col, value_col, top_n)
    
    if not top_addresses.empty:
        col_top1, col_top2 = st.columns([2, 1])
        
        with col_top1:
            # Bar chart
            fig_top = px.bar(
                top_addresses,
                x='total_volume',
                y='address_display',
                orientation='h',
                labels={'total_volume': 'Total Volume (USD)', 'address_display': 'Address'},
                color='total_volume',
                color_continuous_scale='Turbo'
            )
            fig_top.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e3f0'),
                xaxis=dict(showgrid=True, gridcolor='#2a2d3a'),
                yaxis=dict(showgrid=False, autorange='reversed'),
                showlegend=False
            )
            st.plotly_chart(fig_top, use_container_width=True)
            create_download_button_png(fig_top, "top_addresses.png", "📥 Export PNG")
        
        with col_top2:
            st.markdown("### 📋 Details")
            # Display table with full data
            display_df = top_addresses[[address_col, 'total_volume', 'tx_count']].copy()
            display_df['total_volume'] = display_df['total_volume'].apply(format_number)
            display_df.columns = ['Address', 'Volume', 'Tx Count']
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.caption(f"Top {top_n} addresses ranked by total transaction volume")
    
    st.markdown("---")
    
    # ========================================================================
    # COHORT RETENTION (OPTIONAL)
    # ========================================================================
    
    st.markdown("## 🔄 Cohort Retention Analysis")
    st.markdown("*Tracks user retention by grouping addresses by their first activity week*")
    
    try:
        cohort_data = build_cohort_retention(df_prepared, date_col, address_col)
        
        if not cohort_data.empty and cohort_data.shape[0] > 1:
            # Limit to first 12 weeks for better visualization
            cohort_display = cohort_data.iloc[:, :min(12, cohort_data.shape[1])]
            
            fig_cohort = px.imshow(
                cohort_display,
                labels=dict(x="Weeks Since First Activity", y="Cohort Week", color="Retention %"),
                x=[f"Week {i}" for i in range(cohort_display.shape[1])],
                y=[str(idx) for idx in cohort_display.index],
                color_continuous_scale='Blues',
                aspect='auto'
            )
            fig_cohort.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e3f0'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_cohort, use_container_width=True)
            st.caption("Percentage of users from each cohort returning in subsequent weeks")
            create_download_button_png(fig_cohort, "cohort_retention.png", "📥 Export PNG")
        else:
            st.info("Not enough data for cohort analysis. Need multiple weeks of activity.")
    except Exception as e:
        st.warning("Cohort retention analysis unavailable for this dataset.")
    
    st.markdown("---")
    
    # ========================================================================
    # ABOUT SECTION
    # ========================================================================
    
    st.markdown("## ℹ️ About")
    st.markdown("""
    **WDI – Web3 Analytics Dashboard** is a production-quality tool for analyzing on-chain data.
    
    This application allows you to:
    - Upload CSV exports from Dune Analytics or any blockchain data source
    - Dynamically select relevant columns (date, address, value)
    - View key performance indicators at a glance
    - Explore interactive time series visualizations
    - Identify top addresses by activity
    - Analyze user retention patterns
    
    **Built by WDI – Web3 Data Intelligence** for demo purposes.
    
    ---
    *For questions or support, contact WDI.*
    """)


# ============================================================================
# RUN APP
# ============================================================================

# Streamlit Cloud executes the file directly
# Call main() - Streamlit will handle execution
# Using try-except to catch any initialization errors
try:
    if __name__ == "__main__":
        main()
except Exception as e:
    # If there's an error before Streamlit is fully initialized,
    # print it so it appears in logs
    import sys
    print(f"Error starting app: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise


