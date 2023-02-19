from django.urls import path, include


urlpatterns = [
    path('mailings/', include('mailings.urls')),
]
