# Café 216 POS System

Application Point of Sale professionnelle pour Café 216 Express Chicha

## Fonctionnalités

✅ **Écran POS** - Vente rapide avec interface tactile
✅ **Gestion des Produits** - Ajout, édition, suppression
✅ **Historique des Commandes** - Suivi complet
✅ **Rapports** - Statistiques journalières
✅ **Paramètres** - Configuration du restaurant

## Menu Café 216

### Cafés
- Express (25 DT)
- Cappucin (30 DT)
- Direct (25 DT)
- Café Spécial (35 DT)
- Chocolat Chaud (28 DT)
- Américain (25 DT)

### Jus
- Citronade (30 DT)
- Citronade Panachée (35 DT)
- Jus de Saison (32 DT)
- Jwajem (30 DT)

### Chichas
- Quasar (45 DT)
- Kaloud (50 DT)
- Chicha Turc (48 DT)

### Boissons
- Eau 0,5 L (12 DT)
- Eau 1 L (18 DT)
- Eau 1,5 L (25 DT)
- Canette (20 DT)
- Gazouze (22 DT)

### Gâteaux
- Cake (40 DT)
- Croissant (25 DT)
- Mille Feuilles (45 DT)
- Pâté (35 DT)

## Installation

### Depuis l'installer Windows (.exe)
1. Téléchargez `Cafe216_POS_Setup.exe`
2. Double-cliquez pour installer
3. Lancez l'application depuis le menu Démarrer

### Depuis le code source
```bash
# Installation des dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

## Création de l'installer Windows

```bash
# Installation de cx_Freeze
pip install cx_Freeze

# Créer l'installer MSI
python build_installer.py bdist_msi
```

L'installer sera créé dans le dossier `build/msi/`

## Base de Données

- Fichier local: `cafe216_pos.db`
- Format: SQLite3
- Stockage automatique des commandes, paiements et statistiques

## Configuration

- TVA: 20% (configurable dans les paramètres)
- Devises: Dinars Tunisiens (DT)
- Modes de paiement: Espèces, Carte, Chèque

## Support

Pour toute question ou bug, contactez l'équipe Café 216.
