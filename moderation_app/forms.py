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
            'author', 'theme', 'content',
        ]
        labels = {
            'theme': 'Тема жалобы',
            'content': 'Содержание жалобы',
        }
        widgets = {
            'theme': forms.RadioSelect,
            'content': forms.Textarea(attrs={
                'placeholder': 'Содержание жалобы (подробное описание значительно повышает шанс на адекватный ответ)',
                'style': 'width: 95%',
            }),
            'author': forms.TextInput(attrs={
                'type': 'hidden',
                'id': 'author',
            }),
        }
