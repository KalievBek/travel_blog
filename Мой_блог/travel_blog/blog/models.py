from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Название категории"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Заголовок"))
    content = models.TextField(verbose_name=_("Содержимое"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Категория"))
    author = models.CharField(max_length=100, verbose_name=_("Автор"))
    country = models.CharField(max_length=100, verbose_name=_("Страна"))
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name=_("Фото"))

    def __str__(self):
        return f"{self.title} ({self.country})"

    class Meta:
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_("Пост"))
    author = models.CharField(max_length=100, verbose_name=_("Автор"))
    text = models.TextField(verbose_name=_("Комментарий"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата добавления"))
    is_published = models.BooleanField(default=True, verbose_name=_("Опубликовано"))

    def __str__(self):
        return f"Комментарий от {self.author} к '{self.post.title}'"

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")