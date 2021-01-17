from django import forms


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

    