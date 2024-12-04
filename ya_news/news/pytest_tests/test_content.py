import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_comment_form_availability_for_anon(client, detail_url):
    """Форма отправки комментария недоступна анониму."""
    assert 'form' not in client.get(detail_url).context


def test_comment_form_availability_for_user(author_client, detail_url):
    """Форма отправки комментария доступна пользователю."""
    context = author_client.get(detail_url).context
    assert 'form' in context
    assert isinstance(context['form'], CommentForm)


def test_news_count(client, news_bulk, news_home_url):
    """На главную страницу выводится не более 10 новостей."""
    assert (client.get(news_home_url).context['object_list'].count()
            == settings.NEWS_COUNT_ON_HOME_PAGE)


def test_news_order(client, news_bulk, news_home_url):
    """Новости на главной отсортированы по дате от новых к старым."""
    timestamps = [news.date for news in
                  client.get(news_home_url).context['object_list']]
    assert timestamps == sorted(timestamps, reverse=True)


def test_comments_order(client, comments_bulk, detail_url):
    """Комментарии к новости отсортированы по дате от старых к новым."""
    timestamps = [comment.created for comment in
                  client.get(detail_url).context['news'].comment_set.all()]
    assert timestamps == sorted(timestamps)
