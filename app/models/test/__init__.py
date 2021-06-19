from app.models.module import ApiModule, AuthItem
from app.models.settings.crud import settings
from app.models.test.route import test_route


class Test(ApiModule):
    testAuth = AuthItem('test', True)

    def _register_api_bp(self, bp):
        test_route(bp,self.testAuth)

    def _get_tag(self) -> str:
        return '测试'

    def get_module_name(self) -> str:
        return 'test'


test = None
if settings.value['route_test_mode']:
    test = Test()
