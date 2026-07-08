from django import forms

FIELD_CLASS = 'contacto-field-input'


class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        max_length=120,
        widget=forms.TextInput(attrs={'placeholder': 'Tu nombre', 'class': FIELD_CLASS}),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'tu@email.com', 'class': FIELD_CLASS}),
    )
    mensaje = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={
            'placeholder': 'Cuéntame sobre tu proyecto…',
            'rows': 5,
            'class': FIELD_CLASS,
        }),
    )
