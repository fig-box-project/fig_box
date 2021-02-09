import os
import time
from sqlalchemy.orm import Session, load_only
from app.models.settings.crud import settings

class SiteMap:
    # 初始化时创建sitemap文件夹下的东西
    def __init__(self):
        os.makedirs("files", exist_ok=True)
        os.makedirs("files/sitemap", exist_ok=True)
        os.makedirs("files/sitemap/sites", exist_ok=True)

    def create_sitemap(self,db: Session): # db在exec中被使用
        # 定义一个用于装sitemap数据的数组
        site_datas = []

        # 收集单页面
        site_maps = settings.value["site_maps"]
        single_sites = site_maps["single_sites"]
        for v in single_sites.values():
            for i in v:
                # 链接,上次更改日期,更新频率,站内权重
                site_datas.append((i["link"],i["lastmod"],i["changefreq"],i["priority"]))
                print(site_datas)

        # 收集数据库中的页面
        db_sites = site_maps["db_sites"]
        for k, v in db_sites.items():
            exec("from app.insmodes.{0} import mdl as {0}_mdl".format(k))
            for table in v["mdls"]:
                # 读取数据库数据
                fields = (table["link_key"], table["lastmod_key"])
                datas = eval("db.query({0}_mdl.{1}).options(load_only(*fields)).all()".format(k,table["table"]))
                for i in datas:
                    link = eval(f"i.{fields[0]}")
                    lastmod = eval(f"i.{fields[1]}")
                    lastmod = lastmod.strftime("%Y-%-m-%-d") # "%Y-%m-%d" 为有0的配法
                    site_datas.append(("/" + table["prefix"] + link, lastmod, v["changefreq"], v["priority"]))
                    print(site_datas)

        # 已收集完所有页面, 进行转换为文件
        # TODO:当改为直接写入文件:新建空文件再在尾部追加
        lines = []
        first_line = \
'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
'''
        lines.append(first_line)
        for i in site_datas:
            code = \
f''' <url>
  <loc>{settings.value["domain_port"]}{i[0]}</loc>'''
            # 添加可选参数
            if i[1] != None:
                code += f"\n  <lastmod>{i[1]}</lastmod>"
            if i[2] != None:
                code += f"\n  <changefreq>{i[2]}</changefreq>"
            if i[3] != None:
                code += f"\n  <priority>{i[3]}</priority>"

            code += "\n </url>\n"
            lines.append(code)
        lines.append('\n</urlset>')
        with open('files/sitemap/sitemap.xml','w') as w:
            w.write(''.join(lines))