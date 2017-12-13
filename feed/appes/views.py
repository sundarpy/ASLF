from django.views.generic.detail import DetailView
from django.http import JsonResponse
from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
from haystack.query import SearchQuerySet
from django.shortcuts import get_object_or_404, render , redirect, render_to_response
from django.http import Http404
from django.http import HttpResponse
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.forms import ModelForm
from django.contrib import messages
from django.utils.translation import get_language
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import feedparser
import urllib2
from urlparse import urlparse
from django.db import IntegrityError


from appes.models import Myfeed, Addfeed
from appes.forms import FacetedMyfeedSearchForm


class HomeView(TemplateView):
    template_name = "home.html"


class MyfeedView(DetailView):
    template_name = "product.html"
    model = Myfeed



def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(
        content_auto=request.GET.get('query',''))[:5]
    s = []
    for result in sqs:
        d = {"value": result.title, "data": result.object.slug}
        s.append(d)
    output = {'suggestions': s}
    return JsonResponse(output)


class FacetedSearchView(BaseFacetedSearchView):
    form_class = FacetedMyfeedSearchForm    
    facet_fields = ['category', 'main_link']
    template_name = 'search_result.html'
    paginate_by = 10
    context_object_name = 'object_list'


#=====================Newfeed=======================#

class AddfeedForm(ModelForm):
    class Meta:
        model = Addfeed
        fields = (
            'url',
        )

def feed_list(request):
    addfeed = Addfeed.objects.all()
    data = {}
    data['object_list'] = addfeed
    template_name = 'feed_list.html'
    return render(request, template_name, data)

# def feed_create(request):
#     template_name = 'feed_form.html'
#     form = AddfeedForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('feed_list')
#     return render(request, template_name, {'form':form})
def feed_create(request):
    template_name = 'feed_form.html'
    form = AddfeedForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        field = data['url']
        form.save()
        try:
            d = feedparser.parse(field)
            i = 0
            for item in d['items']:
                try:
                    if 'link' in item:
                        ls_feed =  item['link']
                    else:
                        ls_feed = None
                    if 'title' in  item:
                        ts_feed =  item['title']
                    else:
                        ts_feed = None
                    if 'category' in item:
                        c_feed = item['category']
                    else:
                        c_feed = 'others'
                    if 'id' in  item:
                        id_feed =  item['id']
                    else:
                        id_feed = None
                    if 'updated' in item:
                        updates =  item['updated']
                    else:
                        updates = None
                    if 'published' in item:
                        p_feed =  item['published']
                    else:
                        p_feed = None
                    if 'description' in item:
                        des_feed =  item['description'] 
                        remo_uf = des_feed.encode('utf-8').strip()
                        deatil = remo_uf
                    else:
                        deatil = None
                    #======================#
                    myfeed = Myfeed.objects.create()
                    myfeed.category = c_feed
                    myfeed.main_link = field
                    myfeed.description = remo_uf
                    myfeed.title = ts_feed
                    myfeed.sub_link = ls_feed
                    myfeed.updated = updates
                    myfeed.tag_id = id_feed
                    myfeed.published = p_feed
                    myfeed.save()
                    i += 1
                    
                    #======================#
                except KeyError:
                    pass

            return redirect('feed_list')
        except IntegrityError as e:
            return render_to_response("error.html", {"message": e.message})
    return render(request, template_name, {'form':form})

def feed_update(request, pk):
    template_name = 'feed_form.html'
    addfeed= get_object_or_404(Addfeed, pk=pk)
    form = AddfeedForm(request.POST or None, instance=addfeed)
    if form.is_valid():
        form.save()
        return redirect('feed_list')
    return render(request, template_name, {'form':form})

def feed_delete(request, pk):
    template_name = 'feed_confirm_delete.html'
    addfeed= get_object_or_404(Addfeed, pk=pk)    
    if request.method=='POST':
        addfeed.delete()
        return redirect('feed_list')
    return render(request, template_name, {'object':addfeed})      


def url_view(request):
    template_name = 'test.html'
    message = {
    	'RssFeed has been successfully added!'
    }
    addfeed = Addfeed.objects.all()
    l_url = []
    i = 0
    for item in addfeed:
    	url_f = item.url
    	l_url.append(url_f)
    # print(l_url)
    # for i_url in l_url[-1]:
    try:
        d = feedparser.parse (l_url[-1])
        for item in d['items']:
            try:
                if 'link' in item:
                    ls_feed =  item['link']
                else:
                    ls_feed = None
                if 'title' in  item:
                    ts_feed =  item['title']
                else:
                    ts_feed = None
                if 'category' in item:
                    c_feed = item['category']
                else:
                    c_feed = 'others'
                if 'id' in  item:
                    id_feed =  item['id']
                else:
                    id_feed = None
                if 'updated' in item:
                    updates =  item['updated']
                else:
                    updates = None
                if 'published' in item:
                    p_feed =  item['published']
                else:
                    p_feed = None
                if 'description' in item:
                    des_feed =  item['description'] 
                    remo_uf = des_feed.encode('utf-8').strip()
                    deatil = remo_uf
                else:
                    deatil = None
                #======================#
                myfeed = Myfeed.objects.create()
                myfeed.category = c_feed
                myfeed.main_link = l_url[-1]
                myfeed.description = remo_uf
                myfeed.title = ts_feed
                myfeed.sub_link = ls_feed
                myfeed.updated = updates
                myfeed.tag_id = id_feed
                myfeed.published = p_feed
                myfeed.save()
                i += 1
                # print(myfeed)
                
                #======================#
            except KeyError:
                pass

        return HttpResponse(message)
    except IntegrityError as e:
        return render_to_response("error.html", {"message": e.message})
