from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'phone_number', 'first_name', 'last_name')
        read_only_fields = ('id',)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'role', 'first_name', 'last_name', 'phone_number')

    def create(self, validated_data):
        role = validated_data.get('role', User.Role.PATIENT)
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            role=role,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', '')
        )
        
        # Create profile based on role
        from hospital.models import Doctor, Patient
        if role == 'DOCTOR':
            Doctor.objects.create(
                user=user, 
                specialization='General Medicine', 
                consultation_fee=500
            )
        elif role == 'PATIENT':
            from datetime import date
            Patient.objects.create(
                user=user, 
                date_of_birth=date(1990, 1, 1), 
                address='Please update your address'
            )
            
        return user
