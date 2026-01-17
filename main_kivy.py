import os
from pathlib import Path

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.resources import resource_find
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

BASE_DIR = Path(__file__).resolve().parent
KV_PATH = BASE_DIR / "ui" / "main.kv"


class LoginScreen(Screen):
    def do_login(self):
        app = App.get_running_app()
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        if not username or not password:
            self.ids.status.text = "Please enter credentials"
            return
        
        # Simple hardcoded auth for mobile version
        if username == "admin" and password == "admin":
            app.current_user = {"username": username, "role": "admin"}
            self.ids.status.text = ""
            self.ids.username.text = ""
            self.ids.password.text = ""
            app.switch_to("home")
        else:
            self.ids.status.text = "Invalid credentials"


class HomeScreen(Screen):
    pass


class POSScreen(Screen):
    pass


class ProductsScreen(Screen):
    def on_pre_enter(self, *args):
        # e.g., reload list data or totals
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
        self.current_user = None
        self.title = "Cafe216 POS"
        # If an icon exists next to the kv or inside ui/, set it
        icon_path = (
            (BASE_DIR / "icon.png") if (BASE_DIR / "icon.png").exists() else (BASE_DIR / "ui" / "icon.png")
        )
        if icon_path.exists():
            try:
                self.icon = str(icon_path)
            except Exception:
                pass

    def build(self):
        # Prefer resource_find so it works inside packaged APK
        kv_file = resource_find(str(KV_PATH)) or str(KV_PATH)
        Builder.load_file(kv_file)

        # Ensure landscape and keep the app awake (handled by Android manifest/orientation)
        try:
            Window.rotation = 0
        except Exception:
            pass

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

        # Bind Android back button / ESC handling
        Window.bind(on_keyboard=self._on_keyboard)
        Clock.schedule_once(lambda *_: self._post_build_init(), 0)
        return sm

    def switch_to(self, screen_name):
        # Prevent accessing protected screens when not logged in
        protected = {"home", "pos", "products", "orders", "reports", "settings", "price_mgmt", "stock", "tables"}
        if screen_name in protected and not self.current_user:
            self.root.current = "login"
            return
        if screen_name not in {s.name for s in self.root.screens}:
            return
        self.root.current = screen_name

    def logout(self):
        self.current_user = None
        self.switch_to("login")

    def _post_build_init(self):
        # Start at login always
        self.switch_to("login")

    def _on_keyboard(self, window, key, scancode, codepoint, modifier):
        # Android back button = 27 or 1001 depending on provider; ESC on desktop = 27
        if key in (27, 1001):
            current = self.root.current
            if current in ("login", "home"):
                # From home/login, go to login and allow app to close if pressed again
                if current == "home":
                    self.switch_to("login")
                    return True
                return False  # let the OS handle quit from login
            # From any other screen, go back to home
            self.switch_to("home")
            return True
        return False

    def on_pause(self):
        # Keep app state; allow pause on Android
        return True


def main():
    app = Cafe216App()
    app.run()


if __name__ == "__main__":
    main()
