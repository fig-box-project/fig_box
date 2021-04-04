version = "α326.231"

from sqlalchemy.orm import Session
from fastapi import FastAPI

# 初始化数据库, 创建数据表
import app.models.system.create_database as create_database
db: Session = create_database.run()

# app = FastAPI(docs_url=None, redoc_url=None) #关闭文档
# 设置标题,说明,版本
app = FastAPI(
    title = "F-Mod",
    description = "这是自由、易管理的高速模组化cms system.",
    version = version
)

import app.models.system.check_token as ct
check_token = ct.run(db)

# 导入系统模组的蓝图
import app.models.system.blueprint as blueprint
blueprint.run(app)

# 导入模组的蓝图
import app.models.system.mod_blueprint as mod_blueprint
mod_blueprint.run(app)

# 试验
# from .insmodes.article.page import bp as article_page
# app.include_router(
#     article_page,
#     prefix="/article",
#     tags=['文章页面']
# )

# @app.get('/',tags=['测试'],response_class=HTMLResponse)
# def root(request: Request):
#     return "<a href=\"docs\">api</a>" + request.client.host + " | " 
