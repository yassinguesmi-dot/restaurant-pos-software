import sys
from cx_Freeze import setup, Executable
import os

# Fichiers à inclure
include_files = []

# Configuration pour créer l'executable
setup(
    name='Café 216 POS',
    version='1.0.0',
    description='Point of Sale System for Café 216',
    executables=[
        Executable(
            script='main.py',
            base='Win32GUI',
            target_name='Cafe216_POS.exe',
            icon='assets/cafe216.ico' if os.path.exists('assets/cafe216.ico') else None
        )
    ],
    options={
        'build_exe': {
            'include_files': include_files,
            'packages': ['PyQt5', 'sqlite3'],
            'includes': ['src.database', 'src.main_window', 'src.screens.pos_screen', 
                        'src.screens.products_screen', 'src.screens.orders_screen',
                        'src.screens.reports_screen', 'src.screens.settings_screen'],
        }
    }
)
