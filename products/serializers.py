from rest_framework import serializers

from .models.comment import Comment
from .models.product import Product
from .models.rating import Rating
from .models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['telegram_id', 'username']


class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Rating
        fields = ['user', 'value',]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['user', 'text',]


class ProductDetailSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

