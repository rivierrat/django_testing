from http import HTTPStatus

from .constants import (ADD_URL, DELETE_URL, DETAIL_URL, EDIT_URL, HOME_URL,
                        LIST_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL,
                        SUCCESS_URL)
from .core import BaseTest


class TestRoutes(BaseTest):
    """Тестирование маршрутов."""

    def test_pages_availability(self):
        """Проверка доступности страниц.

        Главная страница, регистрация, вход и выход доступны анониму.
        Список заметок и страницы добавления доступны пользователю.
        Редактирование и удаление заметки доступно только её автору.
        """
        routes = [
            [HOME_URL, self.client, HTTPStatus.OK],
            [SIGNUP_URL, self.client, HTTPStatus.OK],
            [LOGIN_URL, self.client, HTTPStatus.OK],
            [LOGOUT_URL, self.client, HTTPStatus.OK],
            [LIST_URL, self.client_author, HTTPStatus.OK],
            [ADD_URL, self.client_author, HTTPStatus.OK],
            [SUCCESS_URL, self.client_author, HTTPStatus.OK],
            [DELETE_URL, self.client_author, HTTPStatus.OK],
            [EDIT_URL, self.client_author, HTTPStatus.OK],
            [DELETE_URL, self.client_reader, HTTPStatus.NOT_FOUND],
            [EDIT_URL, self.client_reader, HTTPStatus.NOT_FOUND],
        ]
        for url, client, status in routes:
            with self.subTest(url=url, client=client, status=status):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirect_for_anon(self):
        """Перенаправления для анонимного пользователя."""
        for url in (EDIT_URL, DELETE_URL, LIST_URL,
                    ADD_URL, SUCCESS_URL, DETAIL_URL):
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url), f'{LOGIN_URL}?next={url}'
                )
