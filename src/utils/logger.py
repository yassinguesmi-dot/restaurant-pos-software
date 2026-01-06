import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, log_file="logs/app.log"):
        # Créer le dossier logs s'il n'existe pas
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configurer le logger
        self.logger = logging.getLogger('POS_System')
        self.logger.setLevel(logging.DEBUG)
        
        # Handler pour fichier
        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            # Handler pour console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Format
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message, exc_info=False):
        self.logger.error(message, exc_info=exc_info)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def debug(self, message):
        self.logger.debug(message)

# Instance globale
logger = Logger()

