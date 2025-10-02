import subprocess
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70 + "\n")

def check_python_version():
    print("Verificando Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("Python 3.8 ou superior é necessário!")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def install_dependencies():
    print("\nInstalando dependências...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-q",
            "sqlalchemy==2.0.23",
            "pandas==2.1.3"
        ])
        print("Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("Erro ao instalar dependências")
        print("Tente executar manualmente: pip install sqlalchemy pandas")
        return False

def check_dependencies():
    print("\nVerificando dependências...")
    
    dependencies = {
        'sqlalchemy': False,
        'pandas': False
    }
    
    for package in dependencies.keys():
        try:
            __import__(package)
            dependencies[package] = True
            print(f"{package} instalado")
        except ImportError:
            print(f"{package} não encontrado")
    
    return all(dependencies.values())

def verify_structure():
    print("\nVerificando estrutura do projeto...")
    
    required_files = [
        'main.py',
        'models/book.py',
        'services/bookstore_service.py',
        'services/database_manager.py',
        'services/backup_service.py',
        'services/csv_service.py',
        'services/report_service.py',
        'services/validation_service.py',
        'services/initialization_service.py',
        'utils/screen_utils.py'
    ]
    
    all_present = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"{file_path}")
        else:
            print(f"{file_path} não encontrado")
            all_present = False
    
    return all_present

def create_sample_csv():
    print("\nCriando arquivo CSV de exemplo...")
    
    imports_dir = Path("imports")
    imports_dir.mkdir(exist_ok=True)
    
    csv_path = imports_dir / "books.csv"
    
    if csv_path.exists():
        print(f"ℹ️  {csv_path} já existe")
        return True
    
    try:
        csv_content = """title,author,publication_year,price
        O SENHOR DOS ANEIS,J.R.R. TOLKIEN,1954,89.90
        1984,GEORGE ORWELL,1949,45.50
        DOM CASMURRO,MACHADO DE ASSIS,1899,35.00
        HARRY POTTER E A PEDRA FILOSOFAL,J.K. ROWLING,1997,65.00
        O PEQUENO PRINCIPE,ANTOINE DE SAINT-EXUPERY,1943,29.90
        ORGULHO E PRECONCEITO,JANE AUSTEN,1813,39.90
        CEM ANOS DE SOLIDAO,GABRIEL GARCIA MARQUEZ,1967,58.00
        O NOME DA ROSA,UMBERTO ECO,1980,62.50
        A DIVINA COMEDIA,DANTE ALIGHIERI,1320,49.90
        MOBY DICK,HERMAN MELVILLE,1851,55.00
        GUERRA E PAZ,LEON TOLSTOI,1869,79.90
        CRIME E CASTIGO,FIODOR DOSTOIEVSKI,1866,64.90
        O HOBBIT,J.R.R. TOLKIEN,1937,54.00
        AS CRÔNICAS DE NARNIA,C.S. LEWIS,1950,70.00
        """
        
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        print(f"{csv_path} criado")
        return True
    except Exception as e:
        print(f"Erro ao criar CSV: {e}")
        return False

def main():
    print_header("SETUP - Sistema de Gerenciamento de Livraria")
    
    print("Este script irá:")
    print("  1. Verificar a versão do Python")
    print("  2. Instalar/verificar dependências")
    print("  3. Verificar estrutura do projeto")
    print("  4. Criar arquivos de exemplo")
    
    input("\nPressione ENTER para continuar...")
    
    if not check_python_version():
        print("\nSetup falhou: Python 3.8+ necessário")
        sys.exit(1)
    
    if not check_dependencies():
        print("\nDependências não encontradas. Instalando...")
        if not install_dependencies():
            print("\nSetup falhou: Não foi possível instalar dependências")
            
    if not verify_structure():
        print("\nSetup falhou: Estrutura de arquivos incompleta")
        print("   Certifique-se de ter todos os arquivos do projeto")
        sys.exit(1)

    create_sample_csv()
    
    print_header("SETUP CONCLUÍDO")
    
    print("✔ Sistema pronto para uso ✔\n")
    print("Para iniciar o sistema, execute:")
    print(f"  python main.py\n")
    
    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        sys.exit(1)
