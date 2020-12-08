
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from blog.models import Post

class BlogForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('id','created_at','like_count','comments','image')

class CommentForm(forms.ModelForm):

	class Mets:
		model=Post
		exclude=('id','created_at','like_count','title','body')
class LoginForm(forms.Form):

    username = forms.CharField(initial='', help_text='Enter username')
    password = forms.CharField(max_length=50,widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'password')
		
class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), )
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	
	
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

	def __init__(self, *args, **kwargs):
	    super(SignUpForm, self).__init__(*args, **kwargs)

	    self.fields['username'].widget.attrs['class'] = 'form-control'
	    self.fields['username'].widget.attrs['placeholder'] = 'User Name'
	    self.fields['username'].label = ''
	    self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

	    self.fields['password1'].widget.attrs['class'] = 'form-control'
	    self.fields['password1'].widget.attrs['placeholder'] = 'Password'
	    self.fields['password1'].label = ''
	    self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

	    self.fields['password2'].widget.attrs['class'] = 'form-control'
	    self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
	    self.fields['password2'].label = ''
	    self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

       
class PasswordResetForm(forms.Form):
    current_password = forms.CharField(max_length=50)
    new_password = forms.CharField(max_length=50)
    confirm_password = forms.CharField(max_length=50)

    def clean(self):
        if not self.user.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError('Current password is not correct')

        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError('Password do not match')
        return self.cleaned_data

