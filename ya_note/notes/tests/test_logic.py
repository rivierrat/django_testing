from pytils.translit import slugify
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.alice = User.objects.create(username='Алиса')
        cls.client = Client()
        cls.url = reverse('notes:add')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.alice)
        cls.form_data = {'title': 'Заголовок заметки',
                         'text': 'Текст заметки',
                         'author': 'alice'}

    def test_anonymous_user_cant_create_note(self):
        """Аноним не может создавать заметки."""
        self.client.post(self.url, data=self.form_data)
        self.assertEqual(Note.objects.count(), 0)

    def test_user_can_create_note(self):
        """Пользователь может создавать заметки."""
        self.auth_client.post(self.url, data=self.form_data)
        self.assertEqual(Note.objects.count(), 1)

    def test_creation_with_same_slug(self):
        """Нельзя создать заметки с одинаковым слагом."""
        self.auth_client.post(self.url, data=self.form_data)
        self.auth_client.post(self.url, data=self.form_data)
        self.assertEqual(Note.objects.count(), 1)

    def test_slugify_slug_matching(self):
        """Сгенерированный слаг заметки идентичен полученному через slugify."""
        self.auth_client.post(self.url, data=self.form_data)
        self.assertEqual(
            slugify(self.form_data['title']),
            Note.objects.get().slug
        )


class TestEditionDeletionNotes(TestCase):
    TEXT_BEFORE = 'Исходный текст'
    TEXT_AFTER = 'Новый текст'

    @classmethod
    def setUpTestData(cls):
        cls.alice = User.objects.create(username='Алиса')
        cls.author_client = Client()
        cls.author_client.force_login(cls.alice)

        cls.bob = User.objects.create(username='Боб')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.bob)

        cls.note = Note.objects.create(title='Заметка Алисы',
                                       text=cls.TEXT_BEFORE,
                                       author=cls.alice)

        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.form_data = {'title': 'Заголовок заметки',
                         'text': cls.TEXT_AFTER,
                         'slug': 'new_slug'}

    def test_author_can_edit_note(self):
        """Пользователь может редактировать свою заметку."""
        self.author_client.post(self.edit_url, data=self.form_data)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.TEXT_AFTER)

    def test_user_cant_edit_note(self):
        """Пользователь не может редактировать чужую заметку."""
        self.reader_client.post(self.edit_url, data=self.form_data)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.TEXT_BEFORE)

    def test_author_can_delete_note(self):
        """Пользователь может удалить свою заметку."""
        self.author_client.delete(self.delete_url)
        self.assertEqual(Note.objects.count(), 0)

    def test_user_cant_delete_note(self):
        """Пользователь не может удалить чужую заметку."""
        self.reader_client.delete(self.delete_url)
        self.assertEqual(Note.objects.count(), 1)
