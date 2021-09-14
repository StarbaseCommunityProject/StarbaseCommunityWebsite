from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ShipEntry, ShipImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from .forms import ShipCreationForm
import json

# Create your views here.


def catalogue(request):
    ships = ShipEntry.objects.all()
    return HttpResponse(render(request, 'shipshop/catalogue.html', {'ships': ships}))


def ship_search(request):
    """
    Example query: http://localhost:8000/ship_search?search=centauri&tags=miner,mining%20laser&attributes=cargo%20crates:200
    TODO: Needs some more sanitising of query inputs & error catching.
    :param request: Request data
    :return: JSON object containing query information and found ships.
    """
    search_term = request.GET.get('search') or None                 # "search term"
    tags = request.GET.get('tags') or None                          # [tag1, tag2, ...]
    attributes = request.GET.get('attributes') or None              # {'attribute': value, ...}
    updated_after = request.GET.get('updated_after') or None        # datetime string TODO
    page_nr = request.GET.get('page') or 1                          # 1
    entries_per_page = request.GET.get('entries_per_page') or 10    # 10

    return_all = True
    ships = ShipEntry.objects.filter(is_public=True).filter(is_deleted=False)
    if search_term:
        return_all = False
        ships = ships.filter(ship_name__unaccent__icontains=search_term)
    if tags:
        return_all = False
        tags = tags.split(",")
        for tag in tags:
            ships = ships.filter(tags__icontains=tag)
    if attributes:
        return_all = False
        attributes = attributes.split(",")
        for attribute in attributes:
            try:
                key, value = attribute.split(":")
                ships = ships.filter(attributes__contains=json.loads(f"{{\"{key}\":{value}}}"))
            except Exception as e:
                print(e)
    if return_all:
        ships = ships.all()

    ships = ships.order_by('updated_at')
    paginator = Paginator(ships, entries_per_page)

    try:
        exception_test = paginator.page(page_nr)
    except PageNotAnInteger:
        page_nr = 1
    except EmptyPage:
        page_nr = paginator.num_pages

    ship_count = len(ships)
    ships = paginator.page(page_nr)
    ship_count_this_page = len(ships)

    ships = serializers.serialize('json', ships)
    result = {'page': 1, 'total_pages': paginator.num_pages, 'total_entries': ship_count, 'total_entries_on_page': ship_count_this_page, 'ships': ships, 'query': {'search_term': search_term, 'tags': tags, 'attributes': attributes, 'page': page_nr, 'ships_per_page': entries_per_page}}
    return JsonResponse(result)


@login_required
def ship_creation(request):
    form = ShipCreationForm(request.POST)
    if form.is_valid() and request.POST:
        ship = form.save(commit=False)
        ship.creator = request.user
        ship.save()

        for image in request.FILES.getlist("images_upload"):
            new_ship_image = ShipImage(image=image)
            new_ship_image.save()
            ship.images.add(new_ship_image)

    return HttpResponse(render(request, 'shipshop/ship_creation.html', {'form': form}))
