from django.db import transaction
from django.db.utils import IntegrityError
from pytils.translit import slugify

from notes.models import Note

from .constants import ADD_URL, DELETE_URL, EDIT_URL, SLUG
from .core import BaseTest


class TestNoteCRUD(BaseTest):
    """Тестирование работы с заметками."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {'title': 'Заголовок',
                         'text': 'Текст',
                         'author': cls.author_user, }

        cls.new_data = {'title': 'Новый заг',
                        'text': 'Новый текст',
                        'author': cls.author_user,
                        'slug': 'new_slug'}

    def test_anonymous_user_cannot_create_note(self):
        """Аноним не может создавать заметки."""
        notes = set(Note.objects.all())
        self.client.post(ADD_URL, data=self.form_data)
        self.assertEqual(set(Note.objects.all()), notes)

    def test_user_can_create_note(self):
        """Пользователь может создавать заметки."""
        notes_before = set(Note.objects.all())
        self.client_author.post(ADD_URL, data=self.form_data)
        notes_after = set(Note.objects.all())
        # Проверяем, что создана одна заметка:
        self.assertEqual(len(notes_after - notes_before), 1)
        # Достаём созданную заметку и сверяем предметные поля:
        new_note = list(notes_after - notes_before).pop()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.form_data['author'])

    def test_creation_with_same_slug(self):
        """Нельзя создать заметки с одинаковым слагом."""
        notes_before = set(Note.objects.all())
        # Проверяем, что БД не позволяет создать заметку с идентичным слагом:
        with self.assertRaises(IntegrityError):
            try:
                # Выполняем во вложенной транзакции, чтобы не ломать основную:
                with transaction.atomic():
                    Note.objects.create(title='Заметка с неуникальным слагом',
                                        text='Текст', author=self.author_user,
                                        slug=SLUG)
            except IntegrityError:
                raise
        # Убедимся, что содержимое таблицы действительно не изменилось. Если бы
        # не эта (лишняя) проверка - обошлись бы без transaction.atomic().
        self.assertEqual(set(Note.objects.all()), notes_before)

    def test_slugify_slug_matching(self):
        """Сгенерированный слаг заметки идентичен полученному через slugify."""
        notes = set(Note.objects.all())
        self.client_author.post(ADD_URL, data=self.form_data)
        new_note = (set(Note.objects.all()) - notes)
        self.assertEqual(len(new_note), 1)
        new_note = new_note.pop()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, slugify(self.form_data['title']))
        self.assertEqual(new_note.author, self.author_user)

    def test_author_can_edit_note(self):
        """Пользователь может редактировать свою заметку."""
        self.client_author.post(EDIT_URL, data=self.new_data)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.new_data['title'])
        self.assertEqual(note.text, self.new_data['text'])
        self.assertEqual(note.slug, self.new_data['slug'])
        self.assertEqual(note.author, self.new_data['author'])

    def test_reader_cannot_edit_note(self):
        """Пользователь не может редактировать чужую заметку."""
        note = Note.objects.get(id=self.note.id)
        self.client_reader.post(EDIT_URL, data=self.new_data)
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, updated_note.title)
        self.assertEqual(note.text, updated_note.text)
        self.assertEqual(note.slug, updated_note.slug)
        self.assertEqual(note.author, updated_note.author)

    def test_author_can_delete_note(self):
        """Пользователь может удалить свою заметку."""
        notes = set(Note.objects.all())
        self.client_author.delete(DELETE_URL)
        self.assertEqual(len(notes - set(Note.objects.all())), 1)
        self.assertIsNone(Note.objects.filter(slug=self.note.slug).first())

    def test_user_cannot_delete_note(self):
        """Пользователь не может удалить чужую заметку."""
        notes = set(Note.objects.all())
        self.client_reader.delete(DELETE_URL)
        self.assertEqual(notes, set(Note.objects.all()))
        note = Note.objects.get(id=self.note.id)
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, updated_note.title)
        self.assertEqual(note.text, updated_note.text)
        self.assertEqual(note.slug, updated_note.slug)
        self.assertEqual(note.author, updated_note.author)
