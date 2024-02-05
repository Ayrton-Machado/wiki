from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

class searchForm(forms.Form):
    text_field = forms.CharField(label='', widget = forms.TextInput(attrs={
    'placeholder': 'Search Wiki', 
    'style': 'width 10%'
    }))

class CreatePage(forms.Form):
    createTitle = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'Title',
        'style': 'width: 80%; margin: 10px;'
    }))
    createContent = forms.CharField(label='', widget=forms.Textarea(attrs={
        'placeholder': 'Content',
        'style': 'height: 60vh;' 
    }))
class EditPage(forms.Form):
    editTitle = forms.CharField(label='', widget=forms.TextInput(attrs={
        'style': 'width: 80%; margin: 10px;'
    }))
    editContent = forms.CharField(label='', widget=forms.Textarea(attrs={
        'style': 'height: 60vh;'
    }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": searchForm()
    })

def entry(request, title):
    entry_md = util.get_entry(title)
    if entry_md is None:
        return(render(request, 'encyclopedia/error.html',{
            'entries': util.list_entries(), 
            'title': title,
            "form": searchForm()
        }))
    entry_HTML = Markdown().convert(entry_md)
    return render(request, "encyclopedia/entry.html", {
        "entries": util.list_entries(),
        'entry': entry_HTML,
        'title': title,
        'form': searchForm()
    })

def search(request):
    if request.method == 'POST':
        entries_found = []
        entries_all = util.list_entries()
        form = searchForm(request.POST)
        if form.is_valid():
            text_field = form.cleaned_data['text_field']
            for entry in entries_all:
                if text_field.lower() == entry.lower():
                    title = entry
                    entry = util.get_entry(title)
                    return HttpResponseRedirect(reverse('entry', args=[title]))
                if text_field.lower() in entry.lower():
                    entries_found.append(entry)
            return render(request, 'encyclopedia/search.html', {
                "entries": util.list_entries(),
                'results': entries_found,
                'text_field': text_field,
                'form': searchForm()
            })
    return render(request, 'encyclopedia/search.html', {
        'text_field': '',
        "form": searchForm()
    })

def create(request):
    if request.method == 'POST':
        create_content = CreatePage(request.POST)
        if create_content.is_valid():
            title = create_content.cleaned_data['createTitle']
            content = create_content.cleaned_data['createContent']
            new_title = '# ' + title
            new_data = '\n' + content
            new_content = new_title + new_data
            util.save_entry(title, new_content)
            return HttpResponseRedirect(reverse('entry', args=[title]))
    return render(request, 'encyclopedia/create.html', {
        "entries": util.list_entries(),
        'form': searchForm(),
        'content_form': CreatePage()
    })

def randomPage(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect(reverse('entry', args=[title]))

def edit(request, title):
    if request.method == 'POST':
        content = util.get_entry(title)
        edit = EditPage(initial={"editTitle":title,'editContent':content})
        return render(request, 'encyclopedia/edit.html', {
            'edit': edit,
            'title': title,
            'form': searchForm(),
            'entries': util.list_entries()
        })

def submitEdit(request, title):
    if request.method == 'POST':
        form = EditPage(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data['editTitle']
            new_content = form.cleaned_data['editContent']
            util.save_entry(new_title, new_content)
        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'entry': Markdown().convert(new_content),
            'form': searchForm(),   
            'entries': util.list_entries()
        })