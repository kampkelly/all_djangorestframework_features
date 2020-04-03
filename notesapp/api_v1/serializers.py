from rest_framework import serializers

from .models import Category
from .helpers.validators import Validations

class CategoryModelSerializer(serializers.ModelSerializer, Validations):

    class Meta:
        model = Category
        fields = ['name']

    def validate(self, data):
        '''
        Perform various validations on category data
        '''
        if len(data['name']) < 10:
            raise serializers.ValidationError("Name must be greater than 10 characters.")
        return data

    

class CategorySerializer(serializers.ModelSerializer, Validations):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=255)
    class Meta:
        model = Category
        fields = ['id', 'name']
        ordering = ['created_at']

    def validate(self, data):
        '''
        Perform various validations on category data
        '''
        if len(data['name']) < 10:
            raise serializers.ValidationError("Name must be greater than 10 characters.")
        return data

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    # def save(self):
    #     name = self.validated_data['name']
    #     pass