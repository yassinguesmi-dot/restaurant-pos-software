from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QLineEdit, QSpinBox, QMessageBox, QGroupBox, QFileDialog,
                             QComboBox, QTimeEdit)
from PyQt5.QtCore import QTime
from PyQt5.QtGui import QFont
import os
from datetime import datetime
import shutil

class SettingsScreen(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.primary_color = "#C8A882"
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Titre
        title = QLabel("Paramètres")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #2C2C2C;")
        layout.addWidget(title)
        
        # Groupe : Informations du Restaurant
        resto_group = QGroupBox("Informations du Restaurant")
        resto_group.setStyleSheet("""
            QGroupBox {
                color: #2C2C2C;
                border: 2px solid #D4A574;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)
        resto_layout = QVBoxLayout()
        
        resto_layout.addWidget(QLabel("Nom du restaurant :"))
        self.restaurant_name = QLineEdit()
        self.restaurant_name.setText("Café 216")
        self.restaurant_name.setStyleSheet("padding: 8px; border: 1px solid #DDD; border-radius: 3px;")
        resto_layout.addWidget(self.restaurant_name)
        
        resto_layout.addWidget(QLabel("Adresse :"))
        self.restaurant_address = QLineEdit()
        self.restaurant_address.setText("Rue du Commerce")
        self.restaurant_address.setStyleSheet("padding: 8px; border: 1px solid #DDD; border-radius: 3px;")
        resto_layout.addWidget(self.restaurant_address)
        
        resto_layout.addWidget(QLabel("Téléphone :"))
        self.restaurant_phone = QLineEdit()
        self.restaurant_phone.setStyleSheet("padding: 8px; border: 1px solid #DDD; border-radius: 3px;")
        resto_layout.addWidget(self.restaurant_phone)
        
        resto_layout.addWidget(QLabel("Devise :"))
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["TND", "EUR", "USD", "DZD"])
        self.currency_combo.setStyleSheet("padding: 8px; border: 1px solid #DDD; border-radius: 3px;")
        resto_layout.addWidget(self.currency_combo)
        
        resto_group.setLayout(resto_layout)
        layout.addWidget(resto_group)
        
        # Groupe : Configuration
        config_group = QGroupBox("Configuration")
        config_group.setStyleSheet("""
            QGroupBox {
                color: #2C2C2C;
                border: 2px solid #D4A574;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        config_layout = QVBoxLayout()
        
        config_layout.addWidget(QLabel("TVA (%) :"))
        self.tax_rate = QSpinBox()
        self.tax_rate.setRange(0, 100)
        self.tax_rate.setStyleSheet("padding: 8px; border: 1px solid #DDD; border-radius: 3px;")
        config_layout.addWidget(self.tax_rate)
        
        config_layout.addWidget(QLabel("Heures d'ouverture :"))
        hours_layout = QHBoxLayout()
        self.opening_time = QTimeEdit()
        self.opening_time.setTime(QTime(8, 0))
        self.opening_time.setDisplayFormat("HH:mm")
        hours_layout.addWidget(self.opening_time)
        hours_layout.addWidget(QLabel(" - "))
        self.closing_time = QTimeEdit()
        self.closing_time.setTime(QTime(22, 0))
        self.closing_time.setDisplayFormat("HH:mm")
        hours_layout.addWidget(self.closing_time)
        config_layout.addLayout(hours_layout)
        
        config_layout.addWidget(QLabel("Préfixe facture :"))
        self.invoice_prefix = QLineEdit()
        self.invoice_prefix.setStyleSheet("padding: 8px; border: 1px solid #DDD; border-radius: 3px;")
        config_layout.addWidget(self.invoice_prefix)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Groupe : Sauvegarde
        backup_group = QGroupBox("Sauvegarde et Restauration")
        backup_group.setStyleSheet("""
            QGroupBox {
                color: #2C2C2C;
                border: 2px solid #D4A574;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        backup_layout = QVBoxLayout()
        
        export_btn = QPushButton("Exporter la base de données")
        export_btn.setFixedHeight(40)
        export_btn.setFont(QFont("Arial", 11, QFont.Bold))
        export_btn.setStyleSheet("""
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
        export_btn.clicked.connect(self.export_database)
        backup_layout.addWidget(export_btn)
        
        backup_btn = QPushButton("Créer une sauvegarde")
        backup_btn.setFixedHeight(40)
        backup_btn.setFont(QFont("Arial", 11, QFont.Bold))
        backup_btn.setStyleSheet("""
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
        backup_btn.clicked.connect(self.create_backup)
        backup_layout.addWidget(backup_btn)
        
        restore_btn = QPushButton("Restaurer depuis un fichier")
        restore_btn.setFixedHeight(40)
        restore_btn.setFont(QFont("Arial", 11, QFont.Bold))
        restore_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        restore_btn.clicked.connect(self.restore_database)
        backup_layout.addWidget(restore_btn)
        
        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)
        
        layout.addStretch()
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("Enregistrer")
        save_btn.setFixedHeight(40)
        save_btn.setFont(QFont("Arial", 11, QFont.Bold))
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #C8A882;
                color: white;
                border: none;
                border-radius: 3px;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("Réinitialiser la base de données")
        reset_btn.setFixedHeight(40)
        reset_btn.setFont(QFont("Arial", 11, QFont.Bold))
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF5733;
                color: white;
                border: none;
                border-radius: 3px;
            }
        """)
        reset_btn.clicked.connect(self.reset_database)
        buttons_layout.addWidget(reset_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)

    def save_settings(self):
        try:
            # Sauvegarder dans la base de données
            self.db.set_setting('restaurant_name', self.restaurant_name.text())
            self.db.set_setting('restaurant_address', self.restaurant_address.text())
            self.db.set_setting('restaurant_phone', self.restaurant_phone.text())
            self.db.set_setting('currency', self.currency_combo.currentText())
            self.db.set_setting('tax_rate', str(self.tax_rate.value()))
            
            opening_hours = f"{self.opening_time.time().toString('HH:mm')}-{self.closing_time.time().toString('HH:mm')}"
            self.db.set_setting('opening_hours', opening_hours)
            self.db.set_setting('invoice_prefix', self.invoice_prefix.text())
            
            QMessageBox.information(self, "Succès", "Paramètres enregistrés avec succès !")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de l'enregistrement : {str(e)}")

    def load_settings(self):
        try:
            self.restaurant_name.setText(self.db.get_setting('restaurant_name', 'Café 216'))
            self.restaurant_address.setText(self.db.get_setting('restaurant_address', 'Rue du Commerce'))
            self.restaurant_phone.setText(self.db.get_setting('restaurant_phone', '+216 XX XXX XXX'))
            
            currency = self.db.get_setting('currency', 'TND')
            index = self.currency_combo.findText(currency)
            if index >= 0:
                self.currency_combo.setCurrentIndex(index)
            
            tax_rate = int(self.db.get_setting('tax_rate', '20'))
            self.tax_rate.setValue(tax_rate)
            
            opening_hours = self.db.get_setting('opening_hours', '08:00-22:00')
            if '-' in opening_hours:
                start, end = opening_hours.split('-')
                start_time = QTime.fromString(start, 'HH:mm')
                end_time = QTime.fromString(end, 'HH:mm')
                if start_time.isValid():
                    self.opening_time.setTime(start_time)
                if end_time.isValid():
                    self.closing_time.setTime(end_time)
            
            self.invoice_prefix.setText(self.db.get_setting('invoice_prefix', 'FAC'))
        except Exception as e:
            print(f"Erreur lors du chargement des paramètres : {e}")

    def export_database(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Exporter la base de données", 
                f"cafe216_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
                "Base de données (*.db);;Tous les fichiers (*.*)"
            )
            if file_path:
                if self.db.backup_database(file_path):
                    QMessageBox.information(self, "Succès", f"Base de données exportée avec succès!\n{file_path}")
                else:
                    QMessageBox.warning(self, "Erreur", "Erreur lors de l'exportation")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {str(e)}")

    def create_backup(self):
        try:
            backup_dir = "backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            backup_filename = f"cafe216_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            if self.db.backup_database(backup_path):
                QMessageBox.information(self, "Succès", f"Sauvegarde créée avec succès!\n{backup_path}")
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de la création de la sauvegarde")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {str(e)}")

    def restore_database(self):
        reply = QMessageBox.warning(
            self, 
            "Attention", 
            "La restauration va remplacer la base de données actuelle.\nÊtes-vous sûr de vouloir continuer?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Sélectionner un fichier de sauvegarde",
                "",
                "Base de données (*.db);;Tous les fichiers (*.*)"
            )
            if file_path and os.path.exists(file_path):
                # Fermer la connexion actuelle
                self.db.close()
                
                # Copier le fichier de sauvegarde
                shutil.copy2(file_path, self.db.db_path)
                
                # Rouvrir la base de données
                self.db.init_database()
                
                QMessageBox.information(
                    self, 
                    "Succès", 
                    "Base de données restaurée avec succès!\nVeuillez redémarrer l'application."
                )
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la restauration: {str(e)}")

    def reset_database(self):
        reply = QMessageBox.question(self, "Confirmation", 
                                     "Êtes-vous sûr de vouloir réinitialiser la base de données ?")
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "Info", "Fonction à implémenter")
