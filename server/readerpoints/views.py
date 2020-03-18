# pylint: disable=missing-docstring
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import get_cards, activate_card

CARD_DATA = {'id':"", 'type':"", 'purchased_date':"", 'activated_date':"", 'expired_date':"",
             'is_deleted':"", 'is_active':"", 'borrowing_limt':0, 'borrowing':[]}
BORROWING_DATA = {'title':"", 'borrow_date':"", 'return_date':""}

@login_required
def pointscard_view(request):
    data = ""
    if request.method == 'GET':
        data = get_cards(request.userid)
    if request.method == 'POST' and "update" in request.POST:
        pass
    if request.method == 'POST' and "activate" in request.POST:
        activate_card(request.POST.get('cardid', None))
    return render(request, 'readerpoints/pointscard.html', {'data':data})

@login_required
def myborrowing_view():
    return redirect('readerpoints/myborrowing.html')
