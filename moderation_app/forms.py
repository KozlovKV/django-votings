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
    comment = forms.CharField(label='Комментарий к решению (необязательно)',
                              widget=forms.Textarea(attrs={
                                    'placeholder': 'Комментарий к решению (необязательно)',
                                    'class': 'input wide',
                                }))
    reset_votes = forms.BooleanField(required=False,
                                     label='Обнулить голоса (только при одобрении)')


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
            'theme': forms.Select(attrs={
                'placeholder': 'Содержание жалобы (подробное описание значительно повышает шанс на адекватный ответ)',
                'class': 'input wide',
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Содержание жалобы (подробное описание значительно повышает шанс на адекватный ответ)',
                'class': 'input wide',
            }),
            'author': forms.TextInput(attrs={
                'type': 'hidden',
                'id': 'author',
            }),
        }
