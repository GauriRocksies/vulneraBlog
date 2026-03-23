"""
VulneraBlog Forms
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post, Comment, Tag


class LoginForm(forms.Form):
    """Login form using VulneraBlog user_id_code."""
    user_id_code = forms.CharField(
        label='USERID',
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your unique ID',
            'autocomplete': 'off',
            'class': 'form-input',
        })
    )
    password = forms.CharField(
        label='PASSWORD',
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'form-input',
        })
    )


class RegisterForm(UserCreationForm):
    """Registration form that creates a new VulneraBlog user."""
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'First name',
            'class': 'form-input',
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last name',
            'class': 'form-input',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-input',
        })
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Choose a username',
            'class': 'form-input',
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style the password fields
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create a password',
            'class': 'form-input',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password',
            'class': 'form-input',
        })
        self.fields['password1'].label = 'PASSWORD'
        self.fields['password2'].label = 'CONFIRM PASSWORD'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts."""
    tag_names = forms.CharField(
        label='Tags',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '#BRUTALISM #CURATION (space-separated)',
            'class': 'form-input',
        }),
        help_text='Enter tags separated by spaces, e.g. #BRUTALISM #DESIGN'
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'cover_image', 'content', 'read_time']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter your post title',
                'class': 'form-input',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your article content here...',
                'class': 'form-textarea',
                'rows': 20,
            }),
            'read_time': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 1,
                'max': 120,
            }),
            'cover_image': forms.ClearableFileInput(attrs={
                'class': 'form-file-input',
                'accept': 'image/*',
            }),
        }

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            # Process tags from the tag_names field
            tag_names_raw = self.cleaned_data.get('tag_names', '')
            if tag_names_raw:
                post.tags.clear()
                for raw_tag in tag_names_raw.split():
                    tag_name = raw_tag.lstrip('#').upper()
                    if tag_name:
                        tag, _ = Tag.objects.get_or_create(name=tag_name)
                        post.tags.add(tag)
        return post


class CommentForm(forms.ModelForm):
    """Comment submission form."""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Add to the conversation...',
                'class': 'comment-textarea',
                'rows': 3,
            }),
        }
        labels = {
            'content': '',
        }


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile information."""
    first_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email address'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'avatar', 'role', 'location', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Write something about yourself...',
                'rows': 4,
            }),
            'role': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Lead Curator & Designer',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Berlin, Germany',
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://yourwebsite.com',
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-file-input',
                'accept': 'image/*',
            }),
        }