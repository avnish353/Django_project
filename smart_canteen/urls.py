from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('canteen.urls')),
    path('account/', include('users.urls')),
    path('adminpanel/', include('adminpanel.urls')),
    path('account/login/', auth_views.LoginView.as_view(), name="login"),  
]
