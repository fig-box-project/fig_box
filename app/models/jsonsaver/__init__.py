from fastapi import APIRouter

from app.models.jsonsaver.route import json_saver
from app.models.module import ApiModule


class JsonSaver(ApiModule):
    def _register_api_bp(self, bp: APIRouter):
        json_saver(bp)

    def _get_tag(self) -> str:
        return 'json储存'

    def get_module_name(self) -> str:
        return 'jsonsaver'


jsonsaver = JsonSaver()
