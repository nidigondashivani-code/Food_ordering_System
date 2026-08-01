from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # Django Internationalization URL
    path('', views.home, name='home'),
    path('users/', include('users.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('menu/', include('menu.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('reviews/', include('reviews.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])