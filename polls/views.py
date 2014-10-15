from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from polls.models import Choice, Poll
# from django.template import RequestContext, loader
from django.http import Http404
from django.core.urlresolvers import reverse
from django.utils import timezone

# Create your views here.
def index_old(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    # get the template
    template = loader.get_template('polls/index.html')
    context = RequestContext(request, {
       'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(template.render(context))

# A simpler coding view, with methode 'render':
def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    # A dictionary
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)

def detail_old(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render(request, 'polls/detail.html', {'poll':poll})
    # return HttpResponse("You're looking at poll %s." % poll_id)

# A simpler coding view, managing 404 with get_object_or_404
def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/detail.html', {'poll':poll})

def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll':poll})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

# Generic View
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # context_object_name : to change the orignial parametre name(defined in
    # gerneric.ListView)
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the last five published polls. """
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'
    #queryset() : A QuerySet represents the objects.
    def get_queryset(self):
        """
        Excludes any polls that aren't published yet
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'
    
