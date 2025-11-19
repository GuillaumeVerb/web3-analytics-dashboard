"""
Dune Analytics API Integration Module
Allows fetching real-time data from Dune Analytics queries
"""

import pandas as pd
import streamlit as st
from typing import Optional, Dict, Any
import os

try:
    from dune_client.client import DuneClient
    from dune_client.query import QueryBase
    DUNE_CLIENT_AVAILABLE = True
except ImportError:
    DUNE_CLIENT_AVAILABLE = False


class DuneIntegration:
    """
    Integration class for Dune Analytics API.
    
    Usage:
        dune = DuneIntegration(api_key="your-api-key")
        df = dune.fetch_query_results(query_id=123456)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Dune client.
        
        Args:
            api_key: Dune Analytics API key (or set DUNE_API_KEY env var)
        """
        if not DUNE_CLIENT_AVAILABLE:
            raise ImportError(
                "dune-client not installed. Run: pip install dune-client"
            )
        
        self.api_key = api_key or os.environ.get('DUNE_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Dune API key required. Set via parameter or DUNE_API_KEY env variable."
            )
        
        self.client = DuneClient(api_key=self.api_key)
    
    def fetch_query_results(
        self,
        query_id: int,
        parameters: Optional[Dict[str, Any]] = None,
        max_retries: int = 3
    ) -> Optional[pd.DataFrame]:
        """
        Execute a Dune query and return results as DataFrame.
        
        Args:
            query_id: Dune query ID (found in query URL)
            parameters: Optional query parameters (e.g., {"wallet": "0x123..."})
            max_retries: Number of retry attempts if query fails
        
        Returns:
            pd.DataFrame with query results, or None if error
        """
        try:
            # Create query object
            if parameters:
                query = QueryBase(
                    query_id=query_id,
                    params=parameters
                )
            else:
                query = QueryBase(query_id=query_id)
            
            # Execute query
            st.info(f"🔄 Executing Dune query {query_id}...")
            results = self.client.run_query(query)
            
            # Convert to DataFrame
            if results and hasattr(results, 'get_rows'):
                rows = results.get_rows()
                df = pd.DataFrame(rows)
                st.success(f"✅ Fetched {len(df)} rows from Dune")
                return df
            else:
                st.error("❌ No results returned from Dune query")
                return None
        
        except Exception as e:
            st.error(f"❌ Error fetching Dune data: {str(e)}")
            return None
    
    def get_query_info(self, query_id: int) -> Optional[Dict]:
        """
        Get metadata about a Dune query.
        
        Args:
            query_id: Dune query ID
        
        Returns:
            Dictionary with query metadata
        """
        try:
            query = QueryBase(query_id=query_id)
            # Note: This is a placeholder - actual implementation depends on SDK version
            return {
                'query_id': query_id,
                'status': 'available'
            }
        except Exception as e:
            st.error(f"Error getting query info: {str(e)}")
            return None


# Pre-configured popular Dune queries
POPULAR_QUERIES = {
    'uniswap_v3_daily_volume': {
        'query_id': 1234567,  # Replace with actual query ID
        'name': 'Uniswap V3 Daily Volume',
        'description': 'Daily trading volume on Uniswap V3',
        'columns': ['date', 'volume_usd', 'tx_count']
    },
    'opensea_collections': {
        'query_id': 2345678,  # Replace with actual query ID
        'name': 'OpenSea Top Collections',
        'description': 'NFT collection rankings by volume',
        'columns': ['collection_name', 'volume_usd', 'sales_count']
    },
    'aave_v3_tvl': {
        'query_id': 3456789,  # Replace with actual query ID
        'name': 'Aave V3 TVL',
        'description': 'Total Value Locked in Aave V3',
        'columns': ['date', 'tvl_usd', 'depositors']
    }
}


def fetch_dune_data_cached(
    api_key: str,
    query_id: int,
    parameters: Optional[Dict[str, Any]] = None
) -> Optional[pd.DataFrame]:
    """
    Cached wrapper for fetching Dune data.
    Results are cached for 1 hour to avoid excessive API calls.
    
    Args:
        api_key: Dune API key
        query_id: Query ID to execute
        parameters: Optional query parameters
    
    Returns:
        pd.DataFrame with results
    """
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def _fetch(api_key_hash: str, qid: int, params_str: str):
        dune = DuneIntegration(api_key=api_key)
        params = eval(params_str) if params_str else None
        return dune.fetch_query_results(qid, params)
    
    # Hash API key for caching (don't store plaintext in cache)
    api_key_hash = str(hash(api_key))
    params_str = str(parameters) if parameters else ""
    
    return _fetch(api_key_hash, query_id, params_str)


def show_dune_config_ui():
    """
    Streamlit UI component for Dune API configuration.
    Place this in your sidebar.
    
    Returns:
        tuple: (api_key, query_id, use_dune)
    """
    st.markdown("### 🔮 Dune Analytics")
    
    use_dune = st.checkbox(
        "Fetch from Dune API",
        value=False,
        help="Load data directly from Dune Analytics queries"
    )
    
    if use_dune:
        # API Key input
        api_key = st.text_input(
            "Dune API Key",
            type="password",
            help="Get your API key from dune.com/settings/api"
        )
        
        # Query ID or preset selector
        query_mode = st.radio(
            "Query Source",
            options=["Popular Queries", "Custom Query ID"],
            horizontal=True
        )
        
        if query_mode == "Popular Queries":
            query_name = st.selectbox(
                "Select Query",
                options=list(POPULAR_QUERIES.keys()),
                format_func=lambda x: POPULAR_QUERIES[x]['name']
            )
            query_id = POPULAR_QUERIES[query_name]['query_id']
            st.caption(POPULAR_QUERIES[query_name]['description'])
        else:
            query_id = st.number_input(
                "Query ID",
                min_value=1,
                value=1234567,
                help="Find the query ID in the Dune query URL"
            )
        
        # Optional parameters
        with st.expander("Query Parameters (Optional)"):
            param_key = st.text_input("Parameter Name", placeholder="e.g., wallet")
            param_value = st.text_input("Parameter Value", placeholder="e.g., 0x123...")
            
            parameters = {}
            if param_key and param_value:
                parameters[param_key] = param_value
        
        return api_key, query_id, use_dune, parameters if parameters else None
    
    return None, None, False, None


def validate_dune_setup() -> bool:
    """
    Validate that Dune client is properly installed.
    
    Returns:
        bool: True if dune-client is available
    """
    return DUNE_CLIENT_AVAILABLE


# Example usage in main app
if __name__ == "__main__":
    st.title("Dune Integration Test")
    
    if not validate_dune_setup():
        st.error("❌ Dune client not installed. Run: pip install dune-client")
        st.stop()
    
    api_key, query_id, use_dune, parameters = show_dune_config_ui()
    
    if use_dune and api_key:
        if st.button("Fetch Data from Dune"):
            df = fetch_dune_data_cached(api_key, query_id, parameters)
            
            if df is not None:
                st.success(f"✅ Loaded {len(df)} rows from Dune")
                st.dataframe(df.head(50))
            else:
                st.error("❌ Failed to fetch data")
    else:
        st.info("👈 Configure Dune API in sidebar to fetch data")

