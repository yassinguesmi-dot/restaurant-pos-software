# Café 216 POS System

Application Point of Sale professionnelle pour Café 216 Express Chicha

## 📱 Disponible sur

- 🪟 **Windows** - Desktop application (PyQt5)
- 🤖 **Android** - APK pour tablettes (Kivy)
- 🍎 **iOS** - En développement

## Fonctionnalités

✅ **Écran POS** - Vente rapide avec interface tactile
✅ **Gestion des Produits** - Ajout, édition, suppression
✅ **Historique des Commandes** - Suivi complet
✅ **Rapports** - Statistiques journalières
✅ **Paramètres** - Configuration du restaurant
✅ **Multi-plateforme** - Windows et Android

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

### 🤖 Android APK

**Quick Start:**
```bash
# In WSL/Ubuntu terminal
cd /mnt/c/Users/yassi/Downloads/restaurant-pos-software\ \(2\)/restaurant-pos-software\ \(1\)/
./build_apk.sh
```

**Documentation complète:**
- 📖 [Quick Start Guide](QUICKSTART.md) - Build en 5 minutes
- 📖 [APK Build Guide](APK_BUILD_GUIDE.md) - Guide détaillé
- 📋 [Build Checklist](BUILD_CHECKLIST.md) - Vérifications avant build

### 🪟 Windows Desktop (.exe)
1. Téléchargez `Cafe216_POS_Setup.exe`
2. Double-cliquez pour installer
3. Lancez l'application depuis le menu Démarrer

### 💻 Depuis le code source
```bash
# Installation des dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

## 🔨 Build Instructions

### Windows Desktop
```bash
# Installation de cx_Freeze
pip install cx_Freeze

# Créer l'installer MSI
python build_installer.py bdist_msi
```

### Android APK
```bash
# Méthode 1: Script automatisé
chmod +x build_apk.sh
./build_apk.sh

# Méthode 2: Buildozer manuel
buildozer -v android debug
```

Voir [APK_BUILD_GUIDE.md](APK_BUILD_GUIDE.md) pour plus de détails.

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
