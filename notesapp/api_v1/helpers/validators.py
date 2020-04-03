from rest_framework import serializers


def name_should_contain_sport(value):
    '''
    To use this validator, include it in a model like this:
    name = serializers.CharField(required=True, max_length=255, validators=[name_should_contain_sport])
    '''
    if 'sport' not in value.lower():
        raise serializers.ValidationError("Name does not contain sport")
    return value


class Validations():
    def validate_name(self, value):
        """
        Check that the name contains sport.
        """
        if 'sport' not in value.lower():
            raise serializers.ValidationError("Name does not contain sport.")
        return value
