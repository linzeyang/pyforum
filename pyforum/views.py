# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

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

def compose(request, forum_id):
    """
    Write a new thread
    """
    get_object_or_404(Forum, pk=forum_id)

    return render(request, 'pyforum/compose.html', {'forum_id': forum_id})

def save_post(request):
    """
    Try to save a new post/thread into database
    """
    title = request.POST['title']
    forum_id = request.POST['forum_id']
    user_id = request.POST['user_id']
    content = request.POST['content']
    if request.POST.has_key('pinned'):
        pinned = True
    else:
        pinned = False
    if request.POST.has_key('highlighted'):
        highlighted = True
    else:
        highlighted = False

    forum = get_object_or_404(Forum, pk=forum_id)
    user = get_object_or_404(User, pk=user_id)

    new_thread = Thread(title=title, forum=forum, pinned=pinned, highlighted=highlighted)
    new_thread.save()

    new_post = Post(title=title, thread=new_thread, user=user, content=content)
    new_post.save()

    return HttpResponseRedirect(reverse('pyforum:forum_detail', args=(forum_id,)))

def thread_detail(request, thread_id):
    """
    Return all posts within a given thread
    """
    thread = get_object_or_404(Thread, pk=thread_id)

    return render(request, 'pyforum/thread_detail.html', {'thread': thread})

def user_detail(request, user_id):
    """
    Display several pieces of information about a given user
    """
    user = get_object_or_404(User, pk=user_id)

    return render(request, 'pyforum/user_detail.html', {'user': user})
