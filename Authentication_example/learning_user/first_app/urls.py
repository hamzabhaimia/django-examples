from django.conf.urls import url
from first_app import views

app_name='first_app'

urlpatterns = [
    url(r'user_login/$',views.user_login,name='user_login'),
    url(r'^registration/$',views.Register,name='registration'),
]