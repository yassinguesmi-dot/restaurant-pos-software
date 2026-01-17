import sqlite3
import os
from datetime import datetime
import bcrypt

# Import logger si disponible
try:
    from src.utils.logger import logger
except ImportError:
    # Logger simple si le module n'est pas disponible
    class SimpleLogger:
        def info(self, msg): print(f"INFO: {msg}")
        def error(self, msg, exc_info=False): print(f"ERROR: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
        def debug(self, msg): print(f"DEBUG: {msg}")
    logger = SimpleLogger()

class Database:
    def __init__(self, db_path="cafe216_pos.db"):
        # Resolve to a stable, user-specific path if default is used
        self.db_path = self._resolve_default_db_path(db_path)
        self.connection = None
        self.init_database()
        self.init_sample_products()

    def _resolve_default_db_path(self, provided_path: str) -> str:
        # If a custom path was provided, use it as-is
        if provided_path and provided_path != "cafe216_pos.db":
            return provided_path
        try:
            # Prefer OS-specific app data locations to avoid cwd issues
            if os.name == "nt":
                appdata = os.environ.get("APPDATA")
                base_dir = os.path.join(appdata or os.path.expanduser("~"), "Cafe216", "POS")
            else:
                base_dir = os.path.join(os.path.expanduser("~"), ".cafe216")
            os.makedirs(base_dir, exist_ok=True)
            new_path = os.path.join(base_dir, "cafe216_pos.db")
            # Migrate existing cwd database if present and target missing
            cwd_path = os.path.join(os.getcwd(), "cafe216_pos.db")
            if os.path.exists(cwd_path) and not os.path.exists(new_path):
                try:
                    import shutil
                    shutil.copy2(cwd_path, new_path)
                except Exception:
                    pass
            return new_path
        except Exception:
            # Fallback to current directory if anything goes wrong
            return provided_path or "cafe216_pos.db"

    def init_database(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.create_tables()
            logger.info(f"Base de données initialisée: {self.db_path}")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la base de données: {e}", exc_info=True)
            raise

    def create_tables(self):
        cursor = self.connection.cursor()
        
        # Table des produits (avec stock)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT,
                image_path TEXT,
                quantity INTEGER DEFAULT 0,
                min_quantity INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Migration: ajouter colonnes stock si elles n'existent pas
        try:
            cursor.execute('ALTER TABLE products ADD COLUMN quantity INTEGER DEFAULT 0')
            logger.info("Colonne 'quantity' ajoutée à la table products")
        except sqlite3.OperationalError:
            pass  # Colonne existe déjà
        except Exception as e:
            logger.warning(f"Erreur lors de l'ajout de la colonne quantity: {e}")
        
        try:
            cursor.execute('ALTER TABLE products ADD COLUMN min_quantity INTEGER DEFAULT 0')
            logger.info("Colonne 'min_quantity' ajoutée à la table products")
        except sqlite3.OperationalError:
            pass  # Colonne existe déjà
        except Exception as e:
            logger.warning(f"Erreur lors de l'ajout de la colonne min_quantity: {e}")
        
        # Table des mouvements de stock
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                movement_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                previous_quantity INTEGER,
                new_quantity INTEGER,
                reason TEXT,
                order_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(product_id) REFERENCES products(id),
                FOREIGN KEY(order_id) REFERENCES orders(id)
            )
        ''')
        
        # Table des tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_number TEXT UNIQUE NOT NULL,
                status TEXT DEFAULT 'libre',
                capacity INTEGER DEFAULT 4,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des utilisateurs/employés
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT,
                full_name TEXT,
                role TEXT DEFAULT 'employé',
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des paramètres
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Table des commandes (avec table_id et invoice_number)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_number TEXT UNIQUE,
                invoice_number TEXT UNIQUE,
                table_id INTEGER,
                user_id INTEGER,
                total_amount REAL,
                payment_method TEXT,
                status TEXT DEFAULT 'en attente',
                is_partial_payment INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY(table_id) REFERENCES tables(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        # Migration: ajouter colonnes si elles n'existent pas
        migrations = [
            ('ALTER TABLE orders ADD COLUMN table_id INTEGER', 'table_id'),
            ('ALTER TABLE orders ADD COLUMN user_id INTEGER', 'user_id'),
            ('ALTER TABLE orders ADD COLUMN invoice_number TEXT UNIQUE', 'invoice_number'),
            ('ALTER TABLE orders ADD COLUMN is_partial_payment INTEGER DEFAULT 0', 'is_partial_payment')
        ]
        
        for sql, col_name in migrations:
            try:
                cursor.execute(sql)
                logger.info(f"Colonne '{col_name}' ajoutée à la table orders")
            except sqlite3.OperationalError:
                pass  # Colonne existe déjà
            except Exception as e:
                logger.warning(f"Erreur lors de l'ajout de la colonne {col_name}: {e}")
        
        # Table des détails des commandes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                unit_price REAL,
                total_price REAL,
                FOREIGN KEY(order_id) REFERENCES orders(id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        ''')
        
        # Table des paiements (avec change et montant reçu)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                amount REAL,
                amount_received REAL,
                change_amount REAL,
                payment_method TEXT,
                is_split INTEGER DEFAULT 0,
                split_number INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(order_id) REFERENCES orders(id)
            )
        ''')
        
        # Migration: ajouter colonnes paiement si elles n'existent pas
        payment_migrations = [
            ('ALTER TABLE payments ADD COLUMN amount_received REAL', 'amount_received'),
            ('ALTER TABLE payments ADD COLUMN change_amount REAL', 'change_amount'),
            ('ALTER TABLE payments ADD COLUMN is_split INTEGER DEFAULT 0', 'is_split'),
            ('ALTER TABLE payments ADD COLUMN split_number INTEGER', 'split_number')
        ]
        
        for sql, col_name in payment_migrations:
            try:
                cursor.execute(sql)
                logger.info(f"Colonne '{col_name}' ajoutée à la table payments")
            except sqlite3.OperationalError:
                pass  # Colonne existe déjà
            except Exception as e:
                logger.warning(f"Erreur lors de l'ajout de la colonne {col_name}: {e}")
        
        # Initialiser les tables par défaut
        cursor.execute('SELECT COUNT(*) FROM tables')
        if cursor.fetchone()[0] == 0:
            for i in range(1, 11):
                cursor.execute('''
                    INSERT INTO tables (table_number, status, capacity)
                    VALUES (?, 'libre', ?)
                ''', (f"Table {i}", 4))
        
        # Initialiser utilisateur admin par défaut
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            hashed_admin = self.hash_password('admin')
            cursor.execute('''
                INSERT INTO users (username, password, full_name, role)
                VALUES (?, ?, ?, ?)
            ''', ('admin', hashed_admin, 'Administrateur', 'admin'))
        
        # Initialiser paramètres par défaut
        default_settings = [
            ('restaurant_name', 'Café 216'),
            ('restaurant_address', 'Rue du Commerce'),
            ('restaurant_phone', '+216 XX XXX XXX'),
            ('currency', 'TND'),
            ('tax_rate', '20'),
            ('opening_hours', '08:00-22:00'),
            ('invoice_prefix', 'FAC'),
            ('dark_mode', '0')
        ]
        for key, value in default_settings:
            cursor.execute('''
                INSERT OR IGNORE INTO settings (key, value)
                VALUES (?, ?)
            ''', (key, value))
        
        # S'assurer que les mots de passe existants sont hachés
        self.ensure_hashed_passwords()

        self.connection.commit()

    def init_sample_products(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM products')
        if cursor.fetchone()[0] == 0:
            products = [
                ("Express", 2.0, "Cafés"),
                ("Cappucin", 2.2, "Cafés"),
                ("Direct", 2.5, "Cafés"),
                ("Café Spécial", 3.5, "Cafés"),
                ("Chocolat Chaud", 2.8, "Cafés"),
                ("Américain", 2.5, "Cafés"),
                # Jus
                ("Citronade", 3.0, "Jus"),
                ("Citronade Panachée", 3.5, "Jus"),
                ("Jus de Saison", 3.2, "Jus"),
                ("Jwajem", 5.0, "Jus"),
                # Chichas
                ("Quasar", 4.5, "Chichas"),
                ("Kaloud", 5.0, "Chichas"),
                ("Chicha Turc", 6.0, "Chichas"),
                # Boissons
                ("Eau 0,5 L", 1.0, "Boissons"),
                ("Eau 1 L", 1.5, "Boissons"),
                ("Eau 1,5 L", 1.5, "Boissons"),
                ("Canette", 2.0, "Boissons"),
                ("Gazouze", 1.5, "Boissons"),
                # Gâteaux
                ("Cake", 2.0, "Gâteaux"),
                ("Croissant", 2.5, "Gâteaux"),
                ("Mille Feuilles", 4.5, "Gâteaux"),
                ("Pâté", 3.5, "Gâteaux"),
            ]
            
            for name, price, category in products:
                cursor.execute('''
                    INSERT INTO products (name, price, category)
                    VALUES (?, ?, ?)
                ''', (name, price, category))
            
            self.connection.commit()

    def add_product(self, name, price, category, image_path=None, quantity=0, min_quantity=0):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO products (name, price, category, image_path, quantity, min_quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, price, category, image_path, quantity, min_quantity))
        self.connection.commit()
        return cursor.lastrowid

    def get_all_products(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM products')
        return [dict(row) for row in cursor.fetchall()]

    def get_products_by_category(self, category):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM products WHERE category = ?', (category,))
        return [dict(row) for row in cursor.fetchall()]

    def get_categories(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT DISTINCT category FROM products ORDER BY category')
        return [row[0] for row in cursor.fetchall()]

    def update_product(self, product_id, name, price, category, quantity=None, min_quantity=None):
        cursor = self.connection.cursor()
        if quantity is not None and min_quantity is not None:
            cursor.execute('''
                UPDATE products SET name = ?, price = ?, category = ?, quantity = ?, min_quantity = ?
                WHERE id = ?
            ''', (name, price, category, quantity, min_quantity, product_id))
        else:
            cursor.execute('''
                UPDATE products SET name = ?, price = ?, category = ?
                WHERE id = ?
            ''', (name, price, category, product_id))
        self.connection.commit()

    def delete_product(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        self.connection.commit()

    def create_order(self, items, table_id=None, user_id=None):
        cursor = self.connection.cursor()
        order_number = f"CMD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        invoice_number = self.get_next_invoice_number()
        
        # Calculer le montant total (en excluant les articles marqués comme retour)
        total_amount = sum(item['quantity'] * item['unit_price'] 
                          for item in items 
                          if not item.get('is_return', False))
        
        # Vérifier le stock avant de créer la commande
        for item in items:
            stock, _ = self.get_product_stock(item['product_id'])
            if stock < item['quantity']:
                raise ValueError(f"Stock insuffisant pour le produit ID {item['product_id']}")
        
        cursor.execute('''
            INSERT INTO orders (order_number, invoice_number, table_id, user_id, total_amount, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (order_number, invoice_number, table_id, user_id, total_amount, 'en attente'))
        
        order_id = cursor.lastrowid
        
        # Traiter chaque article
        for item in items:
            is_return = item.get('is_return', False)
            # Le prix enregistré est 0 pour les retours
            unit_price = 0 if is_return else item['unit_price']
            total_price = 0 if is_return else (item['quantity'] * item['unit_price'])
            
            cursor.execute('''
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (order_id, item['product_id'], item['quantity'], unit_price, total_price))
            
            # Décrémenter le stock (même pour les retours)
            reason = "Remplacement (Retour)" if is_return else "Vente"
            self.decrement_stock(item['product_id'], item['quantity'], order_id, reason)
        
        # Mettre à jour le statut de la table si nécessaire
        if table_id:
            self.update_table_status(table_id, 'occupée')
        
        self.connection.commit()
        return order_id, order_number, invoice_number, total_amount

    def get_all_orders(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM orders ORDER BY created_at DESC')
        return [dict(row) for row in cursor.fetchall()]

    def get_order_details(self, order_id):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT oi.*, p.name 
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        return [dict(row) for row in cursor.fetchall()]

    def record_payment(self, order_id, amount, payment_method, amount_received=None, 
                       change_amount=None, is_split=False, split_number=None, is_partial=False):
        cursor = self.connection.cursor()
        
        # Calculer le change si montant reçu fourni
        if amount_received is not None and change_amount is None:
            change_amount = max(0, amount_received - amount)
        
        cursor.execute('''
            INSERT INTO payments (order_id, amount, amount_received, change_amount, 
                                payment_method, is_split, split_number)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (order_id, amount, amount_received, change_amount, payment_method, 
              is_split, split_number))
        
        # Mettre à jour le statut de la commande
        if is_partial:
            cursor.execute('''
                UPDATE orders SET is_partial_payment = 1
                WHERE id = ?
            ''', (order_id,))
        else:
            cursor.execute('''
                UPDATE orders SET status = 'payé', completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (order_id,))
            
            # Libérer la table si la commande est payée
            cursor.execute('SELECT table_id FROM orders WHERE id = ?', (order_id,))
            result = cursor.fetchone()
            if result and result['table_id']:
                # Vérifier s'il y a d'autres commandes en cours sur cette table
                cursor.execute('''
                    SELECT COUNT(*) FROM orders
                    WHERE table_id = ? AND status != 'payé' AND id != ?
                ''', (result['table_id'], order_id))
                if cursor.fetchone()[0] == 0:
                    self.update_table_status(result['table_id'], 'libre')
        
        self.connection.commit()

    def get_daily_revenue(self, date=None):
        cursor = self.connection.cursor()
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT COALESCE(SUM(total_amount), 0) as revenue, COUNT(*) as orders_count
            FROM orders
            WHERE DATE(created_at) = ? AND status = 'payé'
        ''', (date,))
        result = cursor.fetchone()
        return (result['revenue'] or 0, result['orders_count'] or 0)

    def get_top_products(self, date=None):
        cursor = self.connection.cursor()
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT p.name, SUM(oi.quantity) as total_qty, SUM(oi.total_price) as total_amount
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            JOIN orders o ON oi.order_id = o.id
            WHERE DATE(o.created_at) = ? AND o.status = 'payé'
            GROUP BY p.id, p.name
            ORDER BY total_qty DESC
            LIMIT 10
        ''', (date,))
        return [dict(row) for row in cursor.fetchall()]

    # ========== GESTION DU STOCK ==========
    def update_product_stock(self, product_id, quantity, min_quantity=None):
        cursor = self.connection.cursor()
        if min_quantity is not None:
            cursor.execute('''
                UPDATE products SET quantity = ?, min_quantity = ?
                WHERE id = ?
            ''', (quantity, min_quantity, product_id))
        else:
            cursor.execute('''
                UPDATE products SET quantity = ?
                WHERE id = ?
            ''', (quantity, product_id))
        self.connection.commit()

    def get_product_stock(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT quantity, min_quantity FROM products WHERE id = ?', (product_id,))
        result = cursor.fetchone()
        return result['quantity'] if result else 0, result['min_quantity'] if result else 0

    def decrement_stock(self, product_id, quantity, order_id=None, reason="Vente"):
        cursor = self.connection.cursor()
        cursor.execute('SELECT quantity FROM products WHERE id = ?', (product_id,))
        result = cursor.fetchone()
        if not result:
            return False
        
        previous_qty = result['quantity']
        new_qty = max(0, previous_qty - quantity)
        
        cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (new_qty, product_id))
        
        # Enregistrer le mouvement
        cursor.execute('''
            INSERT INTO stock_movements (product_id, movement_type, quantity, 
                                       previous_quantity, new_quantity, reason, order_id)
            VALUES (?, 'sortie', ?, ?, ?, ?, ?)
        ''', (product_id, quantity, previous_qty, new_qty, reason, order_id))
        
        self.connection.commit()
        return True

    def increment_stock(self, product_id, quantity, reason="Réapprovisionnement"):
        cursor = self.connection.cursor()
        cursor.execute('SELECT quantity FROM products WHERE id = ?', (product_id,))
        result = cursor.fetchone()
        if not result:
            return False
        
        previous_qty = result['quantity']
        new_qty = previous_qty + quantity
        
        cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (new_qty, product_id))
        
        # Enregistrer le mouvement
        cursor.execute('''
            INSERT INTO stock_movements (product_id, movement_type, quantity, 
                                       previous_quantity, new_quantity, reason)
            VALUES (?, 'entrée', ?, ?, ?, ?)
        ''', (product_id, quantity, previous_qty, new_qty, reason))
        
        self.connection.commit()
        return True

    def get_stock_movements(self, product_id=None, limit=100):
        cursor = self.connection.cursor()
        if product_id:
            cursor.execute('''
                SELECT sm.*, p.name as product_name
                FROM stock_movements sm
                JOIN products p ON sm.product_id = p.id
                WHERE sm.product_id = ?
                ORDER BY sm.created_at DESC
                LIMIT ?
            ''', (product_id, limit))
        else:
            cursor.execute('''
                SELECT sm.*, p.name as product_name
                FROM stock_movements sm
                JOIN products p ON sm.product_id = p.id
                ORDER BY sm.created_at DESC
                LIMIT ?
            ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]

    def get_low_stock_products(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT * FROM products
            WHERE quantity <= min_quantity AND min_quantity > 0
            ORDER BY quantity ASC
        ''')
        return cursor.fetchall()

    # ========== GESTION DES TABLES ==========
    def get_all_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM tables ORDER BY table_number')
        return [dict(row) for row in cursor.fetchall()]

    def get_table(self, table_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM tables WHERE id = ?', (table_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_table_status(self, table_id, status):
        cursor = self.connection.cursor()
        cursor.execute('UPDATE tables SET status = ? WHERE id = ?', (status, table_id))
        self.connection.commit()

    def get_table_orders(self, table_id, status=None):
        cursor = self.connection.cursor()
        if status:
            cursor.execute('''
                SELECT * FROM orders
                WHERE table_id = ? AND status = ?
                ORDER BY created_at DESC
            ''', (table_id, status))
        else:
            cursor.execute('''
                SELECT * FROM orders
                WHERE table_id = ?
                ORDER BY created_at DESC
            ''', (table_id,))
        return [dict(row) for row in cursor.fetchall()]

    # ========== GESTION DES UTILISATEURS ==========
    def get_all_users(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE is_active = 1')
        return [dict(row) for row in cursor.fetchall()]
    def get_user(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_user_by_username(self, username):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def hash_password(self, password: str) -> str:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    def is_password_hashed(self, password: str) -> bool:
        return isinstance(password, str) and password.startswith('$2b$')

    def verify_user_credentials(self, username: str, password: str):
        user = self.get_user_by_username(username)
        if not user or not user['is_active']:
            return None

        stored_password = user['password'] or ''
        try:
            if self.is_password_hashed(stored_password):
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    return user
                return None

            # Ancien mot de passe en clair: on vérifie puis on migre en haché
            if password == stored_password:
                new_hash = self.hash_password(password)
                cursor = self.connection.cursor()
                cursor.execute('UPDATE users SET password = ? WHERE id = ?', (new_hash, user['id']))
                self.connection.commit()
                return self.get_user(user['id'])
        except Exception as e:
            logger.error(f"Erreur lors de la vérification des identifiants: {e}", exc_info=True)
            return None

        return None

    def ensure_hashed_passwords(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT id, password FROM users')
        users = cursor.fetchall()
        for user in users:
            pwd = user['password'] or ''
            if not self.is_password_hashed(pwd) and pwd:
                try:
                    new_hash = self.hash_password(pwd)
                    cursor.execute('UPDATE users SET password = ? WHERE id = ?', (new_hash, user['id']))
                    logger.info(f"Mot de passe haché pour l'utilisateur ID {user['id']}")
                except Exception as e:
                    logger.warning(f"Impossible de hacher le mot de passe de l'utilisateur ID {user['id']}: {e}")
        self.connection.commit()

    def get_most_active_user(self, date=None):
        cursor = self.connection.cursor()
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT u.id, u.full_name, COUNT(o.id) as orders_count
            FROM users u
            JOIN orders o ON u.id = o.user_id
            WHERE DATE(o.created_at) = ? AND o.status = 'payé'
            GROUP BY u.id, u.full_name
            ORDER BY orders_count DESC
            LIMIT 1
        ''', (date,))
        row = cursor.fetchone()
        return dict(row) if row else None

    # ========== GESTION DES PARAMÈTRES ==========
    def get_setting(self, key, default=None):
        cursor = self.connection.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        return result['value'] if result else default

    def set_setting(self, key, value):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        ''', (key, str(value)))
        self.connection.commit()

    def get_all_settings(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM settings')
        return {row['key']: row['value'] for row in cursor.fetchall()}

    # ========== GESTION DES FACTURES ==========
    def get_next_invoice_number(self):
        cursor = self.connection.cursor()
        prefix = self.get_setting('invoice_prefix', 'FAC')

        cursor.execute('''
            SELECT MAX(CAST(SUBSTR(invoice_number, LENGTH(?) + 1) AS INTEGER)) as max_num
            FROM orders
            WHERE invoice_number LIKE ? || '%'
        ''', (prefix, prefix))
        result = cursor.fetchone()
        max_num = result['max_num'] if result and result['max_num'] else 0
        return f"{prefix}{max_num + 1:06d}"

    # ========== RAPPORTS AVANCÉS ==========
    def get_monthly_revenue(self, year=None, month=None):
        cursor = self.connection.cursor()
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        cursor.execute('''
            SELECT SUM(total_amount) as revenue, COUNT(*) as orders_count
            FROM orders
            WHERE strftime('%Y', created_at) = ? 
            AND strftime('%m', created_at) = ?
            AND status = 'payé'
        ''', (str(year), f"{month:02d}"))
        result = cursor.fetchone()
        return result['revenue'] if result['revenue'] else 0, result['orders_count'] if result['orders_count'] else 0

    def get_revenue_by_date_range(self, start_date, end_date):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT DATE(created_at) as date, SUM(total_amount) as revenue, COUNT(*) as orders_count
            FROM orders
            WHERE DATE(created_at) BETWEEN ? AND ?
            AND status = 'payé'
            GROUP BY DATE(created_at)
            ORDER BY date
        ''', (start_date, end_date))
        return [dict(row) for row in cursor.fetchall()]

    # ========== SAUVEGARDE ==========
    def backup_database(self, backup_path):
        import shutil
        try:
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()

