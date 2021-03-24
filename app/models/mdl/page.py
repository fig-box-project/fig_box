from .hasid import HasidMdl
from sqlalchemy import Column, String, DateTime

class PageMdl(HasidMdl):
    __abstract__ = True
    
    # unique要改True, 暂时无用
    link               = Column(String, unique=False,index=True) 
    title              = Column(String(64), index=True)
    context            = Column(String)

    create_date        = Column(DateTime)
    update_date        = Column(DateTime)

    image              = Column(String)
    description        = Column(String(200))
    seo_title          = Column(String(40))
    seo_keywords       = Column(String(256))
    seo_description    = Column(String(400))