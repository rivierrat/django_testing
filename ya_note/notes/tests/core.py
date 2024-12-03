from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

from .constants import SLUG


User = get_user_model()


class BaseTest(TestCase):
    """Базовый класс тестов."""

    @classmethod
    def setUpTestData(cls):
        cls.author_user = User.objects.create(username='Писатель')
        cls.client_author = Client()
        cls.client_author.force_login(cls.author_user)
        cls.note = Note.objects.create(title='Заголовок заметки', text='Текст',
                                       author=cls.author_user, slug=SLUG)
        cls.reader_user = User.objects.create(username='Читатель')
        cls.client_reader = Client()
        cls.client_reader.force_login(cls.reader_user)
