from fastapi.testclient import TestClient
from .main import app
import app.conf as conf

client = TestClient(app)
token = ""
article_id = None

def test_login():
    response = client.post(
        conf.url_prefix + '/auth/login',
        json={"username":"test", "password":"test"})
    global token
    token = response.json()["token"]
    print(token)
    assert response.status_code == 200

# 创建文章功能
def test_create_article():
    response = client.post(
        conf.url_prefix + '/article/create',
        json={
        "title": "string",
        "content": "string",
        "description": "string",
        "category_id": 0,
        "image":"ss",
        "seo_title":"string",
        "seo_keywords": "string",
        "seo_description": "string",
        "status":0,
        "is_release": "false",
        "can_search": "true",
        },
        headers={"token":token})
    print(response.json())
    global article_id
    article_id = dict(response.json())["id"]
    assert response.status_code == 200

# 删除文章功能
def test_delete_article():
    global article_id
    print(article_id)
    response = client.delete(
        conf.url_prefix + '/article/delete/'+str(article_id),
        headers={"token":token})
    assert response.status_code == 200

# 普通用户不能查看所有文章
def test_cant_view_all_articles():
    response = client.get(
        conf.url_prefix + '/article/all/articles',
        headers={"token":token})
    assert response.status_code == 403

def test_admin_login():
    response = client.post(
        conf.url_prefix + '/auth/login',
        json={"username":"admin", "password":"admin"})
    global token
    token = response.json()["token"]
    print(token)
    assert response.status_code == 200


# def create_character():
#     response = client.post(
#         conf.url_prefix + '/auth/login',
#         json={"username":"admin", "password":"admin"}
#     )