from django import forms
from .models import Star


class StarForm(forms.ModelForm):
    """Форма для добавления знаменитости"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс form-control для всех полей по умолчанию
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'

    class Meta:
        model = Star
        fields = ['name', 'country', 'category', 'birth_date', 'death_date', 'content', 'photo']
        widgets = {
            'name': forms.TextInput(),
            'country': forms.Select(),
            'category': forms.Select(),  # Изменили на Select для ForeignKey
            'birth_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'  # Формат, который понимает браузер
            ),
            'content': forms.Textarea(attrs={'rows': 5}),
            'photo': forms.FileInput(),
            'death_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }
        labels = {
            'name': 'Имя',
            'country': 'Страна',
            'category': 'Категория',
            'birth_date': 'Дата рождения',
            'content': 'Описание',
            'death_date': 'Дата смерти (необязательно)',
            'photo': 'Фотография'
        }

    def clean_birth_date(self):
        """Валидация даты рождения"""
        birth_date = self.cleaned_data['birth_date']
        # Здесь можно добавить дополнительные проверки
        return birth_date