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
            'Theme', 'Content',
        ]
        labels = {
            'Theme': 'Тема жалобы (на голосование или об ошибке)',
            'Content': 'Содержание жалобы',
            # 'Title': 'Заголовок',
            # 'Image': 'Картинка',
            # 'Description': 'Описание',
            # 'Type': 'Тип голосования',
            # 'Anons_can_vote': 'Разрешить голосовать анонимам',
            # 'Result_see_who': 'Кому видны результаты',
            # 'Result_see_when': 'Когда видные результаты',
            # 'End_date': 'Дата окончания (пусто - бессрочно)',
        }
        widgets = {
            'Theme': forms.RadioSelect,
            'Content': forms.Textarea(attrs={
                'style': 'width: 95%',
            })
            # 'Description': forms.Textarea(attrs={
            #     'style': 'width: 95%',
            # }),
            # 'Type': forms.RadioSelect,
            # 'Result_see_who': forms.RadioSelect,
            # 'Result_see_when': forms.RadioSelect,
            # 'End_date': forms.DateTimeInput(attrs={
            #     'type': 'datetime',
            # }),
        }
