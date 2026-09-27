from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Reminder, MedicineLog

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password']

    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('An account with this email already exists')
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'].strip(),
            password=validated_data['password'],
            phone=validated_data.get('phone', '').strip() or None,
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ReminderSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'])

    class Meta:
        model = Reminder
        fields = [
            'id', 'medicine_name', 'dosage', 'time', 'frequency',
            'alarm_sound', 'last_taken_date', 'created_at',
        ]
        read_only_fields = ['id', 'last_taken_date', 'created_at']


class MedicineLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineLog
        fields = ['id', 'medicine_name', 'dosage', 'taken_at']
        read_only_fields = fields
