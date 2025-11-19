# Dune Analytics Sample Datasets

Ce dossier contient des datasets réalistes simulant des exports Dune Analytics de différents protocoles DeFi et NFT.

## 📊 Datasets Disponibles

### 1. **Uniswap V3 Swaps** (`uniswap_v3_swaps.csv`)
Données de swaps sur Uniswap V3 (DEX)

**Colonnes :**
- `block_time` : Timestamp de la transaction
- `tx_hash` : Hash de la transaction
- `trader` : Adresse du trader
- `token_bought_symbol` : Token acheté (ex: WETH, USDC)
- `token_sold_symbol` : Token vendu
- `token_bought_amount` : Quantité achetée
- `token_sold_amount` : Quantité vendue
- `amount_usd` : Valeur en USD
- `project` : Nom du protocole
- `version` : Version du protocole

**Cas d'usage :**
- Analyse du volume de trading
- Top traders par volume
- Paires de trading les plus populaires
- Distribution des tailles de transactions

**Configuration recommandée :**
- Date Column: `block_time`
- Address Column: `trader`
- Value Column: `amount_usd`

---

### 2. **OpenSea NFT Sales** (`opensea_nft_sales.csv`)
Ventes de NFTs sur OpenSea marketplace

**Colonnes :**
- `block_time` : Timestamp de la vente
- `tx_hash` : Hash de la transaction
- `buyer` : Adresse de l'acheteur
- `seller` : Adresse du vendeur
- `nft_project_name` : Nom de la collection (BAYC, Azuki, etc.)
- `token_id` : ID du NFT
- `amount_usd` : Prix de vente en USD
- `currency_symbol` : Devise utilisée (WETH, ETH)
- `marketplace` : Plateforme (OpenSea)
- `platform_fee_usd` : Frais de plateforme
- `creator_fee_usd` : Royalties créateur

**Cas d'usage :**
- Floor price tracking par collection
- Volume de ventes par collection
- Top collectors (buyers avec plus de volume)
- Analyse des frais (marketplace + royalties)

**Configuration recommandée :**
- Date Column: `block_time`
- Address Column: `buyer` (ou `seller`)
- Value Column: `amount_usd`

---

### 3. **Aave V3 Activity** (`aave_v3_activity.csv`)
Activité de lending/borrowing sur Aave V3

**Colonnes :**
- `block_time` : Timestamp de l'action
- `tx_hash` : Hash de la transaction
- `user_address` : Adresse de l'utilisateur
- `action` : Type d'action (Deposit, Borrow, Repay, Withdraw)
- `reserve_symbol` : Asset utilisé (USDC, WETH, DAI)
- `amount` : Montant en tokens
- `amount_usd` : Valeur en USD
- `protocol_version` : Version du protocole
- `chain` : Blockchain (Ethereum, Polygon, etc.)

**Cas d'usage :**
- Volume de dépôts vs emprunts
- Top depositors/borrowers
- Assets les plus utilisés
- Analyse de la liquidité par période

**Configuration recommandée :**
- Date Column: `block_time`
- Address Column: `user_address`
- Value Column: `amount_usd`

---

## 🎯 Comment Utiliser

1. **Dans le dashboard WDI** :
   ```bash
   streamlit run app.py
   ```

2. **Uploadez un des fichiers CSV** depuis le dossier `dune_samples/`

3. **Le dashboard détectera automatiquement les colonnes**, mais vous pouvez ajuster :
   - Date column
   - Address column  
   - Value column

4. **Explorez les KPIs et visualisations** :
   - Volume total
   - Nombre de transactions
   - Addresses uniques
   - Charts temporels
   - Top addresses
   - Cohort retention

---

## 💡 Suggestions d'Analyses

### Pour Uniswap V3
- **Volume par paire de trading** : Grouper par token_bought + token_sold
- **Analyse des "whale traders"** : Top 10 traders par volume cumulé
- **Distribution temporelle** : Pics d'activité par heure/jour
- **Token flow** : Sankey diagram des swaps

### Pour OpenSea NFT
- **Collections les plus tradées** : Volume par nft_project_name
- **Whale buyers** : Top collectors par nombre d'achats et volume
- **Analyse des prix** : Distribution des prix de vente
- **ROI analysis** : Si un seller=buyer précédent

### Pour Aave V3
- **TVL approximation** : Deposits - Withdrawals
- **Utilization rate** : Borrows / Deposits
- **User behavior** : Deposit-only vs deposit-borrow users
- **Asset preference** : USDC vs WETH vs DAI

---

## 📝 Notes Techniques

### Génération des Données
Ces datasets sont **synthétiques mais réalistes** :
- Addresses Ethereum valides (format 0x...)
- Timestamps cohérents (Jan 2024)
- Montants réalistes basés sur des volumes réels
- Token symbols actuels
- Transaction hashes simulés

### Dune Analytics
Pour obtenir de vraies données :
1. Créez un compte sur [dune.com](https://dune.com)
2. Explorez les queries communautaires
3. Fork une query ou créez la vôtre
4. Exportez en CSV (limite selon plan)

### Queries Dune Populaires
- **Uniswap V3** : `ethereum.uniswap_v3.trades`
- **OpenSea** : `nft.trades` (filtré marketplace = 'OpenSea')
- **Aave V3** : `aave_v3_ethereum.Pool_evt_*`

---

## 🔗 Resources

- [Dune Analytics](https://dune.com)
- [Uniswap V3 Docs](https://docs.uniswap.org/contracts/v3/overview)
- [OpenSea API](https://docs.opensea.io)
- [Aave V3 Docs](https://docs.aave.com/developers)
- [Ethereum Address Format](https://ethereum.org/en/developers/docs/accounts/)

---

**Créé par WDI – Web3 Data Intelligence**

