"""
Protocol Templates for Auto-Detection
Automatically detects dataset type and suggests column mappings
"""

import pandas as pd
from typing import Dict, Optional, Tuple


# Protocol templates with column patterns
PROTOCOL_TEMPLATES = {
    'uniswap': {
        'name': 'Uniswap V3',
        'description': 'DEX swaps on Uniswap V3',
        'patterns': {
            'date': ['block_time', 'timestamp', 'date', 'time'],
            'address': ['trader', 'user', 'from_address', 'to_address', 'wallet'],
            'value': ['amount_usd', 'value_usd', 'volume_usd', 'amount'],
            'optional': ['token_bought_symbol', 'token_sold_symbol', 'project', 'version']
        },
        'sample_columns': ['block_time', 'trader', 'amount_usd', 'token_bought_symbol']
    },
    'opensea': {
        'name': 'OpenSea NFT',
        'description': 'NFT sales on OpenSea marketplace',
        'patterns': {
            'date': ['block_time', 'timestamp', 'date', 'time'],
            'address': ['buyer', 'seller', 'from_address', 'to_address', 'wallet'],
            'value': ['amount_usd', 'price_usd', 'value_usd', 'amount'],
            'optional': ['nft_project_name', 'collection', 'token_id', 'marketplace']
        },
        'sample_columns': ['block_time', 'buyer', 'amount_usd', 'nft_project_name']
    },
    'aave': {
        'name': 'Aave V3',
        'description': 'Lending/borrowing on Aave V3',
        'patterns': {
            'date': ['block_time', 'timestamp', 'date', 'time'],
            'address': ['user_address', 'user', 'borrower', 'depositor', 'wallet'],
            'value': ['amount_usd', 'value_usd', 'amount'],
            'optional': ['action', 'reserve_symbol', 'protocol_version', 'chain']
        },
        'sample_columns': ['block_time', 'user_address', 'amount_usd', 'action']
    },
    'generic': {
        'name': 'Generic Web3 Data',
        'description': 'Generic blockchain/Web3 dataset',
        'patterns': {
            'date': ['block_time', 'timestamp', 'date', 'time', 'created_at'],
            'address': ['address', 'wallet', 'user', 'from', 'to', 'sender', 'receiver'],
            'value': ['amount_usd', 'value_usd', 'volume', 'amount', 'value'],
            'optional': []
        },
        'sample_columns': ['block_time', 'address', 'amount_usd']
    }
}


def detect_protocol(df: pd.DataFrame) -> Tuple[Optional[str], Dict]:
    """
    Auto-detect protocol type from dataframe columns.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        tuple: (protocol_name, confidence_score, matched_columns)
    """
    if df.empty:
        return None, {}
    
    columns_lower = [col.lower() for col in df.columns]
    scores = {}
    
    for protocol, template in PROTOCOL_TEMPLATES.items():
        if protocol == 'generic':
            continue
        
        score = 0
        matched = {}
        
        # Check date patterns
        for pattern in template['patterns']['date']:
            if any(pattern in col for col in columns_lower):
                score += 3
                matched['date'] = [col for col in df.columns if pattern in col.lower()][0]
                break
        
        # Check address patterns
        for pattern in template['patterns']['address']:
            if any(pattern in col for col in columns_lower):
                score += 3
                matched['address'] = [col for col in df.columns if pattern in col.lower()][0]
                break
        
        # Check value patterns
        for pattern in template['patterns']['value']:
            if any(pattern in col for col in columns_lower):
                score += 2
                matched['value'] = [col for col in df.columns if pattern in col.lower()][0]
                break
        
        # Check optional patterns (bonus)
        for pattern in template['patterns']['optional']:
            if any(pattern in col for col in columns_lower):
                score += 1
                matched[f'optional_{pattern}'] = [col for col in df.columns if pattern in col.lower()][0]
        
        scores[protocol] = {'score': score, 'matched': matched}
    
    # Find best match
    if scores:
        best_protocol = max(scores.items(), key=lambda x: x[1]['score'])
        if best_protocol[1]['score'] >= 5:  # Minimum threshold
            return best_protocol[0], best_protocol[1]['matched']
    
    # Fallback to generic
    return 'generic', {}


def get_protocol_template(protocol: str) -> Dict:
    """
    Get template configuration for a protocol.
    
    Args:
        protocol: Protocol name (uniswap, opensea, aave, generic)
    
    Returns:
        dict: Template configuration
    """
    return PROTOCOL_TEMPLATES.get(protocol, PROTOCOL_TEMPLATES['generic'])


def suggest_columns(df: pd.DataFrame) -> Dict[str, str]:
    """
    Suggest column mappings based on auto-detected protocol.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        dict: Suggested column mappings {'date_col': ..., 'address_col': ..., 'value_col': ...}
    """
    protocol, matched = detect_protocol(df)
    
    suggestions = {}
    
    if 'date' in matched:
        suggestions['date_col'] = matched['date']
    if 'address' in matched:
        suggestions['address_col'] = matched['address']
    if 'value' in matched:
        suggestions['value_col'] = matched['value']
    
    return suggestions, protocol


def format_protocol_info(protocol: str) -> str:
    """
    Format protocol information for display.
    
    Args:
        protocol: Protocol name
    
    Returns:
        str: Formatted info string
    """
    template = get_protocol_template(protocol)
    return f"**{template['name']}** - {template['description']}"


# Example usage
if __name__ == "__main__":
    # Test with sample data
    sample_data = pd.DataFrame({
        'block_time': ['2024-01-01', '2024-01-02'],
        'trader': ['0x123', '0x456'],
        'amount_usd': [1000, 2000],
        'token_bought_symbol': ['WETH', 'USDC']
    })
    
    suggestions, protocol = suggest_columns(sample_data)
    print(f"Detected: {protocol}")
    print(f"Suggestions: {suggestions}")

