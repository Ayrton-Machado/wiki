from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from . import util

class search(forms.Form):
    text_field = forms.CharField(label='Search ', required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, title):
    entry_md = util.get_entry(title)
    entry_HTML = Markdown().convert(entry_md)
    return render(request, "encyclopedia/entry.html", {
        "entries": util.list_entries(),
        'entry': entry_HTML,
        'title': title
    })

def search(request, title):
    search_form = search(request.POST)
    if request.method == 'POST':
        if search_form.is_valid():
            search_query = search_form.cleaned_data['text_field']
            search_md = util.get_entry(search_query)
            search_HTML = Markdown().convert(search.md)
            return render(request, 'encyclopedia/search.html', {
                "entries": util.list_entries(),
                'search': search_HTML,
                'search_query': search_query,
                'title': title
            })
