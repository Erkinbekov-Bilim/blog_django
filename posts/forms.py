from django import forms


class PostCreateForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(max_length=1000)
    image = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")

        if (title and content) and (title.lower() == content.lower()):
            raise forms.ValidationError("Title and content must be different")


    def clean_title(self):
        title = self.cleaned_data.get("title")

        if title and title.lower() == "title":
            raise forms.ValidationError("'title' is not a valid title")
        return title
