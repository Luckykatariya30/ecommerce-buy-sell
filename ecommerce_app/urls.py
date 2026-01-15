from django.urls import path
from ecommerce_app import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('contect/', views.contect, name='contect'),
    path('about', views.about, name='about'),
    path('profile', views.profile, name='profile'),
    path('checkout', views.checkout, name='checkout'),
    path('blog', views.blog, name='blog'),
    # path('handlerequest', views.handlerequest, name='handlerequest'),
]
