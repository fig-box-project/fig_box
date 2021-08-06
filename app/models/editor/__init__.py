from fastapi import APIRouter

from app.models.editor.route import editor_route
from app.models.module import ApiModule


class Editor(ApiModule):
    def _register_api_bp(self, bp: APIRouter):
        editor_route(bp)

    def _get_tag(self) -> str:
        return 'ファイルエディター'

    def get_module_name(self) -> str:
        return 'editor'


editor = Editor()
