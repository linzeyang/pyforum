# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from pyforum.models import Forum, Thread, Post, User


def forum_list(request):
    """
    """
    pass

def forum_detail(request, forum_id):
    """
    """
    pass

def thread_detail(request, thread_id):
    """
    """
    pass

def user_detail(request, user_id):
    """
    """
    pass
