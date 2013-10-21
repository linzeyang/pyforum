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

def compose_thread(request, forum_id):
    """
    Write a new thread
    """
    forum = get_object_or_404(Forum, pk=forum_id)

    return render(request, 'pyforum/compose.html', {'mode': 'new_thread',
                                                    'forum': forum})

def compose_post(request, thread_id):
    """
    Make a reply to a existing thread
    """
    thread = get_object_or_404(Thread, pk=thread_id)

    return render(request, 'pyforum/compose.html', {'mode': 'new_post',
                                                    'thread': thread})

def save_post(request):
    """
    Try to save a new thread/post into database
    """
    mode = request.POST['mode']
    title = request.POST['title']
    content = request.POST['content']

    user_id = request.POST['user_id']
    user = get_object_or_404(User, pk=user_id)
    
    if mode == 'new_thread':
        forum_id = request.POST['forum_id']
        forum = get_object_or_404(Forum, pk=forum_id)

        pinned = request.POST.has_key('pinned')
        highlighted = request.POST.has_key('highlighted')

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
