from django import forms
from AdminDashboard.models import User, Language



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    roll = forms.ChoiceField(
        choices=[('student', 'Student'), ('mentor', 'Mentor')]
    )

    language = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date'   # 👈 calendar picker
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'name', 'address', 'email', 'phone', 'dob',
            'username', 'password', 'roll', 'language'
        ]
