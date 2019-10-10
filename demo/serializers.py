from rest_framework import serializers, fields


class ScheduleBotSerializer(serializers.Serializer):
    number_of_users = fields.IntegerField(min_value=1)
    max_posts_per_user = fields.IntegerField(min_value=1)
    max_likes_per_user = fields.IntegerField(min_value=1)

