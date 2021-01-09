from app.main import db
from app.models.article import crud


class Article:
    # 缓存热度链表
    prev_cache_one:Article=None
    next_cache_one:Article=None
    # 文章链表(没有为None,未知为空的Article)
    # prev_one=None
    # next_one=None 
    # 热度
    hot:int = 0
    # 数据
    data=None
    # 构造
    def __init__(self,data):
        self.data=data
    
    # 插入式构造
    @classmethod
    def insert(cls,aim_cache_node,data):
        rt = cls(data)
        rt.cache_insert(aim_cache_node)
        return rt

    # 空类
    @classmethod
    def none(cls):
        return cls(None)

    def cache_insert(self,prev_node:Article):
        if prev_node.next_cache_one == None:
            prev_node.next_cache_one = self
            self.prev_cache_one = prev_node
        else:
            # 目标的下一个的上一个改为自己
            prev_node.next_cache_one.prev_cache_one = self
            self.next_cache_one = prev_node.next_cache_one
            # 目标的下一个变为自己
            prev_node.next_cache_one = self
            self.prev_cache_one = prev_node

    def cache_jump(self):
        if self.next_cache_one is not None:
            # 上一个的下一个是下一个
            self.prev_cache_one.next_cache_one = self.next_cache_one
            # 下一个的上一个是上一个
            self.next_cache_one.prev_cache_one = self.prev_cache_one
            # 将自己插入到下一个
            self.cache_insert(self.next_cache_one)

class Cache:
    # 缓存
    cache = {}
    # 缓存上限
    max = 100
    # 最大id
    max_id = 0
    # 缓存链表的头部
    cache_head_node = Article.none()
    # 构造
    def __init__(self):
        pass

    # 获取一篇文章
    def get_article(self,id):
        if id in self.cache:
            #  增加热度,并排序
            rt = self.cache[id]
            if rt.hot > rt.next_cache_one.hot:
                rt.jump()
            return rt
        else:
            # 查询文章数据
            article = crud.read_one_page(db,id)
            if article is not None:
                article_data = article.__dict__
                self.cache[id] = Article(article_data)
                self.max_id = id
            else:
                return None
            # 插入链表
            self.cache[id].cache_insert(self.cache_head_node)
