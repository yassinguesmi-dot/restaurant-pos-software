#!/bin/bash
# Script de build APK pour téléphone ET tablette
# À exécuter dans WSL Ubuntu

echo "================================================"
echo "  Cafe216 POS - Build APK Phone + Tablet"
echo "================================================"
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Vérifier qu'on est dans le bon répertoire
if [ ! -f "main_kivy.py" ]; then
    echo -e "${RED}Erreur: main_kivy.py introuvable${NC}"
    echo "Exécutez ce script depuis le dossier du projet"
    exit 1
fi

# Fonction de build
build_apk() {
    local TYPE=$1
    local SPEC_FILE=$2
    local OUTPUT_NAME=$3
    
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  Building: ${OUTPUT_NAME}${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
    
    # Clean build
    echo -e "${YELLOW}Nettoyage des fichiers de build précédents...${NC}"
    rm -rf .buildozer
    rm -rf bin
    
    # Build
    echo -e "${YELLOW}Lancement du build (peut prendre 30-60 min)...${NC}"
    buildozer -v android debug --spec="${SPEC_FILE}"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Build réussi pour ${OUTPUT_NAME}!${NC}"
        
        # Renommer l'APK
        if [ -d "bin" ]; then
            APK_FILE=$(find bin -name "*.apk" | head -n 1)
            if [ -n "$APK_FILE" ]; then
                NEW_NAME="bin/${OUTPUT_NAME}.apk"
                mv "$APK_FILE" "$NEW_NAME"
                echo -e "${GREEN}APK créé: ${NEW_NAME}${NC}"
                ls -lh "$NEW_NAME"
            fi
        fi
        return 0
    else
        echo -e "${RED}✗ Échec du build pour ${OUTPUT_NAME}${NC}"
        return 1
    fi
}

# Menu de sélection
echo -e "${YELLOW}Que voulez-vous builder?${NC}"
echo "  1) Téléphone (Portrait)"
echo "  2) Tablette (Landscape)"
echo "  3) Les deux"
echo ""
read -p "Choix [1-3]: " CHOICE

case $CHOICE in
    1)
        echo -e "${BLUE}Build pour TÉLÉPHONE uniquement${NC}"
        build_apk "phone" "buildozer_phone.spec" "Cafe216_POS_Phone_v1.0"
        ;;
    2)
        echo -e "${BLUE}Build pour TABLETTE uniquement${NC}"
        build_apk "tablet" "buildozer_tablet.spec" "Cafe216_POS_Tablet_v1.0"
        ;;
    3)
        echo -e "${BLUE}Build pour TÉLÉPHONE et TABLETTE${NC}"
        echo ""
        
        # Build Phone
        build_apk "phone" "buildozer_phone.spec" "Cafe216_POS_Phone_v1.0"
        PHONE_STATUS=$?
        
        echo ""
        echo -e "${YELLOW}Pause de 10 secondes avant le build tablette...${NC}"
        sleep 10
        
        # Build Tablet
        build_apk "tablet" "buildozer_tablet.spec" "Cafe216_POS_Tablet_v1.0"
        TABLET_STATUS=$?
        
        # Résumé
        echo ""
        echo -e "${BLUE}================================================${NC}"
        echo -e "${BLUE}  RÉSUMÉ DES BUILDS${NC}"
        echo -e "${BLUE}================================================${NC}"
        if [ $PHONE_STATUS -eq 0 ]; then
            echo -e "${GREEN}✓ Téléphone: Réussi${NC}"
        else
            echo -e "${RED}✗ Téléphone: Échoué${NC}"
        fi
        
        if [ $TABLET_STATUS -eq 0 ]; then
            echo -e "${GREEN}✓ Tablette: Réussi${NC}"
        else
            echo -e "${RED}✗ Tablette: Échoué${NC}"
        fi
        ;;
    *)
        echo -e "${RED}Choix invalide${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  TERMINÉ!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# Liste des APK créés
if [ -d "bin" ]; then
    echo -e "${YELLOW}APK créés:${NC}"
    ls -lh bin/*.apk 2>/dev/null || echo "Aucun APK trouvé"
fi

echo ""
echo -e "${BLUE}Pour installer sur Android:${NC}"
echo "  1. Copiez l'APK sur votre appareil"
echo "  2. Ouvrez l'APK sur l'appareil"
echo "  3. Autorisez l'installation depuis sources inconnues"
echo "  4. Installez!"
echo ""
