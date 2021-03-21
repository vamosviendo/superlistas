from django import forms

from listas.models import Item

ERROR_ITEM_VACIO = 'No puede haber un item vacío en la lista.'


class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('texto', )
        widgets = {
            'texto': forms.fields.TextInput(attrs={
                'placeholder': 'Ingrese una tarea',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'texto': {'required': ERROR_ITEM_VACIO}
        }