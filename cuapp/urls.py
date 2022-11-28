from django.urls import URLPattern, path
from cuapp import views
import cuapp.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('index/', cuapp.views.index, name="index"),
    path('signup/',cuapp.views.signup, name= 'signup'),
    path('login/',cuapp.views.login, name= 'login'),
    path('logout/',cuapp.views.logout, name= 'logout'),
    path('mypage/',cuapp.views.mypage, name='mypage'),
    path('update_password/', cuapp.views.update_password, name='update_password'),
    path('update_user/', cuapp.views.update_user, name='update_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
