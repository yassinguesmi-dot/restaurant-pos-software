from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QTimer
from src.utils.styles import ModernStyles


class LoginDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.authenticated_user = None
        self.setWindowTitle("Connexion - Café 216")
        self.setFixedSize(450, 600)
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {ModernStyles.PRIMARY}, 
                    stop:1 #8B5CF6);
            }}
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Logo/Brand section
        brand_container = QFrame()
        brand_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 16px;
            }
        """)
        brand_layout = QVBoxLayout(brand_container)
        brand_layout.setContentsMargins(25, 25, 25, 25)
        brand_layout.setSpacing(12)
        
        icon_label = QLabel("☕")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 42px; background: transparent; color: white;")
        brand_layout.addWidget(icon_label)
        
        title = QLabel("CAFE 216")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; background: transparent; letter-spacing: 3px;")
        brand_layout.addWidget(title)

        subtitle = QLabel("Point de Vente")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: transparent;")
        brand_layout.addWidget(subtitle)
        
        layout.addWidget(brand_container)

        # Login form container
        form_container = QFrame()
        form_container.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 16px;
            }}
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(15)

        self.error_label = QLabel("")
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet(f"""
            QLabel {{
                color: {ModernStyles.DANGER}; 
                background: rgba(239, 68, 68, 0.1);
                padding: 10px;
                border-radius: 6px;
                font-size: 11px;
            }}
        """)
        self.error_label.setVisible(False)
        form_layout.addWidget(self.error_label)

        # Username
        username_label = QLabel("Nom d'utilisateur")
        username_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        username_label.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY}; background: transparent;")
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Entrez votre identifiant")
        self.username_input.setFont(QFont("Segoe UI", 11))
        self.username_input.setStyleSheet(ModernStyles.modern_input())
        self.username_input.setMinimumHeight(44)
        form_layout.addWidget(self.username_input)

        # Password
        password_label = QLabel("Mot de passe")
        password_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        password_label.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY}; background: transparent;")
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Entrez votre mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Segoe UI", 11))
        self.password_input.setStyleSheet(ModernStyles.modern_input())
        self.password_input.setMinimumHeight(44)
        form_layout.addWidget(self.password_input)

        # Rôle disponible (optionnel pour l'affichage)
        role_label = QLabel("Rôle")
        role_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        role_label.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY}; background: transparent;")
        form_layout.addWidget(role_label)
        
        self.role_display = QLineEdit()
        self.role_display.setReadOnly(True)
        self.role_display.setPlaceholderText("Rôle détecté automatiquement")
        self.role_display.setFont(QFont("Segoe UI", 11))
        self.role_display.setStyleSheet(f"{ModernStyles.modern_input()}; background-color: rgba(107, 76, 230, 0.1);")
        self.role_display.setMinimumHeight(44)
        form_layout.addWidget(self.role_display)

        form_layout.addSpacing(5)

        # Login button
        login_btn = QPushButton("Se connecter")
        login_btn.setFixedHeight(48)
        login_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        login_btn.setStyleSheet(ModernStyles.large_action_button(ModernStyles.PRIMARY))
        login_btn.clicked.connect(self.authenticate)
        form_layout.addWidget(login_btn)

        # Hint text
        hint_label = QLabel("Par defaut: admin / admin")
        hint_label.setAlignment(Qt.AlignCenter)
        hint_label.setFont(QFont("Segoe UI", 9))
        hint_label.setStyleSheet(f"color: {ModernStyles.TEXT_SECONDARY}; background: transparent; padding: 5px;")
        form_layout.addWidget(hint_label)

        layout.addWidget(form_container)
        layout.addStretch()

        # Soumission via Entrée
        self.username_input.returnPressed.connect(self.authenticate)
        self.password_input.returnPressed.connect(self.authenticate)

    def authenticate(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.show_error("⚠️ Veuillez saisir identifiant et mot de passe.")
            self.role_display.clear()
            return

        user = self.db.verify_user_credentials(username, password)
        if not user:
            self.show_error("❌ Identifiants invalides ou compte inactif.")
            self.role_display.clear()
            return

        # Afficher le rôle avant de valider
        role = user.get('role', 'employé')
        role_display_text = {
            'admin': '👑 Administrateur',
            'gérant': '🎯 Gérant',
            'gestionnaire_produits': '📦 Gestionnaire Produits',
            'gestionnaire_stock': '📊 Gestionnaire Stock',
            'employé': '👤 Employé'
        }.get(role, role)
        
        self.role_display.setText(role_display_text)
        
        # Valider après une courte pause
        QTimer.singleShot(800, lambda: self._complete_authentication(user))

    def _complete_authentication(self, user):
        self.authenticated_user = user
        self.accept()

    def show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.setVisible(True)

