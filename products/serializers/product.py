from rest_framework import serializers

from ..models.product import Product
from ..models.user import User, UserGroup
from ..models.category import Category
from ..models.flavor import Flavor
from .rating import RatingSerializer
from .comment import CommentSerializer


class ProductDetailSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    flavors = serializers.StringRelatedField(many=True, read_only=True)
    groups = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating products with related objects"""
    category = serializers.CharField()
    flavors = serializers.ListField(
        child=serializers.CharField(), 
        required=False, 
        allow_empty=True
    )
    groups = serializers.ListField(
        child=serializers.CharField(), 
        required=False, 
        allow_empty=True
    )
    telegram_id = serializers.IntegerField()
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Product
        fields = ['category', 'variant', 'telegram_id', 'username', 'flavors', 'groups']

    def validate_category(self, value):
        if not value:
            raise serializers.ValidationError("Category is required")
        return value

    def validate_telegram_id(self, value):
        if not value:
            raise serializers.ValidationError("telegram_id is required")
        return value

    def create(self, validated_data):
        """Create product with related objects"""
        # Extract related data
        category_name = validated_data.pop('category')
        telegram_id = validated_data.pop('telegram_id')
        username = validated_data.pop('username', '')
        flavor_names = validated_data.pop('flavors', [])
        group_names = validated_data.pop('groups', [])

        # Get or create category
        category, _ = Category.objects.get_or_create(name=category_name)

        # Get or create user
        user, _ = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={'username': username}
        )

        # Create product
        product = Product.objects.create(
            category=category,
            user=user,
            **validated_data
        )

        # Add flavors
        for flavor_name in flavor_names:
            if flavor_name:  # Skip empty strings
                flavor, _ = Flavor.objects.get_or_create(name=flavor_name)
                product.flavors.add(flavor)

        # Add groups
        for group_name in group_names:
            if group_name:  # Skip empty strings
                group, _ = UserGroup.objects.get_or_create(name=group_name)
                product.groups.add(group)

        return product

    def update(self, instance, validated_data):
        """Update product with related objects"""
        # Extract related data
        category_name = validated_data.pop('category', None)
        flavor_names = validated_data.pop('flavors', None)
        group_names = validated_data.pop('groups', None)
        
        # Remove fields that shouldn't be updated directly
        validated_data.pop('telegram_id', None)
        validated_data.pop('username', None)

        # Update category if provided
        if category_name is not None:
            category, _ = Category.objects.get_or_create(name=category_name)
            instance.category = category

        # Update flavors if provided
        if flavor_names is not None:
            instance.flavors.clear()
            for flavor_name in flavor_names:
                if flavor_name:  # Skip empty strings
                    flavor, _ = Flavor.objects.get_or_create(name=flavor_name)
                    instance.flavors.add(flavor)

        # Update groups if provided
        if group_names is not None:
            instance.groups.clear()
            for group_name in group_names:
                if group_name:  # Skip empty strings
                    group, _ = UserGroup.objects.get_or_create(name=group_name)
                    instance.groups.add(group)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


