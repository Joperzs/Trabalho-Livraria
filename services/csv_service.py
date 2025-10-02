import csv
import pandas as pd
from pathlib import Path
from datetime import datetime
from models.book import Book
from services.validation_service import ValidationService
import logging

class CSVService:

    def __init__(self, database_manager):
        self.db_manager = database_manager
        self.validator = ValidationService()
        self.logger = logging.getLogger(__name__)
        
        Path("exports").mkdir(exist_ok=True)
        Path("imports").mkdir(exist_ok=True)
    
    def export_to_csv(self, filename=None):
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"books_export_{timestamp}.csv"
            
            filepath = Path("exports") / filename
            
            # Lê os dados do banco usando pandas
            df = pd.read_sql_table(
                "books", 
                self.db_manager.engine,
                columns=['id', 'title', 'author', 'publication_year', 'price', 'created_at']
            )
            
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            self.logger.info(f"Dados exportados com sucesso: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar CSV: {e}")
            return None
    
    def import_from_csv(self, filename="books_import.csv"):
        filepath = Path("imports") / filename
        
        if not filepath.exists():
            self.logger.error(f"Arquivo não encontrado: {filepath}")
            return {
                'success': False,
                'message': 'Arquivo não encontrado',
                'imported': 0,
                'failed': 0,
                'errors': []
            }
        
        imported_count = 0
        failed_count = 0
        errors = []
        
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, start=2):  # Linha 2 porque 1 é o cabeçalho
                    try:
                        title = row.get('title', '').strip().upper()
                        author = row.get('author', '').strip().upper()
                        year_str = row.get('publication_year', '').strip()
                        price_str = row.get('price', '').strip()
                        
                        is_valid, validation_errors = self.validator.validate_book_data(
                            title, author, year_str, price_str
                        )
                        
                        if not is_valid:
                            failed_count += 1
                            error_msg = f"Linha {row_num}: " + "; ".join(validation_errors)
                            errors.append(error_msg)
                            self.logger.warning(error_msg)
                            continue
                        
                        book = Book(
                            title=title,
                            author=author,
                            publication_year=int(year_str),
                            price=float(price_str)
                        )
                        
                        self.db_manager.add_book(book)
                        imported_count += 1
                        
                    except Exception as e:
                        failed_count += 1
                        error_msg = f"Linha {row_num}: {str(e)}"
                        errors.append(error_msg)
                        self.logger.error(error_msg)
            
            return {
                'success': True,
                'imported': imported_count,
                'failed': failed_count,
                'errors': errors
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao importar CSV: {e}")
            return {
                'success': False,
                'message': str(e),
                'imported': imported_count,
                'failed': failed_count,
                'errors': errors
            }
    
    def export_filtered_csv(self, books, filename=None):
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"books_filtered_{timestamp}.csv"
            
            filepath = Path("exports") / filename
            
            # Converte lista de livros para dicionários
            data = [book.to_dict() for book in books]
            
            # Cria DataFrame e exporta
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            self.logger.info(f"Filtro exportado com sucesso: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar filtro: {e}")
            return None
    
    def generate_csv_template(self):
        try:
            filepath = Path("imports") / "template_import.csv"
            
            # Dados de Exemplo
            template_data = [
                {
                    'title': 'O SENHOR DOS ANÉIS',
                    'author': 'J.R.R. TOLKIEN',
                    'publication_year': 1954,
                    'price': 89.90
                },
                {
                    'title': '1984',
                    'author': 'GEORGE ORWELL',
                    'publication_year': 1949,
                    'price': 45.50
                }
            ]
            
            df = pd.DataFrame(template_data)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            self.logger.info(f"Template CSV criado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Erro ao criar template: {e}")
            return None