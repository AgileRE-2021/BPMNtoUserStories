from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('uploadfile/', views.uploadpage, name='uploadpage'),
    path('proses/', views.parsing, name='parsing'),
<<<<<<< HEAD
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
=======
>>>>>>> 3496840375ecde488c3fca323c7ce098f1c3e8af
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)