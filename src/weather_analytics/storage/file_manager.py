import json

class FileManager:
    """Handles file read and write operations"""
    
    def __init__(self):
        """initialize the File Manager"""

    def save_json(self,data,file_path):

        """Save JSON data to a file"""
        with open(file_path,"w") as file:
            json.dump(data,file,indent=4)