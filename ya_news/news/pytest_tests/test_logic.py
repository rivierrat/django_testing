import pytest
from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


pytestmark = pytest.mark.django_db

COMMENT = {'text': 'Текст комментария', }
MODIFIED_COMMENT = {'text': 'Новый текст', }


def test_anon_cannot_make_comment(client, detail_url):
    """Аноним не может оставить комментарий."""
    comments = set(Comment.objects.all())
    client.post(detail_url, data=COMMENT)
    assert set(Comment.objects.all()) == comments


def test_user_can_make_comment(author_client, detail_url,
                               news, author, comment):
    """Авторизованный пользователь может оставить комментарий."""
    comments = set(Comment.objects.all())
    author_client.post(detail_url, data=COMMENT)
    # Проверяем, что создан один комментарий:
    assert len(set(Comment.objects.all()) - comments) == 1
    # Проверяем, что комментарий создан с ожидаемым содержимым
    comment = Comment.objects.get(id=comment.id)
    assert comment.news == news
    assert comment.author == author
    assert comment.text == COMMENT['text']


@pytest.mark.parametrize(
    'test_data',
    [{'text': f'Это {word} текст'} for word in BAD_WORDS]
)
def test_form_refuses_bad_words(author_client, detail_url, test_data):
    """Форма не принимает комментарий с запрещёнными словами.

    Проверяем, что комментарий не создаётся, а форма возвращает ошибку.
    """
    comments = set(Comment.objects.all())
    assertFormError(
        author_client.post(detail_url, test_data),
        'form', 'text', errors=(WARNING))
    # Проверяем, что после процедуры в таблице остались *те же* комменты:
    assert set(Comment.objects.all()) == comments


def test_author_can_delete_comment(author_client, comment, comment_delete_url):
    """Пользователь может удалить свой комментарий."""
    comments_count = Comment.objects.all().count()
    author_client.delete(comment_delete_url)
    # Проверяем, что содержимое таблицы до/после отличается на один коммент:
    assert comments_count - Comment.objects.all().count() == 1
    # Проверяем, что не осталось коммента с данным id:
    assert not Comment.objects.filter(id=comment.id).exists()


def test_user_cannot_delete_comment(not_author_client, comment_delete_url):
    """Пользователь не может удалить чужой комментарий."""
    comments = set(Comment.objects.all())
    not_author_client.delete(comment_delete_url)
    # Проверяем, что после процедуры в таблице остались те же комменты:
    assert set(Comment.objects.all()) == comments


def test_author_can_edit_comment(
        author_client, comment, comment_edit_url):
    """Пользователь может изменить свой комментарий."""
    comment = Comment.objects.get(id=comment.id)
    author_client.post(comment_edit_url, data=MODIFIED_COMMENT)
    attempt_comment = Comment.objects.get(id=comment.id)
    assert comment.news == attempt_comment.news
    assert comment.author == attempt_comment.author
    assert attempt_comment.text == MODIFIED_COMMENT['text']


def test_user_cannot_edit_comment(not_author_client, comment,
                                  comment_edit_url):
    """Пользователь не может изменить чужой комментарий."""
    comment = Comment.objects.get(id=comment.id)
    not_author_client.post(comment_edit_url, data=MODIFIED_COMMENT)
    attempt_comment = Comment.objects.get(id=comment.id)
    assert comment.news == attempt_comment.news
    assert comment.author == attempt_comment.author
    assert comment.text == attempt_comment.text
