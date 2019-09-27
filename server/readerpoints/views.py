# pylint: disable=missing-docstring
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import get_cards, acivate_card

CARD_DATA = {'id':"", 'type':"", 'purchased_date':"", 'activated_date':"", 'expired_date':"",
             'is_deleted':"", 'is_active':"", 'borrowing_limt':0, 'borrowing':[]}
BORROWING_DATA = {'title':"", 'borrow_date':"", 'return_date':""}

@login_required
def pointscard_page_view(request):
    data = ""
    if request.method == 'GET':
        data = get_cards(request.userid)
    if request.method == 'POST' and "update" in request.POST:
        pass
    if request.method == 'POST' and "activate" in request.POST:
        acivate_card(request.POST.get('cardid', None))
    return render(request, 'readerpoints/mycards.html', {'data':data})
