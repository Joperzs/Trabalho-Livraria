from services.database_manager import DatabaseManager
from services.backup_service import BackupService
from services.csv_service import CSVService
from services.report_service import ReportService
import logging

class BookstoreService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_manager = DatabaseManager()
        self.backup_service = BackupService()
        self.csv_service = CSVService(self.db_manager)
        self.report_service = ReportService(self.db_manager)
        
        self.logger.info("BookstoreService inicializado com sucesso")
    
    def add_book(self, book):
        try:
            added_book = self.db_manager.add_book(book)

            self.backup_service.create_backup()
            
            return True, "Livro adicionado com sucesso!", added_book
            
        except Exception as e:
            self.logger.error(f"Erro ao adicionar livro: {e}")
            return False, f"Erro ao adicionar livro: {str(e)}", None
    
    def get_all_books(self):
        try:
            return self.db_manager.get_all_books()
        except Exception as e:
            self.logger.error(f"Erro ao buscar livros: {e}")
            return []
    
    def get_book_by_id(self, book_id):
        try:
            return self.db_manager.get_book_by_id(book_id)
        except Exception as e:
            self.logger.error(f"Erro ao buscar livro: {e}")
            return None
    
    def update_book(self, book_id, **updates):
        try:
            book = self.db_manager.get_book_by_id(book_id)
            if not book:
                return False, f"Livro com ID {book_id} não encontrado."
            
            if not updates:
                return False, "Nenhum campo foi especificado para atualização."
            
            success = self.db_manager.update_book(book_id, **updates)
            
            if success:
                self.backup_service.create_backup()
                
                updated_fields = ", ".join(updates.keys())
                return True, f"Livro atualizado com sucesso! Campos alterados: {updated_fields}"
            else:
                return False, "Erro ao atualizar livro."
                
        except Exception as e:
            self.logger.error(f"Erro ao atualizar livro: {e}")
            return False, f"Erro ao atualizar livro: {str(e)}"
    
    def delete_book(self, book_id):
        try:
            book = self.db_manager.get_book_by_id(book_id)
            if not book:
                return False, f"Livro com ID {book_id} não encontrado."
            
            success = self.db_manager.delete_book(book_id)
            
            if success:
                self.backup_service.create_backup()
                return True, "Livro removido com sucesso!"
            else:
                return False, "Erro ao remover livro."
                
        except Exception as e:
            self.logger.error(f"Erro ao remover livro: {e}")
            return False, f"Erro ao remover livro: {str(e)}"
    
    def search_by_author(self, author):
        try:
            return self.db_manager.search_books_by_author(author)
        except Exception as e:
            self.logger.error(f"Erro na busca por autor: {e}")
            return []
    
    def advanced_search(self, query):
        try:
            return self.db_manager.search_books(query)
        except Exception as e:
            self.logger.error(f"Erro na busca avançada: {e}")
            return []
    
    def export_to_csv(self, filename=None):
        try:
            filepath = self.csv_service.export_to_csv(filename)
            if filepath:
                return True, f"Dados exportados para: {filepath}"
            else:
                return False, "Erro ao exportar dados."
        except Exception as e:
            self.logger.error(f"Erro na exportação: {e}")
            return False, f"Erro ao exportar: {str(e)}"
    
    def import_from_csv(self, filename="books_import.csv"):
        try:
            result = self.csv_service.import_from_csv(filename)
            
            if result['success'] and result['imported'] > 0:
                self.backup_service.create_backup()
                
                message = f"Importação concluída!\n"
                message += f"  • Importados: {result['imported']}\n"
                message += f"  • Falharam: {result['failed']}"
                
                if result['errors']:
                    message += f"\n\nErros encontrados:\n"
                    for error in result['errors'][:5]:  # Mostra apenas os 5 primeiros erros
                        message += f"  • {error}\n"
                    
                    if len(result['errors']) > 5:
                        message += f"  ... e mais {len(result['errors']) - 5} erro(s)\n"
                
                return True, message, result
            else:
                return False, result.get('message', 'Erro ao importar'), result
                
        except Exception as e:
            self.logger.error(f"Erro na importação: {e}")
            return False, f"Erro ao importar: {str(e)}", {}
    
    def create_manual_backup(self):
        try:
            backup_path = self.backup_service.create_backup()
            if backup_path:
                return True, f"Backup criado: {backup_path.name}"
            else:
                return False, "Erro ao criar backup."
        except Exception as e:
            self.logger.error(f"Erro ao criar backup: {e}")
            return False, f"Erro ao criar backup: {str(e)}"
    
    def list_backups(self):
        try:
            return self.backup_service.list_backups()
        except Exception as e:
            self.logger.error(f"Erro ao listar backups: {e}")
            return []
    
    def generate_html_report(self):
        try:
            filepath = self.report_service.generate_html_report()
            if filepath:
                return True, f"Relatório HTML gerado: {filepath}"
            else:
                return False, "Erro ao gerar relatório."
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório: {e}")
            return False, f"Erro ao gerar relatório: {str(e)}"
    
    def generate_text_report(self):
        try:
            filepath = self.report_service.generate_text_report()
            if filepath:
                return True, f"Relatório TXT gerado: {filepath}"
            else:
                return False, "Erro ao gerar relatório."
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório: {e}")
            return False, f"Erro ao gerar relatório: {str(e)}"
    
    def get_statistics(self):
        try:
            return self.db_manager.get_statistics()
        except Exception as e:
            self.logger.error(f"Erro ao obter estatísticas: {e}")
            return {}
