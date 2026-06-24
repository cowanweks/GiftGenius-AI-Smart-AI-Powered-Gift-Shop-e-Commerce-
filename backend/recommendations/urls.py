from django.urls import path

from . import views

urlpatterns = [
    path('gift-finder/', views.GiftFinderView.as_view(), name='gift-finder'),
]
