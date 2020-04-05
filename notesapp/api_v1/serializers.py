from rest_framework import serializers

from .models import Category, Notes, User, Person
from .helpers.validators import CategoryValidations


class PersonModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'is_superuser', 'is_active']
        extra_kwargs = {'password': {'write_only': True}, 'is_superuser': {'write_only': True}}

    def create(self, validated_data):
        person = Person(
            email = validated_data['email'],
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        person.set_password(validated_data['password'])
        person.save()
        return person

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

class NotesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notes
        fields = ['title', 'body', 'category']


class CategoryModelSerializer(serializers.ModelSerializer, CategoryValidations):
    notes = NotesModelSerializer(many=True, read_only=True)
    # to display a string field instead of whole object
    # notes = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    class Meta:
        model = Category
        fields = ['name', 'notes']

    def validate(self, data):
        '''
        Perform various validations on category data
        '''
        if len(data['name']) < 10:
            raise serializers.ValidationError("Name must be greater than 10 characters.")
        return data

    
class CategorySerializer(serializers.ModelSerializer, CategoryValidations):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=255, validators=CategoryValidations().check_name_is_unique)
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

