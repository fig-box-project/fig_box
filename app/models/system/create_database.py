from typing import List

from sqlalchemy import Table

from app.models.character import CharacterMdl, AuthMdl
from app.models.module import TableModule
from app.models.settings.crud import settings
from app.models.mdl import database
from sqlalchemy.orm import sessionmaker, Session
# 引用一下mdl才能创建该数据表
from app.models.user import mdl as user
from app.models.category import mdl as tree_mdl


def run(mods: List[TableModule]):
    # 默认表
    tables = []
    for m in mods:
        for t in m.get_table():
            if isinstance(t, Table):
                tables.append(t)
                continue
            tables.append(t.__table__)

    # 自动引用安装的库
    # for k in mods.keys():
    #     if "has_mdl" in mods[k]:
    #         if mods[k]["has_mdl"] == True:
    #             # 引用下
    #             exec("from app.insmodes.{0} import mdl as {0}_mdl".format(k))
    #             # 加入下列表中等下读取
    #             tables_strs.append(
    #                 "{}_mdl.{}.__table__".format(k, k.capitalize()))

    # 录入到tables中
    # for t in tables_strs:
    #     exec("tables.append({})".format(t))

    # もしテーブルを選びたい時： create_all(bind=engine, tables=[User.__table__])
    # もし改めてテーブルを作りたい時： create_all(bind=engine, checkfirst=False)
    database.Base.metadata.create_all(bind=database.engine, tables=tables)

    # database.Base.metadata.query
    # 初始化数据库
    db: Session = sessionmaker(bind=database.engine)()
    if db.query(user.UserMdl).count() == 0:
        print("---create datas---")
        # add auth
        admin_auth = AuthMdl(name='admin')
        db.add(admin_auth)
        default_auth = AuthMdl(name='default')
        db.add_all([admin_auth, default_auth])
        db.commit()
        # add character
        admin_character = CharacterMdl(name='admin_character')
        admin_character.auths = [admin_auth]
        normal_character = CharacterMdl(name='normal_character')
        normal_character.auths = [default_auth]
        db.commit()

        # add admin
        admin_user = user.UserMdl(
            username="admin",
            character=admin_character
        )
        admin_user.hash_password("admin")
        db.add(admin_user)
        # add test user
        test_user = user.UserMdl(
            username="test",
            character=normal_character
        )
        test_user.hash_password("test")
        db.add(test_user)

        db.commit()
    return db
