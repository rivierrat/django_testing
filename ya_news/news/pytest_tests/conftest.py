import pytest

from datetime import timedelta
from django.conf import settings
from django.test.client import Client
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    """Создаёт одну новость."""
    return News.objects.create(title='Заголовок', text='Текст новости',)


@pytest.fixture
def comment(author, news):
    """Создаёт один комментарий."""
    return Comment.objects.create(text='Текст комментария', news=news,
                                  author=author,)


@pytest.fixture
def news_bulk():
    """Создаёт массив новостей с разными датами публикации и содержимим."""
    now = timezone.now()
    News.objects.bulk_create(
            News(title=f'Новость {index}', text=f'Текст новости {index}',
                 date=now - timedelta(hours=index))
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comments_bulk(news, author):
    """Создаёт массив комментариев с разными датами публикации и содержимим."""
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
                news=news, author=author, text=f'Tекст комментария {index}',
            )
        comment.created = now - timedelta(hours=index)
        comment.save()


@pytest.fixture
def comment_text():
    return {'text': 'Текст комментария', }