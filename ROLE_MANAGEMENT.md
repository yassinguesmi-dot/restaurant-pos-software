# 🔐 Système de Contrôle d'Accès - Café 216 POS

## Vue d'ensemble

L'application dispose maintenant d'un système complet de gestion des utilisateurs avec contrôle d'accès basé sur les rôles (RBAC - Role Based Access Control).

## 👥 Rôles disponibles

### 1. **👑 Administrateur (admin)**
- **Accès complet** à toutes les fonctionnalités
- Peut créer/modifier tous les utilisateurs
- Accès aux paramètres système

**Comptes de test:**
- Username: `admin`
- Password: `admin`

### 2. **🎯 Gérant (gérant)**
- **Accès complet** à toutes les fonctionnalités
- Même permissions que l'administrateur
- Peut gérer les rapports et statistiques

**Comptes de test:**
- Username: `gerant`
- Password: `gerant123`

### 3. **📦 Gestionnaire Produits (gestionnaire_produits)**
- ✅ **Accès autorisé:**
  - Point de Vente (POS)
  - Gestion des Produits
  - Gestion des Prix
  - Gestion du Stock
  - Gestion des Tables
  - Historique des Commandes
  
- ❌ **Accès refusé:**
  - Rapports et Statistiques
  - Paramètres système

**Comptes de test:**
- Username: `produits`
- Password: `produits123`

### 4. **📊 Gestionnaire Stock (gestionnaire_stock)**
- ✅ **Accès autorisé:**
  - Point de Vente (POS)
  - Gestion du Stock
  - Historique des Commandes
  
- ❌ **Accès refusé:**
  - Gestion des Produits
  - Gestion des Prix
  - Gestion des Tables
  - Rapports
  - Paramètres

**Comptes de test:**
- Username: `stock`
- Password: `stock123`

### 5. **👤 Employé (employé)**
- ✅ **Accès autorisé:**
  - Point de Vente (POS) - vendre
  - Gestion des Tables
  - Historique des Commandes
  
- ❌ **Accès refusé:**
  - Gestion des Produits
  - Gestion des Prix
  - Gestion du Stock
  - Rapports
  - Paramètres

**Comptes de test:**
- Username: `employe1`
- Password: `employe123`
- Username: `employe2`
- Password: `employe123`

## 📊 Matrice d'accès

| Module | Admin | Gérant | Prod | Stock | Employé |
|--------|-------|--------|------|-------|---------|
| POS | ✅ | ✅ | ✅ | ✅ | ✅ |
| Produits | ✅ | ✅ | ✅ | ❌ | ❌ |
| Prix | ✅ | ✅ | ✅ | ❌ | ❌ |
| Stock | ✅ | ✅ | ✅ | ✅ | ❌ |
| Tables | ✅ | ✅ | ✅ | ❌ | ✅ |
| Commandes | ✅ | ✅ | ✅ | ✅ | ✅ |
| Rapports | ✅ | ✅ | ❌ | ❌ | ❌ |
| Paramètres | ✅ | ✅ | ❌ | ❌ | ❌ |

## 🔑 Comment utiliser

### 1. Initialiser les utilisateurs (première utilisation)

```bash
python initialize_users.py
```

Cela crée tous les utilisateurs de test avec leurs rôles respectifs.

### 2. Se connecter

1. Lancez l'application: `python main.py`
2. Entrez vos identifiants sur l'écran de connexion
3. Le rôle s'affiche automatiquement dans le champ "Rôle"
4. Les modules inaccessibles sont désactivés dans la barre latérale

### 3. Ajouter un nouvel utilisateur

Via la base de données ou SQL:

```sql
INSERT INTO users (username, password, full_name, role, is_active)
VALUES ('nouveau_user', 'hash_password', 'Nom Complet', 'gestionnaire_produits', 1);
```

## 🔒 Sécurité

- ✅ Les mots de passe sont **hashés avec bcrypt**
- ✅ Les permissions sont **vérifiées à chaque navigation**
- ✅ Les boutons désactivés sont grisés pour les modules non autorisés
- ✅ La migration des mots de passe en clair vers bcrypt est **automatique**

## 🎯 Cas d'usage typiques

### Cas 1: Taper les produits uniquement
➡️ **Utiliser le rôle:** `gestionnaire_produits`
- Peut ajouter, modifier, supprimer les produits
- Peut gérer les prix
- Peut consulter le stock
- Ne peut pas voir les rapports ni accéder aux paramètres

### Cas 2: Gérer le stock uniquement  
➡️ **Utiliser le rôle:** `gestionnaire_stock`
- Peut consulter et modifier le stock
- Peut voir les commandes
- Peut faire des ventes (POS)
- Ne peut pas créer/modifier les produits

### Cas 3: Employé de caisse
➡️ **Utiliser le rôle:** `employé`
- Peut faire des ventes (POS)
- Peut gérer les tables
- Peut voir l'historique des commandes
- Ne peut pas gérer les produits ou le stock

### Cas 4: Accès complet
➡️ **Utiliser le rôle:** `admin` ou `gérant`
- Accès à tout
- Peut créer/gérer les utilisateurs
- Peut consulter les rapports

## 📝 Notes techniques

- **Base de données:** SQLite avec champ `role` dans la table `users`
- **Contrôle d'accès:** Implémenté dans `MainWindow.__init__()`
- **Interface login:** Affiche le rôle avec emojis et icônes
- **État des boutons:** Automatiquement désactivés selon les permissions

## ✅ Checklist de déploiement

- [ ] Initialiser les utilisateurs: `python initialize_users.py`
- [ ] Tester chaque rôle avec ses comptes de test
- [ ] Modifier les mots de passe par défaut en production
- [ ] Documenter les rôles internes pour chaque employé
- [ ] Mettre en place une procédure de changement de mot de passe

---

**Créé le:** 12 janvier 2026  
**Version:** 1.0  
**Statut:** ✅ Production Ready
