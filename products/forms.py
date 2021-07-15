from django import forms


class AddProductForm(forms.Form):
    """
    Adds products. Used with add product view and template
    """
    amazon_asin = forms.CharField(max_length=12)
    ebay_url = forms.CharField(max_length=200)


class ContactUsForm(forms.Form):
    """
    Form for contact us.
    """
    email = forms. EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
