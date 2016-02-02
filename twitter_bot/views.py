"""
    codeauthor:: Noel Wilson <jwnwilson@hotmail.co.uk>
    Date: 22/01/2016

    Main views for the twitter box
"""
import json
import logging
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from models import HashTagBattle
from twitter_bot.common import get_hash_tag_most_typos

logger = logging.getLogger(__name__)

def home(request):
    """
    Index page to test development on docker
    :param request:
    :return:
    """
    ctx = {}
    return render(request, "index.html", ctx)


@csrf_exempt
def hash_tag_battle(request):
    """
    Simple view to get the hash tag battle by id then search for hash tags and
    compare typos in all the tweets
    :param request:
    :return:
    """
    if request.method == "POST":
        battle_id = request.POST.get("id")
        if battle_id:
            try:
                hash_tag_battle = HashTagBattle.objects.get(id=battle_id)
            except ObjectDoesNotExist:
                return HttpResponse("No hash tag battle found with id: %s" % battle_id, status=500)

            hash_tag, hash_tag_data = get_hash_tag_most_typos(hash_tag_battle)
            return_json = { 'winner': None, 'typo_data': {}}

            if hash_tag:
                return_json['winner'] = hash_tag.hash_tag

            for hash_tag in hash_tag_data:
                return_json['typo_data'][hash_tag.hash_tag] = hash_tag_data[hash_tag]

            return_json['start_date_time'] = str(hash_tag_battle.start_date_time)
            return_json['end_date_time'] = str(hash_tag_battle.end_date_time)

            return HttpResponse(json.dumps(return_json), status=200, content_type="application/json")
        else:
            return HttpResponse("No hash tag battle found with id: %s" % battle_id, status=500)

    else:
        return HttpResponse("Expected POST request", status= 500)
