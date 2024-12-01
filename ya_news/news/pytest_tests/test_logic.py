import pytest

from pytest_django.asserts import assertFormError
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


pytestmark = pytest.mark.django_db

NEW_TEXT = 'Это какой-то новый текст'


def test_anon_cant_make_comment(client, news, comment_text):
    """Аноним не может оставить комментарий."""
    comments_count = Comment.objects.count()
    client.post(reverse('news:detail', args=(news.id,)), data=comment_text)
    assert Comment.objects.count() == comments_count


def test_user_can_make_comment(author_client, news, comment_text):
    """Авторизованный пользователь может оставить комментарий."""
    comments_count = Comment.objects.count()
    author_client.post(reverse('news:detail', args=(news.id,)),
                       data=comment_text)
    assert Comment.objects.count() == comments_count + 1


def test_form_refuses_bad_words(author_client, news, comment_text):
    """Форма не принимает комментарий с запрещёнными словами.

    Проверяем, что комментарий не создаётся, а форма возвращает ошибку.
    """
    comments_count = Comment.objects.count()
    comment_text['text'] = f'Это какой-то {BAD_WORDS[0]} текст'
    assertFormError(
        author_client.post(reverse('news:detail', args=(news.id,)),
                           data=comment_text),
        'form', 'text', errors=(WARNING))
    assert Comment.objects.count() == comments_count


def test_author_can_delete_comment(author_client, comment):
    """Пользователь может удалить свой комментарий."""
    comments_count = Comment.objects.count()
    author_client.delete(reverse('news:delete', args=(comment.id,)))
    assert Comment.objects.count() == comments_count - 1


def test_user_cannot_delete_comment(not_author_client, comment):
    """Пользователь не может удалить чужой комментарий."""
    comments_count = Comment.objects.count()
    not_author_client.delete(reverse('news:delete', args=(comment.id,)))
    assert Comment.objects.count() == comments_count


def test_author_can_edit_comment(author_client, news, comment, comment_text):
    """Пользователь может изменить свой комментарий."""
    comment_text['text'] = NEW_TEXT
    author_client.post(reverse('news:edit', args=(comment.id,)),
                       data=comment_text)
    comment.refresh_from_db()
    assert comment.text == NEW_TEXT


def test_user_cannot_edit_comment(
     not_author_client, comment, comment_text):
    """Пользователь не может изменить чужой комментарий."""
    not_author_client.post(reverse('news:edit', args=(comment.id,)),
                           data={'text': NEW_TEXT, })
    comment.refresh_from_db()
    assert comment.text == comment_text['text']
