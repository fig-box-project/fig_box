import os

class SiteMap:
    # 初始化时创建sitemap文件夹下的东西
    def __init__(self):
        os.makedirs("files", exist_ok=True)
        os.makedirs("files/sitemap", exist_ok=True)
        os.makedirs("files/sitemap/sites", exist_ok=True)
        # 如果不存在则创建文件
        if not os.path.exists("files/sitemap/settings.yml"):
            pass