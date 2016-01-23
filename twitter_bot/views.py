"""
    codeauthor:: Noel Wilson <jwnwilson@hotmail.co.uk>
    Date: 22/01/2016

    Main views for the twitter box
"""
from django.shortcuts import redirect, render


def home(request):
    """
    Index page to test development on docker
    :param request:
    :return:
    """
    ctx = {}
    return render(request, "index.html", ctx)