from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Кастомная моделька юзера
# В теории можно использовать встроенную, но пару полей там будет не хватать и придётся их кринжово соединять.
# Потому наследуем модель от AbstractUser - ЧТО ОЧЕНЬ ВАЖНО. 
class CustomUser(AbstractUser):
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    # почта и юзернейм наследуется от AbstractUser

    # Мета, str и функции нужны для всяких разных выводов.
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        """Возвращает ФИО в формате: Фамилия Имя Отчество"""
        parts = [self.last_name, self.first_name]
        if self.patronymic:
            parts.append(self.patronymic)
        return ' '.join(filter(None, parts))

    def get_short_name(self):
        """Возвращает Имя Фамилия"""
        return f'{self.first_name} {self.last_name}'.strip()


class Application(models.Model):
    """Заявки на обучение"""
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Идёт обучение'),
        ('completed', 'Обучение завершено'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Наличными'),
        ('phone_transfer', 'Перевод по номеру телефона'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications', # - с related name можно писать user.applications.all() для вывода всех заявок юзера.
        verbose_name='Пользователь'
    )
    course_name = models.CharField('Название курса', max_length=300)
    desired_start_date = models.DateField('Желаемая дата начала')
    # В choices кидаем массив которые указывали выше с описанием всяких разных значений для дальнейшего вывода во фронте. 
    payment_method = models.CharField(
        'Способ оплаты',
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='cash'
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.course_name} - {self.user.get_full_name()} ({self.get_status_display()})'


class Review(models.Model):
    """Отзывы о качестве образовательных услуг"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Заявка'
    )
    rating = models.PositiveSmallIntegerField('Оценка (1-5)')
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Дата отзыва', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ['user', 'application']
        # Минус чтобы сначала были новые.
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.user.get_full_name()} на {self.application.course_name}'