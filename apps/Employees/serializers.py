from rest_framework import serializers
from .models import CustomUser, History
from apps.Locations.models import Location
from apps.Locations.serializers import LocationSerializer
import os
import face_recognition
from PIL import Image, ImageDraw
import pickle
import cv2
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


# class ImageUsersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImageUsers
#         fields = ['id', 'image_user']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'id', 'date_joined', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        print('YA UPDATE')
        return super(UserSerializer, self).update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})
    repeat_password = serializers.CharField(write_only=True,
                                            style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'repeat_password',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        repeat_password = validated_data['repeat_password']
        if password != repeat_password:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match'})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class EmployeeSerializer(serializers.ModelSerializer):
    # image = ImageUsersSerializer(many=True, read_only=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'dataset', 'date_joined', 'image']

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        face_img = face_recognition.load_image_file(f"media/photo/{validated_data['image']}")
        dataset = face_recognition.face_encodings(face_img)[0]
        user.dataset = dataset
        user.save()
        return user


class HistorySerializer(serializers.ModelSerializer):
    # people = EmployeeSerializer(many=False)
    # location = LocationSerializer(many=False)

    class Meta:
        model = History
        fields = ['people', 'id', 'location', 'entry_date', 'release_date', 'image']


    # def create(self, validated_data):
    #     images_data = validated_data.pop('location')
    #     album = History.objects.create(**validated_data)
    #     for image_data in images_data:
    #         Location.objects.create(album=album, *image_data)
    #     for image_data in images_data:
    #         CustomUser.objects.create(album=album, *image_data)
    #     return album

