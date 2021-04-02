from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required

from pathlib import Path

# from accounts.decorators import token_expire_checked


TEMPLATE = Path('lab')


@require_GET
@login_required
# @token_expire_checked
def index(request):
    return render(request, 'lab/index.html')
