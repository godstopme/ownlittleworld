from typing import Any, Dict

from rest_framework import serializers, fields

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    user = fields.IntegerField(source='user.id', read_only=True)
    likes = fields.IntegerField(source='likes.count', read_only=True)

    class Meta:
        fields = (
            'id',
            'user',
            'content',
            'likes',
        )
        model = Post

    def create(self, validated_data: Dict[str, Any]):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
