from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QTableWidget, QTableWidgetItem, QDialog, QLineEdit, 
                             QDoubleSpinBox, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.utils.styles import ModernStyles

class ProductsScreen(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.primary_color = "#FF9500"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header with title and description
        header_layout = QVBoxLayout()
        title = QLabel("📦 Gestion des Produits")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        header_layout.addWidget(title)
        
        subtitle = QLabel("Gérez votre catalogue de produits")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet(f"color: {ModernStyles.TEXT_SECONDARY};")
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Ajouter un produit")
        add_btn.setMinimumHeight(44)
        add_btn.setFont(QFont("Arial", 11, QFont.Bold))
        add_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.SUCCESS))
        add_btn.clicked.connect(self.add_product)
        buttons_layout.addWidget(add_btn)
        
        refresh_btn = QPushButton("🔄 Rafraîchir")
        refresh_btn.setMinimumHeight(44)
        refresh_btn.setFont(QFont("Arial", 11))
        refresh_btn.setStyleSheet(ModernStyles.modern_button_outline(ModernStyles.INFO))
        refresh_btn.clicked.connect(self.load_products)
        buttons_layout.addWidget(refresh_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Tableau des produits
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels(["ID", "Nom", "Prix", "Catégorie", "Actions"])
        self.products_table.setStyleSheet(ModernStyles.modern_table())
        self.products_table.setAlternatingRowColors(True)
        self.products_table.verticalHeader().setVisible(False)
        self.products_table.horizontalHeader().setStretchLastSection(True)
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setSelectionMode(QTableWidget.SingleSelection)
        # Improve table spacing and column sizes for readability
        self.products_table.verticalHeader().setDefaultSectionSize(52)
        self.products_table.setColumnWidth(0, 60)
        self.products_table.setColumnWidth(1, 320)
        self.products_table.setColumnWidth(2, 100)
        self.products_table.setColumnWidth(3, 140)
        layout.addWidget(self.products_table)
        
        self.load_products()

    def load_products(self):
        products = self.db.get_all_products()
        self.products_table.setRowCount(len(products))
        
        for i, product in enumerate(products):
            self.products_table.setItem(i, 0, QTableWidgetItem(str(product['id'])))
            self.products_table.setItem(i, 1, QTableWidgetItem(product['name']))
            self.products_table.setItem(i, 2, QTableWidgetItem(f"{product['price']:.2f} dt"))
            self.products_table.setItem(i, 3, QTableWidgetItem(product['category'] or "Général"))
            
            # Boutons d'action
            actions_layout = QHBoxLayout()
            
            edit_btn = QPushButton("✏️ Éditer")
            edit_btn.setFixedWidth(80)
            edit_btn.setStyleSheet(ModernStyles.table_button("edit"))
            edit_btn.clicked.connect(lambda checked, p=product: self.edit_product(p))
            
            delete_btn = QPushButton("🗑️ Suppr.")
            delete_btn.setFixedWidth(80)
            delete_btn.setStyleSheet(ModernStyles.table_button("delete"))
            delete_btn.clicked.connect(lambda checked, p=product: self.delete_product(p))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            
            widget = QWidget()
            widget.setLayout(actions_layout)
            self.products_table.setCellWidget(i, 4, widget)

    def add_product(self):
        dialog = ProductDialog(self.db)
        if dialog.exec_():
            self.load_products()

    def edit_product(self, product):
        dialog = ProductDialog(self.db, product)
        if dialog.exec_():
            self.load_products()

    def delete_product(self, product):
        reply = QMessageBox.question(self, "Confirmation", 
                                     f"Êtes-vous sûr de vouloir supprimer {product['name']} ?")
        if reply == QMessageBox.Yes:
            self.db.delete_product(product['id'])
            self.load_products()


class ProductDialog(QDialog):
    def __init__(self, db, product=None):
        super().__init__()
        self.db = db
        self.product = product
        self.primary_color = "#FF9500"
        self.init_ui()

    def init_ui(self):
        if self.product:
            self.setWindowTitle("✏️ Éditer le produit")
        else:
            self.setWindowTitle("➕ Ajouter un produit")
        
        self.setGeometry(400, 300, 480, 400)
        self.setStyleSheet(f"background-color: {ModernStyles.LIGHT_BG};")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(16)
        
        # Title
        title_label = QLabel("✏️ Modifier le produit" if self.product else "➕ Nouveau produit")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        layout.addWidget(title_label)
        
        # Nom
        layout.addWidget(QLabel("Nom du produit"))
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(ModernStyles.modern_input())
        self.name_input.setPlaceholderText("Ex: Express, Cappuccino...")
        if self.product:
            self.name_input.setText(self.product['name'])
        layout.addWidget(self.name_input)
        
        # Prix
        layout.addWidget(QLabel("Prix (dt)"))
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 10000)
        self.price_input.setDecimals(2)
        self.price_input.setStyleSheet(ModernStyles.modern_input())
        if self.product:
            self.price_input.setValue(self.product['price'])
        layout.addWidget(self.price_input)
        
        # Catégorie
        layout.addWidget(QLabel("Catégorie"))
        self.category_input = QComboBox()
        self.category_input.addItems(["Cafés", "Jus", "Chichas", "Boissons", "Gâteaux"])
        self.category_input.setStyleSheet(ModernStyles.modern_input())
        if self.product:
            index = self.category_input.findText(self.product['category'] or "Cafés")
            if index >= 0:
                self.category_input.setCurrentIndex(index)
        layout.addWidget(self.category_input)
        
        layout.addStretch()
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setStyleSheet(ModernStyles.dialog_button(is_primary=False))
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("✓ Enregistrer")
        save_btn.setFixedHeight(40)
        save_btn.setFont(QFont("Arial", 11, QFont.Bold))
        save_btn.setStyleSheet(ModernStyles.dialog_button(is_primary=True))
        save_btn.clicked.connect(self.save)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)

    def save(self):
        if not self.name_input.text():
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom !")
            return
        
        if self.product:
            self.db.update_product(self.product['id'], self.name_input.text(), 
                                  self.price_input.value(), self.category_input.currentText())
        else:
            self.db.add_product(self.name_input.text(), self.price_input.value(), 
                               self.category_input.currentText())
        
        self.accept()
