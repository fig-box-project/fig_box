import os
from ...main import settings
from sqlalchemy.orm import Session, load_only

class SiteMap:
    # 初始化时创建sitemap文件夹下的东西
    def __init__(self):
        os.makedirs("files", exist_ok=True)
        os.makedirs("files/sitemap", exist_ok=True)
        os.makedirs("files/sitemap/sites", exist_ok=True)
        # 如果不存在则创建文件
        if not os.path.exists("files/sitemap/settings.yml"):
            pass

    def create_sitemap(self,db: Session):
        # 定义一个用于装sitemap数据的数组
        site_datas = []

        # 收集单页面
        site_maps = settings["site_maps"]
        single_sites = site_maps["single_sites"]
        for v in single_sites.values():
            for i in v:
                # 链接,上次更改日期,更新频率,站内权重
                site_datas.append((i["link"],i["lastmod"],i["changefreq"],i["priority"]))
                print(site_datas)

        # 收集数据库中的页面
        db_sites = site_maps["db_sites"]
        for k, v in db_sites.items():
            exec("from app.insmodels.{0} import mdl as {0}_mdl".format(k))
            for table in v["mdls"]:
                # 读取数据库数据
                fields = (table["link_key"], table["lastmod_key"])
                datas = eval("db.query({0}_mdl.{1}).options(load_only(*fields)).all()".format(k,table["table"]))
                for i in datas:
                    site_datas.append((i[fields[0]], table[fields[1]], v["changefreq"], v["priority"]))
                    print(site_datas)

        # 已收集完所有页面, 进行转换为文件
        lines = []
        first_line = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n'
        lines.append(first_line)
        for i in datas:
            # print(i.link)
            code = \
f'''<url>
<loc>{conf.sitemap_url}/article/{i.link}</loc>
<priority>1.00</priority>
<lastmod>2020-12-09</lastmod>
<changefreq>daily</changefreq>
</url>
'''
            lines.append(code)
        last_line = '</urlset>'
        lines.append(last_line)
        with open('files/sitemap/sitemap.xml','w') as w:
            w.write(''.join(lines))