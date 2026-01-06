import os
from pathlib import Path

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

# Import existing backend
try:
    from src.database import Database
except ImportError:
    # Fallback if imports fail on Android
    Database = None

BASE_DIR = Path(__file__).resolve().parent
KV_PATH = BASE_DIR / "ui" / "main.kv"


class LoginScreen(Screen):
    def do_login(self):
        app = App.get_running_app()
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        if not username or not password:
            self.ids.status.text = "Veuillez saisir vos identifiants"
            return
        # Use verify_user_credentials instead of authenticate_user
        user = app.db.verify_user_credentials(username, password)
        if user:
            app.current_user = dict(user)
            self.ids.status.text = ""
            self.ids.username.text = ""
            self.ids.password.text = ""
            app.switch_to("home")
        else:
            self.ids.status.text = "Identifiants invalides"


class HomeScreen(Screen):
    pass


class POSScreen(Screen):
    pass


class ProductsScreen(Screen):
    pass


class OrdersScreen(Screen):
    pass


class ReportsScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class PriceManagementScreen(Screen):
    pass


class StockManagementScreen(Screen):
    pass


class TablesScreen(Screen):
    pass


class Cafe216App(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.db = Database()
        except Exception as e:
            print(f"Database error: {e}")
            self.db = None
        self.current_user = None

    def build(self):
        Builder.load_file(str(KV_PATH))
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(POSScreen(name="pos"))
        sm.add_widget(ProductsScreen(name="products"))
        sm.add_widget(OrdersScreen(name="orders"))
        sm.add_widget(ReportsScreen(name="reports"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(PriceManagementScreen(name="price_mgmt"))
        sm.add_widget(StockManagementScreen(name="stock"))
        sm.add_widget(TablesScreen(name="tables"))
        return sm

    def switch_to(self, screen_name):
        self.root.current = screen_name


def main():
    app = Cafe216App()
    app.run()


if __name__ == "__main__":
    main()
