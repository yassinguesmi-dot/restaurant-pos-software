from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QTableWidget, QTableWidgetItem, QDialog, QLineEdit, 
                             QDoubleSpinBox, QComboBox, QMessageBox, QTabWidget, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class PriceManagementScreen(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Titre
        title = QLabel("Gestion des Prix et Produits")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2C2C2C;")
        layout.addWidget(title)
        
        # Tabs
        tabs = QTabWidget()
        
        # Tab 1: Liste des produits
        products_tab = self.create_products_tab()
        tabs.addTab(products_tab, "Tous les Produits")
        
        # Tab 2: Par catégorie
        category_tab = self.create_category_tab()
        tabs.addTab(category_tab, "Par Catégorie")
        
        layout.addWidget(tabs)

    def create_products_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("+ Ajouter un Produit")
        add_btn.setFixedHeight(40)
        add_btn.setFont(QFont("Arial", 11, QFont.Bold))
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #C8A882;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #B8985F;
            }
        """)
        add_btn.clicked.connect(self.add_product)
        buttons_layout.addWidget(add_btn)
        
        refresh_btn = QPushButton("🔄 Rafraîchir")
        refresh_btn.setFixedHeight(40)
        refresh_btn.setFont(QFont("Arial", 11))
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #D4A574;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #C49460;
            }
        """)
        refresh_btn.clicked.connect(self.load_all_products)
        buttons_layout.addWidget(refresh_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Tableau des produits
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(7)
        self.products_table.setHorizontalHeaderLabels(["ID", "Nom du Produit", "Prix (dt)", "Catégorie", "Stock", "Stock Min", "Actions"])
        self.products_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #DDD;
                border: 1px solid #DDD;
            }
            QHeaderView::section {
                background-color: #2C2C2C;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        self.products_table.horizontalHeader().setStretchLastSection(False)
        layout.addWidget(self.products_table)
        
        self.load_all_products()
        return widget

    def create_category_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Sélecteur de catégorie
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("Sélectionner une catégorie:"))
        
        self.category_combo = QComboBox()
        categories = self.db.get_categories()
        self.category_combo.addItems(categories)
        self.category_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #DDD;
                border-radius: 3px;
            }
        """)
        self.category_combo.currentIndexChanged.connect(self.load_category_products)
        category_layout.addWidget(self.category_combo)
        category_layout.addStretch()
        layout.addLayout(category_layout)
        
        # Tableau par catégorie
        self.category_table = QTableWidget()
        self.category_table.setColumnCount(7)
        self.category_table.setHorizontalHeaderLabels(["ID", "Nom du Produit", "Prix (dt)", "Catégorie", "Stock", "Stock Min", "Actions"])
        self.category_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #DDD;
                border: 1px solid #DDD;
            }
            QHeaderView::section {
                background-color: #2C2C2C;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.category_table)
        
        self.load_category_products()
        return widget

    def load_all_products(self):
        products = self.db.get_all_products()
        self.products_table.setRowCount(len(products))
        
        for i, product in enumerate(products):
            stock = product.get('quantity', 0) or 0
            min_stock = product.get('min_quantity', 0) or 0
            
            self.products_table.setItem(i, 0, QTableWidgetItem(str(product['id'])))
            self.products_table.setItem(i, 1, QTableWidgetItem(product['name']))
            self.products_table.setItem(i, 2, QTableWidgetItem(f"{product['price']:.2f} dt"))
            self.products_table.setItem(i, 3, QTableWidgetItem(product['category'] or "Général"))
            
            # Stock avec couleur si faible
            stock_item = QTableWidgetItem(str(stock))
            if min_stock > 0 and stock <= min_stock:
                stock_item.setBackground(QColor("#FFE5E5"))
            self.products_table.setItem(i, 4, stock_item)
            
            self.products_table.setItem(i, 5, QTableWidgetItem(str(min_stock)))
            
            # Boutons d'action
            actions_layout = QHBoxLayout()
            
            edit_btn = QPushButton("✏️ Éditer")
            edit_btn.setFixedWidth(100)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            edit_btn.clicked.connect(lambda checked, p=product: self.edit_product(p))
            
            delete_btn = QPushButton("🗑️ Supprimer")
            delete_btn.setFixedWidth(110)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #F44336;
                    color: white;
                    border: none;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            delete_btn.clicked.connect(lambda checked, p=product: self.delete_product(p))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            
            widget = QWidget()
            widget.setLayout(actions_layout)
            self.products_table.setCellWidget(i, 6, widget)

    def load_category_products(self):
        category = self.category_combo.currentText()
        products = self.db.get_products_by_category(category)
        self.category_table.setRowCount(len(products))
        
        for i, product in enumerate(products):
            stock = product.get('quantity', 0) or 0
            min_stock = product.get('min_quantity', 0) or 0
            
            self.category_table.setItem(i, 0, QTableWidgetItem(str(product['id'])))
            self.category_table.setItem(i, 1, QTableWidgetItem(product['name']))
            self.category_table.setItem(i, 2, QTableWidgetItem(f"{product['price']:.2f} dt"))
            self.category_table.setItem(i, 3, QTableWidgetItem(product['category'] or "Général"))
            
            # Stock avec couleur si faible
            stock_item = QTableWidgetItem(str(stock))
            if min_stock > 0 and stock <= min_stock:
                stock_item.setBackground(QColor("#FFE5E5"))
            self.category_table.setItem(i, 4, stock_item)
            
            self.category_table.setItem(i, 5, QTableWidgetItem(str(min_stock)))
            
            # Boutons d'action
            actions_layout = QHBoxLayout()
            
            edit_btn = QPushButton("✏️ Éditer")
            edit_btn.setFixedWidth(100)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            edit_btn.clicked.connect(lambda checked, p=product: self.edit_product(p))
            
            delete_btn = QPushButton("🗑️ Supprimer")
            delete_btn.setFixedWidth(110)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #F44336;
                    color: white;
                    border: none;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            delete_btn.clicked.connect(lambda checked, p=product: self.delete_product(p))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            
            widget = QWidget()
            widget.setLayout(actions_layout)
            self.category_table.setCellWidget(i, 6, widget)

    def add_product(self):
        dialog = ProductPriceDialog(self.db)
        if dialog.exec_():
            self.load_all_products()
            self.load_category_products()

    def edit_product(self, product):
        dialog = ProductPriceDialog(self.db, product)
        if dialog.exec_():
            self.load_all_products()
            self.load_category_products()

    def delete_product(self, product):
        reply = QMessageBox.question(self, "Confirmation", 
                                     f"Êtes-vous sûr de vouloir supprimer '{product['name']}' ?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_product(product['id'])
            self.load_all_products()
            self.load_category_products()
            QMessageBox.information(self, "Succès", f"Produit '{product['name']}' supprimé avec succès.")


class ProductPriceDialog(QDialog):
    def __init__(self, db, product=None):
        super().__init__()
        self.db = db
        self.product = product
        self.init_ui()

    def init_ui(self):
        if self.product:
            self.setWindowTitle("Modifier le Produit")
        else:
            self.setWindowTitle("Ajouter un Nouveau Produit")
        
        self.setGeometry(400, 300, 500, 400)
        self.setStyleSheet("background-color: #F8F6F3;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Nom du produit
        layout.addWidget(QLabel("Nom du Produit:"))
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #DDD;
                border-radius: 3px;
                background-color: white;
            }
        """)
        if self.product:
            self.name_input.setText(self.product['name'])
        layout.addWidget(self.name_input)
        
        # Prix en dt
        layout.addWidget(QLabel("Prix (dt):"))
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 10000)
        self.price_input.setDecimals(2)
        self.price_input.setSingleStep(0.5)
        self.price_input.setStyleSheet("""
            QDoubleSpinBox {
                padding: 10px;
                border: 1px solid #DDD;
                border-radius: 3px;
                background-color: white;
            }
        """)
        if self.product:
            self.price_input.setValue(self.product['price'])
        layout.addWidget(self.price_input)
        
        # Catégorie
        layout.addWidget(QLabel("Catégorie:"))
        self.category_input = QComboBox()
        self.category_input.addItems(["Cafés", "Jus", "Chichas", "Boissons", "Gâteaux"])
        self.category_input.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #DDD;
                border-radius: 3px;
                background-color: white;
            }
        """)
        if self.product:
            index = self.category_input.findText(self.product['category'] or "Cafés")
            if index >= 0:
                self.category_input.setCurrentIndex(index)
        layout.addWidget(self.category_input)
        
        # Stock
        layout.addWidget(QLabel("Stock actuel:"))
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 10000)
        self.stock_input.setStyleSheet("""
            QSpinBox {
                padding: 10px;
                border: 1px solid #DDD;
                border-radius: 3px;
                background-color: white;
            }
        """)
        if self.product:
            self.stock_input.setValue(self.product.get('quantity', 0) or 0)
        layout.addWidget(self.stock_input)
        
        # Stock minimum (alerte)
        layout.addWidget(QLabel("Stock minimum (alerte):"))
        self.min_stock_input = QSpinBox()
        self.min_stock_input.setRange(0, 10000)
        self.min_stock_input.setStyleSheet("""
            QSpinBox {
                padding: 10px;
                border: 1px solid #DDD;
                border-radius: 3px;
                background-color: white;
            }
        """)
        if self.product:
            self.min_stock_input.setValue(self.product.get('min_quantity', 0) or 0)
        layout.addWidget(self.min_stock_input)
        
        layout.addStretch()
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setFixedHeight(45)
        cancel_btn.setFont(QFont("Arial", 11, QFont.Bold))
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #999999;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Enregistrer")
        save_btn.setFixedHeight(45)
        save_btn.setFont(QFont("Arial", 11, QFont.Bold))
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #C8A882;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #B8985F;
            }
        """)
        save_btn.clicked.connect(self.save)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)

    def save(self):
        if not self.name_input.text():
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom de produit!")
            return
        
        if self.price_input.value() <= 0:
            QMessageBox.warning(self, "Erreur", "Le prix doit être supérieur à 0!")
            return
        
        if self.product:
            self.db.update_product(
                self.product['id'], 
                self.name_input.text(), 
                self.price_input.value(), 
                self.category_input.currentText(),
                self.stock_input.value(),
                self.min_stock_input.value()
            )
            QMessageBox.information(self, "Succès", f"Produit '{self.name_input.text()}' modifié avec succès!")
        else:
            self.db.add_product(
                self.name_input.text(), 
                self.price_input.value(), 
                self.category_input.currentText(),
                None,
                self.stock_input.value(),
                self.min_stock_input.value()
            )
            QMessageBox.information(self, "Succès", f"Produit '{self.name_input.text()}' ajouté avec succès!")
        
        self.accept()
