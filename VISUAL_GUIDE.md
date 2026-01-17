# 🎨 Guide Visuel du Système de Rôles

## 1️⃣ Écran de Connexion

```
┌─────────────────────────────┐
│         CAFE 216 POS        │
│      ☕ CAFE 216           │
│     Point de Vente          │
└─────────────────────────────┘
┌─────────────────────────────┐
│                             │
│  Nom d'utilisateur          │
│  [________________]         │
│                             │
│  Mot de passe              │
│  [________________]        │
│                             │
│  Rôle                      │
│  [👑 Administrateur]  ← Affiché automatiquement │
│                             │
│  [  Se connecter  ]         │
│                             │
│  Par défaut: admin / admin  │
│                             │
└─────────────────────────────┘
```

**Fonctionnalités:**
- Détection automatique du rôle
- Emojis pour chaque rôle (👑 Admin, 🎯 Gérant, etc.)
- Affichage du rôle détecté avant validation
- Animation de 800ms avant l'entrée

---

## 2️⃣ Barre Latérale Avec Contrôle d'Accès

### Pour un **Administrateur:**
```
┌──────────────────┐
│   CAFÉ 216       │
│     POS          │
├──────────────────┤
│ ☕ VENTES       │ ✅ Activé
│ 📦 PRODUITS     │ ✅ Activé
│ 💰 PRIX         │ ✅ Activé
│ 📊 STOCK        │ ✅ Activé
│ 🪑 TABLES       │ ✅ Activé
│ 📋 COMMANDES    │ ✅ Activé
│ 📈 RAPPORTS     │ ✅ Activé
│ ⚙️  PARAMÈTRES   │ ✅ Activé
│ 👥 UTILISATEURS │ ✅ Activé
├──────────────────┤
│ Connecté: admin  │
│ Rôle: admin      │
└──────────────────┘
```

### Pour un **Gestionnaire Produits:**
```
┌──────────────────┐
│   CAFÉ 216       │
│     POS          │
├──────────────────┤
│ ☕ VENTES       │ ✅ Activé
│ 📦 PRODUITS     │ ✅ Activé
│ 💰 PRIX         │ ✅ Activé
│ 📊 STOCK        │ ✅ Activé
│ 🪑 TABLES       │ ✅ Activé
│ 📋 COMMANDES    │ ✅ Activé
│ 📈 RAPPORTS     │ ❌ Désactivé
│ ⚙️  PARAMÈTRES   │ ❌ Désactivé
│ 👥 UTILISATEURS │ ❌ Désactivé
├──────────────────┤
│ Connecté: produits
│ Rôle: gestionnaire_produits
└──────────────────┘
```

### Pour un **Employé:**
```
┌──────────────────┐
│   CAFÉ 216       │
│     POS          │
├──────────────────┤
│ ☕ VENTES       │ ✅ Activé
│ 📦 PRODUITS     │ ❌ Désactivé
│ 💰 PRIX         │ ❌ Désactivé
│ 📊 STOCK        │ ❌ Désactivé
│ 🪑 TABLES       │ ✅ Activé
│ 📋 COMMANDES    │ ✅ Activé
│ 📈 RAPPORTS     │ ❌ Désactivé
│ ⚙️  PARAMÈTRES   │ ❌ Désactivé
│ 👥 UTILISATEURS │ ❌ Désactivé
├──────────────────┤
│ Connecté: employe1
│ Rôle: employé
└──────────────────┘
```

---

## 3️⃣ Écran de Gestion des Utilisateurs

```
┌────────────────────────────────────────────┐
│      👥 Gestion des Utilisateurs          │
│  Gérez les accès et rôles des utilisateurs │
├────────────────────────────────────────────┤
│                                            │
│  [➕ Ajouter un utilisateur]  [🔄 Actualiser]
│                                            │
├────────────────────────────────────────────┤
│ ID │ Utilisateur │ Nom Complet │ Rôle     │
├────────────────────────────────────────────┤
│ 1  │ admin       │ Admin       │ 👑 admin │
│ 2  │ gerant      │ Gérant      │ 🎯 gérant│
│ 3  │ produits    │ Prod Manager│ 📦 ...   │
│ 4  │ stock       │ Stock Mgr   │ 📊 ...   │
│ 5  │ employe1    │ Jean Dupont │ 👤 ...   │
│ 6  │ employe2    │ Marie Martin│ 👤 ...   │
├────────────────────────────────────────────┤
```

**Boutons:**
- ✅ ➕ Ajouter un utilisateur (vert)
- ✅ 🔄 Actualiser (bleu)
- ✅ Éditer (visible au survol)

---

## 4️⃣ Formulaire d'Ajout d'Utilisateur

```
┌──────────────────────────────┐
│  Ajouter un utilisateur      │
├──────────────────────────────┤
│                              │
│  Nom d'utilisateur:          │
│  [________________________]  │
│                              │
│  Nom complet:                │
│  [________________________]  │
│                              │
│  Mot de passe:               │
│  [________________________]  │
│                              │
│  Rôle:                       │
│  [employé                ▼] │
│   - employé                 │
│   - gestionnaire_stock      │
│   - gestionnaire_produits   │
│   - gérant                  │
│   - admin                   │
│                              │
│  [Annuler]  [Créer]         │
│                              │
└──────────────────────────────┘
```

**Rôles disponibles:**
- 👤 employé
- 📊 gestionnaire_stock
- 📦 gestionnaire_produits
- 🎯 gérant
- 👑 admin

---

## 5️⃣ Message d'Erreur (Accès Refusé)

```
Si un utilisateur autre qu'admin/gérant essaie d'accéder 
à l'écran Utilisateurs:

┌────────────────────────────────┐
│                                │
│  🔒 Accès Refusé              │
│                                │
│  Seuls les administrateurs     │
│  et gérants peuvent accéder    │
│  à la gestion des utilisateurs.│
│                                │
│                                │
└────────────────────────────────┘
```

---

## 🎯 Flux de Navigation

```
┌─────────────┐
│  Connexion  │
│  (login)    │
└──────┬──────┘
       │ ✅ Authentification réussie
       │
       ▼
┌──────────────────────────┐
│  Détection du Rôle       │
└──────────┬───────────────┘
           │
       ┌───┴────┬────────┬──────────┬──────────┬──────┐
       │        │        │          │          │      │
       ▼        ▼        ▼          ▼          ▼      ▼
    Admin   Gérant   Produits   Stock    Employé  ???
    ✅✅    ✅✅     ✅❌❌❌   ✅❌❌   ✅❌❌❌
    Tous    Tous     6 modules 3 modules 3 modules
    accès   accès    accessibles accessibles accessibles
```

---

## 📊 Matrice d'Accès Visuelle

```
Module      │ 👑 Admin │ 🎯 Gérant │ 📦 Produits │ 📊 Stock │ 👤 Employé
────────────┼──────────┼───────────┼─────────────┼──────────┼─────────
POS         │    ✅    │     ✅    │      ✅     │    ✅    │    ✅
Produits    │    ✅    │     ✅    │      ✅     │    ❌    │    ❌
Prix        │    ✅    │     ✅    │      ✅     │    ❌    │    ❌
Stock       │    ✅    │     ✅    │      ✅     │    ✅    │    ❌
Tables      │    ✅    │     ✅    │      ✅     │    ❌    │    ✅
Commandes   │    ✅    │     ✅    │      ✅     │    ✅    │    ✅
Rapports    │    ✅    │     ✅    │      ❌     │    ❌    │    ❌
Paramètres  │    ✅    │     ✅    │      ❌     │    ❌    │    ❌
Utilisateurs│    ✅    │     ✅    │      ❌     │    ❌    │    ❌
```

---

## 🔐 Sécurité Appliquée

### 1. Hash des mots de passe
```
Mot de passe: "produits123"
↓
bcrypt hash: "$2b$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
↓
Stocké en DB
```

### 2. Migration des mots de passe
```
Ancien: mot_de_passe_en_clair
↓
Première connexion détectée
↓
Automatiquement hasché en bcrypt
↓
Stocké en DB sécurisé
```

### 3. Vérification des permissions
```
Utilisateur clique sur bouton
↓
Vérification: index ∈ allowed_indices?
↓
Non → Bouton désactivé (grisé)
Oui → Bouton activé (cliquable)
```

---

## 🚀 Étapes d'Implémentation Rapide

1. **Lancer l'initialisation:**
   ```bash
   python initialize_users.py
   ```

2. **Tester avec chaque rôle:**
   - Admin (admin/admin)
   - Gérant (gerant/gerant123)
   - Produits (produits/produits123) ← **Cas demandé**
   - Stock (stock/stock123)
   - Employé (employe1/employe123)

3. **Vérifier:**
   - Rôle affiché au login ✅
   - Boutons grisés selon rôle ✅
   - Accès restreint à Produits pour le rôle "Produits" ✅
   - Erreur "Accès refusé" si non autorisé ✅

---

**Status:** ✅ 100% Implémenté et testé  
**Prêt pour:** Production
