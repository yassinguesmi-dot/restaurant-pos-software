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
        try:
            currency = db.get_setting('currency', 'TND')
            if isinstance(currency, dict):
                self.currency = currency.get('value', 'TND')
            else:
                self.currency = currency if currency else 'TND'
        except:
            self.currency = 'TND'
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
        try:
            orders = self.db.get_all_orders()
            print(f"DEBUG: {len(orders)} commandes chargées")
            
            if not orders:
                print("DEBUG: Aucune commande trouvée")
                self.orders_table.setRowCount(0)
                return
            
            self.orders_table.setRowCount(len(orders))
            
            for i, order in enumerate(orders):
                try:
                    # Afficher les clés disponibles pour debug
                    if i == 0:
                        print(f"DEBUG: Clés disponibles: {list(order.keys())}")
                    
                    # Extraire les valeurs avec des valeurs par défaut
                    order_number = str(order.get('order_number', f"Cmd {order.get('id', i)}"))
                    invoice_num = str(order.get('invoice_number', '-'))
                    created_at = str(order.get('created_at', '-'))[:10]
                    total_amount = float(order.get('total_amount', 0))
                    status = str(order.get('status', 'inconnu'))
                    payment_method = str(order.get('payment_method', '-'))
                    
                    self.orders_table.setItem(i, 0, QTableWidgetItem(order_number))
                    self.orders_table.setItem(i, 1, QTableWidgetItem(invoice_num))
                    self.orders_table.setItem(i, 2, QTableWidgetItem(created_at))
                    self.orders_table.setItem(i, 3, QTableWidgetItem(f"{total_amount:.2f} {self.currency}"))
                    self.orders_table.setItem(i, 4, QTableWidgetItem(status))
                    self.orders_table.setItem(i, 5, QTableWidgetItem(payment_method if payment_method != 'None' else '-'))
                    
                    # Boutons d'action
                    actions_layout = QHBoxLayout()
                    
                    details_btn = QPushButton("Voir")
                    details_btn.setFixedWidth(60)
                    details_btn.setStyleSheet("background-color: #2196F3; color: white; border-radius: 4px;")
                    details_btn.clicked.connect(lambda checked, o=order: self.show_order_details(o))
                    actions_layout.addWidget(details_btn)
                    
                    if status.lower() == 'payé':
                        invoice_btn = QPushButton("Facture")
                        invoice_btn.setFixedWidth(70)
                        invoice_btn.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 4px;")
                        invoice_btn.clicked.connect(lambda checked, o=order: self.generate_invoice(o))
                        actions_layout.addWidget(invoice_btn)
                    
                    actions_layout.addStretch()
                    actions_widget = QWidget()
                    actions_widget.setLayout(actions_layout)
                    self.orders_table.setCellWidget(i, 6, actions_widget)
                    
                except Exception as e:
                    print(f"DEBUG: Erreur à la ligne {i}: {e}")
                    continue
        except Exception as e:
            print(f"DEBUG: Erreur dans load_orders: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement des commandes: {str(e)}")

    def show_order_details(self, order):
        try:
            dialog = OrderDetailsDialog(self.db, order)
            dialog.exec_()
        except Exception as e:
            print(f"DEBUG: Erreur show_order_details: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'affichage des détails: {str(e)}")

    def generate_invoice(self, order):
        try:
            invoice_gen = InvoiceGenerator(self.db)
            pdf_path = invoice_gen.generate_invoice(order.get('id', -1))
            QMessageBox.information(
                self, 
                "Succès", 
                f"Facture générée avec succès!\n\nFichier: {pdf_path}\n\nSouhaitez-vous l'imprimer?",
                QMessageBox.Yes | QMessageBox.No
            )
            # Ouvrir le PDF
            invoice_gen.print_invoice(order.get('id', -1))
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
        try:
            order_number = str(self.order.get('order_number', f"Cmd {self.order.get('id', '?')}"))
            self.setWindowTitle(f"Détails de la commande {order_number}")
            self.setGeometry(300, 200, 600, 400)
            
            layout = QVBoxLayout(self)
            
            # Info commande
            info_layout = QHBoxLayout()
            
            order_num = str(self.order.get('order_number', 'N/A'))
            status = str(self.order.get('status', 'inconnu'))
            total = float(self.order.get('total_amount', 0))
            
            info_layout.addWidget(QLabel(f"N°: {order_num}"))
            info_layout.addWidget(QLabel(f"Statut: {status}"))
            info_layout.addWidget(QLabel(f"Montant: {total:.2f} {self.currency}"))
            layout.addLayout(info_layout)
            
            # Détails des articles
            self.details_table = QTableWidget()
            self.details_table.setColumnCount(4)
            self.details_table.setHorizontalHeaderLabels(["Article", "Quantité", "Prix U.", "Total"])
            
            items = self.db.get_order_details(self.order.get('id', -1))
            self.details_table.setRowCount(len(items))
            
            for i, item in enumerate(items):
                try:
                    name = str(item.get('name', 'N/A'))
                    qty = int(item.get('quantity', 0))
                    unit_price = float(item.get('unit_price', 0))
                    total_price = float(item.get('total_price', 0))
                    
                    self.details_table.setItem(i, 0, QTableWidgetItem(name))
                    self.details_table.setItem(i, 1, QTableWidgetItem(str(qty)))
                    self.details_table.setItem(i, 2, QTableWidgetItem(f"{unit_price:.2f} {self.currency}"))
                    self.details_table.setItem(i, 3, QTableWidgetItem(f"{total_price:.2f} {self.currency}"))
                except Exception as e:
                    print(f"DEBUG: Erreur ligne détail {i}: {e}")
                    continue
            
            layout.addWidget(self.details_table)
            
            # Boutons
            buttons_layout = QHBoxLayout()
            
            status_check = str(self.order.get('status', 'inconnu')).lower()
            if status_check == 'payé' or status_check == 'paye':
                invoice_btn = QPushButton("Générer Facture PDF")
                invoice_btn.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 4px;")
                invoice_btn.clicked.connect(self.generate_invoice)
                buttons_layout.addWidget(invoice_btn)
                
                print_btn = QPushButton("Imprimer")
                print_btn.setStyleSheet("background-color: #2196F3; color: white; border-radius: 4px;")
                print_btn.clicked.connect(self.print_invoice)
                buttons_layout.addWidget(print_btn)
            
            close_btn = QPushButton("Fermer")
            close_btn.setStyleSheet("background-color: #666; color: white; border-radius: 4px;")
            close_btn.clicked.connect(self.accept)
            buttons_layout.addWidget(close_btn)
            
            layout.addLayout(buttons_layout)
        except Exception as e:
            print(f"DEBUG: Erreur init_ui: {e}")
            layout = QVBoxLayout(self)
            error_label = QLabel(f"Erreur lors du chargement: {str(e)}")
            layout.addWidget(error_label)
            close_btn = QPushButton("Fermer")
            close_btn.clicked.connect(self.accept)
            layout.addWidget(close_btn)

    def generate_invoice(self):
        try:
            invoice_gen = InvoiceGenerator(self.db)
            pdf_path = invoice_gen.generate_invoice(self.order.get('id', -1))
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
            invoice_gen.print_invoice(self.order.get('id', -1))
            QMessageBox.information(self, "Succès", "Facture envoyée à l'impression!")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'impression:\n{str(e)}")
