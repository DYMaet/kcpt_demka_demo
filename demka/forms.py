from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Application, Review

User = get_user_model()

# Тут расписываем все формы которые будут вставляться в шаблон. Регистрация и авторизация наследствуют UserCreationForm и AuthenticationForm соответственно чтобы использовать уже готовые решения в джанго
# Остальные формы используют ModelForm и там уже нужно указывать модель к которой она относится, и поля этой модели.


class RegistrationForm(UserCreationForm):

    first_name = forms.CharField(
        label='Имя',
        max_length=100,

# Через виджет задаются классы и прочие аттрибуты html при преобразовании этой части формы в html.

        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'})
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов'})
    )
    patronymic = forms.CharField(
        label='Отчество',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванович (необязательно)'})
    )
    # хз требуют ли по критериям прям regex номера телефона, если что - запоминайте паттерн походу.
    # Как работает хтмлевский + питоновский regex в этом случае, краткий гайд:
    # перед строкой пишем r - воспринимается питоном как raw строка
    # затем 8 - то с чего номер начинается - 8
    # затем \( - открытие скобки в паттерне. Без скобок не примет номер и соответственно \) закрытие скобки.
    # Без слэшей \ скобки будут восприниматься как спец символ наравне с [] и {}.
    # Далее идут указания допустимых символов + их количество в виде [0-9]{3} - т.е цифры от 0 до 9 в количистве три штука на сегмент паттерна
    # Ну и сегмент паттерна это сколько цифр нужно будет пользователю прописать в скобках или между тире. 
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        min_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '8(XXX)XXX-XX-XX', 'type':'tel', 'pattern': r'8\([0-9]{3}\)[0-9]{3}-[0-9]{2}-[0-9]{2}'})
    )
    email = forms.EmailField(
        label='Эл. почта',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )
    username = forms.CharField(
        label='Логин',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте логин'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте пароль'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'patronymic', 'phone', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    """Форма авторизации"""
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логин'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ваш пароль'})
    )


class ApplicationForm(forms.ModelForm):
    """Форма создания заявки"""
    class Meta:
        model = Application
        fields = ['course_name', 'desired_start_date', 'payment_method']
        widgets = {
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Python-разработчик с нуля'
            }),
            'desired_start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'payment_method': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'course_name': 'Название курса',
            'desired_start_date': 'Желаемая дата начала обучения',
            'payment_method': 'Удобный способ оплаты',
        }


class ReviewForm(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} звезда{"ы" if 2 <= i <= 4 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Поделитесь своим мнением о качестве обучения...'
            }),
        }
        labels = {
            'rating': 'Ваша оценка',
            'comment': 'Комментарий (необязательно)',
        }


class ApplicationStatusForm(forms.ModelForm):
    """Форма изменения статуса заявки (для админа)"""
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }