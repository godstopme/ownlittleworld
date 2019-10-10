from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    content = models.TextField(null=False, blank=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)


# although it sounds simple to add like/unlike logic to the app, but if we dig into the problem
# we gonna find out that this is not as simple as it seems
# for example, if we're creating an instagram, this logic should be stored in other service that handles users'
# preferences, mb no-sql approaches should be used or different DB structure should be made for
# performance/consistency goals and so on
# chose this approach for simplicity
class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, related_name='likes')
