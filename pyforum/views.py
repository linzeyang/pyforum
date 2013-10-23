# Create your views here.
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# from django.utils import timezone

from pyforum.models import User, Forum, Thread, Post


def forum_list(request):
    """
    Retuen all the forums in a list
    """
    forums = Forum.objects.all()

    return render(request, 'pyforum/forum_list.html', {'forums': forums})


def forum_detail(request, forum_id):
    """
    Return all threads within a given forum
    """
    forum = get_object_or_404(Forum, pk=forum_id)
    
    return render(request, 'pyforum/forum_detail.html', {'forum': forum})


def compose_thread(request, forum_id):
    """
    Write a new thread
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('pyforum:forum_list'))

    forum = get_object_or_404(Forum, pk=forum_id)

    return render(request, 'pyforum/compose.html', {'mode': 'new_thread',
                                                    'forum': forum})


def compose_post(request, thread_id):
    """
    Make a reply to a existing thread
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('pyforum:forum_list'))

    thread = get_object_or_404(Thread, pk=thread_id)

    return render(request, 'pyforum/compose.html', {'mode': 'new_post',
                                                    'thread': thread})


def edit_post(request, post_id):
    """
    Modify an existing post
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('pyforum:forum_list'))

    post = get_object_or_404(Post, pk=post_id)

    if post.user.id != request.user.id:
        thread_id = post.thread.id
        return HttpResponseRedirect(reverse('pyforum:thread_detail',
                                    args=(thread_id,)))

    return render(request, 'pyforum/compose.html', {'mode': 'edit_post',
                                                    'post': post})


def save_post(request):
    """
    Try to save a new thread/post into database
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('pyforum:forum_list'))

    mode = request.POST['mode']
    title = request.POST['title']
    content = request.POST['content']

    user_id = request.POST['user_id']
    user = get_object_or_404(User, pk=user_id)
    
    if mode == 'new_thread':
        forum_id = request.POST['forum_id']
        forum = get_object_or_404(Forum, pk=forum_id)

        pinned = 'pinned' in request.POST
        highlighted = 'highlighted' in request.POST

        new_thread = Thread(title=title, forum=forum, pinned=pinned,
                            highlighted=highlighted)
        new_thread.save()

        new_post = Post(title=title, thread=new_thread, user=user,
                        content=content)
        new_post.save()

        return HttpResponseRedirect(reverse('pyforum:forum_detail', 
                                            args=(forum_id,)))

    elif mode == 'new_post':
        thread_id = request.POST['thread_id']
        thread = get_object_or_404(Thread, pk=thread_id)

        new_post = Post(title=title, thread=thread, user=user, content=content)
        new_post.save()

        return HttpResponseRedirect(reverse('pyforum:thread_detail', 
                                            args=(thread_id,)))

    elif mode == 'edit_post':
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, pk=post_id)

        post.title = title
        post.content = content
        post.save()

        thread_id = post.thread.id

        return HttpResponseRedirect(reverse('pyforum:thread_detail',
                                            args=(thread_id,)))

    else:
        return HttpResponseRedirect(reverse('pyforum:forum_list'))


def thread_detail(request, thread_id):
    """
    Return all posts within a given thread
    """
    thread = get_object_or_404(Thread, pk=thread_id)

    thread.num_of_clicks += 1
    thread.save()

    return render(request, 'pyforum/thread_detail.html', {'thread': thread})


def user_detail(request, user_id):
    """
    Display several pieces of information about a given user
    """
    user = get_object_or_404(User, pk=user_id)

    return render(request, 'pyforum/user_detail.html', {'user': user})


def sign_up(request):
    """
    Register a new user account
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('pyforum:forum_list'))

    return render(request, 'pyforum/sign_up.html')


def save_user(request):
    """
    Try to save new user info into database
    """
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password_again = request.POST['password_again']
    signature = request.POST['signature']

    if len(username) == 0:
        return render(request, 'pyforum/sign_up.html', 
                        {'error': 'Username cannot be empty !'})

    if len(email) == 0:
        return render(request, 'pyforum/sign_up.html', 
                        {'error': 'Email address cannot be empty !'})

    if password != password_again:
        return render(request, 'pyforum/sign_up.html', 
                        {'error': 'Passwords are not identical !'})
    elif len(password) == 0:
        return render(request, 'pyforum/sign_up.html', 
                        {'error': 'Password cannot be empty !'})

    new_user = User.objects.create_user(username, email, password,
                                        signature=signature)
    new_user.save()

    return HttpResponseRedirect(reverse('pyforum:sign_in'))


def sign_in(request):
    """
    The view for user to enter credentials
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('pyforum:forum_list'))

    return render(request, 'pyforum/sign_in.html')


def auth_user(request):
    """
    Try to log in a user
    """
    username = request.POST['username']
    password = request.POST['password']

    if len(username) == 0 or len(password) == 0:
        return render(request, 'pyforum/sign_in.html', 
                        {'error': 'Username/Password cannot be empty !'})

    user = authenticate(username=username, password=password)

    if user is None:
        return render(request, 'pyforum/sign_in.html', 
                        {'error': 'Username/Password incorrect !'})

    if not user.is_active:
        return render(request, 'pyforum/sign_in.html', 
                        {'error': 'Your account is inactive !'})

    login(request, user)

    return HttpResponseRedirect(reverse('pyforum:forum_list'))


def sign_out(request):
    """
    Log out the current user
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('pyforum:forum_list'))

    logout(request)

    return HttpResponseRedirect(reverse('pyforum:forum_list'))