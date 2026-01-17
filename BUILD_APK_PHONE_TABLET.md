# 📱 Guide de Build APK - Téléphone & Tablette

## 🎯 2 Versions Disponibles

### Version Téléphone (Portrait)
- **Orientation:** Portrait (vertical)
- **Optimisé pour:** Smartphones 720x1280+
- **Package:** `cafe216posphone`
- **Fichier:** `buildozer_phone.spec`

### Version Tablette (Landscape)
- **Orientation:** Landscape (horizontal)  
- **Optimisé pour:** Tablettes 1280x800+
- **Package:** `cafe216postablet`
- **Fichier:** `buildozer_tablet.spec`

---

## ⚡ Build Rapide (Méthode Recommandée)

### Option 1: Avec WSL (Windows)

```powershell
# Dans PowerShell Windows
wsl --shutdown
wsl -d Ubuntu-22.04

# Puis dans Ubuntu WSL:
cd "/mnt/c/Users/yassi/Downloads/restaurant-pos-software (2)/restaurant-pos-software (1)"
chmod +x build_both_apk.sh
./build_both_apk.sh
```

Le script vous demandera:
```
Que voulez-vous builder?
  1) Téléphone (Portrait)
  2) Tablette (Landscape)  
  3) Les deux

Choix [1-3]: 3
```

### Option 2: Build Manuel

**Pour Téléphone:**
```bash
buildozer android debug --spec=buildozer_phone.spec
```

**Pour Tablette:**
```bash
buildozer android debug --spec=buildozer_tablet.spec
```

---

## 🔧 Si WSL Ne Fonctionne Pas

### Alternative 1: Linux natif / Mac

```bash
# Installer buildozer
pip install buildozer

# Build
cd restaurant-pos-software\ (1)
./build_both_apk.sh
```

### Alternative 2: Machine Virtuelle

1. Installer VirtualBox
2. Créer VM Ubuntu 22.04
3. Installer buildozer dans la VM
4. Copier les fichiers du projet
5. Lancer le build

### Alternative 3: GitHub Actions (Cloud Build)

1. Push le projet sur GitHub
2. Le build se fait automatiquement dans le cloud
3. Télécharger les APK depuis GitHub Releases

---

## 📦 Fichiers Générés

Après le build, vous trouverez dans `bin/`:

```
bin/
├── Cafe216_POS_Phone_v1.0.apk     (~40-60 MB)
└── Cafe216_POS_Tablet_v1.0.apk    (~40-60 MB)
```

---

## 📲 Installation sur Android

### Téléphone
1. Transférer `Cafe216_POS_Phone_v1.0.apk` sur votre téléphone
2. Ouvrir le fichier
3. Autoriser "Sources inconnues" si demandé
4. Installer

### Tablette
1. Transférer `Cafe216_POS_Tablet_v1.0.apk` sur votre tablette
2. Ouvrir le fichier
3. Autoriser "Sources inconnues" si demandé
4. Installer

---

## ⚙️ Différences Techniques

| Caractéristique | Téléphone | Tablette |
|-----------------|-----------|----------|
| Orientation | Portrait | Landscape |
| Taille écran min | 720x1280 | 1280x800 |
| Package name | cafe216posphone | cafe216postablet |
| Interface | Adaptée petits écrans | Adaptée grands écrans |

---

## 🐛 Dépannage

### Erreur WSL
```powershell
# Redémarrer WSL
wsl --shutdown
wsl --update

# Vérifier
wsl -l -v
```

### Build échoue
```bash
# Nettoyer et réessayer
rm -rf .buildozer bin
buildozer android clean
buildozer -v android debug --spec=buildozer_phone.spec
```

### Manque de dépendances Ubuntu
```bash
sudo apt update
sudo apt install -y python3-pip build-essential git zip unzip openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --upgrade buildozer cython==0.29.33
```

---

## 🚀 Prochaines Étapes

Après avoir créé les APK:

1. ✅ Tester sur un téléphone Android réel
2. ✅ Tester sur une tablette Android réelle
3. ✅ Vérifier que toutes les fonctionnalités marchent
4. ✅ Ajuster les tailles si nécessaire
5. 🎉 Déployer!

---

## 💡 Astuces

- **Premier build:** Prend 30-60 minutes (télécharge SDK/NDK)
- **Builds suivants:** 5-10 minutes seulement
- **Espace disque:** Besoin de ~5GB pour les outils Android
- **RAM:** Minimum 4GB recommandé
- **Internet:** Requis pour le premier build

---

**Date:** 12 janvier 2026  
**Version:** 1.0.0
