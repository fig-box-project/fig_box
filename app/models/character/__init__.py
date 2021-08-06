from app.models.character.mdl import CharacterMdl, AuthMdl, character_auth
from fastapi import APIRouter

from app.models.character.route import character_router
from app.models.module import ApiModule, TableModule


class Character(ApiModule, TableModule):

    def get_table(self):
        return [CharacterMdl, AuthMdl, character_auth]

    def _register_api_bp(self, bp: APIRouter):
        character_router(bp)

    def _get_tag(self) -> str:
        return 'キャラクター管理'

    def get_module_name(self) -> str:
        return 'character'


character = Character()
