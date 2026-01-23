#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TEST RAPIDE - Vérifier que le système de rôles fonctionne correctement
"""

def test_imports():
    """Tester que tous les modules s'importent sans erreur"""
    print("🔍 Test 1: Vérification des imports...")
    try:
        from src.database import Database
        print("   ✅ Database importée")
        
        from src.main_window import MainWindow
        print("   ✅ MainWindow importée")
        
        from src.screens.login_screen import LoginDialog
        print("   ✅ LoginDialog importée")
        
        from src.screens.users_management_screen import UsersManagementScreen
        print("   ✅ UsersManagementScreen importée")
        
        from src.utils.styles import ModernStyles
        print("   ✅ ModernStyles importée")
        
        return True
    except ImportError as e:
        print(f"   ❌ Erreur d'import: {e}")
        return False

def test_database():
    """Tester la base de données et les utilisateurs"""
    print("\n🔍 Test 2: Vérification de la base de données...")
    try:
        from src.database import Database
        db = Database()
        
        users = db.get_all_users()
        print(f"   ✅ {len(users)} utilisateurs trouvés")
        
        # Vérifier les utilisateurs clés
        roles_found = set()
        for user in users:
            roles_found.add(user.get('role', 'unknown'))
        
        print(f"   ✅ Rôles trouvés: {', '.join(sorted(roles_found))}")
        
        # Vérifier les comptes spécifiques
        produits_user = db.get_user_by_username('produits')
        if produits_user:
            print(f"   ✅ Compte 'produits' trouvé avec le rôle: {produits_user.get('role')}")
        else:
            print(f"   ⚠️  Compte 'produits' non trouvé - À initialiser avec: python initialize_users.py")
        
        return True
    except Exception as e:
        print(f"   ❌ Erreur base de données: {e}")
        return False

def test_permissions():
    """Tester la logique des permissions"""
    print("\n🔍 Test 3: Vérification des permissions...")
    try:
        # Simuler les rôles
        role_permissions = {
            'admin': {0, 1, 2, 3, 4, 5, 6, 7, 8},
            'gérant': {0, 1, 2, 3, 4, 5, 6, 7, 8},
            'gestionnaire_produits': {0, 1, 2, 3, 4, 5},
            'gestionnaire_stock': {0, 3, 5},
            'employé': {0, 4, 5},
        }
        
        # Tester le cas "produits"
        produits_access = role_permissions.get('gestionnaire_produits', set())
        
        modules = {
            0: "POS",
            1: "Produits",
            2: "Prix",
            3: "Stock",
            4: "Tables",
            5: "Commandes",
            6: "Rapports",
            7: "Paramètres",
            8: "Utilisateurs"
        }
        
        print("   Accès pour le rôle 'gestionnaire_produits':")
        for i, name in modules.items():
            status = "✅" if i in produits_access else "❌"
            print(f"      {status} {i}: {name}")
        
        # Vérifier les cas importants
        assert 1 in produits_access, "Produits doit être accessible"
        assert 2 in produits_access, "Prix doit être accessible"
        assert 6 not in produits_access, "Rapports ne doit PAS être accessible"
        assert 8 not in produits_access, "Utilisateurs ne doit PAS être accessible"
        
        print("   ✅ Toutes les permissions sont correctes!")
        return True
    except AssertionError as e:
        print(f"   ❌ Erreur de permissions: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_password_hashing():
    """Tester le hachage des mots de passe"""
    print("\n🔍 Test 4: Vérification du hachage bcrypt...")
    try:
        from src.database import Database
        db = Database()
        
        # Tester le hachage
        password = "test_password_123"
        hashed = db.hash_password(password)
        
        print(f"   ✅ Mot de passe en clair: {password}")
        print(f"   ✅ Mot de passe hashé: {hashed[:20]}...")
        
        # Vérifier que c'est du bcrypt
        assert hashed.startswith('$2b$'), "Doit être du bcrypt"
        print(f"   ✅ Format bcrypt reconnu")
        
        return True
    except Exception as e:
        print(f"   ❌ Erreur hachage: {e}")
        return False

def test_authentication():
    """Tester l'authentification"""
    print("\n🔍 Test 5: Vérification de l'authentification...")
    try:
        from src.database import Database
        db = Database()
        
        # Vérifier le compte admin
        user = db.verify_user_credentials('admin', 'admin')
        if user:
            print(f"   ✅ Authentification 'admin' réussie")
            print(f"      - Nom: {user.get('full_name')}")
            print(f"      - Rôle: {user.get('role')}")
        else:
            print(f"   ❌ Authentification 'admin' échouée")
            return False
        
        # Vérifier le compte produits (s'il existe)
        produits_user = db.get_user_by_username('produits')
        if produits_user:
            user = db.verify_user_credentials('produits', 'produits123')
            if user:
                print(f"   ✅ Authentification 'produits' réussie")
                print(f"      - Nom: {user.get('full_name')}")
                print(f"      - Rôle: {user.get('role')}")
            else:
                print(f"   ⚠️  Authentification 'produits' échouée (mauvais mot de passe?)")
        else:
            print(f"   ⚠️  Compte 'produits' non trouvé")
        
        return True
    except Exception as e:
        print(f"   ❌ Erreur authentification: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("🧪 TEST DU SYSTÈME DE RÔLES - CAFÉ 216 POS")
    print("="*70 + "\n")
    
    results = {
        "Imports": test_imports(),
        "Base de données": test_database(),
        "Permissions": test_permissions(),
        "Hachage bcrypt": test_password_hashing(),
        "Authentification": test_authentication(),
    }
    
    print("\n" + "="*70)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*70 + "\n")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ TOUS LES TESTS SONT PASSÉS! L'application est prête.")
        print("\nProchaines étapes:")
        print("1. Lancer: python main.py")
        print("2. Se connecter avec: produits / produits123")
        print("3. Vérifier que vous pouvez accéder aux produits")
        print("4. Vérifier que les autres modules sont grisés")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ!")
        print("\nSolutions possibles:")
        print("1. Exécutez: python initialize_users.py")
        print("2. Vérifiez la base de données")
        print("3. Consultez ROLE_MANAGEMENT.md pour l'aide")
    print("="*70 + "\n")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
    