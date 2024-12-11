from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    """Pagina Principal do Elearnings"""
    return render(request, 'learnings/index.html')

@login_required
def topics(request):
    """mostra os topicos"""
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learnings/topics.html',context)

@login_required
def topic(request, topic_id):
    """Mostra um unico assumto de um topico"""
    topic = Topic.objects.get(id = topic_id)

    #Verifica o Assuto do Usario logafo
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic,'entries': entries}
    return render(request, 'learnings/topic.html', context)

@login_required
def new_topic(request):
    """Adiciona um assunto novo"""
    if request.method != 'POST' : 
        #Nenhum dado submemtido, cria novo formular
        form = TopicForm()
    else:
        #dados de posts submetidos processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))
        
    context = {'form': form}
    return render(request, 'learnings/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Adiciona uma nova anotação """
    topic = Topic.objects.get(id=topic_id)

    #Verifica o Assuto do Usario logafo
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST' : 
        #Nenhum dado submemtido, cria novo formular
        form = EntryForm()
    else:
        #dados de posts submetidos processa os dados
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id ]))
        
    context = {'topic':topic ,'form': form}
    return render(request, 'learnings/new_entry.html', context)

@login_required
def edit_entry(request,entry_id):
    """AEdite uma nova anotação """
    entry = Entry.objects.get(id=entry_id) 
    topic = entry.topic

    #Verifica o Assuto do Usario logafo
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        #requisição Iniial, preenche o form com os dados da

        form = EntryForm(instance=entry)
    else:
        #dados fornecidos
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic',args=[topic.id]))
        
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learnings/edit_entry.html', context)