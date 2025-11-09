# blog/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

from .models import Category, Post, Comment

User = get_user_model()


class CoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.category = Category.objects.create(name="Путешествия")
        self.post = Post.objects.create(
            title="Тестовый пост",
            content="Содержимое поста",
            category=self.category,
            author="Автор",
            country="Россия"
        )

    def test_main_pages_load(self):
        """Тест загрузки основных страниц"""
        self.assertEqual(self.client.get(reverse('index')).status_code, 200)
        self.assertEqual(self.client.get(reverse('post_detail', args=[self.post.id])).status_code, 200)

    def test_comment_creation(self):
        """Тест создания комментария"""
        # Тестируем анонимного пользователя (проще)
        self.client.post(reverse('post_detail', args=[self.post.id]), {
            'author': 'Тестовый автор',
            'text': 'Тестовый комментарий'
        })

        self.assertTrue(Comment.objects.filter(text='Тестовый комментарий').exists())

    def test_user_auth(self):
        """Тест авторизации пользователя"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_email_sending(self):
        """Тест отправки email"""
        comment = Comment.objects.create(
            post=self.post,
            author="Тест",
            text="Комментарий для email"
        )

        from .views import send_comment_notification
        mail.outbox = []
        send_comment_notification(comment)

        self.assertEqual(len(mail.outbox), 1)