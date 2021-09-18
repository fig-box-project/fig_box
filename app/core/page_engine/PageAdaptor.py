from typing import Type

from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.core.table_class import PageTable
from app.core.table_class.db_core import get_db
from app.core.template_engine.Template import Template


class PageAdaptor:
    def __init__(self, request: Request, db: Session = Depends(get_db)):
        self.request = request
        self.db = db

    def bind(self, table_class: Type[PageTable], link: str, template_path: str) -> Response:
        """
        :template_path
            相対的なテンプレートパスを入れる（モジュール名も入れる）、例えば：/sample/sample.html
        """
        page_row = self.db.query(table_class).filter(table_class.link == link).first()
        if page_row is None:
            return Template.response_404(self.request, '404 cannot find data in database')
        # get a dict from row
        page_data = {}
        for column in page_row.__table__.columns:
            page_data[column.name] = str(getattr(page_row, column.name))
        page_data['request'] = self.request
        # use Template tool to get response
        return Template.response(template_path, page_data)
