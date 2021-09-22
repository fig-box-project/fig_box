from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.core.system import err_handle, create_database, blueprint, start_scheduler
from app.core.system.check_token import token
from app.core.system.modules import get_module_list

version = "α9.20"

mod_datas = get_module_list()

# 初始化数据库, 创建数据表
# データベースの初期化
db: Session = create_database.run(mod_datas['table_mods'])

app = FastAPI(
    title="Figbox",
    description="自由、管理しやすい高速APIエンジン",
    version=version,
    # 关闭文档
    # ドキュメントを閉じる
    # docs_url=None,
    # redoc_url=None,
)

# 检查token的函数
token.set_db(db)
token.get_token_func()

# 导入错误处理系统
err_handle.run(app)

start_scheduler.run(app)

# 导入系统模组的蓝图
blueprint.run(app, mod_datas['all'])

# 导入模组的蓝图
# mod_blueprint.run(app)

# @app.get('/',tags=['测试'],response_class=HTMLResponse)
# def root(request: Request):
#     return "<a href=\"docs\">api</a>" + request.client.host + " | "
