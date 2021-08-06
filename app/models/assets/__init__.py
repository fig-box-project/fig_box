from app.models.assets.route import assets_route
from app.models.module import ApiModule


class Assets(ApiModule):
    def _register_api_bp(self, bp):
        self._api_bp.change_prefix('/' + self.get_module_name())
        assets_route(bp)

    def _get_tag(self) -> str:
        return 'assets管理'

    def get_module_name(self) -> str:
        return 'assets'


assets = Assets()
