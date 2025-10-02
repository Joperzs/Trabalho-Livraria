from pathlib import Path
from datetime import datetime
from collections import Counter
import logging

class ReportService:
    def __init__(self, database_manager):
        self.db_manager = database_manager
        self.logger = logging.getLogger(__name__)
        Path("reports").mkdir(exist_ok=True)
    
    def generate_html_report(self, filename=None):
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"report_{timestamp}.html"
            
            filepath = Path("reports") / filename
            
            books = self.db_manager.get_all_books()
            stats = self.db_manager.get_statistics()
            authors = [book.author for book in books]
            author_count = Counter(authors)
            top_authors = author_count.most_common(5)
            years = [book.publication_year for book in books]
            year_count = Counter(years)
            html_content = self._generate_html_content(
                books, stats, top_authors, year_count
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Relatório HTML gerado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório HTML: {e}")
            return None
    
    def _generate_html_content(self, books, stats, top_authors, year_count):
        current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório da Livraria</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .stat-card h3 {{
            font-size: 2em;
            margin-bottom: 5px;
        }}
        
        .stat-card p {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .section {{
            margin-bottom: 30px;
        }}
        
        .section h2 {{
            color: #667eea;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
        }}
        
        tbody tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        tbody tr:hover {{
            background-color: #e9ecef;
            transition: background-color 0.3s;
        }}
        
        .author-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }}
        
        .author-badge {{
            background: #667eea;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Relatório da Livraria</h1>
            <p>Gerado em {current_date}</p>
        </div>
        
        <div class="content">
            <!-- Estatísticas Gerais -->
            <div class="section">
                <h2>Estatísticas Gerais</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>{stats.get('total_books', 0)}</h3>
                        <p>Total de Livros</p>
                    </div>
                    <div class="stat-card">
                        <h3>{stats.get('total_authors', 0)}</h3>
                        <p>Autores Únicos</p>
                    </div>
                    <div class="stat-card">
                        <h3>R$ {stats.get('average_price', 0):.2f}</h3>
                        <p>Preço Médio</p>
                    </div>
                    <div class="stat-card">
                        <h3>R$ {stats.get('most_expensive', 0):.2f}</h3>
                        <p>Livro Mais Caro</p>
                    </div>
                    <div class="stat-card">
                        <h3>R$ {stats.get('cheapest', 0):.2f}</h3>
                        <p>Livro Mais Barato</p>
                    </div>
                </div>
            </div>
            
            <!-- Top Autores -->
            <div class="section">
                <h2>Top 5 Autores</h2>
                <div class="author-list">
        """
        
        for author, count in top_authors:
            html += f'<div class="author-badge">{author} ({count} livros)</div>\n'
        
        html += """
                </div>
            </div>
            
            <!-- Lista Completa de Livros -->
            <div class="section">
                <h2>Catálogo Completo</h2>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Título</th>
                            <th>Autor</th>
                            <th>Ano</th>
                            <th>Preço</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for book in books:
            html += f"""
                        <tr>
                            <td>{book.id}</td>
                            <td>{book.title}</td>
                            <td>{book.author}</td>
                            <td>{book.publication_year}</td>
                            <td>R$ {book.price:.2f}</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="footer">
            <p>Sistema de Gerenciamento de Livraria | Desenvolvido com Python & SQLAlchemy</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def generate_text_report(self, filename=None):
        """
        Gera um relatório simples em texto.
        
        Args:
            filename: Nome do arquivo
            
        Returns:
            str: Caminho do arquivo gerado
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"report_{timestamp}.txt"
            
            filepath = Path("reports") / filename
            
            books = self.db_manager.get_all_books()
            stats = self.db_manager.get_statistics()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("RELATÓRIO DA LIVRARIA\n")
                f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write("=" * 70 + "\n\n")
                
                f.write("ESTATÍSTICAS GERAIS\n")
                f.write("-" * 70 + "\n")
                f.write(f"Total de Livros: {stats.get('total_books', 0)}\n")
                f.write(f"Autores Únicos: {stats.get('total_authors', 0)}\n")
                f.write(f"Preço Médio: R$ {stats.get('average_price', 0):.2f}\n")
                f.write(f"Livro Mais Caro: R$ {stats.get('most_expensive', 0):.2f}\n")
                f.write(f"Livro Mais Barato: R$ {stats.get('cheapest', 0):.2f}\n\n")
                
                f.write("LISTA DE LIVROS\n")
                f.write("-" * 70 + "\n")
                
                for book in books:
                    f.write(f"\nID: {book.id}\n")
                    f.write(f"Título: {book.title}\n")
                    f.write(f"Autor: {book.author}\n")
                    f.write(f"Ano: {book.publication_year}\n")
                    f.write(f"Preço: R$ {book.price:.2f}\n")
                    f.write("-" * 70 + "\n")
            
            self.logger.info(f"Relatório TXT gerado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório TXT: {e}")
            return None
