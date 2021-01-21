from django import forms

from moderation_app.models import Reports


class CommentForm(forms.Form):
    comment = forms.CharField(
        label='Комментарий',
        widget=forms.Textarea(attrs={
            'placeholder': 'Напишите комментарий',
            'class': 'input wide',
        }))


class EditRequestForm(forms.Form):
    description = forms.CharField(label='Комментарий к решению', widget=forms.Textarea(attrs={
        'placeholder': 'Комментарий к решению',
        'class': 'input',
    }))
    reset_votes = forms.BooleanField(required=False, label='Обнулить ли голоса', widget=forms.NullBooleanSelect(attrs={
        'class': 'input'
    }))


class ModeledReportCreateForm(forms.ModelForm):
    class Meta:
        model = Reports
        fields = [
            'Author', 'Theme', 'Content',
        ]
        labels = {
            'Theme': 'Тема жалобы',
            'Content': 'Содержание жалобы (подробное описание значительно повышает шанс на адекватный ответ)',
        }
        widgets = {
            'Theme': forms.RadioSelect,
            'Content': forms.Textarea(attrs={
                'style': 'width: 95%',
            }),
            'Author': forms.TextInput(attrs={
                'type': 'hidden',
                'id': 'author',
            }),
        }
