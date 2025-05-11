
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from core.views import home_view  # замените 'yourapp' на имя вашего приложения


urlpatterns = [
    path('', home_view, name='home'),  # Главная страница
    path('users/', include('users.urls', namespace='users')),
    path('polls/', include('polls.urls', namespace='polls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

