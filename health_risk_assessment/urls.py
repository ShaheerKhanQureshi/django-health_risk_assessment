from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('assessment/', include('assessment.urls')),  # Ensure this points to your app
]

