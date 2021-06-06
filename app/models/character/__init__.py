from fastapi import APIRouter

from app.models.character.route import character_router
from app.models.module import ApiModule


class Character(ApiModule):

    def _register_api_bp(self, bp: APIRouter):
        character_router(bp)

    def _get_tag(self) -> str:
        return '角色'

    def get_module_name(self) -> str:
        return 'character'


character = Character()
