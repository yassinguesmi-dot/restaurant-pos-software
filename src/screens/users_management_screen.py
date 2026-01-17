"""
Écran de gestion des utilisateurs (réservé aux administrateurs)
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.utils.styles import ModernStyles

class UsersManagementScreen(QWidget):
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        
        # Vérifier les permissions
        if current_user['role'] not in ['admin', 'gérant']:
            self.init_error_ui()
        else:
            self.init_ui()
    
    def init_error_ui(self):
        """Afficher un message d'erreur si non autorisé"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        
        error_label = QLabel("🔒 Accès Refusé")
        error_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        error_label.setStyleSheet(f"color: {ModernStyles.DANGER};")
        layout.addWidget(error_label)
        
        message = QLabel("Seuls les administrateurs et gérants peuvent accéder à la gestion des utilisateurs.")
        message.setFont(QFont("Segoe UI", 12))
        message.setStyleSheet(f"color: {ModernStyles.TEXT_SECONDARY};")
        message.setWordWrap(True)
        layout.addWidget(message)
        
        layout.addStretch()
    
    def init_ui(self):
        """Interface de gestion des utilisateurs"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Titre
        title = QLabel("👥 Gestion des Utilisateurs")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        # Sous-titre
        subtitle = QLabel("Gérez les accès et les rôles des utilisateurs")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet(f"color: {ModernStyles.TEXT_SECONDARY};")
        layout.addWidget(subtitle)
        
        # Boutons d'action
        action_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Ajouter un utilisateur")
        add_btn.setFixedHeight(40)
        add_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        add_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.SUCCESS))
        add_btn.clicked.connect(self.add_user)
        action_layout.addWidget(add_btn)
        
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.setFixedHeight(40)
        refresh_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        refresh_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.INFO))
        refresh_btn.clicked.connect(self.load_users)
        action_layout.addWidget(refresh_btn)
        
        action_layout.addStretch()
        layout.addLayout(action_layout)
        
        # Tableau des utilisateurs
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels(["ID", "Utilisateur", "Nom Complet", "Rôle", "Actions"])
        self.users_table.setStyleSheet(ModernStyles.modern_table())
        self.users_table.setAlternatingRowColors(True)
        layout.addWidget(self.users_table)
        
        # Charger les utilisateurs au démarrage
        self.load_users()
    
    def load_users(self):
        """Charger tous les utilisateurs"""
        try:
            users = self.db.get_all_users()
            self.users_table.setRowCount(len(users))
            
            for i, user in enumerate(users):
                # ID
                id_item = QTableWidgetItem(str(user.get('id', '')))
                self.users_table.setItem(i, 0, id_item)
                
                # Username
                username_item = QTableWidgetItem(user.get('username', ''))
                self.users_table.setItem(i, 1, username_item)
                
                # Full Name
                name_item = QTableWidgetItem(user.get('full_name', ''))
                self.users_table.setItem(i, 2, name_item)
                
                # Role with emoji
                role = user.get('role', 'employé')
                role_emoji = {
                    'admin': '👑',
                    'gérant': '🎯',
                    'gestionnaire_produits': '📦',
                    'gestionnaire_stock': '📊',
                    'employé': '👤'
                }.get(role, '•')
                role_item = QTableWidgetItem(f"{role_emoji} {role}")
                self.users_table.setItem(i, 3, role_item)
                
                # Actions
                action_item = QTableWidgetItem("✏️ Modifier")
                self.users_table.setItem(i, 4, action_item)
            
            # Auto-fit columns
            self.users_table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def add_user(self):
        """Ouvrir le dialogue pour ajouter un utilisateur"""
        dialog = AddUserDialog(self.db, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users()
            QMessageBox.information(self, "Succès", "Utilisateur créé avec succès!")


class AddUserDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Ajouter un utilisateur")
        self.setFixedSize(400, 350)
        self.setStyleSheet(f"background-color: white;")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Username
        layout.addWidget(QLabel("Nom d'utilisateur:"))
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet(ModernStyles.modern_input())
        self.username_input.setMinimumHeight(40)
        layout.addWidget(self.username_input)
        
        # Full Name
        layout.addWidget(QLabel("Nom complet:"))
        self.fullname_input = QLineEdit()
        self.fullname_input.setStyleSheet(ModernStyles.modern_input())
        self.fullname_input.setMinimumHeight(40)
        layout.addWidget(self.fullname_input)
        
        # Password
        layout.addWidget(QLabel("Mot de passe:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(ModernStyles.modern_input())
        self.password_input.setMinimumHeight(40)
        layout.addWidget(self.password_input)
        
        # Role
        layout.addWidget(QLabel("Rôle:"))
        self.role_combo = QComboBox()
        self.role_combo.addItems(['employé', 'gestionnaire_stock', 'gestionnaire_produits', 'gérant', 'admin'])
        self.role_combo.setStyleSheet(ModernStyles.modern_input())
        self.role_combo.setMinimumHeight(40)
        layout.addWidget(self.role_combo)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.TEXT_SECONDARY))
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Créer")
        save_btn.setMinimumHeight(40)
        save_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.SUCCESS))
        save_btn.clicked.connect(self.create_user)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
    
    def create_user(self):
        username = self.username_input.text().strip()
        fullname = self.fullname_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()
        
        if not username or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
            return
        
        try:
            # Vérifier si l'utilisateur existe
            existing = self.db.get_user_by_username(username)
            if existing:
                QMessageBox.warning(self, "Erreur", "Cet utilisateur existe déjà")
                return
            
            # Créer le nouvel utilisateur
            hashed_password = self.db.hash_password(password)
            cursor = self.db.connection.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, password, full_name, role, is_active)
                VALUES (?, ?, ?, ?, 1)
            ''', (username, hashed_password, fullname, role))
            
            self.db.connection.commit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la création: {str(e)}")
