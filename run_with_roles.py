#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DÉMARRAGE RAPIDE - Système de Rôles Café 216 POS

Ce script gère le démarrage complet avec initialisation des utilisateurs.
"""

import sys
import os

def main():
    print("\n" + "="*70)
    print("🎯 CAFÉ 216 POS - DÉMARRAGE AVEC SYSTÈME DE RÔLES")
    print("="*70)
    
    # Vérifier si les utilisateurs existent
    from src.database import Database
    db = Database()
    
    users = db.get_all_users()
    
    if len(users) < 2:
        print("\n⚠️  Aucun utilisateur trouvé dans la base de données.")
        print("📝 Exécution de l'initialisation des utilisateurs...")
        print("-"*70)
        
        import initialize_users
        initialize_users.initialize_test_users()
        
        print("\n✅ Initialisation terminée!")
    else:
        print(f"\n✅ {len(users)} utilisateurs trouvés en base de données")
    
    print("\n" + "="*70)
    print("🔐 COMPTES DE TESTE RAPIDES")
    print("="*70)
    
    test_accounts = [
        ("👑 Admin", "admin", "admin", "Accès complet"),
        ("🎯 Gérant", "gerant", "gerant123", "Accès complet"),
        ("📦 Produits", "produits", "produits123", "Gestion produits/prix/stock"),
        ("📊 Stock", "stock", "stock123", "Gestion du stock uniquement"),
        ("👤 Employé", "employe1", "employe123", "Vente et tables"),
    ]
    
    print("\n")
    for role, username, password, access in test_accounts:
        print(f"{role:20} | {username:12} | {password:15} | {access}")
    
    print("\n" + "="*70)
    print("🚀 DÉMARRAGE DE L'APPLICATION")
    print("="*70)
    print("\nLancement de l'interface graphique...")
    print("Veuillez vous connecter avec l'un des comptes ci-dessus.\n")
    
    # Lancer l'application
    from src.database import Database
    from PyQt5.QtWidgets import QApplication
    from src.screens.login_screen import LoginDialog
    from src.main_window import MainWindow
    
    app = QApplication(sys.argv)
    db = Database()
    
    # Afficher le dialogue de login
    login_dialog = LoginDialog(db)
    
    if login_dialog.exec_() == login_dialog.Accepted:
        user = login_dialog.authenticated_user
        print(f"\n✅ Connexion réussie: {user['full_name']} ({user['role']})")
        
        # Ouvrir la fenêtre principale
        main_window = MainWindow(db, user)
        main_window.show()
        
        sys.exit(app.exec_())
    else:
        print("\n❌ Connexion annulée")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
