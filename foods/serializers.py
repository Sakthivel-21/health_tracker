from rest_framework import serializers
from .models import Category, Food, FoodLog, Routine

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class FoodSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Food
        fields = ['id', 'name',  'category', 'category_id', 'calories', 'protein', 'carbs', 'fats']



class FoodCalculationSerializer(serializers.Serializer):
    food_name = serializers.CharField(max_length=200)
    quantity = serializers.FloatField(min_value=0.1)


class FoodLogSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    food_id = serializers.PrimaryKeyRelatedField(
        queryset=Food.objects.all(), source='food', write_only=True
    )

    class Meta:
        model = FoodLog
        fields = ['id', 'user', 'food', 'food_id', 'meal_type', 'date', 'quantity']
        read_only_fields = ('user', 'date')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ['id', 'user', 'title', 'description', 'is_completed', 'date']
        read_only_fields = ('user',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)



class FoodBulkUploadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    category = serializers.CharField(max_length=100)
    calories = serializers.FloatField()
    protein = serializers.FloatField(required=False, default=0)
    carbs = serializers.FloatField(required=False, default=0)
    fats = serializers.FloatField(required=False, default=0)