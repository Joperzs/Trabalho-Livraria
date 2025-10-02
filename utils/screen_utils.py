from models.book import Book
from services.validation_service import ValidationService

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ScreenUtils:
    validator = ValidationService()
    
    @staticmethod
    def clear_screen():
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(text):
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}")
        print(f"{text.center(70)}")
        print(f"{'=' * 70}{Colors.ENDC}\n")
    
    @staticmethod
    def print_menu():
        ScreenUtils.print_header("SISTEMA DE GERENCIAMENTO DE LIVRARIA")
        
        menu_items = [
            ("1", "Adicionar novo livro", "➕"),
            ("2", "Exibir todos os livros", "📋"),
            ("3", "Atualizar dados de um livro", "✏️"),
            ("4", "Remover um livro", "🗑️"),
            ("5", "Buscar livros por autor", "🔍"),
            ("6", "Busca avançada (título/autor)", "🔎"),
            ("7", "Exportar dados para CSV", "📤"),
            ("8", "Importar dados de CSV", "📥"),
            ("9", "Gerar relatório HTML", "📊"),
            ("10", "Fazer backup do banco de dados", "💾"),
            ("11", "Ver estatísticas", "📈"),
            ("12", "Listar backups disponíveis", "📂"),
            ("0", "Sair", "🚪")
        ]
        
        for num, desc, icon in menu_items:
            print(f"{Colors.CYAN}{num:>3}.{Colors.ENDC} {icon}  {desc}")
        
        print(f"\n{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")
    
    @staticmethod
    def get_validated_input(prompt, validator_func, error_message="Entrada inválida"):
        while True:
            value = input(f"{Colors.BLUE}{prompt}{Colors.ENDC}").strip()
            
            is_valid, error = validator_func(value)
            
            if is_valid:
                return value
            else:
                print(f"{Colors.RED}✗ {error}{Colors.ENDC}")
    
    @classmethod
    def ask_book_info(cls):
        cls.print_header("ADICIONAR NOVO LIVRO")
        
        title = cls.get_validated_input(
            "Título do livro: ",
            cls.validator.validate_title
        ).strip().upper()
        
        author = cls.get_validated_input(
            "Autor: ",
            cls.validator.validate_author
        ).strip().upper()
        
        year = int(cls.get_validated_input(
            "Ano de publicação: ",
            cls.validator.validate_year
        ))
        
        price = float(cls.get_validated_input(
            "Preço (R$): ",
            cls.validator.validate_price
        ))
        
        return Book(
            title=title,
            author=author,
            publication_year=year,
            price=price
        )
    
    @classmethod
    def ask_update_book(cls):
        cls.print_header("ATUALIZAR LIVRO")
        
        book_id = int(cls.get_validated_input(
            "ID do livro: ",
            cls.validator.validate_id
        ))
        
        print(f"\n{Colors.CYAN}Deixe em branco os campos que NÃO deseja alterar{Colors.ENDC}\n")
        
        updates = {}
        
        title = input(f"{Colors.BLUE}Novo título (Enter para manter): {Colors.ENDC}").strip()
        if title:
            valid, error = cls.validator.validate_title(title)
            if valid:
                updates['title'] = title.upper()
            else:
                print(f"{Colors.RED}✗ {error} - Título não será alterado{Colors.ENDC}")
        
        author = input(f"{Colors.BLUE}Novo autor (Enter para manter): {Colors.ENDC}").strip()
        if author:
            valid, error = cls.validator.validate_author(author)
            if valid:
                updates['author'] = author.upper()
            else:
                print(f"{Colors.RED}✗ {error} - Autor não será alterado{Colors.ENDC}")

        year = input(f"{Colors.BLUE}Novo ano de publicação (Enter para manter): {Colors.ENDC}").strip()
        if year:
            valid, error = cls.validator.validate_year(year)
            if valid:
                updates['publication_year'] = int(year)
            else:
                print(f"{Colors.RED}✗ {error} - Ano não será alterado{Colors.ENDC}")

        price = input(f"{Colors.BLUE}Novo preço (Enter para manter): {Colors.ENDC}").strip()
        if price:
            valid, error = cls.validator.validate_price(price)
            if valid:
                updates['price'] = float(price)
            else:
                print(f"{Colors.RED}✗ {error} - Preço não será alterado{Colors.ENDC}")
        
        if not updates:
            print(f"\n{Colors.YELLOW}Nenhum campo será alterado.{Colors.ENDC}")
        
        return book_id, updates
    
    @classmethod
    def ask_delete_book(cls):
        cls.print_header("REMOVER LIVRO")
        
        book_id = int(cls.get_validated_input(
            "ID do livro a ser removido: ",
            cls.validator.validate_id
        ))
        
        confirmation = input(f"{Colors.YELLOW}Confirma a exclusão? (S/N): {Colors.ENDC}").strip().upper()
        
        if confirmation == 'S':
            return book_id
        else:
            print(f"{Colors.YELLOW}Operação cancelada.{Colors.ENDC}")
            return None
    
    @classmethod
    def ask_search_author(cls):
        cls.print_header("BUSCAR POR AUTOR")
        
        author = input(f"{Colors.BLUE}Nome do autor (ou parte dele): {Colors.ENDC}").strip().upper()
        return author
    
    @classmethod
    def ask_search_query(cls):
        cls.print_header("BUSCA AVANÇADA")
        
        query = input(f"{Colors.BLUE}Digite o termo de busca (título ou autor): {Colors.ENDC}").strip().upper()
        return query
    
    @staticmethod
    def print_books(books):
        if not books:
            print(f"{Colors.YELLOW}Nenhum livro encontrado.{Colors.ENDC}\n")
            return
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}📚 {len(books)} livro(s) encontrado(s):{Colors.ENDC}\n")
        
        # Cabeçalho da tabela
        header = f"{'ID':>4} | {'TÍTULO':<40} | {'AUTOR':<30} | {'ANO':>4} | {'PREÇO':>10}"
        print(f"{Colors.BOLD}{header}{Colors.ENDC}")
        print("-" * len(header))
        
        # Dados
        for book in books:
            print(f"{book.id:>4} | {book.title[:40]:<40} | {book.author[:30]:<30} | "
                  f"{book.publication_year:>4} | R$ {book.price:>7.2f}")
        
        print()
    
    @staticmethod
    def print_statistics(stats):
        ScreenUtils.print_header("ESTATÍSTICAS DA LIVRARIA")
        
        print(f"{Colors.CYAN}📚 Total de Livros:{Colors.ENDC} {stats.get('total_books', 0)}")
        print(f"{Colors.CYAN}👤 Autores Únicos:{Colors.ENDC} {stats.get('total_authors', 0)}")
        print(f"{Colors.CYAN}💰 Preço Médio:{Colors.ENDC} R$ {stats.get('average_price', 0):.2f}")
        print(f"{Colors.CYAN}📈 Livro Mais Caro:{Colors.ENDC} R$ {stats.get('most_expensive', 0):.2f}")
        print(f"{Colors.CYAN}📉 Livro Mais Barato:{Colors.ENDC} R$ {stats.get('cheapest', 0):.2f}")
        print()
    
    @staticmethod
    def print_backups(backups):
        if not backups:
            print(f"{Colors.YELLOW}Nenhum backup encontrado.{Colors.ENDC}\n")
            return
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}💾 {len(backups)} backup(s) disponível(eis):{Colors.ENDC}\n")
        
        for idx, backup in enumerate(backups, 1):
            print(f"{idx}. {Colors.CYAN}{backup['name']}{Colors.ENDC}")
            print(f"   Data: {backup['modified'].strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"   Tamanho: {backup['size_mb']} MB\n")
    
    @staticmethod
    def print_success(message):
        print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}\n")
    
    @staticmethod
    def print_error(message):
        print(f"{Colors.RED}✗ {message}{Colors.ENDC}\n")
    
    @staticmethod
    def print_warning(message):
        print(f"{Colors.YELLOW}⚠ {message}{Colors.ENDC}\n")
    
    @staticmethod
    def print_info(message):
        print(f"{Colors.BLUE}ℹ {message}{Colors.ENDC}\n")
    
    @staticmethod
    def pause():
        input(f"\n{Colors.BLUE}Pressione ENTER para continuar...{Colors.ENDC}")
    
    @staticmethod
    def ask_confirmation(message):
        response = input(f"{Colors.YELLOW}{message} (S/N): {Colors.ENDC}").strip().upper()
        return response == 'S'