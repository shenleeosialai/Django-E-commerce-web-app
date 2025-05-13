from django import forms


SIZE_CHOICES = [
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    ('XXL', '2X Large'),
]

SHOE_SIZE_CHOICES = [(str(i), str(i)) for i in range(35, 48)]

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    size = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        size_value = kwargs.pop('size_value', None)  # Pre-fill size if passed
        super().__init__(*args, **kwargs)
        if product:
            if product.has_sizes:
                self.fields['size'].choices = SIZE_CHOICES
                self.fields['size'].required = True
            elif product.has_shoe_sizes:
                self.fields['size'].choices = SHOE_SIZE_CHOICES
                self.fields['size'].required = True
            else:
                self.fields.pop('size')

        if size_value:
            self.initial['size'] = size_value
