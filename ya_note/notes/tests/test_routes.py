from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(title='Заголовок',
                                       text='Текст',
                                       author=cls.author)

    def test_pages_availability_for_anon(self):
        """Главная страница, регистрация, вход и выход доступны анониму."""
        urls = ('notes:home', 'users:signup', 'users:login', 'users:logout')
        for name in urls:
            with self.subTest(name=name):
                self.assertEqual(self.client.get(
                    reverse(name, args=None)
                ).status_code, HTTPStatus.OK)

    def test_pages_availability_for_user(self):
        """Список заметок и страницы добавления доступны пользователю."""
        self.client.force_login(self.reader)
        for name in ('notes:list', 'notes:add', 'notes:success'):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(
                    reverse(name, args=None)
                ).status_code, HTTPStatus.OK)

    def test_availability_for_note_edit_and_delete(self):
        """Редактирование и удаление заметки доступны только её автору."""
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:detail', 'notes:edit', 'notes:delete'):
                with self.subTest(user=user, name=name):
                    self.assertEqual(self.client.get(
                        reverse(name, args=(self.note.slug,))
                    ).status_code, status)

    def test_redirect_for_anon(self):
        login_url = reverse('users:login')
        for name, args in (
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:detail', (self.note.slug,)),
            ('notes:list', None),
            ('notes:add', None),
            ('notes:success', None),
        ):
            with self.subTest(name=name, args=args):
                url = reverse(name, args=args)
                self.assertRedirects(
                    self.client.get(url), f'{login_url}?next={url}'
                )
