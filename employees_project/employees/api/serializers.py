from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from employees.models import Employee, Position
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class PositionSerializer(serializers.ModelSerializer):
    """
    Serializer class for models.Position representation
    """
    class Meta:
        model = Position
        fields = ('title',)


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer class for models.Employee representation
    """
    chief = serializers.SlugRelatedField(slug_field="email", read_only=True)
    position = serializers.SlugRelatedField(slug_field="title", read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'email', 'first_name',
                  'last_name', 'patronymic', 'position', 'employment_date',
                  'salary', 'total_paid', 'chief', 'level', 'groups')


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer class for models.Employee register
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Employee.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Employee
        fields = ('email', 'password', 'confirm_password', 'first_name',
                  'last_name', 'patronymic', 'position', 'employment_date',
                  'salary', 'total_paid', 'chief', 'level', 'groups')

    def create(self, validated_data):
        if validated_data.get('chief') is None:
            chief = None
            level = Employee.FIRST_LEVEL
        else:
            chief = validated_data.get('chief')
            chief_level = Employee.check_possibility_of_having_subordinates(chief)
            if chief_level is None:
                raise serializers.ValidationError({'chief': 'This employee cannot have subordinates'})
            level = chief_level + 1

        validated_data.pop('confirm_password')
        user = Employee.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'].capitalize(),
            last_name=validated_data['last_name'].capitalize(),
            patronymic=validated_data['patronymic'].capitalize(),
            position=validated_data.get('position'),
            employment_date=validated_data.get('employment_date'),
            salary=validated_data['salary'],
            total_paid=validated_data['total_paid'],
            chief=chief,
            level=level
        )
        user.is_active = True
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer class for user log-in
    """


class LogoutSerializer(serializers.Serializer):
    """
    Serializer class for user log-out
    """
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as error:
            self.fail('bad_token')
