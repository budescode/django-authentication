import random
from rest_framework import serializers
from django.contrib.auth import get_user_model
from acc_users.models import ResetPasswordCode
User = get_user_model()
from django.contrib.auth import authenticate
from django.core.mail import send_mail

#the serializer to create a user
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phonenumber = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    class Meta:
        model = get_user_model() 
        fields = ['first_name', 'last_name', 'email', 'id', 'password', 'phonenumber', 'username']
        read_only_fields = ['id']

    def validate(self, data):
        email = data["email"]
        username = data["username"]
        phonenumber = data["phonenumber"]
        if not "email" in data and not "username" in data:
            raise serializers.ValidationError("Enter Username Or Email")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email Already Exist")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username Already Exist")
        if User.objects.filter(phonenumber=phonenumber).exists():
            raise serializers.ValidationError("Phonenumber Already Exist")
        return data

    def create(self, data):
        password = data['password']      
        user = User.objects.create(**data)      
        user.set_password(password)
        user.save()
        return user
        
#the serializer to login a user
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data['username']
        password = data['password']        
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid Login details')
        elif not user.is_active:
            raise serializers.ValidationError('User is disabled.')
        return data

class SendResetPasswordCodeSerializer(serializers.ModelSerializer): 
    #When a user wants to reset password, the code is saved in the model and send to their email
    class Meta:
        model = ResetPasswordCode
        exclude = ["resetcode"]

    def validate(self, data):
        email = data["email"]
        qs = User.objects.filter(email=email)
        if not qs.exists():
            raise serializers.ValidationError("Email Does Not Exist")
        return data

    def create(self, data):             
        qs = ResetPasswordCode.objects.create(**data)
        email = data["email"]           
        resetcode = str(random.randint(1111, 9999))
        qs = ResetPasswordCode.objects.filter(email=email)
        if qs.exists():
            for i in qs:
                i.delete()
        qs = ResetPasswordCode.objects.create(email=email, resetcode=resetcode)           

        send_mail(
            "Reset Password",
            f'Here is the OTP to reset your password {resetcode}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return qs


class ResetPasswordSerializer(serializers.Serializer):
    resetcode = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        resetcode = data["resetcode"]
        email = data["email"]
        qs = ResetPasswordCode.objects.filter(resetcode=resetcode, email=email)
        if not qs.exists():
            raise serializers.ValidationError("Invalid Email Or ResetCode")
        return data

    def create(self, data):
        password = data["password"]
        resetcode = data["resetcode"]
        qs = ResetPasswordCode.objects.get(resetcode=resetcode)
        qs1 = User.objects.get(email=qs.email)
        qs1.set_password(password)
        qs1.save()
        qs.delete()
        return qs1







# class ResetPinCodeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ResetPinCode
#         exclude = ["resetcode"]

#     def validate(self, data):
#         email = data["email"]
#         qs = User.objects.filter(email=email)
#         if not qs.exists():
#             raise serializers.ValidationError("Email Does Not Exist")
#         return data


# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(required=True)

#     def validate(self, data):
#         email = data["email"]
#         if not "email" in data and not "username" in data:
#             raise serializers.ValidationError("Enter Username Or Email")
#         return data


