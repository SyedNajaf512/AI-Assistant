"""
Anna AI Assistant - File Operations
Handles file system operations
"""

import os
import shutil
from pathlib import Path
from logger import logger
from safety import safety


class FileOperations:
    """Manages file system operations"""
    
    def open_file(self, file_path):
        """Open a file with default application"""
        try:
            file_path = safety.sanitize_path(file_path)
            if not file_path:
                return {"success": False, "message": "Invalid file path"}
            
            if os.path.exists(file_path):
                os.startfile(file_path)
                logger.log_action("open_file", file_path, True)
                return {"success": True, "message": f"Opened {file_path}"}
            else:
                return {"success": False, "message": f"File not found: {file_path}"}
                
        except Exception as e:
            logger.log_error("OPEN_FILE", str(e), file_path)
            return {"success": False, "message": f"Error opening file: {str(e)}"}
    
    def open_folder(self, folder_path):
        """Open a folder in File Explorer"""
        try:
            folder_path = safety.sanitize_path(folder_path)
            if not folder_path:
                return {"success": False, "message": "Invalid folder path"}
            
            if os.path.exists(folder_path):
                os.startfile(folder_path)
                logger.log_action("open_folder", folder_path, True)
                return {"success": True, "message": f"Opened {folder_path}"}
            else:
                return {"success": False, "message": f"Folder not found: {folder_path}"}
                
        except Exception as e:
            logger.log_error("OPEN_FOLDER", str(e), folder_path)
            return {"success": False, "message": f"Error opening folder: {str(e)}"}
    
    def read_file(self, file_path):
        """Read file contents"""
        try:
            file_path = safety.sanitize_path(file_path)
            if not file_path:
                return {"success": False, "message": "Invalid file path"}
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                logger.log_action("read_file", file_path, True)
                return {"success": True, "content": content}
            else:
                return {"success": False, "message": f"File not found: {file_path}"}
                
        except Exception as e:
            logger.log_error("READ_FILE", str(e), file_path)
            return {"success": False, "message": f"Error reading file: {str(e)}"}
    
    def write_file(self, file_path, content):
        """Write content to file (DANGEROUS - requires PIN)"""
        try:
            file_path = safety.sanitize_path(file_path)
            if not file_path:
                return {"success": False, "message": "Invalid file path"}
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.log_action("write_file", file_path, True)
            return {"success": True, "message": f"Written to {file_path}"}
                
        except Exception as e:
            logger.log_error("WRITE_FILE", str(e), file_path)
            return {"success": False, "message": f"Error writing file: {str(e)}"}
    
    def search_files(self, search_term, search_path=None):
        """Search for files by name"""
        try:
            if search_path is None:
                search_path = os.path.expanduser("~")
            
            search_path = safety.sanitize_path(search_path)
            if not search_path:
                return {"success": False, "message": "Invalid search path"}
            
            results = []
            max_results = 20
            
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if search_term.lower() in file.lower():
                        results.append(os.path.join(root, file))
                        if len(results) >= max_results:
                            break
                if len(results) >= max_results:
                    break
            
            logger.log_action("search_files", search_term, True, f"Found {len(results)} results")
            return {"success": True, "results": results, "count": len(results)}
                
        except Exception as e:
            logger.log_error("SEARCH_FILES", str(e), search_term)
            return {"success": False, "message": f"Error searching: {str(e)}"}
    
    def delete_file(self, file_path):
        """Delete a file (DANGEROUS - requires PIN)"""
        try:
            file_path = safety.sanitize_path(file_path)
            if not file_path:
                return {"success": False, "message": "Invalid file path"}
            
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.log_action("delete_file", file_path, True)
                return {"success": True, "message": f"Deleted {file_path}"}
            else:
                return {"success": False, "message": f"File not found: {file_path}"}
                
        except Exception as e:
            logger.log_error("DELETE_FILE", str(e), file_path)
            return {"success": False, "message": f"Error deleting file: {str(e)}"}
    
    def copy_file(self, source, destination):
        """Copy a file"""
        try:
            source = safety.sanitize_path(source)
            destination = safety.sanitize_path(destination)
            
            if not source or not destination:
                return {"success": False, "message": "Invalid file path"}
            
            if os.path.exists(source):
                shutil.copy2(source, destination)
                logger.log_action("copy_file", f"{source} -> {destination}", True)
                return {"success": True, "message": f"Copied to {destination}"}
            else:
                return {"success": False, "message": f"Source file not found: {source}"}
                
        except Exception as e:
            logger.log_error("COPY_FILE", str(e), f"{source} -> {destination}")
            return {"success": False, "message": f"Error copying file: {str(e)}"}


# Global file operations instance
file_ops = FileOperations()
