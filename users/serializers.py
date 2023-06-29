from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="username already taken."
            )
        ]
    )
    email = serializers.EmailField(
        max_length=127,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="email already registered."
            )
        ],
    )
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    birthdate = serializers.DateField(allow_null=True, required=False)
    is_employee = serializers.BooleanField(required=False, default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data: dict) -> User:

        if validated_data["is_employee"]:
            return User.objects.create_superuser(**validated_data)
        else:
            return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data) -> User:

        for key, value in validated_data.items():
            setattr(instance, key, value)

        new_password = validated_data.get('password')
        if new_password:
            instance.password = make_password(new_password)

        instance.save()

        return instance
