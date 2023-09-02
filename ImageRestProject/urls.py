from django.contrib import admin
from django.urls import path
from ImageApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index, name='home'),
    # path('prediction', views.prediction, name='prediction'),
    path('profile/', views.ProfilesView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
