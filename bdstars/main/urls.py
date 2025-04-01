from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('about/', views.about, name='about'),
    #path('contacts/', views.contacts, name='contacts'),  # Добавьте эту строку
    path('person/<slug:slug>/', views.star_detail, name='star_detail'), # Детальная страница по slug
    # Знаменитости по стране
    path('country/<slug:slug>/', views.stars_by_country, name='stars_by_country'),

    # Знаменитости по виду деятельности
    path('industry/<slug:slug>/', views.stars_by_category, name='stars_by_category'),
    path('add/', views.add_star, name='add_star'),
]