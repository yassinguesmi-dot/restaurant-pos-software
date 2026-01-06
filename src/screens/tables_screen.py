from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QGridLayout, QMessageBox, QDialog, QComboBox, QLineEdit,
                             QTableWidget, QTableWidgetItem, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class TablesScreen(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Titre
        title = QLabel("Gestion des Tables")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2C2C2C;")
        layout.addWidget(title)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        add_table_btn = QPushButton("+ Ajouter une Table")
        add_table_btn.setFixedHeight(40)
        add_table_btn.setFont(QFont("Arial", 11, QFont.Bold))
        add_table_btn.setStyleSheet("""
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
        add_table_btn.clicked.connect(self.add_table)
        buttons_layout.addWidget(add_table_btn)
        
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
        refresh_btn.clicked.connect(self.load_tables)
        buttons_layout.addWidget(refresh_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Grille des tables
        self.tables_grid = QGridLayout()
        self.tables_grid.setSpacing(15)
        self.tables_grid.setContentsMargins(15, 15, 15, 15)
        
        grid_widget = QWidget()
        grid_widget.setLayout(self.tables_grid)
        layout.addWidget(grid_widget)
        
        self.load_tables()

    def load_tables(self):
        # Vider la grille
        while self.tables_grid.count():
            self.tables_grid.takeAt(0).widget().deleteLater()
        
        tables = self.db.get_all_tables()
        
        row, col = 0, 0
        for table in tables:
            btn = self.create_table_button(table)
            self.tables_grid.addWidget(btn, row, col)
            col += 1
            if col >= 5:  # 5 colonnes
                col = 0
                row += 1

    def create_table_button(self, table):
        btn = QPushButton()
        btn.setFixedSize(150, 120)
        
        table_number = table['table_number']
        status = table['status']
        capacity = table.get('capacity', 4)
        
        # Compter les commandes en cours
        orders = self.db.get_table_orders(table['id'], status='en attente')
        orders_count = len(orders)
        
        # Texte du bouton
        status_text = "🟢 Libre" if status == 'libre' else "🔴 Occupée"
        btn_text = f"{table_number}\n{status_text}\nCapacité: {capacity}"
        if orders_count > 0:
            btn_text += f"\n{orders_count} commande(s)"
        
        btn.setText(btn_text)
        btn.setFont(QFont("Arial", 10, QFont.Bold))
        
        # Couleur selon le statut
        if status == 'libre':
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #E8F5E9;
                    border: 3px solid #4CAF50;
                    border-radius: 10px;
                    color: #2C2C2C;
                }
                QPushButton:hover {
                    background-color: #C8E6C9;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFEBEE;
                    border: 3px solid #F44336;
                    border-radius: 10px;
                    color: #2C2C2C;
                }
                QPushButton:hover {
                    background-color: #FFCDD2;
                }
            """)
        
        btn.clicked.connect(lambda checked, t=table: self.table_clicked(t))
        return btn

    def table_clicked(self, table):
        dialog = TableDetailsDialog(self.db, table)
        dialog.exec_()
        self.load_tables()

    def add_table(self):
        dialog = AddTableDialog(self.db)
        if dialog.exec_():
            self.load_tables()


class TableDetailsDialog(QDialog):
    def __init__(self, db, table):
        super().__init__()
        self.db = db
        self.table = table
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Détails - {self.table['table_number']}")
        self.setGeometry(400, 300, 600, 500)
        self.setStyleSheet("background-color: #F8F6F3;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Informations de la table
        info_label = QLabel(f"Table: {self.table['table_number']}")
        info_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(info_label)
        
        status_label = QLabel(f"Statut: {self.table['status']}")
        status_label.setFont(QFont("Arial", 12))
        layout.addWidget(status_label)
        
        # Commandes en cours
        orders_label = QLabel("Commandes en cours:")
        orders_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(orders_label)
        
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(4)
        self.orders_table.setHorizontalHeaderLabels(["N° Commande", "Montant", "Statut", "Actions"])
        self.orders_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #DDD;
                border: 1px solid #DDD;
            }
            QHeaderView::section {
                background-color: #2C2C2C;
                color: white;
                padding: 5px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.orders_table)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        if self.table['status'] == 'libre':
            occupy_btn = QPushButton("Marquer comme occupée")
            occupy_btn.setStyleSheet("background-color: #FF9800; color: white;")
            occupy_btn.clicked.connect(lambda: self.change_status('occupée'))
            buttons_layout.addWidget(occupy_btn)
        else:
            free_btn = QPushButton("Libérer la table")
            free_btn.setStyleSheet("background-color: #4CAF50; color: white;")
            free_btn.clicked.connect(lambda: self.change_status('libre'))
            buttons_layout.addWidget(free_btn)
        
        new_order_btn = QPushButton("Nouvelle commande")
        new_order_btn.setStyleSheet("background-color: #2196F3; color: white;")
        new_order_btn.clicked.connect(self.create_order)
        buttons_layout.addWidget(new_order_btn)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        
        self.load_orders()

    def load_orders(self):
        orders = self.db.get_table_orders(self.table['id'])
        self.orders_table.setRowCount(len(orders))
        
        for i, order in enumerate(orders):
            self.orders_table.setItem(i, 0, QTableWidgetItem(order['order_number']))
            self.orders_table.setItem(i, 1, QTableWidgetItem(f"{order['total_amount']:.2f} dt"))
            self.orders_table.setItem(i, 2, QTableWidgetItem(order['status']))
            
            # Bouton voir détails
            details_btn = QPushButton("Voir")
            details_btn.setFixedWidth(60)
            details_btn.clicked.connect(lambda checked, o=order: self.view_order_details(o))
            self.orders_table.setCellWidget(i, 3, details_btn)

    def change_status(self, new_status):
        self.db.update_table_status(self.table['id'], new_status)
        QMessageBox.information(self, "Succès", f"Statut de la table mis à jour: {new_status}")
        self.accept()

    def create_order(self):
        # Cette fonction sera appelée depuis le POS screen avec la table sélectionnée
        QMessageBox.information(self, "Info", "Retournez à l'écran Ventes pour créer une commande pour cette table.")
        self.accept()

    def view_order_details(self, order):
        QMessageBox.information(self, "Détails", f"Commande: {order['order_number']}\nMontant: {order['total_amount']:.2f} dt")


class AddTableDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ajouter une Table")
        self.setGeometry(400, 300, 400, 200)
        self.setStyleSheet("background-color: #F8F6F3;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        layout.addWidget(QLabel("Numéro de table:"))
        self.table_number_input = QLineEdit()
        self.table_number_input.setPlaceholderText("Ex: Table 11")
        layout.addWidget(self.table_number_input)
        
        layout.addWidget(QLabel("Capacité:"))
        self.capacity_input = QSpinBox()
        self.capacity_input.setRange(1, 20)
        self.capacity_input.setValue(4)
        layout.addWidget(self.capacity_input)
        
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
        table_number = self.table_number_input.text().strip()
        if not table_number:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un numéro de table!")
            return
        
        capacity = self.capacity_input.value()
        
        try:
            cursor = self.db.connection.cursor()
            cursor.execute('''
                INSERT INTO tables (table_number, capacity)
                VALUES (?, ?)
            ''', (table_number, capacity))
            self.db.connection.commit()
            QMessageBox.information(self, "Succès", f"Table '{table_number}' ajoutée avec succès!")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur: {str(e)}")

