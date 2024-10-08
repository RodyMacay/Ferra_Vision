from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from ..models import User

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza los campos aquí si es necesario
        self.fields['username'].widget.attrs.update({
            'class': 'inline-block w-full rounded-full bg-white p-2.5 leading-none text-black placeholder-indigo-900 shadow placeholder:opacity-30',
            'placeholder': 'mail@user.com'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'inline-block w-full rounded-full bg-white p-2.5 leading-none text-black placeholder-indigo-900 shadow',
            'placeholder': 'Password'
        })
        

# class CustomUserCreationForm(forms.Form):
#     username = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
#     )
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
#     )
#     cedula = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cédula o DNI'})
#     )
#     image = forms.ImageField(
#         widget=forms.FileInput(attrs={'class': 'form-control'}),
#         required=False
#     )
#     phone = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
#         required=False
#     )
#     password1 = forms.CharField(
#         strip=False,
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     password2 = forms.CharField(
#         strip=False,
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
#     )

#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(_("Las contraseñas no coinciden."))
#         return password2

#     def save(self, commit=True):
#         # Crea un nuevo usuario utilizando los datos del formulario
#         username = self.cleaned_data['username']
#         email = self.cleaned_data['email']
#         cedula = self.cleaned_data['cedula']
#         image = self.cleaned_data.get('image')
#         phone = self.cleaned_data.get('phone')
#         password = self.cleaned_data['password1']
#         user = User.objects.create_user(username=username, email=email, cedula=cedula, image=image, phone=phone, password=password)
#         return user

# class CustomUserCreationForm(forms.ModelForm):

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('username', 'email', 'password', 'cedula', 'image', 'phone')
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Personalizar los campos de usuario y contraseña
#         self.fields['username'].widget.attrs.update({
#             'class': 'inline-block w-full rounded-full bg-white p-2.5 leading-none text-black placeholder-indigo-900 shadow placeholder:opacity-30',
#             'placeholder': 'Nombre de usuario'
#         })
#         self.fields['password'].widget.attrs.update({
#             'class': 'inline-block w-full rounded-full bg-white p-2.5 leading-none text-black placeholder-indigo-900 shadow placeholder:opacity-30',
#             'placeholder': 'Contraseña'
#         })
#         # Personalizar otros campos
#         self.fields['cedula'].widget.attrs.update({
#             'class': 'inline-block w-full rounded-full bg-white p-2.5 leading-none text-black placeholder-indigo-900 shadow placeholder:opacity-30',
#             'placeholder': 'Cédula o DNI'
#         })
#         self.fields['image'].widget.attrs.update({
#             'class': 'inline-block w-full rounded-full bg-white p-2.5 leading-none text-black placeholder-indigo-900 shadow placeholder:opacity-30',
#             'placeholder': 'Archivo de imagen'
#         })
#         self.fields['phone'].widget.attrs.update({
#             'class': 'inline-block w-full rounded-full bg-white p-2.5 leading-none text-black placeholder-indigo-900 shadow placeholder:opacity-30',
#             'placeholder': 'Teléfono'
#         })
        
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'inline-block w-full rounded-full bg-white p-2.5 leading-none text-black placeholder-indigo-900 shadow', 'placeholder': 'Contraseña'}),
        help_text=None
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'inline-block w-full rounded-full bg-white p-2.5 leading-none text-black placeholder-indigo-900 shadow', 'placeholder': 'Confirmar contraseña'}),
        help_text=None
    )
    
    username = forms.CharField(
        help_text=None
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'cedula', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar otros campos
        for field_name in ['username', 'email', 'cedula', 'phone']:
            self.fields[field_name].widget.attrs.update({
                'class': 'inline-block w-full rounded-full bg-white p-2 shadow text-xs text-black placeholder-indigo-900 placeholder-opacity-30',
                'placeholder': f'{self.fields[field_name].label}'
            })
            
        # self.fields['image'].widget.attrs.update({
        #     'class': 'inline-block w-full p-2 shadow text-xs bg-white rounded-full',
        #     'placeholder': 'Seleccione un archivo',
        #     'accept': 'image/*',  # Limitar a archivos de imagen
        # })

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user