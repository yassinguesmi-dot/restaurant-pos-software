# 📦 BUILD APK SUR PC LINUX - Guide Complet

## 🎯 Ce dont vous avez besoin

- **PC Linux** (Ubuntu 20.04+ recommandé) ou Mac
- **Clé USB** (minimum 1 GB)
- **Internet** sur le PC Linux
- **30-60 minutes** pour le premier build

---

## 📋 ÉTAPE 1: Préparer le Package (Sur Windows)

### A. Créer l'archive ZIP

```powershell
# Dans PowerShell sur votre PC Windows
cd "C:\Users\yassi\Downloads\restaurant-pos-software (2)"

# Créer l'archive (peut prendre 2-3 minutes)
Compress-Archive -Path "restaurant-pos-software (1)\*" -DestinationPath "Cafe216_Build_Package.zip" -Force
```

### B. Copier sur clé USB

1. Brancher votre clé USB
2. Copier `Cafe216_Build_Package.zip` sur la clé
3. Le fichier fait environ **200-300 MB**

---

## 🖥️ ÉTAPE 2: Sur le PC Linux

### A. Copier les fichiers

```bash
# Créer un dossier de travail
mkdir -p ~/Cafe216_Build
cd ~/Cafe216_Build

# Copier depuis la clé USB (adapter le chemin)
cp /media/USB_NAME/Cafe216_Build_Package.zip .

# Extraire
unzip Cafe216_Build_Package.zip
```

### B. Installer Buildozer (Une seule fois)

```bash
# Rendre le script exécutable
chmod +x install_buildozer_linux.sh

# Lancer l'installation (prend 5-10 minutes)
./install_buildozer_linux.sh
```

**Note:** Le script va demander votre mot de passe sudo pour installer les dépendances système.

---

## 🚀 ÉTAPE 3: Build des APK

### Option A: Build Automatique (Les 2 versions)

```bash
# Rendre le script exécutable
chmod +x build_both_apk.sh

# Lancer le build
./build_both_apk.sh

# Quand on vous demande, tapez: 3
# Pour builder Téléphone + Tablette
```

**Temps estimé:** 
- Premier build: 30-60 minutes
- Builds suivants: 5-10 minutes

### Option B: Build Manuel

**Pour Téléphone (Portrait):**
```bash
buildozer android debug --spec=buildozer_phone.spec
```

**Pour Tablette (Landscape):**
```bash
# Nettoyer avant
rm -rf .buildozer

# Build
buildozer android debug --spec=buildozer_tablet.spec
```

---

## 📲 ÉTAPE 4: Récupérer les APK

### A. Localiser les fichiers

Les APK seront dans le dossier `bin/`:

```bash
ls -lh bin/
```

Vous devriez voir:
```
Cafe216_POS_Phone_v1.0.apk     (~45-60 MB)
Cafe216_POS_Tablet_v1.0.apk    (~45-60 MB)
```

### B. Copier sur clé USB

```bash
# Copier sur clé USB
cp bin/*.apk /media/USB_NAME/
```

Ou utiliser l'interface graphique pour glisser-déposer.

---

## 📱 ÉTAPE 5: Installation sur Android

### A. Transférer les APK

1. Brancher la clé USB sur votre PC
2. Connecter le téléphone/tablette Android via USB
3. Copier l'APK approprié sur l'appareil

**Ou via email/cloud:**
- Envoyez-vous l'APK par email
- Téléchargez depuis Google Drive/Dropbox

### B. Installer

**Sur Téléphone:**
1. Ouvrir `Cafe216_POS_Phone_v1.0.apk`
2. Autoriser "Sources inconnues" si demandé
3. Installer
4. Lancer l'application

**Sur Tablette:**
1. Ouvrir `Cafe216_POS_Tablet_v1.0.apk`
2. Autoriser "Sources inconnues" si demandé
3. Installer
4. Lancer l'application

---

## 🔧 Dépannage

### Erreur: "buildozer: command not found"

```bash
# Ajouter au PATH
export PATH=$PATH:~/.local/bin

# Ou réinstaller
pip3 install --user buildozer
```

### Erreur: "SDK license not accepted"

```bash
# Dans buildozer.spec, vérifier:
android.accept_sdk_license = True
```

### Build échoue avec erreur Java

```bash
# Vérifier Java
java -version

# Doit être Java 11
# Si différent:
sudo apt install openjdk-11-jdk
sudo update-alternatives --config java
```

### Manque d'espace disque

```bash
# Vérifier l'espace
df -h

# Buildozer nécessite ~5GB libres
# Nettoyer si besoin:
rm -rf ~/.buildozer/android/platform/build-*
```

### Internet lent/coupé

Le premier build télécharge:
- Android SDK (~500 MB)
- Android NDK (~800 MB)
- Python-for-android (~200 MB)

**Solution:** Utiliser une bonne connexion Internet ou laisser tourner toute la nuit.

---

## 📊 Timeline Typique

| Étape | Temps |
|-------|-------|
| Copier sur clé USB | 2 min |
| Extraire sur Linux | 1 min |
| Installer buildozer | 5-10 min |
| Premier build Phone | 30-45 min |
| Build Tablet | 5-10 min |
| Copier les APK | 2 min |
| **TOTAL** | **45-70 min** |

---

## ✅ Checklist

### Avant de partir de chez vous:
- [ ] Créé `Cafe216_Build_Package.zip`
- [ ] Copié sur clé USB
- [ ] Clé USB avec vous

### Sur le PC Linux:
- [ ] Copié et extrait le ZIP
- [ ] Exécuté `install_buildozer_linux.sh`
- [ ] Lancé `build_both_apk.sh`
- [ ] Sélectionné option 3 (les deux)
- [ ] Attendu la fin du build
- [ ] Copié les APK sur clé USB

### De retour chez vous:
- [ ] Transféré APK sur téléphone
- [ ] Installé version Phone
- [ ] Transféré APK sur tablette
- [ ] Installé version Tablet
- [ ] Testé les 2 versions
- [ ] 🎉 Succès!

---

## 💡 Conseils Pratiques

### Pour gagner du temps:
1. **Cyber café Linux:** Cherchez un cyber avec Ubuntu/Linux
2. **Ami avec Linux:** Demandez 1h sur son PC
3. **Live USB Ubuntu:** Bootez temporairement en Linux depuis USB

### Pour éviter les erreurs:
1. **Bonne connexion Internet** pour le premier build
2. **Ne pas interrompre** pendant le téléchargement SDK/NDK
3. **Au moins 5GB libres** sur le disque
4. **Patience** - le premier build est long mais normal

### Alternative rapide:
Si vraiment pas d'accès Linux, utilisez **Replit.com** (voir SOLUTION_BUILD_APK.md)

---

## 🆘 Besoin d'Aide?

### Erreurs communes et solutions:

**"Permission denied"**
```bash
chmod +x *.sh
```

**"pip: command not found"**
```bash
sudo apt install python3-pip
```

**"Java version wrong"**
```bash
sudo update-alternatives --config java
# Sélectionner Java 11
```

---

## 📞 Support

Si vous êtes bloqué sur le PC Linux:
1. Notez le message d'erreur exact
2. Prenez une photo de l'écran
3. Regardez `APK_BUILD_GUIDE.md` pour plus de détails

---

**Bonne chance! Le résultat en vaut la peine! 🚀**

Date: 12 janvier 2026
