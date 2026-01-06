from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QDateEdit, QTableWidget, QTableWidgetItem, QComboBox,
                             QFileDialog, QMessageBox, QTabWidget)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from src.utils.invoice_generator import InvoiceGenerator

class ReportsScreen(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.primary_color = "#FF9500"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Titre
        title = QLabel("Rapports et Statistiques")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #2C2C2C;")
        layout.addWidget(title)
        
        # Tabs pour différents types de rapports
        tabs = QTabWidget()
        
        # Tab 1: Rapport journalier
        daily_tab = self.create_daily_report_tab()
        tabs.addTab(daily_tab, "Rapport Journalier")
        
        # Tab 2: Rapport mensuel
        monthly_tab = self.create_monthly_report_tab()
        tabs.addTab(monthly_tab, "Rapport Mensuel")
        
        # Tab 3: Produits les plus vendus
        products_tab = self.create_products_report_tab()
        tabs.addTab(products_tab, "Produits")
        
        layout.addWidget(tabs)

    def create_daily_report_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Filtres
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Sélectionner une date :"))
        
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setStyleSheet("padding: 8px; border: 1px solid #DDD; border-radius: 3px;")
        filter_layout.addWidget(self.date_input)
        
        search_btn = QPushButton("Générer le rapport")
        search_btn.setFixedHeight(40)
        search_btn.setFont(QFont("Arial", 11, QFont.Bold))
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #C8A882;
                color: white;
                border: none;
                border-radius: 3px;
            }
        """)
        search_btn.clicked.connect(self.generate_daily_report)
        filter_layout.addWidget(search_btn)
        
        export_btn = QPushButton("Exporter Excel")
        export_btn.setFixedHeight(40)
        export_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        export_btn.clicked.connect(self.export_daily_excel)
        filter_layout.addWidget(export_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Statistiques
        stats_layout = QHBoxLayout()
        
        self.revenue_label = QLabel("Chiffre d'affaires : 0.00 dt")
        self.revenue_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.revenue_label.setStyleSheet(f"background-color: #C8A882; color: white; padding: 15px; border-radius: 3px;")
        stats_layout.addWidget(self.revenue_label)
        
        self.orders_label = QLabel("Commandes : 0")
        self.orders_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.orders_label.setStyleSheet("background-color: #D4A574; color: white; padding: 15px; border-radius: 3px;")
        stats_layout.addWidget(self.orders_label)
        
        layout.addLayout(stats_layout)
        
        # Employé le plus actif
        self.active_employee_label = QLabel("Employé le plus actif : -")
        self.active_employee_label.setFont(QFont("Arial", 11))
        layout.addWidget(self.active_employee_label)
        
        # Tableau des produits les plus vendus
        sales_label = QLabel("Produits les plus vendus :")
        sales_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(sales_label)
        
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(3)
        self.sales_table.setHorizontalHeaderLabels(["Produit", "Quantité", "Montant"])
        self.sales_table.setStyleSheet("""
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
        layout.addWidget(self.sales_table)
        
        self.generate_daily_report()
        return widget

    def create_monthly_report_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Filtres
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Mois :"))
        
        self.month_combo = QComboBox()
        current_month = datetime.now().month
        months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                  "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        self.month_combo.addItems(months)
        self.month_combo.setCurrentIndex(current_month - 1)
        filter_layout.addWidget(self.month_combo)
        
        filter_layout.addWidget(QLabel("Année :"))
        self.year_spinbox = QComboBox()
        current_year = datetime.now().year
        for year in range(current_year - 2, current_year + 1):
            self.year_spinbox.addItem(str(year))
        self.year_spinbox.setCurrentText(str(current_year))
        filter_layout.addWidget(self.year_spinbox)
        
        search_btn = QPushButton("Générer")
        search_btn.clicked.connect(self.generate_monthly_report)
        filter_layout.addWidget(search_btn)
        
        export_btn = QPushButton("Exporter Excel")
        export_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        export_btn.clicked.connect(self.export_monthly_excel)
        filter_layout.addWidget(export_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Statistiques mensuelles
        self.monthly_revenue_label = QLabel("Chiffre d'affaires mensuel : 0.00 dt")
        self.monthly_revenue_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.monthly_revenue_label.setStyleSheet("background-color: #C8A882; color: white; padding: 15px; border-radius: 3px;")
        layout.addWidget(self.monthly_revenue_label)
        
        self.monthly_orders_label = QLabel("Nombre de commandes : 0")
        self.monthly_orders_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.monthly_orders_label)
        
        layout.addStretch()
        self.generate_monthly_report()
        return widget

    def create_products_report_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Filtres par période
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Du :"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-7))
        filter_layout.addWidget(self.start_date)
        
        filter_layout.addWidget(QLabel("Au :"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        filter_layout.addWidget(self.end_date)
        
        search_btn = QPushButton("Générer")
        search_btn.clicked.connect(self.generate_products_report)
        filter_layout.addWidget(search_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Tableau produits
        self.products_report_table = QTableWidget()
        self.products_report_table.setColumnCount(3)
        self.products_report_table.setHorizontalHeaderLabels(["Produit", "Quantité vendue", "Montant total"])
        layout.addWidget(self.products_report_table)
        
        self.generate_products_report()
        return widget

    def generate_daily_report(self):
        selected_date = self.date_input.date().toString("yyyy-MM-dd")
        
        result = self.db.get_daily_revenue(selected_date)
        revenue = result[0] if result else 0
        orders_count = result[1] if result else 0
        
        currency = self.db.get_setting('currency', 'TND')
        self.revenue_label.setText(f"Chiffre d'affaires : {revenue:.2f} {currency}")
        self.orders_label.setText(f"Commandes : {orders_count}")
        
        # Employé le plus actif
        active_user = self.db.get_most_active_user(selected_date)
        if active_user:
            self.active_employee_label.setText(
                f"Employé le plus actif : {active_user['full_name']} ({active_user['orders_count']} commandes)"
            )
        else:
            self.active_employee_label.setText("Employé le plus actif : Aucune donnée")
        
        # Produits les plus vendus
        top_products = self.db.get_top_products(selected_date)
        self.sales_table.setRowCount(len(top_products))
        
        for i, product in enumerate(top_products):
            self.sales_table.setItem(i, 0, QTableWidgetItem(product[0]))
            self.sales_table.setItem(i, 1, QTableWidgetItem(str(product[1])))
            self.sales_table.setItem(i, 2, QTableWidgetItem(f"{product[2]:.2f} {currency}"))

    def generate_monthly_report(self):
        month = self.month_combo.currentIndex() + 1
        year = int(self.year_spinbox.currentText())
        
        revenue, orders_count = self.db.get_monthly_revenue(year, month)
        currency = self.db.get_setting('currency', 'TND')
        
        self.monthly_revenue_label.setText(f"Chiffre d'affaires mensuel : {revenue:.2f} {currency}")
        self.monthly_orders_label.setText(f"Nombre de commandes : {orders_count}")

    def generate_products_report(self):
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        
        revenue_data = self.db.get_revenue_by_date_range(start_date, end_date)
        # Pour l'instant, on utilise get_top_products avec la date de fin
        top_products = self.db.get_top_products(end_date)
        
        self.products_report_table.setRowCount(len(top_products))
        currency = self.db.get_setting('currency', 'TND')
        
        for i, product in enumerate(top_products):
            self.products_report_table.setItem(i, 0, QTableWidgetItem(product[0]))
            self.products_report_table.setItem(i, 1, QTableWidgetItem(str(product[1])))
            self.products_report_table.setItem(i, 2, QTableWidgetItem(f"{product[2]:.2f} {currency}"))

    def export_daily_excel(self):
        self.export_to_excel("daily")

    def export_monthly_excel(self):
        self.export_to_excel("monthly")

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
            header_fill = PatternFill(start_color="2C2C2C", end_color="2C2C2C", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF")
            
            if report_type == "daily":
                date = self.date_input.date().toString("yyyy-MM-dd")
                result = self.db.get_daily_revenue(date)
                revenue = result[0] if result else 0
                orders_count = result[1] if result else 0
                
                ws['A1'] = "Rapport Journalier"
                ws['A2'] = f"Date: {date}"
                ws['A4'] = "Chiffre d'affaires"
                ws['B4'] = revenue
                ws['A5'] = "Nombre de commandes"
                ws['B5'] = orders_count
                
                ws['A7'] = "Produit"
                ws['B7'] = "Quantité"
                ws['C7'] = "Montant"
                
                top_products = self.db.get_top_products(date)
                for i, product in enumerate(top_products, start=8):
                    ws[f'A{i}'] = product[0]
                    ws[f'B{i}'] = product[1]
                    ws[f'C{i}'] = product[2]
            
            elif report_type == "monthly":
                month = self.month_combo.currentIndex() + 1
                year = int(self.year_spinbox.currentText())
                revenue, orders_count = self.db.get_monthly_revenue(year, month)
                
                ws['A1'] = "Rapport Mensuel"
                ws['A2'] = f"Mois: {month}/{year}"
                ws['A4'] = "Chiffre d'affaires"
                ws['B4'] = revenue
                ws['A5'] = "Nombre de commandes"
                ws['B5'] = orders_count
            
            # Style des en-têtes
            for cell in ws[7]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center')
            
            wb.save(file_path)
            QMessageBox.information(self, "Succès", f"Rapport exporté avec succès!\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export:\n{str(e)}")

    def generate_report(self):
        # Méthode de compatibilité
        self.generate_daily_report()

    def generate_report(self):
        selected_date = self.date_input.date().toString("yyyy-MM-dd")
        
        result = self.db.get_daily_revenue(selected_date)
        
        if result and result[0]:
            revenue = result[0]
            orders_count = result[1]
        else:
            revenue = 0
            orders_count = 0
        
        self.revenue_label.setText(f"Chiffre d'affaires : {revenue:.2f} dt")
        self.orders_label.setText(f"Commandes : {orders_count}")
        
        top_products = self.db.get_top_products(selected_date)
        self.sales_table.setRowCount(len(top_products))
        
        for i, product in enumerate(top_products):
            self.sales_table.setItem(i, 0, QTableWidgetItem(product[0]))
            self.sales_table.setItem(i, 1, QTableWidgetItem(str(product[1])))
            self.sales_table.setItem(i, 2, QTableWidgetItem(f"{product[2]:.2f} dt"))
