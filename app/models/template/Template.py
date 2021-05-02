import os

# TODO:对Element类进行一个继承,返回{{}}所包含的内容之类的
from starlette.responses import Response


class Template:
    ROOT_PATH = 'files/templates'

    @staticmethod
    def get_root():
        """获取绝对路径,并在不存在时创建"""
        # TODO:把这个改成只有第一次执行
        os.makedirs(Template.ROOT_PATH, exist_ok=True)
        return Template.ROOT_PATH

    @staticmethod
    def get_full_path(template_path: str):
        """通过相对路径获取全路径"""
        return f'{Template.ROOT_PATH}/{template_path}'

    @staticmethod
    def response() -> Response:
        """获取用于返回的资源"""
        ...

    @staticmethod
    def auto_create_html(template_path: str, get_creator_func):
        """检查html地址是否存在,不存在则用Html来自动创建"""
        full_path = Template.get_full_path(template_path)
        if not os.path.exists(full_path):
            html = str(get_creator_func())
            with open(full_path, 'w') as f:
                f.write(html)
