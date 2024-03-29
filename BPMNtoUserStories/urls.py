from django.contrib import admin
from django.urls import path
from bpmn_to_us import views
from django.conf import settings
from django.conf.urls.static import static
from bpmn_to_us.views import Pdf


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('uploadfile/', views.uploadpage, name='uploadpage'),
    path('proses/', views.parsing, name='parsing'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('documentation/', views.documentation, name='documentation'),
    path('/pdf/<int:id>',Pdf.getpdf, name='pdf'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)