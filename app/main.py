import app.models.system.mod_blueprint as mod_blueprint
import app.models.system.blueprint as blueprint
import app.models.system.check_token as ct
import app.models.system.create_database as create_database
from fastapi import FastAPI
from sqlalchemy.orm import Session
version = "α4.11"
# 初始化数据库, 创建数据表
db: Session = create_database.run()

# app = FastAPI(docs_url=None, redoc_url=None) #关闭文档
app = FastAPI(
    title="F-Mod",
    description="这是自由、易管理的高速模组化cms system.",
    version=version
)

# 检查token的函数
check_token = ct.run(db)

# 导入系统模组的蓝图
blueprint.run(app)

# 导入模组的蓝图
mod_blueprint.run(app)

# @app.get('/',tags=['测试'],response_class=HTMLResponse)
# def root(request: Request):
#     return "<a href=\"docs\">api</a>" + request.client.host + " | "
