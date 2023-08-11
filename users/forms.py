from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

class CustomerUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", )

    # Добавляем дополнительные поля профиля
    customer_name = forms.CharField(label='Ім\'я', max_length=100)
    address = forms.CharField(label='Адреса', max_length=200)

    def save(self, commit=True):
        user = super(CustomerUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        # Сохраняем дополнительные поля профиля
        profile = CustomUser.objects.create(user=user, customer_name=self.cleaned_data['customer_name'], address=self.cleaned_data['address'])
        profile.save()

        return user
