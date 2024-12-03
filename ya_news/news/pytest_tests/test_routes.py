from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, role, status',
    (
        (lazy_fixture('news_home_url'), lazy_fixture('client'), HTTPStatus.OK),
        (lazy_fixture('login_url'), lazy_fixture('client'), HTTPStatus.OK),
        (lazy_fixture('logout_url'), lazy_fixture('client'), HTTPStatus.OK),
        (lazy_fixture('signup_url'), lazy_fixture('client'), HTTPStatus.OK),
        (lazy_fixture('detail_url'), lazy_fixture('client'), HTTPStatus.OK),
        (lazy_fixture('comment_edit_url'), lazy_fixture('author_client'),
         HTTPStatus.OK),
        (lazy_fixture('comment_delete_url'), lazy_fixture('author_client'),
         HTTPStatus.OK),
        (lazy_fixture('comment_edit_url'), lazy_fixture('not_author_client'),
         HTTPStatus.NOT_FOUND),
        (lazy_fixture('comment_delete_url'), lazy_fixture('not_author_client'),
         HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability(role, url, status):
    """Тест доступности страниц.

    Главная страница, вход, выход, регистрация и страница новости доступны
    анонимному пользователю. Страницы удаления и редактирования комментария
    доступны автору и недоступны другому пользователю.
    """
    assert role.get(url).status_code == status


@pytest.mark.parametrize(
    'url',
    (
        lazy_fixture('comment_edit_url'),
        lazy_fixture('comment_delete_url'),
    )
)
def test_edit_delete_pages_redirects(client, url, login_url):
    """Страницы удаления, редактирования переадресовывают анонима."""
    expected_url = f'{login_url}?next={url}'
    assertRedirects(client.get(url), expected_url)
