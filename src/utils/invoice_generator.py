from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import os

class InvoiceGenerator:
    def __init__(self, db):
        self.db = db
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()

    def setup_custom_styles(self):
        # Style pour le titre
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C2C2C'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Style pour les en-têtes
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#2C2C2C'),
            alignment=TA_LEFT
        )
        
        # Style pour le total
        self.total_style = ParagraphStyle(
            'CustomTotal',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#2C2C2C'),
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT
        )

    def generate_invoice(self, order_id, output_path=None):
        """Génère une facture PDF pour une commande"""
        try:
            # Récupérer les données de la commande
            cursor = self.db.connection.cursor()
            cursor.execute('''
                SELECT o.*, t.table_number, u.full_name as cashier_name
                FROM orders o
                LEFT JOIN tables t ON o.table_id = t.id
                LEFT JOIN users u ON o.user_id = u.id
                WHERE o.id = ?
            ''', (order_id,))
            order = cursor.fetchone()
            
            if not order:
                raise ValueError(f"Commande {order_id} introuvable")
            # convertir sqlite3.Row en dict pour utiliser .get()
            try:
                order = dict(order)
            except Exception:
                pass
            
            # Récupérer les items
            order_items = self.db.get_order_details(order_id)
            
            # Récupérer les paramètres du restaurant
            restaurant_name = self.db.get_setting('restaurant_name', 'Café 216')
            restaurant_address = self.db.get_setting('restaurant_address', '')
            restaurant_phone = self.db.get_setting('restaurant_phone', '')
            currency = self.db.get_setting('currency', 'TND')
            tax_rate = float(self.db.get_setting('tax_rate', '20'))
            
            # Chemin de sortie
            if output_path is None:
                invoices_dir = "invoices"
                if not os.path.exists(invoices_dir):
                    os.makedirs(invoices_dir)
                invoice_number = order.get('invoice_number', order['order_number'])
                output_path = os.path.join(invoices_dir, f"{invoice_number}.pdf")
            
            # Créer le document PDF
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            story = []
            
            # En-tête
            story.append(Paragraph(restaurant_name, self.title_style))
            
            if restaurant_address:
                story.append(Paragraph(restaurant_address, self.header_style))
            if restaurant_phone:
                story.append(Paragraph(f"Tél: {restaurant_phone}", self.header_style))
            
            story.append(Spacer(1, 20))
            
            # Informations de la facture
            invoice_data = [
                [f"<b>Facture N°:</b> {order.get('invoice_number', order['order_number'])}"],
                [f"<b>Date:</b> {datetime.fromisoformat(order['created_at']).strftime('%d/%m/%Y %H:%M')}"],
            ]
            
            if order.get('table_number'):
                invoice_data.append([f"<b>Table:</b> {order['table_number']}"])
            
            invoice_table = Table(invoice_data, colWidths=[150*mm])
            invoice_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            story.append(invoice_table)
            story.append(Spacer(1, 20))
            
            # Tableau des articles
            items_data = [['Article', 'Qté', 'P.U.', 'Total']]
            
            subtotal = 0
            for item in order_items:
                items_data.append([
                    item['name'],
                    str(item['quantity']),
                    f"{item['unit_price']:.2f} {currency}",
                    f"{item['total_price']:.2f} {currency}"
                ])
                subtotal += item['total_price']
            
            tax = subtotal * (tax_rate / 100)
            total = subtotal + tax
            
            # Ajouter les totaux
            items_data.append(['', '', '', ''])
            items_data.append(['', '', f'<b>Sous-total:</b>', f'{subtotal:.2f} {currency}'])
            items_data.append(['', '', f'<b>TVA ({tax_rate}%):</b>', f'{tax:.2f} {currency}'])
            items_data.append(['', '', f'<b>TOTAL TTC:</b>', f'<b>{total:.2f} {currency}</b>'])
            
            items_table = Table(items_data, colWidths=[80*mm, 25*mm, 35*mm, 40*mm])
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C2C2C')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -4), 1, colors.grey),
                ('LINEBELOW', (0, -4), (-1, -4), 2, colors.black),
            ]))
            story.append(items_table)
            story.append(Spacer(1, 20))
            
            # Méthode de paiement
            if order.get('payment_method'):
                payment_info = Paragraph(
                    f"<b>Mode de paiement:</b> {order['payment_method']}",
                    self.header_style
                )
                story.append(payment_info)
            
            # Pied de page
            story.append(Spacer(1, 30))
            footer = Paragraph(
                "Merci de votre visite!",
                ParagraphStyle(
                    'Footer',
                    parent=self.styles['Normal'],
                    fontSize=10,
                    textColor=colors.grey,
                    alignment=TA_CENTER
                )
            )
            story.append(footer)
            
            # Construire le PDF
            doc.build(story)
            return output_path
            
        except Exception as e:
            print(f"Erreur lors de la génération de la facture: {e}")
            raise

    def print_invoice(self, order_id):
        """Génère et imprime une facture"""
        try:
            pdf_path = self.generate_invoice(order_id)
            # Ouvrir le PDF avec le visualiseur par défaut (qui peut imprimer)
            import subprocess
            import platform
            
            if platform.system() == 'Windows':
                os.startfile(pdf_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', pdf_path])
            else:  # Linux
                subprocess.call(['xdg-open', pdf_path])
            
            return pdf_path
        except Exception as e:
            print(f"Erreur lors de l'impression: {e}")
            raise

