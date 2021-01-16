from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(
        label='Комментарий',
        widget=forms.Textarea(attrs={
            'placeholder': 'Напишите комментарий',
            'class': 'input wide',
        }))