from typing import List
import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_posts_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/777")
    assert res.status_code == 404

@pytest.mark.parametrize("title, content, published", [
    ("TMD", "Towa Maji Daitenshi", True),
    ("Konbota Konbota", "Gawr", True),
    ("amelia gremlin", "ground pound", False)
])

def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "Non-stop Nut November", "content": "putang ina si optimum pride"})

    post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert post.published == True
    assert post.owner_id == test_user['id']
    assert post.title == "Non-stop Nut November"
    assert post.content == "putang ina si optimum pride"

def test_unauthorized_user_create_post(client, test_posts, test_user):
    res = client.post("/posts/", json={"title": "Non-stop Nut November", "content": "putang ina si optimum pride"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts, test_user):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exists(authorized_client, test_posts, test_user):
    res = authorized_client.delete("/posts/666")
    assert res.status_code == 404

def test_delete_post_success(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_udpate_post_success(authorized_client, test_posts, test_user):
    data = {
        "title": "updated tile",
        "content": "a wish upon deez nuts",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.id == data['id']

def test_update_another_user_post(authorized_client, test_posts):
    data = {
        "title": "updated tile",
        "content": "a wish upon deez nuts",
        "id": test_posts[3].id
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert res.status_code == 403

def test_unauthorized_update(client, test_posts):
    data = {
        "title": "updated tile",
        "content": "a wish upon deez nuts",
        "id": test_posts[0].id
    }

    res = client.put(f"/posts/{test_posts[0].id}", json=data)

    assert res.status_code == 401

def test_update_non_existing_post(authorized_client, test_posts):
    data = {
        "title": "updated tile",
        "content": "a wish upon deez nuts",
        "id": 666
    }

    res = authorized_client.put("/posts/666", json=data)

    assert res.status_code == 404