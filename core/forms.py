from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Product, Image

class ContactForm(forms.Form):
    full_name=forms.CharField(max_length=100)
    email=forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProductForm(forms.ModelForm):
    product_images = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']

    def save(self, commit=True):
        product = super(ProductForm, self).save(commit=False)
        if commit:
            product.save()
            # Save images related to the product
            for image in self.cleaned_data.get('product_images', []):
                Image.objects.create(product=product, image=image)
        return product
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter product name'})
        self.fields['description'].widget.attrs.update({'rows':'3' ,'class': 'form-control', 'placeholder': 'Enter product description'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter product price'})
        self.fields['category'].widget.attrs.update({'class': 'form-select', 'placeholder': 'Select category'})

        # Update widget attributes for multiple file input
        self.fields['product_images'].widget.attrs.update({'class': 'form-control', 'multiple': True})