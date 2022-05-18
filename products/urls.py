from django.urls import path, include

from .views import HomePageView, ProductCreateView, ProductDeleteView, ProductUpdateView, invalidate_cache

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='delete'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='update'),
    path('invalidate_cache/', invalidate_cache, name='invalidate_cache'),
]
