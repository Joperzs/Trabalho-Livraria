from pathlib import Path
from datetime import datetime
import shutil
import logging

class BackupService:
    def __init__(self, source_db="data/bookstore.db", backup_dir="backups"):
        self.source_db = Path(source_db)
        self.backup_dir = Path(backup_dir)
        self.logger = logging.getLogger(__name__)
        
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def cleanup_old_backups(self, max_backups=5):
        if not self.backup_dir.exists():
            return
        
        backup_files = sorted(
            self.backup_dir.glob("backup_*.db"),
            key=lambda p: p.stat().st_mtime,
            reverse=True #RECENTES
        )

        for old_backup in backup_files[max_backups:]:
            try:
                old_backup.unlink()
                self.logger.info(f"Backup antigo removido: {old_backup.name}")
            except Exception as e:
                self.logger.error(f"Erro ao remover backup {old_backup.name}: {e}")
    
    def create_backup(self):
        if not self.source_db.exists():
            self.logger.error(f"Banco de dados não encontrado: {self.source_db}")
            return None
        
        try:
            self.cleanup_old_backups(max_backups=4)
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_name = f"backup_bookstore_{timestamp}.db"
            backup_path = self.backup_dir / backup_name
            
            shutil.copy2(self.source_db, backup_path)
            
            self.logger.info(f"Backup criado com sucesso: {backup_name}")
            return backup_path
            
        except Exception as e:
            self.logger.error(f"Erro ao criar backup: {e}")
            return None
    
    def list_backups(self):
        if not self.backup_dir.exists():
            return []
        
        backups = []
        for backup_file in sorted(self.backup_dir.glob("backup_*.db"), 
                                   key=lambda p: p.stat().st_mtime, 
                                   reverse=True):
            stat = backup_file.stat()
            backups.append({
                'name': backup_file.name,
                'path': backup_file,
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'size_bytes': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2)
            })
        
        return backups
    
    def restore_backup(self, backup_name):
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            self.logger.error(f"Backup não encontrado: {backup_name}")
            return False
        
        try:
            current_backup = self.source_db.parent / f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            if self.source_db.exists():
                shutil.copy2(self.source_db, current_backup)
            
            shutil.copy2(backup_path, self.source_db)
            
            self.logger.info(f"Backup restaurado com sucesso: {backup_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao restaurar backup: {e}")
            return False
    
    def get_backup_size_total(self):
        if not self.backup_dir.exists():
            return {'bytes': 0, 'mb': 0}
        
        total_bytes = sum(f.stat().st_size for f in self.backup_dir.glob("backup_*.db"))
        
        return {
            'bytes': total_bytes,
            'mb': round(total_bytes / (1024 * 1024), 2)
        }
