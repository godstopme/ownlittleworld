from rest_framework.routers import DefaultRouter

from posts.views import PostsViewSet

router = DefaultRouter()

router.register(r'', PostsViewSet, 'posts')

urlpatterns = []
urlpatterns += router.urls
