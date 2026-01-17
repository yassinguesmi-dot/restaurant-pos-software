# 🎯 INSTRUCTIONS RAPIDES - Build APK sur Linux

## 📦 CE QUE VOUS AVEZ

**Fichier ZIP créé:**
```
C:\Users\yassi\Downloads\restaurant-pos-software (2)\Cafe216_Build_Package.zip
Taille: 0.28 MB
```

---

## 🚀 ÉTAPES SIMPLES

### 1️⃣ SUR VOTRE PC WINDOWS (MAINTENANT)

```powershell
# Le fichier ZIP est déjà créé à:
C:\Users\yassi\Downloads\restaurant-pos-software (2)\Cafe216_Build_Package.zip

# Copiez-le sur une clé USB
```

### 2️⃣ SUR LE PC LINUX

#### A. Préparer
```bash
# Créer dossier
mkdir ~/Cafe216_Build
cd ~/Cafe216_Build

# Copier et extraire
cp /media/VOTRE_CLE_USB/Cafe216_Build_Package.zip .
unzip Cafe216_Build_Package.zip
```

#### B. Installer Buildozer (une seule fois)
```bash
chmod +x install_buildozer_linux.sh
./install_buildozer_linux.sh
```

**Temps:** 5-10 minutes
**Requiert:** Connexion Internet + mot de passe sudo

#### C. Builder les APK
```bash
chmod +x build_both_apk.sh
./build_both_apk.sh
```

**Quand demandé, tapez:** `3` (pour Phone + Tablet)

**Temps:**
- Premier build: 30-60 minutes
- Télécharge Android SDK/NDK automatiquement
- Crée 2 APK

#### D. Récupérer les APK
```bash
# Vérifier
ls -lh bin/

# Copier sur clé USB
cp bin/*.apk /media/VOTRE_CLE_USB/
```

### 3️⃣ DE RETOUR SUR WINDOWS

Les APK sont sur votre clé USB:
- `Cafe216_POS_Phone_v1.0.apk` - Pour téléphone
- `Cafe216_POS_Tablet_v1.0.apk` - Pour tablette

Transférez sur vos appareils Android et installez!

---

## 📋 CHECKLIST ULTRA-RAPIDE

```
[ ] Copier Cafe216_Build_Package.zip sur clé USB
[ ] Aller sur PC Linux avec la clé
[ ] Extraire le ZIP
[ ] ./install_buildozer_linux.sh
[ ] ./build_both_apk.sh
[ ] Taper "3" et ENTER
[ ] Attendre 30-60 min ☕
[ ] Copier bin/*.apk sur clé USB
[ ] Retour chez vous avec les APK
[ ] Installer sur téléphone + tablette
[ ] 🎉 TERMINÉ!
```

---

## ⏱️ TEMPS TOTAL

- **Copier sur clé:** 1 minute
- **Sur Linux:** 45-70 minutes (dont 30-60 min automatique)
- **Installation Android:** 5 minutes

**Total:** ~1 heure (mais vous attendez juste pendant le build)

---

## 💡 OÙ TROUVER UN PC LINUX?

1. **Cyber café** avec Ubuntu/Linux
2. **Ami** qui a Linux
3. **Université/École** - souvent ont des labs Linux
4. **Installer Ubuntu** sur un vieux PC temporairement
5. **Live USB Ubuntu** - boot temporaire sans installer

---

## 🆘 SI PROBLÈME

Tous les détails dans: **`BUILD_LINUX_GUIDE.md`**

---

**C'est parti! 🚀**

---

## 🔧 Scripts fournis

J'ai ajouté deux scripts utiles dans le dossier `scripts/`:

- `scripts/build_apk.sh` — lance `buildozer android debug` depuis la racine du projet et affiche le chemin de l'APK construit.
- `scripts/deploy_apk_adb.sh` — installe un APK sur un appareil Android connecté via `adb` (USB ou Wi‑Fi).

Rendez-les exécutables et utilisez-les ainsi (exemples pour Ubuntu/WSL):

```bash
# depuis la racine du projet
chmod +x scripts/*.sh
./scripts/build_apk.sh

# après la construction (ou avec le chemin vers l'APK)
./scripts/deploy_apk_adb.sh bin/your_app-debug.apk

# pour installer via Wi‑Fi (sur la tablette exécuter dans un terminal Android: `adb tcpip 5555` ou activer le debug réseau)
adb connect 192.168.x.y
./scripts/deploy_apk_adb.sh
```

Notes:
- Assurez-vous d'avoir `buildozer` et `adb` installés dans l'environnement Linux/WSL.
- Si `adb` n'est pas installé sur Ubuntu: `sudo apt update && sudo apt install -y android-tools-adb`.

Souhaitez-vous que je rende ces scripts plus avancés (ex: signature release, choose archs, upload to Google Drive)?
