import pytest

from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup',)
)
def test_pages_availability_for_anon(client, name):
    """Главная страница, вход, выход и регистрация доступны анониму."""
    assert client.get(reverse(name)).status_code == HTTPStatus.OK


def test_detail_availability_for_anon(news, client):
    """Страница новости доступна анониму."""
    assert client.get(
        reverse('news:detail', args=(news.id,))
    ).status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_edit_delete_pages_availability_for_author(comment, name,
                                                   author_client,
                                                   not_author_client):
    """Страницы удаления, редактирования комментария доступны только автору."""
    assert author_client.get(
        reverse(name, args=(comment.id,))
    ).status_code == HTTPStatus.OK
    assert not_author_client.get(
        reverse(name, args=(comment.id,))
    ).status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_edit_delete_pages_redirects(client, name, comment):
    """Страницы удаления, редактирования переадресовывают анонима."""
    redirect_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    expected_url = f'{redirect_url}?next={url}'
    assertRedirects(client.get(url), expected_url)
