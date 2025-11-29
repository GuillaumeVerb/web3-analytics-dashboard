# 🔧 Troubleshooting Déploiement Streamlit Cloud

## Problème : App reste "in the oven" après "Resolved packages"

### Symptômes
- Logs s'arrêtent à "Resolved 47 packages"
- Pas de message "Installing collected packages..."
- Plusieurs tentatives échouent au même point

### Solutions à Essayer

#### Solution 1 : Version Flexible de Kaleido ✅ (Déjà appliquée)

J'ai modifié `requirements.txt` pour utiliser `kaleido>=0.2.1` au lieu de `kaleido==0.2.1`.

**Action** : Le changement est déjà pushé sur GitHub. Redéployez l'app.

#### Solution 2 : Retirer Temporairement Kaleido

Si Solution 1 ne fonctionne pas :

1. Dans Streamlit Cloud, allez dans **Settings**
2. Changez le fichier requirements : `requirements_minimal.txt`
3. Redéployez

**Note** : L'export PNG affichera un warning mais l'app fonctionnera.

#### Solution 3 : Vérifier les Versions Python

Streamlit Cloud utilise Python 3.13.9 (très récent). Certaines dépendances peuvent avoir des problèmes.

**Alternative** : Créer un fichier `runtime.txt` :
```
python-3.11.9
```

Mais Streamlit Cloud ne supporte pas toujours `runtime.txt`. Essayez d'abord les solutions 1 et 2.

#### Solution 4 : Vérifier les Conflits de Dépendances

Le problème pourrait venir d'un conflit entre versions. Essayez de simplifier :

```txt
streamlit>=1.29.0
pandas>=2.1.0
plotly>=5.18.0
numpy>=1.26.0
```

#### Solution 5 : Contacter le Support Streamlit

Si rien ne fonctionne :
- Forum : https://discuss.streamlit.io
- GitHub Issues : https://github.com/streamlit/streamlit/issues

---

## 🔍 Diagnostic

### Vérifier les Logs Complets

1. Dans Streamlit Cloud → Manage app → Logs
2. Cherchez les dernières lignes
3. Cherchez des erreurs (même subtiles)

### Erreurs Courantes

- `ERROR: Could not find a version...` → Problème de version
- `ModuleNotFoundError` → Dépendance manquante
- `Timeout` → Problème réseau/temps d'installation trop long

---

## ✅ Ce Qui Est Déjà Vérifié

- ✅ Code syntaxe : OK
- ✅ Imports : OK
- ✅ Structure fichiers : OK
- ✅ Fichiers présents : OK

---

## 🚀 Prochaines Étapes

1. **Attendre 5 minutes** après le push du fix kaleido
2. **Redéployer** l'app dans Streamlit Cloud
3. **Vérifier les logs** pour voir si l'installation continue
4. Si ça bloque encore, essayer **Solution 2** (requirements_minimal.txt)

---

## 📝 Notes Techniques

- Python 3.13.9 est très récent (novembre 2024)
- Certaines dépendances peuvent ne pas être 100% compatibles
- Kaleido nécessite des binaires système qui peuvent poser problème
- Streamlit Cloud utilise `uv` pour installer (plus rapide mais peut avoir des bugs)

---

**Dernière mise à jour** : Après analyse des logs montrant blocage à "Resolved packages"

