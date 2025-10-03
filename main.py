from services.initialization_service import InitializationService
from services.bookstore_service import BookstoreService
from utils.screen_utils import ScreenUtils as ui
import sys

def main():
    init_service = InitializationService()
    init_service.initialize_system()
    
    bookstore = BookstoreService()
    
    running = True
    
    while running:
        try:
            ui.print_menu()
            
            try:
                choice = int(input(f"Escolha uma opção: ").strip())
            except ValueError:
                ui.print_error("Por favor, digite um número válido.")
                ui.pause()
                continue
            
            if choice == 1:
                try:
                    book = ui.ask_book_info()
                    success, message, added_book = bookstore.add_book(book)
                    
                    if success:
                        ui.print_success(message)
                        print(f"ID gerado: {added_book.id}")
                    else:
                        ui.print_error(message)
                except Exception as e:
                    ui.print_error(f"Erro ao adicionar livro: {e}")
                
                ui.pause()
            
            elif choice == 2:
                ui.print_header("LISTA DE LIVROS")
                books = bookstore.get_all_books()
                ui.print_books(books)
                ui.pause()
            
            elif choice == 3:
                try:
                    book_id, updates = ui.ask_update_book()
                    
                    if updates:
                        success, message = bookstore.update_book(book_id, **updates)
                        
                        if success:
                            ui.print_success(message)
                        else:
                            ui.print_error(message)
                    else:
                        ui.print_warning("Nenhuma alteração foi realizada.")
                except Exception as e:
                    ui.print_error(f"Erro ao atualizar livro: {e}")
                
                ui.pause()
            
            elif choice == 4:
                try:
                    book_id = ui.ask_delete_book()
                    
                    if book_id is not None:
                        success, message = bookstore.delete_book(book_id)
                        
                        if success:
                            ui.print_success(message)
                        else:
                            ui.print_error(message)
                except Exception as e:
                    ui.print_error(f"Erro ao remover livro: {e}")
                
                ui.pause()
            
            elif choice == 5:
                try:
                    author = ui.ask_search_author()
                    books = bookstore.search_by_author(author)
                    ui.print_books(books)
                except Exception as e:
                    ui.print_error(f"Erro na busca: {e}")
                
                ui.pause()
            
            elif choice == 6:
                try:
                    query = ui.ask_search_query()
                    books = bookstore.advanced_search(query)
                    ui.print_books(books)
                except Exception as e:
                    ui.print_error(f"Erro na busca: {e}")
                
                ui.pause()
            
            elif choice == 7:
                ui.print_header("EXPORTAR PARA CSV")
                
                try:
                    success, message = bookstore.export_to_csv()
                    
                    if success:
                        ui.print_success(message)
                    else:
                        ui.print_error(message)
                except Exception as e:
                    ui.print_error(f"Erro na exportação: {e}")
                
                ui.pause()
            
            elif choice == 8:
                ui.print_header("IMPORTAR DE CSV")
                
                filename = input("Nome do arquivo (padrão: books.csv): ").strip()
                if not filename:
                    filename = "books.csv"
                
                try:
                    success, message, stats = bookstore.import_from_csv(filename)
                    
                    if success:
                        ui.print_success("Importação concluída!")
                        print(message)
                    else:
                        ui.print_error(message)
                except Exception as e:
                    ui.print_error(f"Erro na importação: {e}")
                
                ui.pause()
            
            elif choice == 9:
                ui.print_header("GERAR RELATÓRIO HTML")
                
                try:
                    success, message = bookstore.generate_html_report()
                    
                    if success:
                        ui.print_success(message)
                        ui.print_info("Abra o arquivo HTML no seu navegador para visualizar.")
                    else:
                        ui.print_error(message)
                except Exception as e:
                    ui.print_error(f"Erro ao gerar relatório: {e}")
                
                ui.pause()
            
            elif choice == 10:
                ui.print_header("CRIAR BACKUP")
                
                try:
                    success, message = bookstore.create_manual_backup()
                    
                    if success:
                        ui.print_success(message)
                    else:
                        ui.print_error(message)
                except Exception as e:
                    ui.print_error(f"Erro ao criar backup: {e}")
                
                ui.pause()
            
            elif choice == 11:
                try:
                    stats = bookstore.get_statistics()
                    ui.print_statistics(stats)
                except Exception as e:
                    ui.print_error(f"Erro ao obter estatísticas: {e}")
                
                ui.pause()
            
            elif choice == 12:
                ui.print_header("BACKUPS DISPONÍVEIS")
                
                try:
                    backups = bookstore.list_backups()
                    ui.print_backups(backups)
                    
                    if backups:
                        total_size = bookstore.backup_service.get_backup_size_total()
                        ui.print_info(f"Espaço total ocupado: {total_size['mb']} MB")
                except Exception as e:
                    ui.print_error(f"Erro ao listar backups: {e}")
                
                ui.pause()
            
            elif choice == 0:
                ui.print_header("ENCERRANDO SISTEMA")
                
                if ui.ask_confirmation("Deseja fazer um backup antes de sair?"):
                    success, message = bookstore.create_manual_backup()
                    if success:
                        ui.print_success(message)
                print("Todos os dados foram salvos com segurança.\n")
                running = False
            
            else:
                ui.print_warning("Opção inválida! Por favor, escolha uma opção do menu.")
                ui.pause()
        
        except KeyboardInterrupt:
            print("\n\nInterrupção detectada!")
            if ui.ask_confirmation("Deseja realmente sair?"):
                running = False
        
        except Exception as e:
            ui.print_error(f"Erro inesperado: {e}")
            ui.pause()
    
    sys.exit(0)

if __name__ == "__main__":
    main()
