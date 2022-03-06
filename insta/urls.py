from django.urls import path
from .views import PostLikeView, PostDetailView, PostListView, CommentDetailView, CommentListView

urlpatterns = [
    path('', PostListView.as_view()),
    path('<int:pk>/', PostDetailView.as_view()),
    path('<int:post_pk>/like/', PostLikeView.as_view()),
    path('<int:post_pk>/comment/', CommentListView.as_view()),
    path('<int:post_pk>/comment/<int:comment_pk>/', CommentDetailView.as_view())
]