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
    comment = forms.CharField(required=False,
                              label='Комментарий к решению (необязательно)',
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
            'author', 'element', 'theme', 'content',
        ]
        labels = {
            'theme': 'Тема жалобы',
            'content': 'Содержание жалобы',
            'element': 'Объект жалобы, для заполнения нужно нажимать на кнопку жалобы около объектов',
        }
        widgets = {
            'theme': forms.Select(attrs={
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
            'element': forms.NumberInput(attrs={
                'placeholder': 'Пусто',
                'readonly': True,
                'disabled': True,
                'class': 'input wide',
                'id': 'element',
            }),
        }
