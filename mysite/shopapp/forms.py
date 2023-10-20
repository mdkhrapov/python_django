from django import forms
from .models import Product, Order
from django.contrib.auth.models import Group
from django.forms import ModelForm


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=10000, decimal_places=2)
#     description = forms.CharField(
#         label="Product description",
#         widget=forms.Textarea(attrs={"rows":5, "cols":30}),
#         validators=[validators.RegexValidator(
#             regex=r"great",
#             message="Field must contain word 'great'"
#         )]
#     )

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

    images = forms.ImageField(
        widget=MultipleFileInput(),
    )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "delivery_address", "promocode", "user", "products"

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["name"]