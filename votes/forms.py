from django import forms
from .models import Post, Option, Vote


class PostForm(forms.ModelForm):
    options = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Вариант 1, Вариант 2, Вариант 3'}),
        label='Варианты ответов (через запятую)',
        help_text='Введите варианты ответов, разделяя их запятыми'
    )

    class Meta:
        model = Post
        fields = ['title', 'description_question_short', 'description_question_long', 'image', 'time_of_life_minutes']
        labels = {
            'title': 'Заголовок опроса',
            'description_question_short': 'Краткое описание',
            'description_question_long': 'Полное описание',
            'image': 'Изображение (необязательно)',
            'time_of_life_minutes': 'Время жизни опроса (в минутах)',
        }
        help_texts = {
            'time_of_life_minutes': 'Например: 60 (1 час), 1440 (1 день), 10080 (1 неделя)',
        }
        widgets = {
            'time_of_life_minutes': forms.NumberInput(attrs={'min': 1, 'value': 1440}),
        }


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['option']
        labels = {
            'option': 'Вариант ответа',
        }

    def __init__(self, *args, **kwargs):
        post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
        if post:
            self.fields['option'].queryset = Option.objects.filter(post=post)
            self.fields['option'].empty_label = None