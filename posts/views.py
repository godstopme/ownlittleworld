from django.contrib.auth.models import AbstractUser
from django.core import exceptions
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from posts import models
from posts.models import Like, Post
from posts.serializer import PostSerializer


class PostsViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects
    serializer_class = PostSerializer

    def destroy(self, request, *args, **kwargs):
        user: AbstractUser = self.request.user

        if user.is_superuser or user.id == self.get_object().user.id:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['POST'], detail=True, url_path='like')
    def like(self, request, *args, **kwargs):
        # a perfect place for this code would be somehow organized `service` object that performs like/unlike logic
        post: Post = self.get_object()

        try:
            post.likes.get(user=self.request.user)

            return Response({'error': 'You already liked this post'}, status=status.HTTP_409_CONFLICT)
        except exceptions.ObjectDoesNotExist:
            post.likes.create(user=self.request.user)

            return Response(status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True, url_path='unlike')
    def unlike(self, request, *args, pk=None, **kwargs):
        Like.objects.filter(user=self.request.user, post=pk).delete()

        return Response(status.HTTP_202_ACCEPTED)
