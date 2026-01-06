"""
Script pour créer l'executable Windows pour Café 216 POS
Exécutez : python build_installer.py
"""
import PyInstaller.__main__
import os
import sys

# Déterminer le dossier du projet
project_dir = os.path.dirname(os.path.abspath(__file__))

# Configuration PyInstaller
args = [
    os.path.join(project_dir, 'main.py'),
    '--name=Cafe216_POS',
    '--onefile',
    '--windowed',
    '--add-data=src:src',
    '--hidden-import=PyQt5.sip',
    '--hidden-import=sqlite3',
    '--collect-all=PyQt5',
]

# Lancer PyInstaller
PyInstaller.__main__.run(args)

print('\nEXECUTABLE CRÉÉ AVEC SUCCÈS!')
print(f'Fichier : {os.path.join(project_dir, "dist", "Cafe216_POS.exe")}')
