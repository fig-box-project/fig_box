from app.core.module_class import ApiModule
from app.core.module_class.AuthModule import AuthItem
from app.core.settings.crud import settings
from app.core.test.route import test_route


class Test(ApiModule):
    testAuth = AuthItem('test', False)

    def _register_api_bp(self, bp):
        test_route(bp, self.testAuth)

    def _get_tag(self) -> str:
        return 'テスト用モジュール'

    def get_module_name(self) -> str:
        return 'test'


test = None
if settings.value['route_test_mode']:
    test = Test()
