from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QStackedWidget, QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QPixmap
from src.screens.pos_screen import POSScreen
from src.screens.products_screen import ProductsScreen
from src.screens.orders_screen import OrdersScreen
from src.screens.reports_screen import ReportsScreen
from src.screens.settings_screen import SettingsScreen
from src.screens.price_management_screen import PriceManagementScreen
from src.screens.stock_management_screen import StockManagementScreen
from src.screens.tables_screen import TablesScreen
from src.screens.users_management_screen import UsersManagementScreen
from src.database import Database
from src.utils.styles import ModernStyles
import os

class MainWindow(QMainWindow):
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        
        # Définir les permissions par rôle
        # Rôles: admin, gérant, employé, gestionnaire_stock, gestionnaire_produits
        role = current_user['role'] if current_user else 'employé'
        
        # Définir les indices accessibles selon le rôle
        # 0=POS, 1=Produits, 2=Prix, 3=Stock, 4=Tables, 5=Commandes, 6=Rapports, 7=Paramètres, 8=Utilisateurs
        self.role_permissions = {
            'admin': {0, 1, 2, 3, 4, 5, 6, 7, 8},  # Accès complet
            'gérant': {0, 1, 2, 3, 4, 5, 6, 7, 8},  # Accès complet
            'gestionnaire_produits': {0, 1, 2, 3, 4, 5},  # POS, Produits, Prix, Stock, Tables, Commandes
            'gestionnaire_stock': {0, 3, 5},  # POS, Stock, Commandes
            'employé': {0, 4, 5},  # POS, Tables, Commandes
        }
        
        self.allowed_indices = self.role_permissions.get(role, {0})
        self.init_ui()
        self.setWindowTitle("Café 216 - POS System")
        self.setGeometry(0, 0, 1400, 900)
        self.showMaximized()

    def init_ui(self):
        self.primary_color = "#C8A882"  # Warm beige/coffee
        self.secondary_color = "#2C2C2C"  # Dark charcoal
        self.accent_color = "#D4A574"  # Gold accent
        self.background_color = "#F8F6F3"  # Off-white
        
        # Set modern window styling
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {ModernStyles.LIGHT_BG};
            }}
        """)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal (sidebar + contenu)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar de navigation
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar, 0)
        
        # Stack widget pour les écrans
        self.stacked_widget = QStackedWidget()
        
        self.pos_screen = POSScreen(self.db, self.current_user)
        self.products_screen = ProductsScreen(self.db)
        self.price_management_screen = PriceManagementScreen(self.db)
        self.stock_management_screen = StockManagementScreen(self.db)
        self.tables_screen = TablesScreen(self.db)
        self.orders_screen = OrdersScreen(self.db)
        self.reports_screen = ReportsScreen(self.db)
        self.settings_screen = SettingsScreen(self.db)
        self.users_screen = UsersManagementScreen(self.db, self.current_user)
        
        self.stacked_widget.addWidget(self.pos_screen)
        self.stacked_widget.addWidget(self.products_screen)
        self.stacked_widget.addWidget(self.price_management_screen)
        self.stacked_widget.addWidget(self.stock_management_screen)
        self.stacked_widget.addWidget(self.tables_screen)
        self.stacked_widget.addWidget(self.orders_screen)
        self.stacked_widget.addWidget(self.reports_screen)
        self.stacked_widget.addWidget(self.settings_screen)
        self.stacked_widget.addWidget(self.users_screen)
        
        main_layout.addWidget(self.stacked_widget, 1)
        
        # Afficher l'écran POS par défaut
        self.stacked_widget.setCurrentIndex(0)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(10, 20, 10, 20)
        
        icon_label = QLabel("☕")
        icon_label.setFont(QFont("Arial", 32))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"color: {self.accent_color};")
        logo_layout.addWidget(icon_label)
        
        title = QLabel("CAFÉ 216")
        title_font = QFont("Arial", 18, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {self.accent_color}; font-weight: bold; letter-spacing: 2px;")
        logo_layout.addWidget(title)
        
        subtitle = QLabel("Point de Vente")
        subtitle_font = QFont("Arial", 9)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color: rgba(255, 255, 255, 0.8);")
        logo_layout.addWidget(subtitle)
        
        logo_container.setStyleSheet(f"background-color: {self.secondary_color}; padding: 5px;")
        sidebar_layout.addWidget(logo_container)
        
        nav_buttons = [
            ("Ventes", 0, "☕"),
            ("Produits", 1, "📦"),
            ("Prix & Produits", 2, "💰"),
            ("Stock", 3, "📊"),
            ("Tables", 4, "🪑"),
            ("Commandes", 5, "📋"),
            ("Rapports", 6, "📈"),
            ("Paramètres", 7, "⚙️"),
            ("Utilisateurs", 8, "👥")
        ]
        
        for btn_text, index, icon in nav_buttons:
            btn = QPushButton(f"{icon}\n{btn_text}")
            btn.setFixedHeight(70)
            btn.setFont(QFont("Arial", 10, QFont.Bold))
            btn.setStyleSheet(ModernStyles.sidebar_button())
            if index in self.allowed_indices:
                btn.clicked.connect(lambda checked, i=index: self.navigate(i))
            else:
                btn.setDisabled(True)
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()

        if self.current_user:
            user_info = QLabel(f"Connecté: {self.current_user['username']}\nRôle: {self.current_user['role']}")
            user_info.setAlignment(Qt.AlignCenter)
            user_info.setStyleSheet("color: white; padding: 8px;")
            sidebar_layout.addWidget(user_info)
        
        # Bouton déconnexion
        logout_btn = QPushButton("🚪 Déconnexion")
        logout_btn.setFixedHeight(50)
        logout_btn.setFont(QFont("Arial", 11, QFont.Bold))
        logout_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.DANGER))
        logout_btn.clicked.connect(self.close)
        sidebar_layout.addWidget(logout_btn)
        
        sidebar.setStyleSheet(f"background-color: {self.secondary_color};")
        return sidebar

    def navigate(self, index: int):
        if index in self.allowed_indices:
            self.stacked_widget.setCurrentIndex(index)
