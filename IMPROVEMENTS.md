# Axes d'Amélioration - WDI Dashboard

## 🎯 Améliorations Prioritaires

### 1. **Filtres Temporels Avancés**
- [ ] Sélecteur de période (Last 7d, 30d, 90d, All time)
- [ ] Date picker pour périodes custom
- [ ] Comparaison période vs période précédente (% change)

### 2. **Export & Partage**
- [ ] Bouton export PNG/PDF des charts
- [ ] Export CSV des données filtrées
- [ ] Génération de rapport automatique
- [ ] Lien de partage avec paramètres pré-configurés

### 3. **Métriques Additionnelles**
- [ ] Wallet concentration (% détenu par top 10)
- [ ] New vs Returning users
- [ ] Transaction size distribution (histogram)
- [ ] Gas fees analysis (si disponible dans data)
- [ ] Active addresses par période
- [ ] Churn rate

### 4. **Visualisations Supplémentaires**
- [ ] Sankey diagram (flow entre addresses)
- [ ] Heatmap calendrier (GitHub-style)
- [ ] Distribution des montants (violin plot)
- [ ] Cumulative volume chart
- [ ] Moving averages (7d, 30d)

### 5. **Performance & UX**
- [ ] Pagination pour grandes datasets (>100k rows)
- [ ] Loading states avec spinners
- [ ] Progressive data loading
- [ ] Données cached avec timestamp
- [ ] Mode "Live" avec auto-refresh

### 6. **Analytics Avancés**
- [ ] Détection d'anomalies (spikes de volume)
- [ ] Prédictions ML (trend futur)
- [ ] Segmentation des users (whales, retail, etc.)
- [ ] Network analysis (graph de connexions)
- [ ] Wallet profiling

### 7. **Multi-Protocol Support**
- [ ] Templates pré-configurés par protocole:
  - Uniswap (swaps, liquidity)
  - OpenSea (NFT sales)
  - Aave (lending/borrowing)
  - Compound, MakerDAO, etc.
- [ ] Auto-detection du type de dataset

### 8. **Comparaisons**
- [ ] Comparer plusieurs CSV (benchmark)
- [ ] Side-by-side protocols
- [ ] Multi-chain analysis

### 9. **Notifications & Alerts**
- [ ] Seuils d'alerte configurables
- [ ] Email/webhook notifications
- [ ] Monitoring de métriques clés

### 10. **Data Quality**
- [ ] Validation des données à l'upload
- [ ] Détection de valeurs aberrantes
- [ ] Data cleaning automatique
- [ ] Rapport de qualité des données

## 🎨 Améliorations UI/UX

### Design
- [ ] Mode light/dark toggle
- [ ] Thèmes customisables (couleurs par protocole)
- [ ] Animations subtiles sur les KPIs
- [ ] Skeleton loaders pendant chargement
- [ ] Tooltips explicatifs sur chaque métrique

### Navigation
- [ ] Menu tabs (Overview, Details, Analytics, Settings)
- [ ] Breadcrumbs pour navigation
- [ ] Favoris / Saved views
- [ ] Historique des analyses

### Interactivité
- [ ] Click sur charts pour drill-down
- [ ] Filtres croisés entre charts
- [ ] Brush & zoom synchronisés
- [ ] Table interactive avec tri/recherche

## 🔧 Techniques

### Code
- [ ] Refactoring en modules séparés (utils/, charts/, data/)
- [ ] Tests unitaires (pytest)
- [ ] Type hints complets
- [ ] Logging structuré
- [ ] Configuration via YAML/ENV

### Déploiement
- [ ] Docker containerization
- [ ] CI/CD avec GitHub Actions
- [ ] Déploiement Streamlit Cloud / AWS / Heroku
- [ ] Monitoring (Sentry, Datadog)

### Base de Données
- [ ] Support PostgreSQL / MongoDB
- [ ] Historique des uploads
- [ ] User accounts & authentication
- [ ] Saved queries & dashboards

## 📊 Intégrations Possibles

- [ ] **Dune API** - Fetch direct depuis Dune
- [ ] **The Graph** - Query subgraphs
- [ ] **Etherscan API** - Enrichissement données
- [ ] **CoinGecko** - Prix en temps réel
- [ ] **DeBank** - Wallet profiling
- [ ] **Nansen** - Labels et tags

## 🎯 Quick Wins (Implémentation Rapide)

1. **Filtres temporels** (2h)
2. **Export PNG des charts** (1h)
3. **Moving averages sur time series** (1h)
4. **Wallet address truncation cliquable** (30min)
5. **Tooltips explicatifs** (1h)
6. **Mode fullscreen pour charts** (30min)
7. **Cumulative volume chart** (1h)
8. **Distribution histogram** (1h)

## 💡 Features "Premium"

Pour version payante / enterprise:
- Multi-user avec roles
- Alertes en temps réel
- API access
- White-label branding
- Support prioritaire
- Data retention illimitée
- Custom integrations

