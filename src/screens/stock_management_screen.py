from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QTableWidget, QTableWidgetItem, QDialog, QSpinBox, 
                             QMessageBox, QTabWidget, QComboBox, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from datetime import datetime

class StockManagementScreen(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Titre
        title = QLabel("Gestion du Stock")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2C2C2C;")
        layout.addWidget(title)
        
        # Tabs
        tabs = QTabWidget()
        
        # Tab 1: Vue d'ensemble du stock
        overview_tab = self.create_overview_tab()
        tabs.addTab(overview_tab, "Vue d'ensemble")
        
        # Tab 2: Alertes stock faible
        alerts_tab = self.create_alerts_tab()
        tabs.addTab(alerts_tab, "Alertes Stock Faible")
        
        # Tab 3: Historique des mouvements
        history_tab = self.create_history_tab()
        tabs.addTab(history_tab, "Historique")
        
        layout.addWidget(tabs)

    def create_overview_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        add_stock_btn = QPushButton("+ Réapprovisionner")
        add_stock_btn.setFixedHeight(40)
        add_stock_btn.setFont(QFont("Arial", 11, QFont.Bold))
        add_stock_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        add_stock_btn.clicked.connect(self.add_stock)
        buttons_layout.addWidget(add_stock_btn)
        
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
        refresh_btn.clicked.connect(self.load_stock)
        buttons_layout.addWidget(refresh_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Tableau du stock
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(6)
        self.stock_table.setHorizontalHeaderLabels(["ID", "Produit", "Stock Actuel", "Stock Min", "Statut", "Actions"])
        self.stock_table.setStyleSheet("""
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
        layout.addWidget(self.stock_table)
        
        self.load_stock()
        return widget

    def create_alerts_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel("Produits avec stock faible ou épuisé:")
        info_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(info_label)
        
        self.alerts_table = QTableWidget()
        self.alerts_table.setColumnCount(5)
        self.alerts_table.setHorizontalHeaderLabels(["ID", "Produit", "Stock Actuel", "Stock Min", "Actions"])
        self.alerts_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #DDD;
                border: 1px solid #DDD;
            }
            QHeaderView::section {
                background-color: #FF5733;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.alerts_table)
        
        self.load_alerts()
        return widget

    def create_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Filtres
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Produit:"))
        
        self.product_filter = QComboBox()
        self.product_filter.addItem("Tous")
        products = self.db.get_all_products()
        for product in products:
            self.product_filter.addItem(product['name'], product['id'])
        self.product_filter.currentIndexChanged.connect(self.load_history)
        filter_layout.addWidget(self.product_filter)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Tableau historique
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels(["Date", "Produit", "Type", "Quantité", "Avant", "Après", "Raison"])
        self.history_table.setStyleSheet("""
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
        layout.addWidget(self.history_table)
        
        self.load_history()
        return widget

    def load_stock(self):
        products = self.db.get_all_products()
        self.stock_table.setRowCount(len(products))
        
        for i, product in enumerate(products):
            stock = product.get('quantity', 0) or 0
            min_stock = product.get('min_quantity', 0) or 0
            
            self.stock_table.setItem(i, 0, QTableWidgetItem(str(product['id'])))
            self.stock_table.setItem(i, 1, QTableWidgetItem(product['name']))
            
            stock_item = QTableWidgetItem(str(stock))
            min_stock_item = QTableWidgetItem(str(min_stock))
            
            # Statut
            if stock == 0:
                status = "Épuisé"
                status_color = QColor("#FF0000")
            elif min_stock > 0 and stock <= min_stock:
                status = "Stock faible"
                status_color = QColor("#FFA500")
            else:
                status = "OK"
                status_color = QColor("#4CAF50")
            
            status_item = QTableWidgetItem(status)
            status_item.setBackground(status_color)
            status_item.setForeground(QColor("white"))
            
            self.stock_table.setItem(i, 2, stock_item)
            self.stock_table.setItem(i, 3, min_stock_item)
            self.stock_table.setItem(i, 4, status_item)
            
            # Bouton ajuster
            adjust_btn = QPushButton("Ajuster")
            adjust_btn.setFixedWidth(80)
            adjust_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            adjust_btn.clicked.connect(lambda checked, p=product: self.adjust_stock(p))
            self.stock_table.setCellWidget(i, 5, adjust_btn)

    def load_alerts(self):
        low_stock_products = self.db.get_low_stock_products()
        self.alerts_table.setRowCount(len(low_stock_products))
        
        for i, product in enumerate(low_stock_products):
            stock = product.get('quantity', 0) or 0
            min_stock = product.get('min_quantity', 0) or 0
            
            self.alerts_table.setItem(i, 0, QTableWidgetItem(str(product['id'])))
            self.alerts_table.setItem(i, 1, QTableWidgetItem(product['name']))
            
            stock_item = QTableWidgetItem(str(stock))
            stock_item.setBackground(QColor("#FFE5E5"))
            self.alerts_table.setItem(i, 2, stock_item)
            self.alerts_table.setItem(i, 3, QTableWidgetItem(str(min_stock)))
            
            # Bouton réapprovisionner
            restock_btn = QPushButton("Réapprovisionner")
            restock_btn.setFixedWidth(120)
            restock_btn.setStyleSheet("""
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
            restock_btn.clicked.connect(lambda checked, p=product: self.add_stock_for_product(p))
            self.alerts_table.setCellWidget(i, 4, restock_btn)

    def load_history(self):
        product_id = self.product_filter.currentData()
        if product_id:
            movements = self.db.get_stock_movements(product_id, limit=100)
        else:
            movements = self.db.get_stock_movements(limit=100)
        
        self.history_table.setRowCount(len(movements))
        
        for i, movement in enumerate(movements):
            date_str = datetime.fromisoformat(movement['created_at']).strftime('%Y-%m-%d %H:%M')
            self.history_table.setItem(i, 0, QTableWidgetItem(date_str))
            self.history_table.setItem(i, 1, QTableWidgetItem(movement.get('product_name', 'N/A')))
            
            type_item = QTableWidgetItem("Entrée" if movement['movement_type'] == 'entrée' else "Sortie")
            if movement['movement_type'] == 'entrée':
                type_item.setBackground(QColor("#E8F5E9"))
            else:
                type_item.setBackground(QColor("#FFEBEE"))
            self.history_table.setItem(i, 2, type_item)
            
            self.history_table.setItem(i, 3, QTableWidgetItem(str(movement['quantity'])))
            self.history_table.setItem(i, 4, QTableWidgetItem(str(movement['previous_quantity'])))
            self.history_table.setItem(i, 5, QTableWidgetItem(str(movement['new_quantity'])))
            self.history_table.setItem(i, 6, QTableWidgetItem(movement.get('reason', 'N/A')))

    def add_stock(self):
        dialog = AddStockDialog(self.db)
        if dialog.exec_():
            self.load_stock()
            self.load_alerts()
            self.load_history()

    def add_stock_for_product(self, product):
        dialog = AddStockDialog(self.db, product)
        if dialog.exec_():
            self.load_stock()
            self.load_alerts()
            self.load_history()

    def adjust_stock(self, product):
        dialog = AdjustStockDialog(self.db, product)
        if dialog.exec_():
            self.load_stock()
            self.load_alerts()
            self.load_history()


class AddStockDialog(QDialog):
    def __init__(self, db, product=None):
        super().__init__()
        self.db = db
        self.product = product
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Réapprovisionner le Stock")
        self.setGeometry(400, 300, 400, 250)
        self.setStyleSheet("background-color: #F8F6F3;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        if self.product:
            layout.addWidget(QLabel(f"Produit: {self.product['name']}"))
            layout.addWidget(QLabel(f"Stock actuel: {self.product.get('quantity', 0) or 0}"))
        
        layout.addWidget(QLabel("Sélectionner le produit:"))
        self.product_combo = QComboBox()
        products = self.db.get_all_products()
        for p in products:
            self.product_combo.addItem(p['name'], p['id'])
        if self.product:
            index = self.product_combo.findData(self.product['id'])
            if index >= 0:
                self.product_combo.setCurrentIndex(index)
        layout.addWidget(self.product_combo)
        
        layout.addWidget(QLabel("Quantité à ajouter:"))
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 10000)
        self.quantity_input.setValue(10)
        layout.addWidget(self.quantity_input)
        
        layout.addWidget(QLabel("Raison:"))
        self.reason_input = QLineEdit()
        self.reason_input.setText("Réapprovisionnement")
        layout.addWidget(self.reason_input)
        
        buttons_layout = QHBoxLayout()
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Enregistrer")
        save_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        save_btn.clicked.connect(self.save)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)

    def save(self):
        product_id = self.product_combo.currentData()
        quantity = self.quantity_input.value()
        reason = self.reason_input.text() or "Réapprovisionnement"
        
        if self.db.increment_stock(product_id, quantity, reason):
            QMessageBox.information(self, "Succès", f"Stock mis à jour avec succès!")
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", "Erreur lors de la mise à jour du stock")


class AdjustStockDialog(QDialog):
    def __init__(self, db, product):
        super().__init__()
        self.db = db
        self.product = product
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ajuster le Stock")
        self.setGeometry(400, 300, 400, 200)
        self.setStyleSheet("background-color: #F8F6F3;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        layout.addWidget(QLabel(f"Produit: {self.product['name']}"))
        layout.addWidget(QLabel(f"Stock actuel: {self.product.get('quantity', 0) or 0}"))
        
        layout.addWidget(QLabel("Nouveau stock:"))
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 10000)
        self.quantity_input.setValue(self.product.get('quantity', 0) or 0)
        layout.addWidget(self.quantity_input)
        
        layout.addWidget(QLabel("Stock minimum:"))
        self.min_quantity_input = QSpinBox()
        self.min_quantity_input.setRange(0, 10000)
        self.min_quantity_input.setValue(self.product.get('min_quantity', 0) or 0)
        layout.addWidget(self.min_quantity_input)
        
        buttons_layout = QHBoxLayout()
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Enregistrer")
        save_btn.setStyleSheet("background-color: #2196F3; color: white;")
        save_btn.clicked.connect(self.save)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)

    def save(self):
        quantity = self.quantity_input.value()
        min_quantity = self.min_quantity_input.value()
        
        self.db.update_product_stock(self.product['id'], quantity, min_quantity)
        QMessageBox.information(self, "Succès", "Stock ajusté avec succès!")
        self.accept()

