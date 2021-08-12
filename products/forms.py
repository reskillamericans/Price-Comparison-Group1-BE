from django import forms


class AddProductForm(forms.Form):
    """
    Adds products. Used with add product view and template
    """
    amazon_asin = forms.CharField(max_length=12,
                                  widget=forms.TextInput(attrs={
                                      'autofocus': 'True',
                                      'placeholder': 'Bxxxxxxxxx'
                                      }))
    ebay_url = forms.CharField(max_length=200,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'https://www.ebay.com/itm/xxxxxxxxxxxx'
                                   }))


class ContactUsForm(forms.Form):
    """
    Form for contact us.
    """
    email = forms. EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
