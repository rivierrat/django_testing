from pytest_lazyfixture import lazy_fixture


# Урлы
COMMENT_DELETE_URL = lazy_fixture('comment_delete_url')
COMMENT_EDIT_URL = lazy_fixture('comment_edit_url')
DELETE_REDIRECT_URL = lazy_fixture('delete_redirect_url')
DETAIL_URL = lazy_fixture('detail_url')
EDIT_REDIRECT_URL = lazy_fixture('edit_redirect_url')
HOME_URL = lazy_fixture('news_home_url')
LOGIN_URL = lazy_fixture('login_url')
LOGOUT_URL = lazy_fixture('logout_url')
SIGNUP_URL = lazy_fixture('signup_url')

# Клиенты
ANON_CLIENT = lazy_fixture('client')
AUTHOR_CLIENT = lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = lazy_fixture('not_author_client')
