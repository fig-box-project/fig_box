from shutil import copyfile
import yaml
import os

class Settings:
    def __init__(self):
        self.yaml_path = "settings.yml"
        if not os.path.exists(self.yaml_path):
            # 复制默认文件
            copyfile("settings_default.yml", "settings.yml")
        # 获取设置
        with open(self.yaml_path, "r") as f:
            self.value: dict = yaml.load(f, Loader=yaml.SafeLoader)
    
    def update(self):
        with open(self.yaml_path, "w") as f:
            yaml.dump(self.value, f)

# 单例
settings = Settings()
    