from app.models.orm import Page
from typing import Optional


class CategoryCU(Page):
    father_id: Optional[int] = None
