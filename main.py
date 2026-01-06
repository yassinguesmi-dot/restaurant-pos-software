import sys
from PyQt5.QtWidgets import QApplication
from src.main_window import MainWindow
from src.database import Database
from src.screens.login_screen import LoginDialog

def main():
    app = QApplication(sys.argv)
    db = Database()

    login = LoginDialog(db)
    if login.exec_() != login.Accepted:
        sys.exit(0)

    window = MainWindow(db, login.authenticated_user)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
