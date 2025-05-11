
from django.contrib import admin
from django.urls import include, path

from core.views import home_view  # замените 'yourapp' на имя вашего приложения


urlpatterns = [
    path('', home_view, name='home'),  # Главная страница
    path('users/', include('users.urls', namespace='users')),
    path('polls/', include('polls.urls', namespace='polls')),
    path('admin/', admin.site.urls),
]

