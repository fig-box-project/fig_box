import os

# TODO:对Element类进行一个继承,返回{{}}所包含的内容之类的
from fastapi import HTTPException
from starlette.responses import Response
from fastapi.templating import Jinja2Templates


class Template:
    __ROOT_PATH = 'files/templates'
    __PATH_404 = '404.html'
    __ENGINE: Jinja2Templates = Jinja2Templates(__ROOT_PATH)
    # 设置是否在404页面不存在时自动创建404,TODO:创建自动创建器并改为True.
    __AUTO_CREATE_404 = False

    @staticmethod
    def get_root():
        """获取绝对路径,并在不存在时创建"""
        # TODO:把这个改成只有第一次执行
        os.makedirs(Template.__ROOT_PATH, exist_ok=True)
        return Template.__ROOT_PATH

    @staticmethod
    def get_full_path(template_path: str):
        """通过相对路径获取全路径"""
        return f'{Template.get_root()}/{template_path}'

    @staticmethod
    def response(path: str, data: dict, get_creator_func=None) -> Response:
        """输入相对路径,要绑定的数据,html构筑函数,
        :return 获取用于返回给前端的对象"""
        # 存在就直接返回
        if os.path.exists(Template.get_full_path(path)):
            return Template.__ENGINE.TemplateResponse(path, data)
        # 不存在时确认有无传入自动创建器
        if get_creator_func is not None:
            Template.auto_create_html(path, get_creator_func)
            return Template.__ENGINE.TemplateResponse(path, data)
        return Template.response_404(data['request'], f'template path: {path} un exists.')

    @staticmethod
    def response_404(request, message: str):
        # 以上都无是检查404的存在
        if os.path.exists(Template.get_full_path(Template.__PATH_404)):
            return Template.__ENGINE.TemplateResponse(
                Template.__PATH_404,
                {'request': request, 'err': message}
            )
        # 无404页面时确定是否自动创建404页面
        if Template.__AUTO_CREATE_404:
            Template.__auto_create_404()
            return Template.__ENGINE.TemplateResponse(
                Template.__PATH_404,
                {'request': request, 'err': message}
            )
        # 直接报404
        raise HTTPException(404, f'can not find 404.html. 404 message: [{message}]')

    @staticmethod
    def __auto_create_404():
        # TODO
        ...

    @staticmethod
    def auto_create_html(template_path: str, get_creator_func):
        """检查相对地址是否存在,不存在则用Html来自动创建"""
        full_path = Template.get_full_path(template_path)
        if not os.path.exists(full_path):
            Template.auto_create_dirs(full_path)
            html = str(get_creator_func())
            with open(full_path, 'w') as f:
                f.write(html)

    @staticmethod
    def auto_create_dirs(path: str):
        index = path.rfind('/')
        if index != -1:
            path = path[:index]
            os.makedirs(path, exist_ok=True)
