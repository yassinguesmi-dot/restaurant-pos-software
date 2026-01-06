from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QPushButton, QLabel, QSpinBox, QTableWidget, QTableWidgetItem,
                             QComboBox, QMessageBox, QDialog, QLineEdit, QTabWidget, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from datetime import datetime
from src.utils.invoice_generator import InvoiceGenerator

class POSScreen(QWidget):
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self.current_order = []
        self.primary_color = "#FF9500"
        self.currency = db.get_setting('currency', 'TND')
        self.tax_rate = float(db.get_setting('tax_rate', '20')) / 100
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        
        # Partie gauche : produits
        left_layout = QVBoxLayout()
        
        # Header avec catégories
        header = QLabel("SÉLECTIONNEZ VOS PRODUITS")
        header.setFont(QFont("Arial", 14, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(f"background-color: #C8A882; color: white; padding: 15px;")
        left_layout.addWidget(header)
        
        categories_layout = QHBoxLayout()
        categories_label = QLabel("Catégorie :")
        categories_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.category_combo = QComboBox()
        self.category_combo.addItem("Tous")
        self.category_combo.addItems(["Cafés", "Jus", "Chichas", "Boissons", "Gâteaux"])
        self.category_combo.currentTextChanged.connect(self.load_products)
        self.category_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #D4A574;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        categories_layout.addWidget(categories_label)
        categories_layout.addWidget(self.category_combo)
        categories_layout.addStretch()
        categories_layout.setContentsMargins(15, 10, 15, 10)
        left_layout.addLayout(categories_layout)
        
        # Grille des produits
        self.products_grid = QGridLayout()
        self.products_grid.setSpacing(12)
        self.products_grid.setContentsMargins(15, 15, 15, 15)
        left_layout.addLayout(self.products_grid)
        left_layout.addStretch()
        
        main_layout.addLayout(left_layout, 2)
        
        # Partie droite : panier
        right_layout = QVBoxLayout()
        
        # Sélection de table
        table_layout = QHBoxLayout()
        table_layout.addWidget(QLabel("Table:"))
        self.table_combo = QComboBox()
        self.table_combo.addItem("Aucune")
        tables = self.db.get_all_tables()
        for table in tables:
            self.table_combo.addItem(table['table_number'], table['id'])
        self.table_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #D4A574;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        table_layout.addWidget(self.table_combo)
        table_layout.addStretch()
        right_layout.addLayout(table_layout)
        
        # Titre du panier
        cart_title = QLabel("PANIER")
        cart_title.setFont(QFont("Arial", 14, QFont.Bold))
        cart_title.setAlignment(Qt.AlignCenter)
        cart_title.setStyleSheet(f"background-color: #C8A882; color: white; padding: 15px;")
        right_layout.addWidget(cart_title)
        
        # Tableau du panier
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["Article", "Qté", "PU", "Total", ""])
        self.cart_table.setColumnWidth(0, 120)
        self.cart_table.setColumnWidth(1, 40)
        self.cart_table.setColumnWidth(2, 60)
        self.cart_table.setColumnWidth(3, 70)
        self.cart_table.setColumnWidth(4, 30)
        self.cart_table.setStyleSheet("""
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
        right_layout.addWidget(self.cart_table)
        
        # Totaux
        totals_layout = QVBoxLayout()
        
        self.subtotal_label = QLabel(f"Sous-total : 0.00 {self.currency}")
        self.subtotal_label.setFont(QFont("Arial", 11, QFont.Bold))
        totals_layout.addWidget(self.subtotal_label)
        
        self.tax_label = QLabel(f"TVA ({self.tax_rate*100:.0f}%) : 0.00 {self.currency}")
        self.tax_label.setFont(QFont("Arial", 11))
        totals_layout.addWidget(self.tax_label)
        
        self.total_label = QLabel(f"TOTAL TTC : 0.00 {self.currency}")
        self.total_label.setFont(QFont("Arial", 13, QFont.Bold))
        self.total_label.setStyleSheet(f"background-color: #D4A574; color: white; padding: 10px; border-radius: 3px;")
        totals_layout.addWidget(self.total_label)
        
        totals_widget = QWidget()
        totals_widget.setLayout(totals_layout)
        totals_widget.setStyleSheet("background-color: #F8F6F3;")
        right_layout.addWidget(totals_widget)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Vider")
        clear_btn.setFixedHeight(45)
        clear_btn.setFont(QFont("Arial", 11, QFont.Bold))
        clear_btn.setStyleSheet("""
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
        clear_btn.clicked.connect(self.clear_cart)
        buttons_layout.addWidget(clear_btn)
        
        payment_btn = QPushButton("PAYER")
        payment_btn.setFixedHeight(45)
        payment_btn.setFont(QFont("Arial", 12, QFont.Bold))
        payment_btn.setStyleSheet("""
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
        payment_btn.clicked.connect(self.process_payment)
        buttons_layout.addWidget(payment_btn)
        
        right_layout.addLayout(buttons_layout)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        main_layout.addLayout(right_layout, 1)
        
        self.setStyleSheet("background-color: #F8F6F3;")
        self.load_products()

    def load_products(self):
        # Vider la grille
        while self.products_grid.count():
            self.products_grid.takeAt(0).widget().deleteLater()
        
        category = self.category_combo.currentText()
        
        if category == "Tous":
            products = self.db.get_all_products()
        else:
            products = self.db.get_products_by_category(category)
        
        row, col = 0, 0
        for product in products:
            btn = QPushButton()
            btn.setFixedSize(140, 100)
            btn.setFont(QFont("Arial", 10, QFont.Bold))
            
            # Vérifier le stock
            stock = product.get('quantity', 0) or 0
            stock_text = f"\nStock: {stock}" if stock > 0 else "\n⚠️ Épuisé"
            
            btn.setText(f"{product['name']}\n{product['price']:.2f} {self.currency}{stock_text}")
            
            # Style selon le stock
            if stock == 0:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #FFEBEE;
                        border: 2px solid #F44336;
                        border-radius: 5px;
                        color: #2C2C2C;
                    }}
                """)
                btn.setEnabled(False)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: white;
                        border: 2px solid #D4A574;
                        border-radius: 5px;
                        color: #2C2C2C;
                    }}
                    QPushButton:hover {{
                        background-color: #F8F6F3;
                        border: 2px solid #C8A882;
                    }}
                """)
                btn.clicked.connect(lambda checked, p=product: self.add_to_cart(p))
            
            self.products_grid.addWidget(btn, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

    def add_to_cart(self, product):
        # Vérifier le stock
        stock, _ = self.db.get_product_stock(product['id'])
        if stock == 0:
            QMessageBox.warning(self, "Stock épuisé", f"Le produit '{product['name']}' est épuisé!")
            return
        
        # Vérifier si le produit est déjà dans le panier
        for i, item in enumerate(self.current_order):
            if item['product_id'] == product['id']:
                # Vérifier le stock disponible
                current_qty = item['quantity']
                if current_qty + 1 > stock:
                    QMessageBox.warning(self, "Stock insuffisant", 
                                      f"Stock disponible: {stock}\nQuantité dans le panier: {current_qty}")
                    return
                self.current_order[i]['quantity'] += 1
                self.update_cart_display()
                return
        
        # Ajouter le nouveau produit
        self.current_order.append({
            'product_id': product['id'],
            'name': product['name'],
            'quantity': 1,
            'unit_price': product['price']
        })
        
        self.update_cart_display()

    def update_cart_display(self):
        self.cart_table.setRowCount(len(self.current_order))
        
        subtotal = 0
        for i, item in enumerate(self.current_order):
            total_price = item['quantity'] * item['unit_price']
            subtotal += total_price
            
            self.cart_table.setItem(i, 0, QTableWidgetItem(item['name']))
            
            qty_spinbox = QSpinBox()
            qty_spinbox.setValue(item['quantity'])
            qty_spinbox.setMinimum(1)
            qty_spinbox.valueChanged.connect(lambda val, idx=i: self.update_quantity(idx, val))
            self.cart_table.setCellWidget(i, 1, qty_spinbox)
            
            self.cart_table.setItem(i, 2, QTableWidgetItem(f"{item['unit_price']:.2f} {self.currency}"))
            self.cart_table.setItem(i, 3, QTableWidgetItem(f"{total_price:.2f} {self.currency}"))
            
            delete_btn = QPushButton("✕")
            delete_btn.setFixedWidth(30)
            delete_btn.clicked.connect(lambda checked, idx=i: self.remove_from_cart(idx))
            self.cart_table.setCellWidget(i, 4, delete_btn)
        
        tax = subtotal * self.tax_rate
        total = subtotal + tax
        
        self.subtotal_label.setText(f"Sous-total : {subtotal:.2f} {self.currency}")
        self.tax_label.setText(f"TVA ({self.tax_rate*100:.0f}%) : {tax:.2f} {self.currency}")
        self.total_label.setText(f"TOTAL TTC : {total:.2f} {self.currency}")

    def update_quantity(self, index, value):
        item = self.current_order[index]
        stock, _ = self.db.get_product_stock(item['product_id'])
        if value > stock:
            QMessageBox.warning(self, "Stock insuffisant", 
                              f"Stock disponible: {stock}")
            # Réinitialiser à la valeur maximale possible
            qty_spinbox = self.cart_table.cellWidget(index, 1)
            if qty_spinbox:
                qty_spinbox.setValue(min(value - 1, stock))
            return
        self.current_order[index]['quantity'] = value
        self.update_cart_display()

    def remove_from_cart(self, index):
        del self.current_order[index]
        self.update_cart_display()

    def clear_cart(self):
        self.current_order = []
        self.update_cart_display()

    def process_payment(self):
        if not self.current_order:
            QMessageBox.warning(self, "Erreur", "Le panier est vide !")
            return
        
        # Vérifier le stock une dernière fois avant le paiement
        for item in self.current_order:
            stock, _ = self.db.get_product_stock(item['product_id'])
            if stock < item['quantity']:
                QMessageBox.warning(self, "Stock insuffisant", 
                                  f"Stock insuffisant pour '{item['name']}'\nStock disponible: {stock}")
                return
        
        table_id = self.table_combo.currentData()
        dialog = PaymentDialog(self.current_order, self.db, table_id, self.current_user)
        if dialog.exec_() == QDialog.Accepted:
            self.clear_cart()
            QMessageBox.information(self, "Succès", "Paiement effectué avec succès !")


class PaymentDialog(QDialog):
    def __init__(self, order_items, db, table_id=None, current_user=None):
        super().__init__()
        self.order_items = order_items
        self.db = db
        self.table_id = table_id
        self.current_user = current_user
        self.primary_color = "#C8A882"
        self.currency = db.get_setting('currency', 'TND')
        self.tax_rate = float(db.get_setting('tax_rate', '20')) / 100
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Paiement")
        self.setGeometry(400, 300, 400, 350)
        self.setStyleSheet("background-color: #F8F6F3;")
        layout = QVBoxLayout(self)
        
        # Résumé
        summary = QLabel("Résumé de la commande:")
        summary.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(summary)
        
        total = sum(item['quantity'] * item['unit_price'] for item in self.order_items)
        tax = total * self.tax_rate
        total_with_tax = total + tax
        
        subtotal_label = QLabel(f"Sous-total : {total:.2f} {self.currency}")
        subtotal_label.setFont(QFont("Arial", 11))
        layout.addWidget(subtotal_label)
        
        tax_label = QLabel(f"TVA ({self.tax_rate*100:.0f}%) : {tax:.2f} {self.currency}")
        tax_label.setFont(QFont("Arial", 11))
        layout.addWidget(tax_label)
        
        total_label = QLabel(f"Total TTC : {total_with_tax:.2f} {self.currency}")
        total_label.setFont(QFont("Arial", 14, QFont.Bold))
        total_label.setStyleSheet(f"background-color: {self.primary_color}; color: white; padding: 10px; border-radius: 3px;")
        layout.addWidget(total_label)
        
        # Méthode de paiement
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("Mode de paiement :"))
        self.payment_method = QComboBox()
        self.payment_method.addItems(["Espèces", "Carte", "Chèque"])
        self.payment_method.currentTextChanged.connect(self.on_payment_method_changed)
        self.payment_method.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #D4A574;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        method_layout.addWidget(self.payment_method)
        layout.addLayout(method_layout)
        
        # Montant reçu (pour espèces)
        self.amount_received_layout = QHBoxLayout()
        self.amount_received_layout.addWidget(QLabel("Montant reçu :"))
        self.amount_received_input = QLineEdit()
        self.amount_received_input.setPlaceholderText("0.00")
        self.amount_received_input.textChanged.connect(self.calculate_change)
        self.amount_received_layout.addWidget(self.amount_received_input)
        layout.addLayout(self.amount_received_layout)
        
        # Monnaie
        self.change_label = QLabel("Monnaie : 0.00 " + self.currency)
        self.change_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.change_label.setStyleSheet("color: #4CAF50;")
        layout.addWidget(self.change_label)
        
        # Paiement fractionné
        self.split_checkbox = QCheckBox("Paiement fractionné")
        self.split_checkbox.stateChanged.connect(self.on_split_changed)
        layout.addWidget(self.split_checkbox)
        
        self.split_number_input = QSpinBox()
        self.split_number_input.setRange(2, 10)
        self.split_number_input.setValue(2)
        self.split_number_input.setEnabled(False)
        split_layout = QHBoxLayout()
        split_layout.addWidget(QLabel("Nombre de parts:"))
        split_layout.addWidget(self.split_number_input)
        layout.addLayout(split_layout)
        
        layout.addStretch()
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #999999;
                color: white;
                border: none;
                border-radius: 3px;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        partial_btn = QPushButton("Paiement partiel")
        partial_btn.setFixedHeight(40)
        partial_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 3px;
            }
        """)
        partial_btn.clicked.connect(self.partial_payment)
        buttons_layout.addWidget(partial_btn)
        
        confirm_btn = QPushButton("Confirmer le paiement")
        confirm_btn.setFixedHeight(40)
        confirm_btn.setFont(QFont("Arial", 11, QFont.Bold))
        confirm_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.primary_color};
                color: white;
                border: none;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: #B8985F;
            }}
        """)
        confirm_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(confirm_btn)
        
        layout.addLayout(buttons_layout)
        
        # Initialiser l'affichage
        self.on_payment_method_changed()
        self.total_amount = total_with_tax

    def on_payment_method_changed(self):
        method = self.payment_method.currentText()
        if method == "Espèces":
            self.amount_received_input.setEnabled(True)
            self.amount_received_input.setVisible(True)
            self.change_label.setVisible(True)
        else:
            self.amount_received_input.setEnabled(False)
            self.amount_received_input.setVisible(False)
            self.change_label.setVisible(False)

    def on_split_changed(self):
        self.split_number_input.setEnabled(self.split_checkbox.isChecked())

    def calculate_change(self):
        try:
            amount_received = float(self.amount_received_input.text() or 0)
            change = amount_received - self.total_amount
            if change >= 0:
                self.change_label.setText(f"Monnaie : {change:.2f} {self.currency}")
                self.change_label.setStyleSheet("color: #4CAF50;")
            else:
                self.change_label.setText(f"Manquant : {abs(change):.2f} {self.currency}")
                self.change_label.setStyleSheet("color: #F44336;")
        except ValueError:
            self.change_label.setText("Monnaie : 0.00 " + self.currency)

    def accept(self):
        try:
            total = sum(item['quantity'] * item['unit_price'] for item in self.order_items)
            total_with_tax = total * (1 + self.tax_rate)
            
            # Créer la commande
            order_id, order_number, invoice_number, _ = self.db.create_order(
                self.order_items, 
                table_id=self.table_id,
                user_id=self.current_user['id'] if self.current_user else None
            )
            
            # Calculer le montant reçu et le change
            payment_method = self.payment_method.currentText()
            amount_received = None
            change_amount = None
            
            if payment_method == "Espèces":
                try:
                    amount_received = float(self.amount_received_input.text() or 0)
                    if amount_received < total_with_tax:
                        QMessageBox.warning(self, "Erreur", 
                                          f"Montant insuffisant!\nReçu: {amount_received:.2f}\nTotal: {total_with_tax:.2f}")
                        return
                    change_amount = amount_received - total_with_tax
                except ValueError:
                    QMessageBox.warning(self, "Erreur", "Montant reçu invalide!")
                    return
            
            # Paiement fractionné
            is_split = self.split_checkbox.isChecked()
            split_number = self.split_number_input.value() if is_split else None
            
            # Enregistrer le paiement
            self.db.record_payment(
                order_id, 
                total_with_tax, 
                payment_method,
                amount_received=amount_received,
                change_amount=change_amount,
                is_split=is_split,
                split_number=split_number,
                is_partial=False
            )
            
            # Générer la facture automatiquement
            try:
                invoice_gen = InvoiceGenerator(self.db)
                pdf_path = invoice_gen.generate_invoice(order_id)
                reply = QMessageBox.question(
                    self, 
                    "Paiement effectué!", 
                    f"Paiement effectué avec succès!\n\nFacture: {invoice_number}\nCommande: {order_number}\n\nFacture générée: {pdf_path}\n\nVoulez-vous ouvrir la facture?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    invoice_gen.print_invoice(order_id)
            except Exception as e:
                QMessageBox.warning(self, "Avertissement", 
                                  f"Paiement effectué mais erreur lors de la génération de la facture:\n{str(e)}")
            
            super().accept()
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du paiement: {str(e)}")

    def partial_payment(self):
        try:
            total = sum(item['quantity'] * item['unit_price'] for item in self.order_items)
            total_with_tax = total * (1 + self.tax_rate)
            
            # Créer la commande
            order_id, order_number, invoice_number, _ = self.db.create_order(
                self.order_items, 
                table_id=self.table_id,
                user_id=self.current_user['id'] if self.current_user else None
            )
            
            # Paiement partiel
            payment_method = self.payment_method.currentText()
            amount_received = None
            change_amount = None
            
            if payment_method == "Espèces":
                try:
                    amount_received = float(self.amount_received_input.text() or 0)
                    if amount_received > total_with_tax:
                        change_amount = amount_received - total_with_tax
                except ValueError:
                    pass
            
            self.db.record_payment(
                order_id, 
                total_with_tax, 
                payment_method,
                amount_received=amount_received,
                change_amount=change_amount,
                is_split=False,
                split_number=None,
                is_partial=True
            )
            
            QMessageBox.information(self, "Succès", 
                                  f"Paiement partiel enregistré!\nFacture: {invoice_number}\nCommande: {order_number}")
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {str(e)}")
