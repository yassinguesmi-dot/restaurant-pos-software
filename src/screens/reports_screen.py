from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QDateEdit, QTableWidget, QTableWidgetItem, QComboBox,
                             QFileDialog, QMessageBox, QTabWidget)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from src.utils.invoice_generator import InvoiceGenerator
from src.utils.styles import ModernStyles

class ReportsScreen(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.primary_color = "#FF9500"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Titre
        title = QLabel("📊 Rapports et Statistiques")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        subtitle = QLabel("Analysez vos ventes et performances")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet(f"color: {ModernStyles.TEXT_SECONDARY};")
        layout.addWidget(subtitle)
        
        # Tabs pour différents types de rapports
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid #E5E7EB;
                background-color: white;
            }}
            QTabBar::tab {{
                background-color: #F3F4F6;
                color: {ModernStyles.TEXT_PRIMARY};
                padding: 10px 20px;
                margin-right: 2px;
                border: 1px solid #E5E7EB;
                border-bottom: none;
                font-weight: bold;
                font-family: Segoe UI;
            }}
            QTabBar::tab:selected {{
                background-color: {ModernStyles.PRIMARY};
                color: white;
                border-bottom: 3px solid {ModernStyles.PRIMARY};
            }}
            QTabBar::tab:hover {{
                background-color: #E5E7EB;
            }}
        """)
        
        # Tab 1: Rapport journalier
        daily_tab = self.create_daily_report_tab()
        tabs.addTab(daily_tab, "📅 Rapport Journalier")
        
        # Tab 2: Rapport mensuel
        monthly_tab = self.create_monthly_report_tab()
        tabs.addTab(monthly_tab, "📆 Rapport Mensuel")
        
        # Tab 3: Produits les plus vendus
        products_tab = self.create_products_report_tab()
        tabs.addTab(products_tab, "📦 Produits")
        
        layout.addWidget(tabs)

    def create_daily_report_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Section Filtres avec style clair
        filter_frame = QWidget()
        filter_frame.setStyleSheet(f"background-color: white; border-radius: 8px; border: 1px solid #E5E7EB;")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(15, 15, 15, 15)
        
        date_label = QLabel("Date :")
        date_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        date_label.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        filter_layout.addWidget(date_label)
        
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setStyleSheet(ModernStyles.modern_input())
        self.date_input.setMinimumWidth(120)
        self.date_input.setMaximumWidth(150)
        filter_layout.addWidget(self.date_input)
        
        search_btn = QPushButton("📈 Générer")
        search_btn.setFixedHeight(40)
        search_btn.setFixedWidth(140)
        search_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        search_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.INFO))
        search_btn.clicked.connect(self.generate_daily_report)
        filter_layout.addWidget(search_btn)
        
        export_btn = QPushButton("💾 Excel")
        export_btn.setFixedHeight(40)
        export_btn.setFixedWidth(140)
        export_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        export_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.SUCCESS))
        export_btn.clicked.connect(self.export_daily_excel)
        filter_layout.addWidget(export_btn)
        
        filter_layout.addStretch()
        layout.addWidget(filter_frame)
        
        # Statistiques en 3 colonnes avec cartes colorées
        stats_container = QHBoxLayout()
        stats_container.setSpacing(15)
        
        # Chiffre d'affaires
        revenue_card = QWidget()
        revenue_card.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #10B981, stop:1 #059669);
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        revenue_card.setMinimumHeight(120)
        revenue_layout = QVBoxLayout(revenue_card)
        revenue_layout.setSpacing(8)
        revenue_label = QLabel("💵 Chiffre d'affaires")
        revenue_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        revenue_label.setStyleSheet("color: rgba(255,255,255,0.85);")
        revenue_layout.addWidget(revenue_label)
        self.revenue_label = QLabel("0.00 TND")
        self.revenue_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.revenue_label.setStyleSheet("color: white;")
        revenue_layout.addWidget(self.revenue_label)
        stats_container.addWidget(revenue_card)
        
        # Nombre de commandes
        orders_card = QWidget()
        orders_card.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3B82F6, stop:1 #1D4ED8);
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        orders_card.setMinimumHeight(120)
        orders_layout = QVBoxLayout(orders_card)
        orders_layout.setSpacing(8)
        orders_label = QLabel("🛍️ Commandes")
        orders_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        orders_label.setStyleSheet("color: rgba(255,255,255,0.85);")
        orders_layout.addWidget(orders_label)
        self.orders_label = QLabel("0")
        self.orders_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.orders_label.setStyleSheet("color: white;")
        orders_layout.addWidget(self.orders_label)
        stats_container.addWidget(orders_card)
        
        # Employé le plus actif
        employee_card = QWidget()
        employee_card.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #8B5CF6, stop:1 #6D28D9);
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        employee_card.setMinimumHeight(120)
        employee_layout = QVBoxLayout(employee_card)
        employee_layout.setSpacing(8)
        employee_label = QLabel("👤 Top vendeur")
        employee_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        employee_label.setStyleSheet("color: rgba(255,255,255,0.85);")
        employee_layout.addWidget(employee_label)
        self.active_employee_label = QLabel("-")
        self.active_employee_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.active_employee_label.setStyleSheet("color: white;")
        employee_layout.addWidget(self.active_employee_label)
        stats_container.addWidget(employee_card)
        
        layout.addLayout(stats_container)
        
        # Tableau des produits les plus vendus
        sales_label = QLabel("📦 Produits les plus vendus")
        sales_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        sales_label.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        layout.addWidget(sales_label)
        
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(3)
        self.sales_table.setHorizontalHeaderLabels(["Produit", "Quantité", "Montant"])
        self.sales_table.setStyleSheet(ModernStyles.modern_table())
        self.sales_table.setAlternatingRowColors(True)
        self.sales_table.setMinimumHeight(200)
        layout.addWidget(self.sales_table)
        
        # Auto-générer au démarrage
        self.generate_daily_report()
        return widget

    def create_monthly_report_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Section Filtres avec style clair
        filter_frame = QWidget()
        filter_frame.setStyleSheet(f"background-color: white; border-radius: 8px; border: 1px solid #E5E7EB;")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(15, 15, 15, 15)
        
        filter_layout.addWidget(QLabel("Mois :"))
        
        self.month_combo = QComboBox()
        current_month = datetime.now().month
        months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                  "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        self.month_combo.addItems(months)
        self.month_combo.setCurrentIndex(current_month - 1)
        self.month_combo.setStyleSheet(ModernStyles.modern_input())
        self.month_combo.setFixedWidth(120)
        filter_layout.addWidget(self.month_combo)
        
        filter_layout.addWidget(QLabel("Année :"))
        self.year_spinbox = QComboBox()
        current_year = datetime.now().year
        for year in range(current_year - 2, current_year + 1):
            self.year_spinbox.addItem(str(year))
        self.year_spinbox.setCurrentText(str(current_year))
        self.year_spinbox.setStyleSheet(ModernStyles.modern_input())
        self.year_spinbox.setFixedWidth(100)
        filter_layout.addWidget(self.year_spinbox)
        
        search_btn = QPushButton("📈 Générer")
        search_btn.setFixedHeight(40)
        search_btn.setFixedWidth(140)
        search_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        search_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.INFO))
        search_btn.clicked.connect(self.generate_monthly_report)
        filter_layout.addWidget(search_btn)
        
        export_btn = QPushButton("💾 Excel")
        export_btn.setFixedHeight(40)
        export_btn.setFixedWidth(140)
        export_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        export_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.SUCCESS))
        export_btn.clicked.connect(self.export_monthly_excel)
        filter_layout.addWidget(export_btn)
        
        filter_layout.addStretch()
        layout.addWidget(filter_frame)
        
        # Statistiques mensuelles en 2 colonnes
        stats_container = QHBoxLayout()
        stats_container.setSpacing(15)
        
        # Chiffre d'affaires mensuel
        revenue_card = QWidget()
        revenue_card.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #F59E0B, stop:1 #D97706);
                border-radius: 10px;
                padding: 25px;
            }}
        """)
        revenue_card.setMinimumHeight(130)
        revenue_layout = QVBoxLayout(revenue_card)
        revenue_layout.setSpacing(10)
        revenue_label = QLabel("💰 Chiffre d'affaires")
        revenue_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        revenue_label.setStyleSheet("color: rgba(255,255,255,0.9);")
        revenue_layout.addWidget(revenue_label)
        self.monthly_revenue_label = QLabel("0.00 TND")
        self.monthly_revenue_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.monthly_revenue_label.setStyleSheet("color: white;")
        revenue_layout.addWidget(self.monthly_revenue_label)
        stats_container.addWidget(revenue_card)
        
        # Nombre de commandes mensuelles
        orders_card = QWidget()
        orders_card.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #EC4899, stop:1 #BE185D);
                border-radius: 10px;
                padding: 25px;
            }}
        """)
        orders_card.setMinimumHeight(130)
        orders_layout = QVBoxLayout(orders_card)
        orders_layout.setSpacing(10)
        orders_label = QLabel("📊 Commandes")
        orders_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        orders_label.setStyleSheet("color: rgba(255,255,255,0.9);")
        orders_layout.addWidget(orders_label)
        self.monthly_orders_label = QLabel("0")
        self.monthly_orders_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.monthly_orders_label.setStyleSheet("color: white;")
        orders_layout.addWidget(self.monthly_orders_label)
        stats_container.addWidget(orders_card)
        
        stats_container.addStretch()
        layout.addLayout(stats_container)
        
        layout.addStretch()
        self.generate_monthly_report()
        return widget

    def create_products_report_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Filtres par période
        filter_frame = QWidget()
        filter_frame.setStyleSheet(f"background-color: white; border-radius: 8px; border: 1px solid #E5E7EB;")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(15, 15, 15, 15)
        
        filter_layout.addWidget(QLabel("Période :"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setStyleSheet(ModernStyles.modern_input())
        filter_layout.addWidget(self.start_date)
        
        filter_layout.addWidget(QLabel("au"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setStyleSheet(ModernStyles.modern_input())
        filter_layout.addWidget(self.end_date)
        
        search_btn = QPushButton("📈 Générer")
        search_btn.setFixedHeight(40)
        search_btn.setFixedWidth(140)
        search_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        search_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.INFO))
        search_btn.clicked.connect(self.generate_products_report)
        filter_layout.addWidget(search_btn)
        
        export_btn = QPushButton("💾 Excel")
        export_btn.setFixedHeight(40)
        export_btn.setFixedWidth(140)
        export_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        export_btn.setStyleSheet(ModernStyles.modern_button(ModernStyles.SUCCESS))
        export_btn.clicked.connect(self.export_products_excel)
        filter_layout.addWidget(export_btn)
        
        filter_layout.addStretch()
        layout.addWidget(filter_frame)
        
        # Titre du tableau
        products_label = QLabel("📦 Produits les plus vendus")
        products_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        products_label.setStyleSheet(f"color: {ModernStyles.TEXT_PRIMARY};")
        layout.addWidget(products_label)
        
        # Tableau produits
        self.products_report_table = QTableWidget()
        self.products_report_table.setColumnCount(3)
        self.products_report_table.setHorizontalHeaderLabels(["Produit", "Quantité vendue", "Montant total"])
        self.products_report_table.setStyleSheet(ModernStyles.modern_table())
        self.products_report_table.setAlternatingRowColors(True)
        self.products_report_table.setMinimumHeight(300)
        layout.addWidget(self.products_report_table)
        
        self.generate_products_report()
        return widget

    def generate_daily_report(self):
        try:
            selected_date = self.date_input.date().toString("yyyy-MM-dd")
            
            # Récupérer le revenu du jour
            try:
                result = self.db.get_daily_revenue(selected_date)
                revenue = float(result[0]) if result and result[0] else 0.0
                orders_count = int(result[1]) if result and result[1] else 0
            except Exception as e:
                print(f"Erreur get_daily_revenue: {e}")
                revenue = 0.0
                orders_count = 0
            
            # Récupérer la devise
            try:
                currency = self.db.get_setting('currency')
                if currency is None:
                    currency = 'TND'
                elif isinstance(currency, dict):
                    currency = currency.get('value', 'TND')
            except:
                currency = 'TND'
            
            self.revenue_label.setText(f"{revenue:.2f} {currency}")
            self.orders_label.setText(str(orders_count))
            
            # Employé le plus actif
            try:
                active_user = self.db.get_most_active_user(selected_date)
                if active_user:
                    user_name = active_user.get('full_name', 'Inconnu') if isinstance(active_user, dict) else str(active_user)
                    self.active_employee_label.setText(user_name)
                else:
                    self.active_employee_label.setText("-")
            except Exception as e:
                print(f"Erreur get_most_active_user: {e}")
                self.active_employee_label.setText("-")
            
            # Produits les plus vendus
            try:
                top_products = self.db.get_top_products(selected_date)
                self.sales_table.setRowCount(len(top_products))
                
                for i, product in enumerate(top_products):
                    if isinstance(product, dict):
                        name = str(product.get('name', ''))
                        qty = int(product.get('total_qty', 0)) if product.get('total_qty') else 0
                        amount = float(product.get('total_amount', 0)) if product.get('total_amount') else 0.0
                    else:
                        # Fallback si ce n'est pas un dict
                        name = str(product[0]) if len(product) > 0 else ''
                        qty = int(product[1]) if len(product) > 1 else 0
                        amount = float(product[2]) if len(product) > 2 else 0.0
                    
                    self.sales_table.setItem(i, 0, QTableWidgetItem(name))
                    self.sales_table.setItem(i, 1, QTableWidgetItem(str(qty)))
                    self.sales_table.setItem(i, 2, QTableWidgetItem(f"{amount:.2f} {currency}"))
            except Exception as e:
                print(f"Erreur get_top_products: {e}")
                self.sales_table.setRowCount(0)
                
        except Exception as e:
            print(f"Erreur globale generate_daily_report: {e}")

    def generate_monthly_report(self):
        try:
            month = self.month_combo.currentIndex() + 1
            year = int(self.year_spinbox.currentText())
            
            try:
                result = self.db.get_monthly_revenue(year, month)
                revenue = float(result[0]) if result and result[0] else 0.0
                orders_count = int(result[1]) if result and result[1] else 0
            except Exception as e:
                print(f"Erreur get_monthly_revenue: {e}")
                revenue = 0.0
                orders_count = 0
            
            try:
                currency = self.db.get_setting('currency')
                if currency is None:
                    currency = 'TND'
                elif isinstance(currency, dict):
                    currency = currency.get('value', 'TND')
            except:
                currency = 'TND'
            
            self.monthly_revenue_label.setText(f"{revenue:.2f} {currency}")
            self.monthly_orders_label.setText(str(orders_count))
        except Exception as e:
            print(f"Erreur generate_monthly_report: {e}")

    def generate_products_report(self):
        try:
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            try:
                top_products = self.db.get_top_products(end_date)
            except Exception as e:
                print(f"Erreur get_top_products: {e}")
                top_products = []
            
            try:
                currency = self.db.get_setting('currency')
                if currency is None:
                    currency = 'TND'
                elif isinstance(currency, dict):
                    currency = currency.get('value', 'TND')
            except:
                currency = 'TND'
            
            self.products_report_table.setRowCount(len(top_products))
            
            for i, product in enumerate(top_products):
                try:
                    if isinstance(product, dict):
                        name = str(product.get('name', ''))
                        qty = int(product.get('total_qty', 0)) if product.get('total_qty') else 0
                        amount = float(product.get('total_amount', 0)) if product.get('total_amount') else 0.0
                    else:
                        # Fallback si ce n'est pas un dict
                        name = str(product[0]) if len(product) > 0 else ''
                        qty = int(product[1]) if len(product) > 1 else 0
                        amount = float(product[2]) if len(product) > 2 else 0.0
                    
                    self.products_report_table.setItem(i, 0, QTableWidgetItem(name))
                    self.products_report_table.setItem(i, 1, QTableWidgetItem(str(qty)))
                    self.products_report_table.setItem(i, 2, QTableWidgetItem(f"{amount:.2f} {currency}"))
                except Exception as e:
                    print(f"Erreur ligne {i}: {e}")
                    continue
        except Exception as e:
            print(f"Erreur generate_products_report: {e}")

    def export_daily_excel(self):
        self.export_to_excel("daily")

    def export_monthly_excel(self):
        self.export_to_excel("monthly")

    def export_products_excel(self):
        self.export_to_excel("products")

    def export_to_excel(self, report_type):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Exporter vers Excel",
                f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "Fichiers Excel (*.xlsx);;Tous les fichiers (*.*)"
            )
            
            if not file_path:
                return
            
            wb = Workbook()
            ws = wb.active
            ws.title = "Rapport"
            
            # En-têtes
            header_fill = PatternFill(start_color="6B4CE6", end_color="6B4CE6", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF", size=12)
            
            if report_type == "daily":
                date = self.date_input.date().toString("yyyy-MM-dd")
                result = self.db.get_daily_revenue(date)
                revenue = result[0] if result else 0
                orders_count = result[1] if result else 0
                
                ws['A1'] = "RAPPORT JOURNALIER"
                ws['A1'].font = Font(bold=True, size=14, color="FFFFFF")
                ws['A1'].fill = PatternFill(start_color="6B4CE6", end_color="6B4CE6", fill_type="solid")
                ws['A2'] = f"Date: {date}"
                ws['A4'] = "Chiffre d'affaires"
                ws['B4'] = revenue
                ws['A5'] = "Nombre de commandes"
                ws['B5'] = orders_count
                
                ws['A7'] = "Produit"
                ws['B7'] = "Quantité"
                ws['C7'] = "Montant"
                
                for cell in [ws['A7'], ws['B7'], ws['C7']]:
                    cell.fill = header_fill
                    cell.font = header_font
                
                try:
                    top_products = self.db.get_top_products(date)
                    for i, product in enumerate(top_products, start=8):
                        name = product.get('name', '') if isinstance(product, dict) else str(product[0])
                        qty = int(product.get('total_qty', 0)) if isinstance(product, dict) else int(product[1])
                        amount = float(product.get('total_amount', 0)) if isinstance(product, dict) else float(product[2])
                        
                        ws[f'A{i}'] = name
                        ws[f'B{i}'] = qty
                        ws[f'C{i}'] = amount
                except:
                    pass
            
            elif report_type == "monthly":
                month = self.month_combo.currentIndex() + 1
                year = int(self.year_spinbox.currentText())
                result = self.db.get_monthly_revenue(year, month)
                revenue = result[0] if result else 0
                orders_count = result[1] if result else 0
                
                ws['A1'] = "RAPPORT MENSUEL"
                ws['A1'].font = Font(bold=True, size=14, color="FFFFFF")
                ws['A1'].fill = PatternFill(start_color="6B4CE6", end_color="6B4CE6", fill_type="solid")
                ws['A2'] = f"Mois: {month}/{year}"
                ws['A4'] = "Chiffre d'affaires"
                ws['B4'] = revenue
                ws['A5'] = "Nombre de commandes"
                ws['B5'] = orders_count
            
            elif report_type == "products":
                end_date = self.end_date.date().toString("yyyy-MM-dd")
                ws['A1'] = "RAPPORT PRODUITS"
                ws['A1'].font = Font(bold=True, size=14, color="FFFFFF")
                ws['A1'].fill = PatternFill(start_color="6B4CE6", end_color="6B4CE6", fill_type="solid")
                ws['A2'] = f"Période: jusqu'au {end_date}"
                
                ws['A4'] = "Produit"
                ws['B4'] = "Quantité"
                ws['C4'] = "Montant"
                
                for cell in [ws['A4'], ws['B4'], ws['C4']]:
                    cell.fill = header_fill
                    cell.font = header_font
                
                try:
                    top_products = self.db.get_top_products(end_date)
                    for i, product in enumerate(top_products, start=5):
                        name = product.get('name', '') if isinstance(product, dict) else str(product[0])
                        qty = int(product.get('total_qty', 0)) if isinstance(product, dict) else int(product[1])
                        amount = float(product.get('total_amount', 0)) if isinstance(product, dict) else float(product[2])
                        
                        ws[f'A{i}'] = name
                        ws[f'B{i}'] = qty
                        ws[f'C{i}'] = amount
                except:
                    pass
            
            # Auto-fit columns
            for column in ['A', 'B', 'C']:
                ws.column_dimensions[column].width = 25
            
            wb.save(file_path)
            QMessageBox.information(self, "Succès", f"Rapport exporté avec succès!\n{file_path}")
            
        except Exception as e:
            print(f"Erreur export: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export:\n{str(e)}")

    def generate_report(self):
        # Méthode de compatibilité
        self.generate_daily_report()
