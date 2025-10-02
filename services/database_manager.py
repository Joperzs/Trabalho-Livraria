from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models.book import Base, Book
import logging

class DatabaseManager:
    def __init__(self, db_path="data/bookstore.db"):
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.logger = logging.getLogger(__name__)
        
        # Cria as tabelas se não existirem
        Base.metadata.create_all(self.engine)
        self.logger.info("Banco de dados inicializado com sucesso")
    
    def _get_session(self):
        return self.Session()
    
    def add_book(self, book):
        session = self._get_session()
        try:
            session.add(book)
            session.commit()
            session.refresh(book)
            self.logger.info(f"Livro adicionado: ID={book.id}, Título='{book.title}'")
            return book
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Erro ao adicionar livro: {e}")
            raise
        finally:
            session.close()
    
    def get_all_books(self):
        session = self._get_session()
        try:
            books = session.query(Book).order_by(Book.id).all()
            self.logger.info(f"Recuperados {len(books)} livros do banco de dados")
            return books
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao buscar livros: {e}")
            return []
        finally:
            session.close()
    
    def get_book_by_id(self, book_id):
        session = self._get_session()
        try:
            book = session.query(Book).filter_by(id=book_id).first()
            if book:
                self.logger.info(f"Livro encontrado: ID={book_id}")
            else:
                self.logger.warning(f"Livro não encontrado: ID={book_id}")
            return book
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao buscar livro por ID: {e}")
            return None
        finally:
            session.close()
    
    def update_book(self, book_id, **kwargs):
        session = self._get_session()
        try:
            book = session.query(Book).filter_by(id=book_id).first()
            
            if not book:
                self.logger.warning(f"Livro não encontrado para atualização: ID={book_id}")
                return False
            
            # Atualiza apenas os campos fornecidos
            if "title" in kwargs:
                book.title = kwargs["title"]
            if "author" in kwargs:
                book.author = kwargs["author"]
            if "publication_year" in kwargs:
                book.publication_year = kwargs["publication_year"]
            if "price" in kwargs:
                book.price = kwargs["price"]
            
            session.commit()
            self.logger.info(f"Livro atualizado: ID={book_id}")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Erro ao atualizar livro: {e}")
            return False
        finally:
            session.close()
    
    def delete_book(self, book_id):
        session = self._get_session()
        try:
            book = session.query(Book).filter_by(id=book_id).first()
            
            if not book:
                self.logger.warning(f"Livro não encontrado para exclusão: ID={book_id}")
                return False
            
            session.delete(book)
            session.commit()
            self.logger.info(f"Livro removido: ID={book_id}")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Erro ao remover livro: {e}")
            return False
        finally:
            session.close()
    
    def search_books_by_author(self, author):
        session = self._get_session()
        try:
            books = session.query(Book).filter(
                Book.author.ilike(f"%{author}%")
            ).all()
            self.logger.info(f"Encontrados {len(books)} livros do autor '{author}'")
            return books
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao buscar livros por autor: {e}")
            return []
        finally:
            session.close()
    
    def search_books(self, query):
        session = self._get_session()
        try:
            books = session.query(Book).filter(
                or_(
                    Book.title.ilike(f"%{query}%"),
                    Book.author.ilike(f"%{query}%")
                )
            ).all()
            self.logger.info(f"Busca por '{query}' retornou {len(books)} resultados")
            return books
        except SQLAlchemyError as e:
            self.logger.error(f"Erro na busca: {e}")
            return []
        finally:
            session.close()
    
    def get_statistics(self):
        session = self._get_session()
        try:
            from sqlalchemy import func
            
            stats = {
                'total_books': session.query(func.count(Book.id)).scalar(),
                'total_authors': session.query(func.count(func.distinct(Book.author))).scalar(),
                'average_price': session.query(func.avg(Book.price)).scalar() or 0,
                'most_expensive': session.query(func.max(Book.price)).scalar() or 0,
                'cheapest': session.query(func.min(Book.price)).scalar() or 0
            }
            
            return stats
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao calcular estatísticas: {e}")
            return {}
        finally:
            session.close()
