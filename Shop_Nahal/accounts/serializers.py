from rest_framework import serializers
from .models import User


class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number','email','full_name','password')

