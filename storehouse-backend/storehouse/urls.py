from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'I4 Lab Storehouse'
admin.site.site_title = 'I4 Lab Storehouse Admin Site'
admin.site.index_title = 'Admin Site'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),
]
