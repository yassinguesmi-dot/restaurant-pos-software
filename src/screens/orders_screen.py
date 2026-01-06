from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
                             QTableWidgetItem, QPushButton, QDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.utils.invoice_generator import InvoiceGenerator

class OrdersScreen(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.primary_color = "#FF9500"
        self.currency = db.get_setting('currency', 'TND')
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Titre
        title = QLabel("Historique des Commandes")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #2C2C2C;")
        layout.addWidget(title)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Rafraîchir")
        refresh_btn.setFixedHeight(40)
        refresh_btn.setFont(QFont("Arial", 11, QFont.Bold))
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #C8A882;
                color: white;
                border: none;
                border-radius: 3px;
            }
        """)
        refresh_btn.clicked.connect(self.load_orders)
        buttons_layout.addWidget(refresh_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Tableau des commandes
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(7)
        self.orders_table.setHorizontalHeaderLabels(["N° Commande", "N° Facture", "Date", "Montant", "Statut", "Paiement", "Actions"])
        self.orders_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #DDD;
            }
            QHeaderView::section {
                background-color: #2C2C2C;
                color: white;
                padding: 5px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.orders_table)
        
        self.load_orders()

    def load_orders(self):
        orders = self.db.get_all_orders()
        self.orders_table.setRowCount(len(orders))
        
        for i, order in enumerate(orders):
            self.orders_table.setItem(i, 0, QTableWidgetItem(order['order_number']))
            invoice_num = order.get('invoice_number', '-')
            self.orders_table.setItem(i, 1, QTableWidgetItem(invoice_num))
            self.orders_table.setItem(i, 2, QTableWidgetItem(order['created_at'][:10]))
            self.orders_table.setItem(i, 3, QTableWidgetItem(f"{order['total_amount']:.2f} {self.currency}"))
            self.orders_table.setItem(i, 4, QTableWidgetItem(order['status']))
            self.orders_table.setItem(i, 5, QTableWidgetItem(order['payment_method'] or "-"))
            
            # Boutons d'action
            actions_layout = QHBoxLayout()
            
            details_btn = QPushButton("Voir")
            details_btn.setFixedWidth(60)
            details_btn.setStyleSheet("background-color: #2196F3; color: white;")
            details_btn.clicked.connect(lambda checked, o=order: self.show_order_details(o))
            actions_layout.addWidget(details_btn)
            
            if order['status'] == 'payé':
                invoice_btn = QPushButton("Facture")
                invoice_btn.setFixedWidth(70)
                invoice_btn.setStyleSheet("background-color: #4CAF50; color: white;")
                invoice_btn.clicked.connect(lambda checked, o=order: self.generate_invoice(o))
                actions_layout.addWidget(invoice_btn)
            
            actions_widget = QWidget()
            actions_widget.setLayout(actions_layout)
            self.orders_table.setCellWidget(i, 6, actions_widget)

    def show_order_details(self, order):
        dialog = OrderDetailsDialog(self.db, order)
        dialog.exec_()

    def generate_invoice(self, order):
        try:
            invoice_gen = InvoiceGenerator(self.db)
            pdf_path = invoice_gen.generate_invoice(order['id'])
            QMessageBox.information(
                self, 
                "Succès", 
                f"Facture générée avec succès!\n\nFichier: {pdf_path}\n\nSouhaitez-vous l'imprimer?",
                QMessageBox.Yes | QMessageBox.No
            )
            # Ouvrir le PDF
            invoice_gen.print_invoice(order['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération de la facture:\n{str(e)}")


class OrderDetailsDialog(QDialog):
    def __init__(self, db, order):
        super().__init__()
        self.db = db
        self.order = order
        self.currency = "dt"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Détails de la commande {self.order['order_number']}")
        self.setGeometry(300, 200, 600, 400)
        
        layout = QVBoxLayout(self)
        
        # Info commande
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel(f"N°: {self.order['order_number']}"))
        info_layout.addWidget(QLabel(f"Statut: {self.order['status']}"))
        info_layout.addWidget(QLabel(f"Montant: {self.order['total_amount']:.2f} {self.currency}"))
        layout.addLayout(info_layout)
        
        # Détails des articles
        self.details_table = QTableWidget()
        self.details_table.setColumnCount(4)
        self.details_table.setHorizontalHeaderLabels(["Article", "Quantité", "Prix U.", "Total"])
        
        items = self.db.get_order_details(self.order['id'])
        self.details_table.setRowCount(len(items))
        
        for i, item in enumerate(items):
            self.details_table.setItem(i, 0, QTableWidgetItem(item['name']))
            self.details_table.setItem(i, 1, QTableWidgetItem(str(item['quantity'])))
            self.details_table.setItem(i, 2, QTableWidgetItem(f"{item['unit_price']:.2f} {self.currency}"))
            self.details_table.setItem(i, 3, QTableWidgetItem(f"{item['total_price']:.2f} {self.currency}"))
        
        layout.addWidget(self.details_table)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        if self.order['status'] == 'payé':
            invoice_btn = QPushButton("Générer Facture PDF")
            invoice_btn.setStyleSheet("background-color: #4CAF50; color: white;")
            invoice_btn.clicked.connect(self.generate_invoice)
            buttons_layout.addWidget(invoice_btn)
            
            print_btn = QPushButton("Imprimer")
            print_btn.setStyleSheet("background-color: #2196F3; color: white;")
            print_btn.clicked.connect(self.print_invoice)
            buttons_layout.addWidget(print_btn)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)

    def generate_invoice(self):
        try:
            invoice_gen = InvoiceGenerator(self.db)
            pdf_path = invoice_gen.generate_invoice(self.order['id'])
            QMessageBox.information(
                self, 
                "Succès", 
                f"Facture générée avec succès!\n\nFichier: {pdf_path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération:\n{str(e)}")

    def print_invoice(self):
        try:
            invoice_gen = InvoiceGenerator(self.db)
            invoice_gen.print_invoice(self.order['id'])
            QMessageBox.information(self, "Succès", "Facture envoyée à l'impression!")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'impression:\n{str(e)}")
