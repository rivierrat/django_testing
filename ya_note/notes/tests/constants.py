from django.urls import reverse


SLUG = 'zametka'
LIST_URL = reverse('notes:list')
ADD_URL = reverse('notes:add')
EDIT_URL = reverse('notes:edit', args=(SLUG,))
DELETE_URL = reverse('notes:delete', args=(SLUG,))
HOME_URL = reverse('notes:home')
SIGNUP_URL = reverse('users:signup')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SUCCESS_URL = reverse('notes:success', args=None)
DETAIL_URL = reverse('notes:detail', args=(SLUG,))
