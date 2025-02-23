from django import forms
from posts.models import Category, Tag


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


class SearchForm(forms.Form):
    search = forms.CharField(required=False ,max_length=100, widget=forms.TextInput(attrs={"placeholder": "Search"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="All", required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    orderings = (
        ("title", "По заголовку"), # ascending - по возрастанию
        ("-title", "По заголовку в обратном порядке"), # descending - по убыванию
        ("rate", "По рейтингу"),
        ("-rate", "По рейтингу в обратном порядке"),
        ("created_at", "По дате создания"),
        ("-created_at", "По дате создания в обратном порядке"),
    )

    ordering = forms.ChoiceField(choices=orderings, widget=forms.Select(attrs={"class": "form-select"}))