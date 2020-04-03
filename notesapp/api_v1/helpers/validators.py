from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api_v1.models import Category


class CategoryValidations():
    # an example of built in validation to override unique constraint validation
    check_name_is_unique = [UniqueValidator(queryset=Category.objects.all(), message='This name already does exists!')]

    def validate_name(self, value):
        """
        Check that the name contains sport.
        """
        if 'sport' not in value.lower():
            raise serializers.ValidationError("Name does not contain sport.")
        return value

    def name_should_contain_sport(self, value):
        '''
        To use this validator, include it in a model like this:
        name = serializers.CharField(required=True, max_length=255, validators=[name_should_contain_sport])
        '''
        if 'sport' not in value.lower():
            raise serializers.ValidationError("Name does not contain sport")
        return value
