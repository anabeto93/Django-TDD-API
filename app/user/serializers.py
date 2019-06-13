from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    '''Serializer for the User object.'''

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def create(self, validated_data):
        '''Create a new user with encrypted password and return it.'''

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        '''Update a User, setting the password correctly and return it.'''
        password = validated_data.pop('password', None)  # default None
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            # if save() here, then no update if password is not passed
        user.save()  # will work regardless if password was passed

        return user


class AuthTokenSerializer(serializers.Serializer):
    '''Serializer for the User authentication object'''
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        '''Validate and authenticate the User.'''
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email, password=password
        )

        if not user:
            msg = _('These credentials do not match our records.')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
