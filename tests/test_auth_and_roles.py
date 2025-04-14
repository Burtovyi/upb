import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os, sys

# Налаштування шляху до застосунку
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app
from app.db import database as db
from app.authors.models import Author

# Тестова БД (SQLite in-memory)
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Перевизначення залежності get_db для використання тестової БД
def override_get_db():
    try:
        db.Base.metadata.create_all(bind=engine)
        session = TestingSessionLocal()
        yield session
    finally:
        session.close()

app.dependency_overrides[db.get_db] = override_get_db
client = TestClient(app)

def create_user(email: str, name: str, password: str):
    return client.post("/api/v1/auth/register", json={"email": email, "name": name, "password": password})

def login_user(email: str, password: str):
    return client.post("/api/v1/auth/login", data={"username": email, "password": password})

def get_auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}

def test_registration_and_login_and_me():
    # Реєстрація нового користувача
    email = "testuser@example.com"
    resp = create_user(email, "Test User", "password123")
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == email
    assert "id" in data
    # Логін та отримання токенів
    resp = login_user(email, "password123")
    assert resp.status_code == 200
    tokens = resp.json()
    assert "access_token" in tokens and "refresh_token" in tokens
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    # Перевірка ендпоїнту /me з access-токеном
    me_resp = client.get("/api/v1/auth/me", headers=get_auth_headers(access_token))
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["email"] == email
    # Спроба використати refresh-токен там, де потрібен access-токен, має дати 401
    me_resp2 = client.get("/api/v1/auth/me", headers=get_auth_headers(refresh_token))
    assert me_resp2.status_code == 401

def test_refresh_token_flow():
    email = "refresher@example.com"
    create_user(email, "Refresher User", "refreshpass")
    resp = login_user(email, "refreshpass")
    tokens = resp.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    # Отримання нових токенів через refresh
    refresh_resp = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_resp.status_code == 200
    new_tokens = refresh_resp.json()
    assert "access_token" in new_tokens and "refresh_token" in new_tokens
    assert new_tokens["token_type"] == "bearer"
    # Новий access-токен працює
    me_resp = client.get("/api/v1/auth/me", headers=get_auth_headers(new_tokens["access_token"]))
    assert me_resp.status_code == 200

def test_role_based_access():
    # Створення 3 користувачів: user, editor, admin
    create_user("user1@example.com", "Normal User", "pass12345")
    create_user("editor1@example.com", "Editor User", "pass12345")
    create_user("admin1@example.com", "Admin User", "pass12345")
    # Призначення ролей editor та admin
    session = TestingSessionLocal()
    user = session.query(Author).filter(Author.email == "user1@example.com").first()
    editor = session.query(Author).filter(Author.email == "editor1@example.com").first()
    admin = session.query(Author).filter(Author.email == "admin1@example.com").first()
    assert user and editor and admin
    editor.role = "editor"
    admin.role = "admin"
    session.commit()
    session.close()
    # Отримання токенів для кожного
    tok_user = login_user("user1@example.com", "pass12345").json()
    tok_editor = login_user("editor1@example.com", "pass12345").json()
    tok_admin = login_user("admin1@example.com", "pass12345").json()
    at_user = tok_user["access_token"]; at_editor = tok_editor["access_token"]; at_admin = tok_admin["access_token"]
    # Звичайний користувач створює статтю
    art_data = {
        "title": "Test Article", "description": "Desc", "content": "Content", "view_count": 0,
        "author_id": 999, "category_id": 1, "content_type_id": 1, "tag_ids": []
    }
    create_resp = client.post("/api/v1/articles/", json=art_data, headers=get_auth_headers(at_user))
    assert create_resp.status_code == 200
    article = create_resp.json()
    article_id = article["id"]
    # Редактор створює іншу статтю від імені user
    art_data2 = {
        "title": "Other Article", "description": "Desc", "content": "Content", "view_count": 0,
        "author_id": user.id, "category_id": 1, "content_type_id": 1, "tag_ids": []
    }
    resp2 = client.post("/api/v1/articles/", json=art_data2, headers=get_auth_headers(at_editor))
    assert resp2.status_code == 200
    other_article = resp2.json()
    # Звичайний користувач намагається видалити статтю, яку створив редактор від його імені (тобто він є автором)
    del_resp = client.delete(f"/api/v1/articles/{other_article['id']}", headers=get_auth_headers(at_user))
    # Автор коментаря (user) має мати право видалити свою статтю – очікуємо 204
    assert del_resp.status_code == 204
    # Редактор може видалити статтю, створену користувачем
    del_resp2 = client.delete(f"/api/v1/articles/{article_id}", headers=get_auth_headers(at_editor))
    assert del_resp2.status_code == 204
    # Звичайний користувач не може створювати категорії або теги
    cat_resp = client.post("/api/v1/categories/", json={"name": "NewCat"}, headers=get_auth_headers(at_user))
    assert cat_resp.status_code == 403
    tag_resp = client.post("/api/v1/tags/", json={"name": "NewTag"}, headers=get_auth_headers(at_user))
    assert tag_resp.status_code == 403
    # Редактор може створити категорію і тег
    cat_resp2 = client.post("/api/v1/categories/", json={"name": "News"}, headers=get_auth_headers(at_editor))
    assert cat_resp2.status_code == 200
    tag_resp2 = client.post("/api/v1/tags/", json={"name": "Update"}, headers=get_auth_headers(at_editor))
    assert tag_resp2.status_code == 200
    cat_id = cat_resp2.json()["id"]
    # Редактор може оновити категорію
    cat_upd = client.put(f"/api/v1/categories/{cat_id}", json={"name": "NewsUpdated"}, headers=get_auth_headers(at_editor))
    assert cat_upd.status_code == 200
    # Звичайний користувач не може видалити категорію
    cat_del = client.delete(f"/api/v1/categories/{cat_id}", headers=get_auth_headers(at_user))
    assert cat_del.status_code == 403
    # Адмін може видалити категорію
    cat_del2 = client.delete(f"/api/v1/categories/{cat_id}", headers=get_auth_headers(at_admin))
    assert cat_del2.status_code == 204
