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
    threads = Thread.objects.filter(forum_id=forum_id).order_by('-time_posted')

    return render(request, 'pyforum/forum_detail.html', {'forum': forum,
                                                         'threads': threads})

def thread_detail(request, thread_id):
    """
    Return all posts within a given thread
    """
    thread = get_object_or_404(Thread, pk=thread_id)
    forum = Forum.objects.get(id=thread.forum_id)
    posts = Post.objects.filter(thread_id=thread_id).order_by('time_posted')

    return render(request, 'pyforum/thread_detail.html', {'forum': forum,
                                                          'thread': thread,
                                                          'posts': posts})

def user_detail(request, user_id):
    """
    Display several pieces of information about a given user
    """
    user = get_object_or_404(User, pk=user_id)

    return render(request, 'pyforum/user_detail.html', {'user': user})
