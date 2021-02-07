import yaml
import os

class Settings:
    def __init__(self):
        self.yaml_path = "settings.yml"
        if not os.path.exists(self.yaml_path):
            raise Exception("Settings.yml not found")
        else:
            # 获取设置
            with open(self.yaml_path, "r") as f:
                self.value = yaml.load(f.read())
            # TODO del
            print(self.value)
    
    def update(self):
        with open(self.yaml_path, "w") as f:
            yaml.dump(self.value, f)

# 单例
settings = Settings()
    