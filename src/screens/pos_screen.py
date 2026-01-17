from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QPushButton, QLabel, QSpinBox, QTableWidget, QTableWidgetItem,
                             QComboBox, QMessageBox, QDialog, QLineEdit, QTabWidget, QCheckBox,
                             QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from datetime import datetime
from src.utils.invoice_generator import InvoiceGenerator
from src.utils.styles import ModernStyles

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
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Partie gauche : produits
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        
        # Header avec catégories
        header = QLabel("🛒 SÉLECTIONNEZ VOS PRODUITS")
        header.setFont(QFont("Segoe UI", 22, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {ModernStyles.PRIMARY}, stop:1 #8B5CF6);
            color: white;
            padding: 15px;
            border-radius: 8px;
        """)
        left_layout.addWidget(header)
        
        categories_layout = QHBoxLayout()
        categories_label = QLabel("Catégorie:")
        categories_label.setFont(QFont("Segoe UI", 15, QFont.Bold))
        categories_label.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        self.category_combo = QComboBox()
        self.category_combo.addItem("Tous")
        self.category_combo.addItems(["Cafés", "Jus", "Chichas", "Boissons", "Gâteaux"])
        self.category_combo.currentTextChanged.connect(self.load_products)
        self.category_combo.setStyleSheet(ModernStyles.modern_input())
        self.category_combo.setMinimumHeight(65)
        categories_layout.addWidget(categories_label)
        categories_layout.addWidget(self.category_combo, 1)
        categories_layout.setContentsMargins(10, 5, 10, 5)
        left_layout.addLayout(categories_layout)
        
        # Grille des produits
        self.products_grid = QGridLayout()
        self.products_grid.setSpacing(12)
        self.products_grid.setContentsMargins(10, 10, 10, 10)
        left_layout.addLayout(self.products_grid)
        left_layout.addStretch()
        
        main_layout.addLayout(left_layout, 2)
        
        # Partie droite : panier
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        
        # Sélection de table
        table_layout = QHBoxLayout()
        table_label = QLabel("Table:")
        table_label.setFont(QFont("Segoe UI", 15, QFont.Bold))
        table_label.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        table_layout.addWidget(table_label)
        self.table_combo = QComboBox()
        self.table_combo.addItem("Aucune")
        tables = self.db.get_all_tables()
        for table in tables:
            self.table_combo.addItem(table['table_number'], table['id'])
        self.table_combo.setStyleSheet(ModernStyles.modern_input())
        self.table_combo.setMinimumHeight(65)
        table_layout.addWidget(self.table_combo, 1)
        right_layout.addLayout(table_layout)
        
        # Titre du panier
        cart_title = QLabel("🛍️ PANIER")
        cart_title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        cart_title.setAlignment(Qt.AlignCenter)
        cart_title.setStyleSheet(f"""
            background-color: {ModernStyles.SECONDARY};
            color: white;
            padding: 12px;
            border-radius: 8px;
        """)
        right_layout.addWidget(cart_title)
        
        # Tableau du panier
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(6)
        self.cart_table.setHorizontalHeaderLabels(["Article", "Qté", "PU", "Total", "Retour", ""])
        self.cart_table.setColumnWidth(0, 220)
        self.cart_table.setColumnWidth(1, 80)
        self.cart_table.setColumnWidth(2, 100)
        self.cart_table.setColumnWidth(3, 120)
        self.cart_table.setColumnWidth(4, 110)
        self.cart_table.setColumnWidth(5, 70)
        self.cart_table.setStyleSheet(ModernStyles.modern_table())
        self.cart_table.verticalHeader().setVisible(False)
        self.cart_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.cart_table.setRowHeight(0, 55)
        self.cart_table.horizontalHeader().setMinimumHeight(45)
        right_layout.addWidget(self.cart_table)
        
        # Totaux
        totals_layout = QVBoxLayout()
        totals_layout.setSpacing(8)
        totals_layout.setContentsMargins(10, 10, 10, 10)
        
        self.subtotal_label = QLabel(f"Sous-total : 0.00 {self.currency}")
        self.subtotal_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.subtotal_label.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY}; padding: 5px;")
        totals_layout.addWidget(self.subtotal_label)
        
        self.tax_label = QLabel(f"TVA ({self.tax_rate*100:.0f}%) : 0.00 {self.currency}")
        self.tax_label.setFont(QFont("Segoe UI", 15))
        self.tax_label.setStyleSheet(f"color: {ModernStyles.TEXT_SECONDARY}; padding: 5px;")
        totals_layout.addWidget(self.tax_label)
        
        self.total_label = QLabel(f"TOTAL TTC : 0.00 {self.currency}")
        self.total_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.total_label.setAlignment(Qt.AlignCenter)
        self.total_label.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {ModernStyles.SUCCESS}, stop:1 #059669);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-top: 5px;
        """)
        totals_layout.addWidget(self.total_label)
        
        totals_widget = QWidget()
        totals_widget.setLayout(totals_layout)
        totals_widget.setStyleSheet(f"background-color: {ModernStyles.LIGHT_BG}; border-radius: 8px;")
        right_layout.addWidget(totals_widget)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        clear_btn = QPushButton("🗑️ Vider")
        clear_btn.setMinimumHeight(60)
        clear_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        clear_btn.setStyleSheet(ModernStyles.modern_button_outline(ModernStyles.TEXT_SECONDARY))
        clear_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        clear_btn.clicked.connect(self.clear_cart)
        buttons_layout.addWidget(clear_btn)
        
        payment_btn = QPushButton("💳 PAYER")
        payment_btn.setMinimumHeight(60)
        payment_btn.setFont(QFont("Segoe UI", 17, QFont.Bold))
        payment_btn.setStyleSheet(ModernStyles.large_action_button(ModernStyles.PRIMARY))
        payment_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        payment_btn.clicked.connect(self.process_payment)
        buttons_layout.addWidget(payment_btn)
        
        right_layout.addLayout(buttons_layout)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        main_layout.addLayout(right_layout, 1)
        
        self.setStyleSheet(f"background-color: {ModernStyles.LIGHT_BG};")
        self.load_products()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Rebuild product grid responsively on resize
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
        
        # responsive columns: adapt to window width (left pane ~66% of total)
        left_width = max(600, int(self.width() * 0.66) - 40)
        columns = 3
        if left_width >= 1200:
            columns = 4
        elif left_width < 900:
            columns = 2

        # compute button size
        spacing = self.products_grid.spacing() or 12
        btn_width = max(160, (left_width - (columns - 1) * spacing) // columns - 12)
        btn_height = int(btn_width * 0.56)

        row, col = 0, 0
        for product in products:
            btn = QPushButton()
            btn.setMinimumSize(btn_width, btn_height)
            btn.setMaximumSize(btn_width + 40, btn_height + 30)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
            
            # Vérifier le stock
            stock = product.get('quantity', 0) or 0
            stock_text = f"📦 {stock}" if stock > 0 else "⚠️ Épuisé"
            
            # nicer layout: name on top, price line, stock badge
            btn.setText(f"{product['name']}\n\n{product['price']:.2f} {self.currency}    {stock_text}")
            
            # Style selon le stock
            if stock == 0:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #FFF5F5;
                        border: 2px solid {ModernStyles.DANGER};
                        border-radius: 10px;
                        color: {ModernStyles.TEXT_SECONDARY};
                        padding: 10px;
                        text-align: center;
                    }}
                """)
                btn.setEnabled(False)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {ModernStyles.CARD_BG};
                        border: 1px solid {ModernStyles.BORDER};
                        border-radius: 12px;
                        color: {ModernStyles.TEXT_PRIMARY};
                        padding: 8px;
                        text-align: center;
                    }}
                    QPushButton:hover {{
                        background-color: {ModernStyles.PRIMARY};
                        color: white;
                        border: 1px solid {ModernStyles.PRIMARY};
                    }}
                    QPushButton:pressed {{
                        background-color: {ModernStyles._darken(ModernStyles.PRIMARY, 10)};
                    }}
                """)
                btn.clicked.connect(lambda checked, p=product: self.add_to_cart(p))
            
            self.products_grid.addWidget(btn, row, col)
            col += 1
            if col >= columns:
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
            # Vérifier si c'est un retour
            is_return = item.get('is_return', False)
            total_price = item['quantity'] * item['unit_price']
            # Si c'est un retour, le prix ne compte pas dans le subtotal
            if not is_return:
                subtotal += total_price
            
            self.cart_table.setItem(i, 0, QTableWidgetItem(item['name']))
            
            qty_spinbox = QSpinBox()
            qty_spinbox.setValue(item['quantity'])
            qty_spinbox.setMinimum(1)
            qty_spinbox.valueChanged.connect(lambda val, idx=i: self.update_quantity(idx, val))
            self.cart_table.setCellWidget(i, 1, qty_spinbox)
            
            # Afficher le prix réduit si c'est un retour
            display_price = "--" if is_return else f"{item['unit_price']:.2f} {self.currency}"
            self.cart_table.setItem(i, 2, QTableWidgetItem(display_price))
            
            display_total = "(Gratuit)" if is_return else f"{total_price:.2f} {self.currency}"
            self.cart_table.setItem(i, 3, QTableWidgetItem(display_total))
            
            # Bouton Retour
            return_btn = QPushButton("✓ Retour" if not is_return else "✓✓ Retour")
            return_btn.setFixedHeight(34)
            return_btn.setStyleSheet(f"background-color: {'#10B981' if is_return else '#EF4444'}; color: white; border: none; border-radius: 6px; font-weight: bold; padding: 6px 10px;")
            return_btn.clicked.connect(lambda checked, idx=i: self.toggle_return(idx))
            self.cart_table.setCellWidget(i, 4, return_btn)

            delete_btn = QPushButton("✕")
            delete_btn.setFixedSize(36, 34)
            delete_btn.setStyleSheet(ModernStyles.icon_button())
            delete_btn.clicked.connect(lambda checked, idx=i: self.remove_from_cart(idx))
            self.cart_table.setCellWidget(i, 5, delete_btn)
        
        tax = subtotal * self.tax_rate
        total = subtotal + tax
        
        self.subtotal_label.setText(f"Sous-total : {subtotal:.2f} {self.currency}")
        self.tax_label.setText(f"TVA ({self.tax_rate*100:.0f}%) : {tax:.2f} {self.currency}")
        self.total_label.setText(f"TOTAL TTC : {total:.2f} {self.currency}")

    def toggle_return(self, index):
        """Marquer/démarquer un article comme retour/remplacement"""
        item = self.current_order[index]
        item['is_return'] = not item.get('is_return', False)
        self.update_cart_display()

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
        try:
            currency = db.get_setting('currency', 'TND')
            if isinstance(currency, dict):
                self.currency = currency.get('value', 'TND')
            else:
                self.currency = currency if currency else 'TND'
        except:
            self.currency = 'TND'
        try:
            tax = db.get_setting('tax_rate', '20')
            if isinstance(tax, dict):
                tax = tax.get('value', '20')
            self.tax_rate = float(tax) / 100 if tax else 0.20
        except:
            self.tax_rate = 0.20
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("💳 Paiement")
        self.setGeometry(400, 300, 500, 480)
        self.setStyleSheet(f"background-color: white;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Titre
        title = QLabel("Résumé de la commande")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        total = sum(item['quantity'] * item['unit_price'] for item in self.order_items)
        tax = total * self.tax_rate
        total_with_tax = total + tax
        
        # Détails du montant
        details_layout = QVBoxLayout()
        details_layout.setSpacing(8)
        
        subtotal_label = QLabel(f"Sous-total : {total:.2f} {self.currency}")
        subtotal_label.setFont(QFont("Segoe UI", 11))
        subtotal_label.setStyleSheet(f"color: {ModernStyles.TEXT_SECONDARY};")
        details_layout.addWidget(subtotal_label)
        
        tax_label = QLabel(f"TVA ({self.tax_rate*100:.0f}%) : {tax:.2f} {self.currency}")
        tax_label.setFont(QFont("Segoe UI", 11))
        tax_label.setStyleSheet(f"color: {ModernStyles.TEXT_SECONDARY};")
        details_layout.addWidget(tax_label)
        
        layout.addLayout(details_layout)
        
        # Total avec gradient
        total_label = QLabel(f"Total TTC : {total_with_tax:.2f} {self.currency}")
        total_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        total_label.setAlignment(Qt.AlignCenter)
        total_label.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {ModernStyles.PRIMARY}, stop:1 #8B5CF6); color: white; padding: 15px; border-radius: 8px;")
        layout.addWidget(total_label)
        
        # Méthode de paiement
        method_label = QLabel("🔵 Mode de paiement :")
        method_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        method_label.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        layout.addWidget(method_label)
        
        self.payment_method = QComboBox()
        self.payment_method.addItems(["💵 Espèces", "💳 Carte", "✓ Chèque"])
        self.payment_method.currentTextChanged.connect(self.on_payment_method_changed)
        self.payment_method.setStyleSheet(ModernStyles.modern_input())
        self.payment_method.setMinimumHeight(40)
        layout.addWidget(self.payment_method)
        
        # Montant reçu (pour espèces)
        self.amount_received_layout = QVBoxLayout()
        amount_label = QLabel("💰 Montant reçu :")
        amount_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        amount_label.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        self.amount_received_layout.addWidget(amount_label)
        
        self.amount_received_input = QLineEdit()
        self.amount_received_input.setPlaceholderText("0.00")
        self.amount_received_input.setFont(QFont("Segoe UI", 12))
        self.amount_received_input.textChanged.connect(self.calculate_change)
        self.amount_received_input.setStyleSheet(ModernStyles.modern_input())
        self.amount_received_input.setMinimumHeight(40)
        self.amount_received_layout.addWidget(self.amount_received_input)
        layout.addLayout(self.amount_received_layout)
        
        # Monnaie
        self.change_label = QLabel("Monnaie : 0.00 " + self.currency)
        self.change_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.change_label.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10B981, stop:1 #059669); color: white; padding: 10px; border-radius: 6px; text-align: center;")
        self.change_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.change_label)
        
        # Paiement fractionné
        self.split_checkbox = QCheckBox("🔀 Paiement fractionné")
        self.split_checkbox.setFont(QFont("Segoe UI", 11))
        self.split_checkbox.stateChanged.connect(self.on_split_changed)
        self.split_checkbox.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        layout.addWidget(self.split_checkbox)
        
        split_layout = QHBoxLayout()
        split_label = QLabel("Nombre de parts:")
        split_label.setFont(QFont("Segoe UI", 11))
        split_label.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        split_layout.addWidget(split_label)
        
        self.split_number_input = QSpinBox()
        self.split_number_input.setRange(2, 10)
        self.split_number_input.setValue(2)
        self.split_number_input.setEnabled(False)
        self.split_number_input.setStyleSheet(ModernStyles.modern_input())
        self.split_number_input.setMinimumHeight(35)
        self.split_number_input.setMaximumWidth(100)
        split_layout.addWidget(self.split_number_input)
        split_layout.addStretch()
        layout.addLayout(split_layout)
        
        layout.addStretch()
        
        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        cancel_btn = QPushButton("❌ Annuler")
        cancel_btn.setFixedHeight(45)
        cancel_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        cancel_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.TEXT_SECONDARY))
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        partial_btn = QPushButton("⏸️ Paiement partiel")
        partial_btn.setFixedHeight(45)
        partial_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        partial_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.INFO))
        partial_btn.clicked.connect(self.partial_payment)
        buttons_layout.addWidget(partial_btn)
        
        confirm_btn = QPushButton("✓ Confirmer le paiement")
        confirm_btn.setFixedHeight(45)
        confirm_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        confirm_btn.setStyleSheet(ModernStyles.large_action_button(ModernStyles.SUCCESS))
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
                self.change_label.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10B981, stop:1 #059669); color: white; padding: 10px; border-radius: 6px;")
            else:
                self.change_label.setText(f"Manquant : {abs(change):.2f} {self.currency}")
                self.change_label.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #EF4444, stop:1 #DC2626); color: white; padding: 10px; border-radius: 6px;")
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
