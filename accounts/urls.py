from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:pk>/', views.user_profile_view, name="user_profile"),
    # path('', views.HomeView.as_view(), name="homepage"),
    # path('', views.MaterialMovementsList.as_view(), name="movements_list"),
    # path('users/', views.UserList.as_view(), name="user_list"),
    # path('user/<username>/', views.userProfileView, name="user_profile"),
    # path('search/', views.search, name="search_function"),
]
