from django.contrib.auth.forms import UserCreationForm


class CustomerUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", )
