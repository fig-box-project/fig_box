from app.main import db
from app.models.article import crud


class Article:
    # 缓存热度链表
    prev_cache_one=None
    next_cache_one=None
    # 文章链表(没有为None,未知为空的Article)
    prev_one=None
    next_one=None
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

    def cache_insert(self,prev_node):
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
    cache_by_id = {}
    cache_by_link = {}
    # 缓存上限
    max_articles = 100
    # 最大id
    max_id = 0
    # 缓存链表的头部
    cache_head_node = Article.none()
    # 构造
    def __init__(self):
        pass

    # 获取一篇文章
    def get_article(self,link):
        rt = {}
        if link in self.cache_by_link:
            #  增加热度,并排序
            article = self.cache_by_link[link]
            if article.next_cache_one is not None:
                if article.hot > article.next_cache_one.hot:
                    article.jump()
            rt["pagedata"] = article.data
        else:
            # 查询文章数据
            article_mdl = crud.read_one_page(db,link)
            if article_mdl is not None:
                article_data = article_mdl.__dict__
                article = Article(article_data)
                self.cache_by_id[link] = article
                # 如果id较大则替换
                if link > self.max_id:
                    self.max_id = link
            else:
                return None
            # 插入链表
            self.cache_by_id[link].cache_insert(self.cache_head_node)
            rt["pagedata"] = self.cache_by_id[link].data
            # TODO 当超过某数量时删除一定的数量
        # 添加前后
        prevdata,nextdata = self.to_be_between(article)
        rt["prevdata"] = prevdata
        rt["nextdata"] = nextdata
        return rt

    # 数据处理
    def to_be_between(self,article:Article):
        prevdata = None
        nextdata = None
        if article.data is not None:
            if article.prev_one == None:
                for i in range(article.data['id']-1,0,-1):
                    if i in self.cache_by_id.keys():
                        prevdata = self.cache_by_id[i]
                        article.prev_one = prevdata
            else:
                prevdata = article.prev_one
            if article.next_one == None:
                for i in range(article.data['id']+1,self.max_id):
                    if i in self.cache_by_id.keys():
                        nextdata = self.cache_by_id[i]
                        article.next_one = nextdata
            else:
                nextdata = article.next_one
        if prevdata is not None:
            prevdata = prevdata.data
        if nextdata is not None:
            nextdata = nextdata.data
        return prevdata,nextdata

cache = Cache()