import pytest

from django.conf import settings
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test_comment_form_availability_for_anon(news, client):
    """Форма отправки комментария недоступна анониму."""
    assert 'form' not in client.get(
        reverse('news:detail', args=(news.id,))
        ).context


def test_comment_form_availability_for_user(news, author_client):
    """Форма отправки комментария доступна пользователю."""
    assert 'form' in author_client.get(
        reverse('news:detail', args=(news.id,))
        ).context


def test_news_count(client, news_bulk):
    """На главную страницу выводится не более 10 новостей."""
    assert (client.get(reverse('news:home')).context['object_list'].count() ==
            settings.NEWS_COUNT_ON_HOME_PAGE)


def test_news_order(client, news_bulk):
    """Новости на главной отсортированы по дате от новых к старым."""
    all_dates = [news.date for news in
                 client.get(reverse('news:home')).context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(client, news, comments_bulk):
    """Комментарии к новости отсортированы по дате от старых к новым."""
    all_comments = client.get(
        reverse('news:detail', args=(news.id,))
        ).context['news'].comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    assert all_timestamps == sorted(all_timestamps)
