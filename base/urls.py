from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('telegramlipa.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
