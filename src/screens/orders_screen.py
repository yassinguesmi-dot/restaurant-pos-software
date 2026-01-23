from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
                             QTableWidgetItem, QPushButton, QDialog, QMessageBox,
                             QLineEdit, QDateEdit, QComboBox, QSizePolicy, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.utils.invoice_generator import InvoiceGenerator
from src.utils.styles import ModernStyles

def _safe_get(obj, key, default=None):
    try:
        if obj is None:
            return default
        if hasattr(obj, 'get'):
            return obj.get(key, default)
        if hasattr(obj, 'keys') and key in obj.keys():
            v = obj[key]
            return default if v is None else v
        return getattr(obj, key, default)
    except Exception:
        return default

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
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        # Header card with title and filters
        header = QFrame()
        header.setStyleSheet(ModernStyles.card_style())
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 12, 12, 12)
        header_layout.setSpacing(10)

        title = QLabel("Historique des Commandes")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet(ModernStyles.modern_label('large'))
        header_layout.addWidget(title)

        # Spacer between title and filters
        header_layout.addStretch()

        # Search / filter controls
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher par N° commande, facture ou client...")
        self.search_input.setFixedWidth(360)
        self.search_input.setStyleSheet(ModernStyles.modern_input())
        self.search_input.returnPressed.connect(self.load_orders)
        header_layout.addWidget(self.search_input)

        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setStyleSheet(ModernStyles.modern_input())
        self.date_filter.setDisplayFormat("yyyy-MM-dd")
        header_layout.addWidget(self.date_filter)

        refresh_btn = QPushButton("🔄")
        refresh_btn.setToolTip("Rafraîchir")
        refresh_btn.setFixedSize(44, 44)
        refresh_btn.setStyleSheet(ModernStyles.icon_button())
        refresh_btn.clicked.connect(self.load_orders)
        header_layout.addWidget(refresh_btn)

        layout.addWidget(header)

        # Table card
        table_card = QFrame()
        table_card.setStyleSheet(ModernStyles.card_style())
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(8, 8, 8, 8)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(7)
        self.orders_table.setHorizontalHeaderLabels(["N° Commande", "N° Facture", "Date", "Montant", "Statut", "Paiement", "Actions"])
        self.orders_table.setStyleSheet(ModernStyles.modern_table())
        self.orders_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.orders_table.setMinimumHeight(320)
        # sensible default column widths
        self.orders_table.setColumnWidth(0, 180)
        self.orders_table.setColumnWidth(1, 120)
        self.orders_table.setColumnWidth(2, 110)
        self.orders_table.setColumnWidth(3, 120)
        self.orders_table.setColumnWidth(4, 100)
        self.orders_table.setColumnWidth(5, 90)

        table_layout.addWidget(self.orders_table)
        layout.addWidget(table_card)

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
                    order_number = str(_safe_get(order, 'order_number', f"Cmd {_safe_get(order,'id', i)}"))
                    invoice_num = str(_safe_get(order, 'invoice_number', '-'))
                    created_at = str(_safe_get(order, 'created_at', '-'))[:10]
                    total_amount = float(_safe_get(order, 'total_amount', 0) or 0)
                    status = str(_safe_get(order, 'status', 'inconnu'))
                    payment_method = str(_safe_get(order, 'payment_method', '-'))
                    
                    self.orders_table.setItem(i, 0, QTableWidgetItem(order_number))
                    self.orders_table.setItem(i, 1, QTableWidgetItem(invoice_num))
                    self.orders_table.setItem(i, 2, QTableWidgetItem(created_at))
                    self.orders_table.setItem(i, 3, QTableWidgetItem(f"{total_amount:.2f} {self.currency}"))
                    self.orders_table.setItem(i, 4, QTableWidgetItem(status))
                    self.orders_table.setItem(i, 5, QTableWidgetItem(payment_method if payment_method != 'None' else '-'))
                    
                    # Boutons d'action
                    actions_layout = QHBoxLayout()
                    
                    details_btn = QPushButton("Voir")
                    details_btn.setFixedWidth(64)
                    details_btn.setStyleSheet(ModernStyles.table_button("edit"))
                    details_btn.clicked.connect(lambda checked, o=order: self.show_order_details(o))
                    actions_layout.addWidget(details_btn)
                    
                    if status.lower() == 'payé':
                        invoice_btn = QPushButton("Facture")
                        invoice_btn.setFixedWidth(72)
                        invoice_btn.setStyleSheet(ModernStyles.table_button("add"))
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
            order_id = _safe_get(order, 'id', -1)
            pdf_path = invoice_gen.generate_invoice(order_id)
            QMessageBox.information(
                self, 
                "Succès", 
                f"Facture générée avec succès!\n\nFichier: {pdf_path}\n\nSouhaitez-vous l'imprimer?",
                QMessageBox.Yes | QMessageBox.No
            )
            # Ouvrir le PDF
            invoice_gen.print_invoice(order_id)
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
            order_number = str(_safe_get(self.order, 'order_number', f"Cmd {_safe_get(self.order,'id','?')}"))
            self.setWindowTitle(f"Détails de la commande {order_number}")
            self.setGeometry(300, 200, 600, 400)
            
            layout = QVBoxLayout(self)
            
            # Info commande
            info_layout = QHBoxLayout()
            
            order_num = str(_safe_get(self.order, 'order_number', 'N/A'))
            status = str(_safe_get(self.order, 'status', 'inconnu'))
            total = float(_safe_get(self.order, 'total_amount', 0) or 0)
            
            info_layout.addWidget(QLabel(f"N°: {order_num}"))
            info_layout.addWidget(QLabel(f"Statut: {status}"))
            info_layout.addWidget(QLabel(f"Montant: {total:.2f} {self.currency}"))
            layout.addLayout(info_layout)
            
            # Détails des articles
            self.details_table = QTableWidget()
            self.details_table.setColumnCount(4)
            self.details_table.setHorizontalHeaderLabels(["Article", "Quantité", "Prix U.", "Total"])
            
            items = self.db.get_order_details(_safe_get(self.order, 'id', -1))
            self.details_table.setRowCount(len(items))
            
            for i, item in enumerate(items):
                try:
                    name = str(_safe_get(item, 'name', 'N/A'))
                    qty = int(_safe_get(item, 'quantity', 0) or 0)
                    unit_price = float(_safe_get(item, 'unit_price', 0) or 0)
                    total_price = float(_safe_get(item, 'total_price', 0) or 0)
                    
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
            
            status_check = str(_safe_get(self.order, 'status', 'inconnu')).lower()
            if status_check == 'payé' or status_check == 'paye':
                invoice_btn = QPushButton("Générer Facture PDF")
                invoice_btn.setStyleSheet(ModernStyles.dialog_button(is_primary=True))
                invoice_btn.clicked.connect(self.generate_invoice)
                buttons_layout.addWidget(invoice_btn)

                print_btn = QPushButton("Imprimer")
                print_btn.setStyleSheet(ModernStyles.dialog_button(is_primary=False))
                print_btn.clicked.connect(self.print_invoice)
                buttons_layout.addWidget(print_btn)
            
            close_btn = QPushButton("Fermer")
            close_btn.setStyleSheet(ModernStyles.dialog_button(is_primary=False))
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
            order_id = _safe_get(self.order, 'id', -1)
            invoice_gen.print_invoice(order_id)
            QMessageBox.information(self, "Succès", "Facture envoyée à l'impression!")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'impression:\n{str(e)}")
