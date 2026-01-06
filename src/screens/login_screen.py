from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class LoginDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.authenticated_user = None
        self.setWindowTitle("Connexion")
        self.setFixedSize(360, 240)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Café 216 - Connexion")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #D32F2F;")
        self.error_label.setVisible(False)
        layout.addWidget(self.error_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setFont(QFont("Arial", 11))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Arial", 11))
        layout.addWidget(self.password_input)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        login_btn = QPushButton("Se connecter")
        login_btn.setFixedHeight(42)
        login_btn.setFont(QFont("Arial", 11, QFont.Bold))
        login_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #C8A882;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 14px;
            }
            QPushButton:hover { background-color: #B8985F; }
            """
        )
        login_btn.clicked.connect(self.authenticate)
        buttons_layout.addWidget(login_btn)
        layout.addLayout(buttons_layout)

        # Soumission via Entrée
        self.username_input.returnPressed.connect(self.authenticate)
        self.password_input.returnPressed.connect(self.authenticate)

    def authenticate(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.show_error("Veuillez saisir identifiant et mot de passe.")
            return

        user = self.db.verify_user_credentials(username, password)
        if not user:
            self.show_error("Identifiants invalides ou compte inactif.")
            return

        self.authenticated_user = user
        self.accept()

    def show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.setVisible(True)

