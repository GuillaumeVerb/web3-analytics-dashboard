# 🔮 Guide d'Intégration Dune Analytics API

Ce guide explique comment intégrer l'API Dune Analytics pour récupérer des données en temps réel.

## 🎯 Pourquoi Utiliser l'API Dune ?

### Avantages
✅ **Données en temps réel** : Récupérez les dernières données blockchain  
✅ **Pas de limite de taille CSV** : Accès direct aux données  
✅ **Automatisation** : Rafraîchissement automatique des dashboards  
✅ **Requêtes SQL personnalisées** : Créez vos propres analyses sur Dune  

### Limitations
⚠️ **Crédits API** : L'API Dune utilise un système de crédits (payant selon plan)  
⚠️ **Rate limits** : Limite du nombre de requêtes par minute  
⚠️ **Temps d'exécution** : Les queries complexes peuvent prendre plusieurs secondes  

---

## 🚀 Setup Rapide (5 minutes)

### Étape 1 : Obtenir une Clé API Dune

1. Créez un compte sur [dune.com](https://dune.com) (gratuit)
2. Allez dans **Settings** → **API**
3. Cliquez sur **Create API Key**
4. Copiez votre clé (format : `dqn_xxxxxxxxxxxxxx`)

📚 [Documentation officielle Dune API](https://docs.dune.com/api-reference/overview/introduction)

### Étape 2 : Installer le Client Python

```bash
pip install dune-client
```

Ou ajoutez à votre `requirements.txt` :
```
dune-client==1.2.0
```

### Étape 3 : Configurer votre Environnement

#### Option A : Variable d'Environnement (Recommandé)
```bash
# Dans votre terminal
export DUNE_API_KEY="dqn_xxxxxxxxxxxxxx"

# Ou créez un fichier .env
echo "DUNE_API_KEY=dqn_xxxxxxxxxxxxxx" > .env
```

#### Option B : Dans Streamlit Secrets
Créez `.streamlit/secrets.toml` :
```toml
DUNE_API_KEY = "dqn_xxxxxxxxxxxxxx"
```

⚠️ **Important** : Ne commitez jamais votre clé API sur GitHub !

---

## 📊 Comment Trouver un Query ID

1. Allez sur [dune.com](https://dune.com)
2. Cherchez une query (ex: "uniswap v3 swaps")
3. Regardez l'URL : `https://dune.com/queries/1234567`
4. Le **Query ID** est `1234567`

### Queries Populaires Recommandées

| Protocole | Description | Exemple Query ID |
|-----------|-------------|------------------|
| Uniswap V3 | Daily swaps volume | [3339988](https://dune.com/queries/3339988) |
| OpenSea | NFT collection stats | [1234567](https://dune.com/queries/1234567) |
| Aave V3 | Lending/borrowing | [2345678](https://dune.com/queries/2345678) |

💡 **Astuce** : Vous pouvez "fork" n'importe quelle query publique et l'utiliser !

---

## 🔧 Utilisation dans le Dashboard

### Mode 1 : Via l'Interface UI

1. Lancez l'app : `streamlit run app.py`
2. Dans la sidebar, cochez **"Fetch from Dune API"**
3. Entrez votre **API Key**
4. Sélectionnez une query populaire OU entrez un Query ID custom
5. Cliquez sur **"Fetch Data"**

### Mode 2 : Via Code Python

```python
from dune_integration import DuneIntegration
import pandas as pd

# Initialiser le client
dune = DuneIntegration(api_key="dqn_xxxxx")

# Fetch une query
df = dune.fetch_query_results(query_id=1234567)

# Utiliser les données
print(df.head())
print(f"Loaded {len(df)} rows")
```

### Mode 3 : Avec Paramètres

Certaines queries Dune acceptent des paramètres :

```python
# Query avec paramètres
df = dune.fetch_query_results(
    query_id=1234567,
    parameters={
        "wallet_address": "0x742d35cc6634c0532925a3b844bc9e7595f0beda",
        "start_date": "2024-01-01",
        "token": "WETH"
    }
)
```

---

## 🏗️ Créer Vos Propres Queries

### 1. Créer une Query sur Dune

1. Allez sur [dune.com/queries](https://dune.com/queries)
2. Cliquez **"New Query"**
3. Écrivez votre SQL (ex: requête sur `uniswap_v3.trades`)
4. **Save** et notez le Query ID

### Exemple de Query : Uniswap V3 Swaps

```sql
SELECT
    block_time,
    tx_hash,
    trader,
    token_bought_symbol,
    token_sold_symbol,
    token_bought_amount,
    token_sold_amount,
    amount_usd,
    project,
    version
FROM dex.trades
WHERE project = 'uniswap'
    AND version = '3'
    AND block_time >= NOW() - INTERVAL '7' DAY
ORDER BY block_time DESC
LIMIT 1000
```

### 2. Ajouter des Paramètres

Dans votre query SQL, utilisez `{{parameter_name}}` :

```sql
SELECT *
FROM dex.trades
WHERE trader = {{wallet_address}}
    AND block_time >= {{start_date}}
```

Puis dans Python :
```python
df = dune.fetch_query_results(
    query_id=123456,
    parameters={
        "wallet_address": "0x123...",
        "start_date": "2024-01-01"
    }
)
```

---

## ⚡ Optimisations & Best Practices

### 1. Caching
Le module utilise `@st.cache_data` avec TTL 1h :
```python
# Les résultats sont mis en cache pendant 1 heure
df = fetch_dune_data_cached(api_key, query_id)
```

### 2. Limiter les Requêtes
```python
# N'exécutez pas de query à chaque interaction UI
# Utilisez un bouton :
if st.button("Refresh Data from Dune"):
    df = dune.fetch_query_results(query_id)
```

### 3. Gestion des Erreurs
```python
try:
    df = dune.fetch_query_results(query_id)
    if df is not None:
        st.success("Data loaded!")
    else:
        st.error("No results")
except Exception as e:
    st.error(f"Error: {e}")
```

### 4. Progress Bar
```python
with st.spinner("Fetching from Dune..."):
    df = dune.fetch_query_results(query_id)
```

---

## 💰 Coûts & Crédits API

### Plans Dune (2024)

| Plan | Crédits/mois | Prix | Exécutions | Idéal pour |
|------|--------------|------|-----------|-----------|
| **Free** | 100 | $0 | ~100 queries | Exploration |
| **Plus** | 1,000 | $99/mo | ~1,000 queries | Dashboards perso |
| **Premium** | 10,000 | $399/mo | ~10,000 queries | Production |
| **Enterprise** | Illimité | Custom | Illimité | Enterprise |

💡 **Astuce** : 1 crédit = 1 exécution de query simple

📖 [Pricing Dune officiel](https://dune.com/pricing)

---

## 🔒 Sécurité

### ❌ Ne JAMAIS faire :
```python
# NE PAS hardcoder l'API key
api_key = "dqn_123456789..."  # ❌ DANGER
```

### ✅ Bonne pratique :
```python
# Utiliser des variables d'environnement
import os
api_key = os.environ.get('DUNE_API_KEY')

# Ou Streamlit secrets
api_key = st.secrets.get('DUNE_API_KEY')
```

### Ajouter au .gitignore
```bash
# .gitignore
.env
.streamlit/secrets.toml
```

---

## 🐛 Troubleshooting

### Erreur : "API key required"
**Solution** : Vérifiez que `DUNE_API_KEY` est bien défini
```bash
echo $DUNE_API_KEY  # Doit afficher votre clé
```

### Erreur : "Query execution failed"
**Causes possibles** :
- Query ID invalide
- Query trop longue (timeout)
- Crédits API épuisés
- Paramètres manquants

**Solution** : Testez d'abord la query sur dune.com

### Erreur : "Rate limit exceeded"
**Solution** : Ajoutez du délai entre les requêtes
```python
import time
time.sleep(2)  # 2 secondes entre queries
```

### Données vides
**Causes** :
- Filtres trop restrictifs dans la query
- Période sans données (ex: weekend)
- Erreur dans les paramètres

**Solution** : Vérifiez les résultats sur dune.com d'abord

---

## 📚 Ressources

### Documentation Officielle
- [Dune API Reference](https://docs.dune.com/api-reference/overview/introduction)
- [Python SDK GitHub](https://github.com/duneanalytics/dune-client)
- [Query Examples](https://dune.com/browse/queries)

### Communauté
- [Dune Discord](https://discord.gg/dune)
- [Dune Twitter](https://twitter.com/dune)
- [Tutoriels YouTube](https://www.youtube.com/c/DuneAnalytics)

### Alternatives
Si Dune API ne convient pas :
- **The Graph** : GraphQL API pour données blockchain
- **Etherscan API** : Données Ethereum
- **Alchemy** / **Infura** : Nodes RPC
- **Covalent** : API multi-chain

---

## 🚀 Prochaines Étapes

1. ✅ Obtenez votre API key Dune
2. ✅ Installez `dune-client`
3. ✅ Testez avec une query simple
4. ✅ Intégrez dans votre dashboard
5. ✅ Créez vos propres queries
6. ✅ Partagez vos dashboards !

---

**Questions ? Besoin d'aide ?**  
Contactez **WDI – Web3 Data Intelligence**

Happy analyzing! 📊🚀

