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
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Available Students"
    )

    class Meta:
        model = Teacher
        fields = ['students']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['students'].label_from_instance = lambda obj: f"{obj.get_full_name()} ({obj.user.email})"
        
        if self.instance.pk:
            self.fields['students'].queryset = Student.objects.exclude(
                id__in=self.instance.students.values_list('id', flat=True)
            )
