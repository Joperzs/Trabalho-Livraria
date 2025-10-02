import os
import sqlite3
from pathlib import Path
import logging

class InitializationService:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.directories = ['exports', 'backups', 'data', 'imports', 'reports', 'logs']
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        log_dir = self.base_dir / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / 'bookstore.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def create_directories(self):
        self.logger.info("Criando estrutura de diretórios...")
        
        for directory in self.directories:
            dir_path = self.base_dir / directory
            
            try:
                if not dir_path.exists():
                    os.makedirs(dir_path, exist_ok=True)
                    self.logger.info(f"✓ Diretório '{directory}' criado com sucesso")
                else:
                    self.logger.info(f"✓ Diretório '{directory}' já existe")
            except Exception as e:
                self.logger.error(f"✗ Erro ao criar diretório '{directory}': {e}")
    
    def create_database(self):
        db_path = self.base_dir / 'data' / 'bookstore.db'
        
        self.logger.info("Verificando banco de dados...")
        
        try:
            if not db_path.exists():
                conn = sqlite3.connect(str(db_path))
                self.logger.info(f"✓ Banco de dados criado: {db_path}")
                conn.close()
            else:
                self.logger.info(f"✓ Banco de dados já existe: {db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"✗ Erro ao criar banco de dados: {e}")
    
    def check_system_health(self):
        health = {
            'directories': True,
            'database': True,
            'issues': []
        }
        
        for directory in self.directories:
            dir_path = self.base_dir / directory
            if not dir_path.exists():
                health['directories'] = False
                health['issues'].append(f"Diretório '{directory}' não existe")
        
        db_path = self.base_dir / 'data' / 'bookstore.db'
        if not db_path.exists():
            health['database'] = False
            health['issues'].append("Banco de dados não existe")
        
        return health
    
    def initialize_system(self):
        print("\n" + "=" * 70)
        print("INICIALIZANDO SISTEMA DE GERENCIAMENTO DE LIVRARIA".center(70))
        print("=" * 70 + "\n")
        
        self.logger.info("Iniciando processo de inicialização do sistema...")
        self.create_directories()
        self.create_database()
        health = self.check_system_health()
        
        if health['directories'] and health['database']:
            self.logger.info("Sistema inicializado com sucesso!")
            print("\n✓ Sistema inicializado com sucesso!\n")
            print("=" * 70 + "\n")
        else:
            self.logger.warning("Sistema inicializado com problemas:")
            for issue in health['issues']:
                self.logger.warning(f"  - {issue}")
            print("\n⚠ Sistema inicializado com avisos. Verifique o log.\n")
            print("=" * 70 + "\n")
        
        return health
    
    def display_system_info(self):
        print("INFORMAÇÕES DO SISTEMA")
        print("-" * 70)
        print(f"Diretório base: {self.base_dir}")
        print(f"Banco de dados: {self.base_dir / 'data' / 'bookstore.db'}")
        print(f"Diretórios configurados: {', '.join(self.directories)}")
        print("-" * 70 + "\n")
