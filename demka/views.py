from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, ApplicationForm, ReviewForm
from .models import Application, Review

"""
Краткое описание работы
1. Пользователь открывает URL.
2. Django по urls.py находит нужную view-функцию.
3. View-функция получает объект request (всё о запросе: метод, POST-данные,
   текущий пользователь, cookies, сессия).
4. View-функция делает что-то (читает/пишет БД, валидирует форму).
5. View-функция возвращает:
      - render(request, 'шаблон.html', context)  → HTML
      - redirect('имя_url')                       → перенаправление

КОНТЕКСТ (context) — это словарь, который передаётся в шаблон.
Ключи словаря = имена переменных, доступных в шаблоне.
Пример: {'form': form} → в шаблоне можно писать {{ form }}.
Для вьюх в которых заполняется форма в контекст пихаем {'form': form}, это позволяет рендерить переданную форму на странице
Для остальных - в контекст передаём всякие разные данные нужные для вывода на странице
"""

def is_admin(user):
    """Проверка, является ли пользователь админом
        По факту можно прописывать каждый раз user.is_superuser or user.is_staff. Просто экономит время
    """
    return user.is_superuser or user.is_staff


def register_view(request):
    """Страница регистрации"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    # если метод - ПОСТ, передаём в форму все данные из запроса, если валидно - получаем юзера, логиним его, редиректим на дэшборд.
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно! Добро пожаловать!')
            return redirect('dashboard')
    else:
        form = RegistrationForm()

    # Рендерим страничку, указываем нужный шаблон и нужную форму которую хотим там отображать.
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """Страница авторизации"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.get_full_name()}!')
                return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


# Приколдесный декоратор login_required - защищает эндпойнты от неавторизированных юзеров
@login_required
def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """Дашборд пользователя - просмотр своих заявок и отзывов"""
    # Тут получаем инфу из моделек с нужной фильтрацией
    # Заявки - только свои, отзывы - только свои + связь с заявкой.
    applications = Application.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user).select_related('application')

    # Проверяем, для каких заявок уже есть отзывы
    reviewed_application_ids = set(reviews.values_list('application_id', flat=True))

    # Передаём в контекст нужные данные. Далее эти данные будут использоваться в самих шаблонах.
    context = {
        'applications': applications,
        'reviews': reviews,
        'reviewed_application_ids': reviewed_application_ids,
    }
    return render(request, 'dashboard.html', context)


@login_required
def create_application_view(request):
    """Создание новой заявки"""
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно отправлена! Ожидайте рассмотрения администратором.')
            return redirect('dashboard')
    else:
        form = ApplicationForm()

    return render(request, 'create_application.html', {'form': form})


@login_required
def create_review_view(request, application_id):
    """Создание отзыва для заявки"""
    application = get_object_or_404(Application, id=application_id, user=request.user)

    # Проверяем, не оставлен ли уже отзыв
    if Review.objects.filter(user=request.user, application=application).exists():
        messages.warning(request, 'Вы уже оставили отзыв для этой заявки.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.application = application
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('dashboard')
    else:
        form = ReviewForm()

    return render(request, 'create_review.html', {'form': form, 'application': application})


@user_passes_test(is_admin)
def admin_panel_view(request):
    """Админ панель - просмотр всех заявок"""
    applications = Application.objects.select_related('user').all()

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        application = get_object_or_404(Application, id=application_id)

        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, f'Статус заявки #{application.id} изменен на "{application.get_status_display()}"')
        return redirect('admin_panel')

    context = {
        'applications': applications,
        'status_choices': Application.STATUS_CHOICES,
    }
    return render(request, 'admin_panel.html', context)