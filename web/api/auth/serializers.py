from allauth.account.adapter import get_adapter
from allauth.utils import email_address_exists
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from api.public.company.serializers import CompanySerializer
from api.public.reference.serializers import UserAddressSerializer
from reference.models import Address


User = get_user_model()


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Сериалайзер возвращает профиль пользователя
    """

    address = UserAddressSerializer(label='Адрес', required=False)
    company = CompanySerializer(label='Компания', read_only=True)

    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name', 'phone', 'address', 'company')
        read_only_fields = ('email',)

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)

        if address_data:
            if instance.address:
                Address.objects.filter(id=instance.address.id).update(**address_data)
            else:
                address = Address.objects.create(**address_data)
                validated_data.update({'address': address})

            instance.refresh_from_db()

        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    address = UserAddressSerializer(label='Адрес')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'address')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):

        return {
            'email': self.validated_data['email'],
            'first_name': self.validated_data['first_name'],
            'last_name': self.validated_data['last_name'],
        }

    def save(self, request):

        cleaned_data = self.get_cleaned_data()
        address = Address.objects.create(**self.validated_data['address'])

        user = User(**cleaned_data, address=address)
        user.set_password(self.validated_data['password1'])
        user.save()

        return user
