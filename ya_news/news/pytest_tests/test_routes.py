from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from .constants import (ANON_CLIENT, AUTHOR_CLIENT, COMMENT_DELETE_URL,
                        COMMENT_EDIT_URL, DELETE_REDIRECT_URL, DETAIL_URL,
                        EDIT_REDIRECT_URL, HOME_URL, LOGIN_URL, LOGOUT_URL,
                        NOT_AUTHOR_CLIENT, SIGNUP_URL)


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, user_client, status',
    (
        (HOME_URL, ANON_CLIENT, HTTPStatus.OK),
        (LOGIN_URL, ANON_CLIENT, HTTPStatus.OK),
        (LOGOUT_URL, ANON_CLIENT, HTTPStatus.OK),
        (SIGNUP_URL, ANON_CLIENT, HTTPStatus.OK),
        (DETAIL_URL, ANON_CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (COMMENT_DELETE_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (COMMENT_EDIT_URL, ANON_CLIENT, HTTPStatus.FOUND),
        (COMMENT_DELETE_URL, ANON_CLIENT, HTTPStatus.FOUND),
    )
)
def test_pages_availability(user_client, url, status):
    """Тест доступности страниц.

    Главная страница, вход, выход, регистрация и страница новости доступны
    анонимному пользователю. Страницы удаления и редактирования комментария
    доступны автору и недоступны другому пользователю.
    """
    assert user_client.get(url).status_code == status


@pytest.mark.parametrize(
    'url, expected_url',
    [
        [COMMENT_EDIT_URL, EDIT_REDIRECT_URL],
        [COMMENT_DELETE_URL, DELETE_REDIRECT_URL],
    ]
)
def test_edit_delete_pages_redirects(client, url, expected_url):
    """Страницы удаления, редактирования переадресовывают анонима."""
    assertRedirects(client.get(url), expected_url)
