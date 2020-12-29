import os
import json

directory_name = 'files/templates/jsaver/'

class Jsaver:
    cache = {}
    def __init__(self):
        os.makedirs("files", exist_ok=True)
        os.makedirs("files/templates", exist_ok=True)
        os.makedirs("files/templates/jsaver", exist_ok=True)
    def read(self, name: str):
        if name not in self.cache:
            # 从文件中查找
            if os.path.exists(directory_name + name):
                with open(directory_name + name,"r") as f:
                    self.cache[name] = json.loads(f.read())
            else:
                return None
        return self.cache[name]
    def write(self, name: str, json_str: str):
        with open( directory_name + name,"w" ) as f:
            f.write(json_str)
        if name in self.cache:
            self.cache[name] = json.loads(json_str)
            
    
jsaver = Jsaver()