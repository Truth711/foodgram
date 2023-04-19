from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Введите адрес электронной почты',
        unique=True,
    )
    role = models.CharField(choices=ROLES,
                            default=USER,
                            max_length=25,
                            blank=True)
    first_name = models.CharField(
        verbose_name='Имя',
        help_text='Введите имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        help_text='Введите фамилию',
        max_length=150,
    )

    class Meta:
        ordering = ('id', )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser


class Subscribe(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Подписка',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique-user-author'
            ),
        ]
