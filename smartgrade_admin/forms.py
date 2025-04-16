from django import forms
from accounts.models import User, Teacher, Student  

class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'gender', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        user.is_staff = False
        if commit:
            user.save()
        return user
    

class TeacherStudentUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=User.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'gender']  
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and hasattr(self.instance, 'gender'):
            self.initial['gender'] = self.instance.gender


class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'gender', 'password']

        def save(self, commit=True):
            user = super().save(commit=False)
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.is_staff = False
            if commit:
                user.save()
            return user

# class AssignStudentForm(forms.ModelForm):
#     students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), widget=forms.CheckboxSelectMultiple)

#     class Meta:
#         model = Teacher
#         fields = ['students']


class AssignStudentForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Teacher
        fields = ['students']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['students'].queryset = Student.objects.filter(is_current=True)

        self.fields['students'].label_from_instance = lambda obj: obj.get_full_name()
        