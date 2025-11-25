# 🚀 Déploiement sur Streamlit Cloud

Guide complet pour déployer votre dashboard WDI sur Streamlit Cloud (gratuit !)

## ✅ Prérequis

1. ✅ Votre code est déjà sur GitHub : https://github.com/GuillaumeVerb/web3-analytics-dashboard
2. ✅ Vous avez un compte GitHub
3. ✅ L'app fonctionne localement

---

## 📋 Étapes de Déploiement (5 minutes)

### Étape 1 : Créer un Compte Streamlit Cloud

1. Allez sur **[share.streamlit.io](https://share.streamlit.io)**
2. Cliquez sur **"Sign in"**
3. Connectez-vous avec votre compte **GitHub**
4. Autorisez Streamlit Cloud à accéder à vos repos

### Étape 2 : Déployer l'Application

1. Sur Streamlit Cloud, cliquez sur **"New app"**
2. Remplissez le formulaire :
   - **Repository** : `GuillaumeVerb/web3-analytics-dashboard`
   - **Branch** : `main`
   - **Main file path** : `app.py`
   - **App URL** (optionnel) : `wdi-web3-dashboard` (votre URL sera : `wdi-web3-dashboard.streamlit.app`)

3. Cliquez sur **"Deploy"**

### Étape 3 : Attendre le Déploiement

- Streamlit Cloud va automatiquement :
  - Installer les dépendances depuis `requirements.txt`
  - Lancer l'application
  - Générer une URL publique

⏱️ **Temps estimé** : 2-3 minutes

### Étape 4 : Votre App est Live ! 🎉

Votre URL sera quelque chose comme :
```
https://wdi-web3-dashboard.streamlit.app
```

---

## ⚙️ Configuration Avancée (Optionnel)

### Secrets pour Dune API (si vous voulez utiliser Dune)

Si vous voulez utiliser l'intégration Dune API :

1. Dans Streamlit Cloud, allez dans **Settings** → **Secrets**
2. Ajoutez :
```toml
DUNE_API_KEY = "dqn_votre_cle_api"
```
3. L'app redémarre automatiquement

### Configuration du Fichier de Secrets

Vous pouvez aussi créer `.streamlit/secrets.toml` dans votre repo (mais ne commitez JAMAIS de vraies clés !) :

```toml
# .streamlit/secrets.toml (exemple - ne pas commiter avec vraie clé)
DUNE_API_KEY = "dqn_xxxxx"
```

---

## 🔧 Fichiers Nécessaires

Votre repo contient déjà tout ce qu'il faut :

✅ `app.py` - Application principale  
✅ `requirements.txt` - Dépendances Python  
✅ `protocol_templates.py` - Module de détection  
✅ `.streamlit/config.toml` - Configuration thème  

**Tout est prêt !** 🎯

---

## 📊 Fonctionnalités Disponibles sur Cloud

Une fois déployé, vous aurez accès à :

✅ **Upload CSV** : Les utilisateurs peuvent uploader leurs fichiers  
✅ **Tous les charts** : Tous les graphiques interactifs  
✅ **Export PNG** : Fonctionne sur Streamlit Cloud  
✅ **Filtres temporels** : Toutes les fonctionnalités  
✅ **Auto-détection** : Détection de protocole  
✅ **Datasets samples** : Accessibles depuis le repo  

⚠️ **Note** : Les fichiers uploadés ne sont pas persistés entre les sessions (c'est normal, Streamlit Cloud est stateless)

---

## 🐛 Troubleshooting

### Erreur : "Module not found"
**Solution** : Vérifiez que toutes les dépendances sont dans `requirements.txt`

### Erreur : "App failed to load"
**Solution** : 
1. Vérifiez les logs dans Streamlit Cloud
2. Testez localement d'abord : `streamlit run app.py`
3. Vérifiez que `app.py` est à la racine du repo

### L'app est lente
**Solution** : 
- Normal pour la première exécution (cold start)
- Les données sont mises en cache avec `@st.cache_data`
- Les grandes datasets peuvent prendre quelques secondes

### Export PNG ne fonctionne pas
**Solution** : 
- Vérifiez que `kaleido` est dans `requirements.txt` ✅ (déjà fait)
- Streamlit Cloud supporte kaleido nativement

---

## 🔗 Liens Utiles

- **Streamlit Cloud** : https://share.streamlit.io
- **Documentation** : https://docs.streamlit.io/streamlit-cloud
- **Votre Repo** : https://github.com/GuillaumeVerb/web3-analytics-dashboard
- **Support Streamlit** : https://discuss.streamlit.io

---

## 🎯 Prochaines Étapes Après Déploiement

1. ✅ **Partagez l'URL** avec votre équipe
2. ✅ **Ajoutez un README** avec le lien vers l'app live
3. ✅ **Configurez un domaine custom** (optionnel, payant)
4. ✅ **Activez les analytics** dans Streamlit Cloud (optionnel)

---

## 💡 Astuces

### Mise à Jour Automatique
- Chaque push sur `main` redéploie automatiquement l'app
- Pas besoin de redéployer manuellement

### Versioning
- Vous pouvez créer des branches pour tester
- Déployez depuis différentes branches si besoin

### Performance
- Les premières requêtes peuvent être lentes (cold start)
- Les suivantes sont rapides grâce au cache

---

## 🎉 C'est Prêt !

Votre dashboard sera accessible publiquement (ou en privé selon vos paramètres GitHub) sur Streamlit Cloud.

**Temps total** : ~5 minutes  
**Coût** : **GRATUIT** pour les apps publiques ! 🎁

---

**Questions ?** Consultez la [documentation officielle Streamlit Cloud](https://docs.streamlit.io/streamlit-cloud)

**Built by WDI – Web3 Data Intelligence** 🚀

