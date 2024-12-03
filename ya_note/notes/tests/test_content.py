from notes.forms import NoteForm
from notes.models import Note

from .constants import ADD_URL, EDIT_URL, LIST_URL
from .core import BaseTest


class TestNotes(BaseTest):
    """Тестирование передачи данных на страницы."""
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.readers_note = Note.objects.create(title='Заметка Читателя',
                                               text='Текст',
                                               author=cls.reader_user)

    def test_note_is_in_list_context(self):
        """Передача заметки на страницу.

        Отдельная заметка передаётся на страницу со списком заметок
        в списке object_list в словаре context.
        """
        notes_list = self.client_author.get(LIST_URL).context['object_list']
        self.assertIn(self.note, notes_list)
        # Достаём из контекста заметку с нужным id и сверяем предметные поля:
        sent_note = next((note for note in notes_list
                          if getattr(note, 'id', None) == self.note.id), None)
        self.assertEqual(self.note.title, sent_note.title)
        self.assertEqual(self.note.text, sent_note.text)
        self.assertEqual(self.note.author, sent_note.author)
        self.assertEqual(self.note.slug, sent_note.slug)

    def test_forms_is_on_create_and_edit_pages(self):
        """Передача форм на страницы создания и редактирования заметки."""
        urls = (ADD_URL, EDIT_URL)
        for url in urls:
            with self.subTest():
                context = self.client_author.get(url).context
                self.assertIn('form', context)
                self.assertIsInstance(context['form'], NoteForm)

    def test_no_alien_notes_in_users_notes(self):
        """В заметки одного пользователя не попадают заметки другого."""
        self.assertNotIn(
            Note.objects.get(author=self.reader_user),
            self.client_author.get(LIST_URL).context['object_list']
        )
