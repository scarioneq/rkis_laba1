from django.db import models
from users.models import CustomUser
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description_question_long = models.TextField(verbose_name='Полное описание')
    description_question_short = models.CharField(max_length=300, verbose_name='Краткое описание')
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Изображение')
    time_of_life_minutes = models.PositiveIntegerField(
        default=1440,
        verbose_name='Время жизни опроса (в минутах)',
        help_text='Сколько минут опрос будет активен'
    )
    user_created = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Создатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    @property
    def time_of_life(self):
        return self.created_at + timezone.timedelta(minutes=self.time_of_life_minutes)

    def is_active(self):
        return self.time_of_life > timezone.now()

    def time_remaining(self):
        remaining = self.time_of_life - timezone.now()
        if remaining.total_seconds() <= 0:
            return "Истек"

        days = remaining.days
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60

        if days > 0:
            return f"{days} дн. {hours} ч."
        elif hours > 0:
            return f"{hours} ч. {minutes} мин."
        else:
            return f"{minutes} мин."

    def __str__(self):
        return self.title


class Option(models.Model):
    description = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"