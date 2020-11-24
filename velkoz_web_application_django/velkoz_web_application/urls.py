from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),

    # Url Paths for User Authentication system:
    path('auth/', include('user_management.urls')),

    # Url Paths for the dashboard core application:
    path('', include('dashboard_core.urls')),

    # Url Paths for the Stock Data Dashboard:
    path('stock_data_db/', include('stock_dashboard.urls'))
]
