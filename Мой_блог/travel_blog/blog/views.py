from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page, never_cache
from django.conf import settings
from .models import Post, Comment
from .forms import CommentForm, CustomUserCreationForm, CustomAuthenticationForm

@never_cache
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/index.html', {'posts': posts})

@cache_page(60 * 2)
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post, is_published=True).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST, user=request.user)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()

            send_comment_notification(new_comment)
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm(user=request.user)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

def send_comment_notification(comment):
    """Отправка уведомления о новом комментарии"""
    subject = _('Новый комментарий к посту "%s"') % comment.post.title

    message = _("""
    Новый комментарий от %(author)s:

    %(text)s

    Пост: %(post_title)s
    Дата: %(date)s

    Ссылка на пост: http://localhost:8000/post/%(post_id)s/
    """) % {
        'author': comment.author,
        'text': comment.text,
        'post_title': comment.post.title,
        'date': comment.created_at.strftime("%d.%m.%Y %H:%M"),
        'post_id': comment.post.id
    }

    recipient_list = [settings.ADMIN_EMAIL]

    try:
        send_mail(
            subject,
            message.strip(),
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        print("Email отправлен успешно на:", settings.ADMIN_EMAIL)
    except Exception as e:
        print(f"Ошибка отправки email: {e}")

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@never_cache
def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

@never_cache
def custom_logout(request):
    """Функция выхода из системы"""
    logout(request)
    # Очищаем сессию для надежности
    request.session.flush()
    return redirect('index')