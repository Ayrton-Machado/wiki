from django.shortcuts import render
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, title):
    entry_md = util.get_entry(title)
    entry_HTML = Markdown().convert(entry_md)
    return render(request, "encyclopedia/entry.html", {
        'entry': entry_HTML,
        'title': title
    })
