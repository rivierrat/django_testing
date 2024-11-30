from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestNotes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.alice = User.objects.create(username='Алиса')
        cls.note = Note.objects.create(title='Заметка Алисы',
                                       text='Текст',
                                       author=cls.alice)

    def test_note_is_in_list_context(self):
        """Передача заметки на страницу.

        Отдельная заметка передаётся на страницу со списком заметок
        в списке object_list в словаре context.
        """
        self.client.force_login(self.alice)
        self.assertIn(self.note, self.client.get(
            reverse('notes:list')
            ).context['object_list'])

    def test_forms_is_on_create_and_edit_pages(self):
        """Передача форм на страницы создания и редактирования заметки."""
        self.client.force_login(self.alice)
        self.assertIn('form', self.client.get(reverse('notes:add')).context)
        self.assertIn('form',
                      self.client.get(
                          reverse('notes:edit', args=(self.note.slug,))
                          ).context)

class TestAlienNotes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.alice = User.objects.create(username='Алиса')
        cls.note = Note.objects.create(title='Заметка Алисы',
                                       text='Текст',
                                       author=cls.alice)
        cls.bob = User.objects.create(username='Боб')
        cls.note = Note.objects.create(title='Заметка Боба',
                                       text='Текст',
                                       author=cls.bob)

    def test_no_alien_notes_in_users_notes(self):
        """В заметки одного пользователя не попадают заметки другого."""
        self.client.force_login(self.alice)
        self.assertNotIn(
            Note.objects.get(author=User.objects.get(username='Боб')),
            self.client.get(reverse('notes:list')).context['object_list']
        )
