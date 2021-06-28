from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.models.system import err_handle, create_database, blueprint
from app.models.system.check_token import token
from app.models.system.modules import get_module_list

version = "α6.28"

mod_datas = get_module_list()

# 初始化数据库, 创建数据表
db: Session = create_database.run(mod_datas['table_mods'])

app = FastAPI(
    title="F-Mod",
    description="这是自由、易管理的高速模组化cms system.",
    version=version,
    # 关闭文档
    # docs_url=None,
    # redoc_url=None,
)

# 检查token的函数
token.set_db(db)
token.get_token_func()

# 导入错误处理系统
err_handle.run(app)



# 导入系统模组的蓝图
blueprint.run(app, mod_datas['all'])

# 导入模组的蓝图
# mod_blueprint.run(app)

# @app.get('/',tags=['测试'],response_class=HTMLResponse)
# def root(request: Request):
#     return "<a href=\"docs\">api</a>" + request.client.host + " | "
