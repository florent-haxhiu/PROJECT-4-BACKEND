from django.urls import path
from .views import EditProfileView, RegisterView, LoginView, ProfileView, UserDetailView, UserListView, UserMessageCreateView, UserFollowView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('users/', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('<int:pk>/edit/', EditProfileView.as_view()),
    path('<int:user_pk>/follow/', UserFollowView.as_view()),
    path('<int:recipient_pk>/message/', UserMessageCreateView.as_view())
]