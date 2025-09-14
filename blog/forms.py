from django import forms 

#The EmailPostForm inherits from the Form class.
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required = False,
        widget = forms.Textarea,
    )