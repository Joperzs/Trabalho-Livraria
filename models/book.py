from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Book(Base):
    """
    Modelo de dados para representar um livro no sistema.
    
    Attributes:
        id: Identificador único do livro (chave primária)
        title: Título do livro
        author: Nome do autor
        publication_year: Ano de publicação
        price: Preço do livro
        created_at: Data e hora de cadastro no sistema
    """
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    publication_year = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"
    
    def to_dict(self):
        """Converte o objeto Book em um dicionário."""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'publication_year': self.publication_year,
            'price': self.price,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
