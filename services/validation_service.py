from datetime import datetime
import re

class ValidationService:
    @staticmethod
    def validate_title(title):
        if not title or not title.strip():
            return False, "O título não pode estar vazio."
        
        if len(title.strip()) < 1:
            return False, "O título deve ter pelo menos 1 caracter."
        
        if len(title.strip()) > 80:
            return False, "O título não pode ter mais de 80 caracteres."
        
        return True, ""
    
    @staticmethod
    def validate_author(author):
        if not author or not author.strip():
            return False, "O nome do autor não pode estar vazio."
        
        if len(author.strip()) < 1:
            return False, "O nome do autor deve ter pelo menos 2 caracteres."
        
        if len(author.strip()) > 30:
            return False, "O nome do autor não pode ter mais de 30 caracteres."
        
        return True, ""
    
    @staticmethod
    def validate_year(year):
        try:
            year_int = int(year)
            current_year = datetime.now().year

            if year_int > current_year + 1:
                return False, f"O ano de publicação não pode ser maior que {current_year + 1}."
            
            return True, ""
        except (ValueError, TypeError):
            return False, "O ano deve ser um número inteiro válido."
    
    @staticmethod
    def validate_price(price):
        try:
            price_float = float(price)
            
            if price_float < 0:
                return False, "O preço não pode ser negativo."
            
            return True, ""
        except (ValueError, TypeError):
            return False, "O preço deve ser um número válido."
    
    @staticmethod
    def validate_id(book_id):
        try:
            id_int = int(book_id)
            
            if id_int < 1:
                return False, "O ID deve ser um número positivo."
            
            return True, ""
        except (ValueError, TypeError):
            return False, "O ID deve ser um número inteiro válido."
    
    @classmethod
    def validate_book_data(cls, title, author, year, price):
        """
        Valida todos os dados de um livro de uma vez.
        
        Args:
            title: Título do livro
            author: Autor do livro
            year: Ano de publicação
            price: Preço do livro
            
        Returns:
            tuple: (bool, list) - (válido, lista_de_erros)
        """
        errors = []
        
        valid, error = cls.validate_title(title)
        if not valid:
            errors.append(error)
        
        valid, error = cls.validate_author(author)
        if not valid:
            errors.append(error)
        
        valid, error = cls.validate_year(year)
        if not valid:
            errors.append(error)
        
        valid, error = cls.validate_price(price)
        if not valid:
            errors.append(error)
        
        return len(errors) == 0, errors
