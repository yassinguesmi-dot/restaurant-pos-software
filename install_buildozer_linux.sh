#!/bin/bash
# Installation rapide de Buildozer sur Linux/Ubuntu
# Exécuter ce script en premier sur le PC Linux

echo "================================================"
echo "  Installation Buildozer pour Cafe216 POS"
echo "================================================"
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Vérifier qu'on est sur Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}Erreur: Ce script doit être exécuté sur Linux${NC}"
    exit 1
fi

echo -e "${YELLOW}1. Mise à jour du système...${NC}"
sudo apt-get update

echo ""
echo -e "${YELLOW}2. Installation des dépendances système...${NC}"
sudo apt-get install -y \
    python3 \
    python3-pip \
    git \
    zip \
    unzip \
    openjdk-11-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    build-essential

if [ $? -ne 0 ]; then
    echo -e "${RED}Erreur lors de l'installation des dépendances${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}3. Installation de Buildozer et Cython...${NC}"
pip3 install --upgrade pip
pip3 install --upgrade buildozer
pip3 install cython==0.29.33

if [ $? -ne 0 ]; then
    echo -e "${RED}Erreur lors de l'installation de Buildozer${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}4. Vérification de l'installation...${NC}"
buildozer --version

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}  ✓ Installation réussie!${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    echo -e "${BLUE}Prochaine étape:${NC}"
    echo "  1. Copiez le dossier du projet ici"
    echo "  2. cd dans le dossier"
    echo "  3. chmod +x build_both_apk.sh"
    echo "  4. ./build_both_apk.sh"
    echo ""
else
    echo -e "${RED}Erreur: Buildozer n'est pas installé correctement${NC}"
    exit 1
fi
