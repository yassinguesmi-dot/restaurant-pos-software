"""
Script pour initialiser les utilisateurs avec différents rôles.
À exécuter une fois pour configurer les comptes de test.
"""

import sys
sys.path.insert(0, '.')

from src.database import Database

def initialize_test_users():
    """Initialise les utilisateurs de test avec leurs rôles respectifs"""
    db = Database()
    
    test_users = [
        {
            'username': 'admin',
            'password': 'admin',
            'full_name': 'Administrateur',
            'role': 'admin'
        },
        {
            'username': 'gerant',
            'password': 'gerant123',
            'full_name': 'Gérant Principal',
            'role': 'gérant'
        },
        {
            'username': 'produits',
            'password': 'produits123',
            'full_name': 'Gestionnaire Produits',
            'role': 'gestionnaire_produits'
        },
        {
            'username': 'stock',
            'password': 'stock123',
            'full_name': 'Gestionnaire Stock',
            'role': 'gestionnaire_stock'
        },
        {
            'username': 'employe1',
            'password': 'employe123',
            'full_name': 'Jean Dupont',
            'role': 'employé'
        },
        {
            'username': 'employe2',
            'password': 'employe123',
            'full_name': 'Marie Martin',
            'role': 'employé'
        }
    ]
    
    for user in test_users:
        try:
            # Vérifier si l'utilisateur existe
            existing = db.get_user_by_username(user['username'])
            
            if existing:
                print(f"✅ Utilisateur '{user['username']}' existe déjà (Rôle: {user['role']})")
            else:
                # Créer le nouvel utilisateur
                hashed_password = db.hash_password(user['password'])
                cursor = db.connection.cursor()
                
                cursor.execute('''
                    INSERT INTO users (username, password, full_name, role, is_active)
                    VALUES (?, ?, ?, ?, 1)
                ''', (user['username'], hashed_password, user['full_name'], user['role']))
                
                db.connection.commit()
                print(f"✅ Utilisateur '{user['username']}' créé avec le rôle: {user['role']}")
                
        except Exception as e:
            print(f"❌ Erreur lors de la création de '{user['username']}': {e}")
    
    print("\n" + "="*60)
    print("📋 ACCÈS PAR RÔLE:")
    print("="*60)
    
    roles_access = {
        'admin': ['✅ POS', '✅ Produits', '✅ Prix', '✅ Stock', '✅ Tables', '✅ Commandes', '✅ Rapports', '✅ Paramètres'],
        'gérant': ['✅ POS', '✅ Produits', '✅ Prix', '✅ Stock', '✅ Tables', '✅ Commandes', '✅ Rapports', '✅ Paramètres'],
        'gestionnaire_produits': ['✅ POS', '✅ Produits', '✅ Prix', '✅ Stock', '✅ Tables', '✅ Commandes', '❌ Rapports', '❌ Paramètres'],
        'gestionnaire_stock': ['✅ POS', '❌ Produits', '❌ Prix', '✅ Stock', '❌ Tables', '✅ Commandes', '❌ Rapports', '❌ Paramètres'],
        'employé': ['✅ POS', '❌ Produits', '❌ Prix', '❌ Stock', '✅ Tables', '✅ Commandes', '❌ Rapports', '❌ Paramètres']
    }
    
    for role, access in roles_access.items():
        print(f"\n👤 {role.upper()}")
        for feature in access:
            print(f"   {feature}")
    
    print("\n" + "="*60)
    print("🔐 COMPTES DE TEST CRÉÉS:")
    print("="*60)
    for user in test_users:
        print(f"Username: {user['username']} | Password: {user['password']} | Rôle: {user['role']}")

if __name__ == '__main__':
    print("\n🔧 Initialisation des utilisateurs de test...\n")
    initialize_test_users()
    print("\n✅ Initialisation terminée!")
