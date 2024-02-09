from django import forms
from testapp.models import Comments, Blog
from django.contrib.auth.models import User
class SignUp(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', "password", "email", "first_name", "last_name"]
class EmailForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('name', 'email', 'body')

class AddPost(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"