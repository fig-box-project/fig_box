import os


# TODO:对Element类进行一个继承,返回{{}}所包含的内容之类的
class Template:
    @staticmethod
    def get_root():
        rt = 'files/templates'
        os.makedirs(rt, exist_ok=True)
        return rt
