from django import forms
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
import markdown2, random
from django.urls import reverse

from . import util

class SearchForm(forms.Form):
    SearchQuery = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia', 'class': 'search'}), label='', min_length=1)

class UpdateContentForm(forms.Form):
    NewContent = forms.CharField(widget=forms.Textarea(attrs={'style': 'position: absolute; margin-left: 2%; margin-top: 0.5%; width: 93%; height: 85%'}), label='', min_length=1)

class NewPageForm(forms.Form):
    Title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter title for your page!', 'style': 'position: absolute; left: 50%; top: 2%; width: 20%'}), label='', min_length=1)
    NewContent = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Create your new page! All the best!','style': 'position: absolute; margin-left: 2%; margin-top: 0.5%; width: 93%; height: 85%'}), label='', min_length=1)

def index(request):
    search_form = SearchForm()
    entries_list = util.list_entries()
    random_entry = random.choice(entries_list)
    print("random entry is " + random_entry)

    return render(request, "encyclopedia/index.html", {
        "entries": entries_list,
        "random_entry": random_entry,
        "search_form": search_form,
        "is_anything_searched": False
    })

def entry(request, title):
    # I need this variable since entry file also uses layout
    search_form = SearchForm()
    random_entry = random.choice(util.list_entries())

    entry_data = util.get_entry(title)
    if (entry_data == None):
        return HttpResponse('<h1>Page Not Found :(</h1>', status=404)
    else:
        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'html': markdown2.markdown(entry_data),
            'random_entry': random_entry,
            'search_form': search_form
        })

def contribute(request, page):
    # I need this variable since contribute file also uses layout
    search_form = SearchForm()
    random_entry = random.choice(util.list_entries())
    page_markdown = util.get_entry(page)

    form = UpdateContentForm(initial={'NewContent': page_markdown}) # sets the initial value of NewContent

    if request.method == 'POST':
        form = UpdateContentForm(request.POST)
        if (form.is_valid()): # this will always happen though
            updated_page_markdown = form.cleaned_data["NewContent"]
            util.save_entry(page, updated_page_markdown) # updating the database of entries
            return HttpResponseRedirect(reverse('entry', args=[page]))

    return render(request, 'encyclopedia/contribute.html', {
        'title': page,
        'random_entry': random_entry,
        'textarea': form,
        'search_form': search_form
    })

def newpage(request):
    # I need this variable since newpage file also uses layout
    search_form = SearchForm()
    entries_list = util.list_entries()
    random_entry = random.choice(entries_list)   

    form = NewPageForm()
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if (form.is_valid()): #this will always happen though
            new_page_markdown = form.cleaned_data["NewContent"]
            new_title = form.cleaned_data["Title"]
            
            # check if new_title exits in records
            if new_title in entries_list:
                return render(request, 'encyclopedia/errorpage.html')
            else:
                util.save_entry(new_title, new_page_markdown)
                return HttpResponseRedirect(reverse('entry', args=[new_title]))

    return render(request, 'encyclopedia/newpage.html', {
        'random_entry': random_entry,
        'form': form,
        'search_form': search_form
    })

def search(request):
    # this route should only be visited on POST
    assert(request.method=='POST')


    entries_list = util.list_entries()

    random_entry = random.choice(entries_list)
    valid_list = []

    submitted_search_form = SearchForm(request.POST)
    if submitted_search_form.is_valid():
        search_string = submitted_search_form.cleaned_data["SearchQuery"]
        # now iterate over the list of available encyclopedias to check whether search_string is substring of some title
        for entry in entries_list:
            if search_string.lower() in entry.lower():
                valid_list += [entry]

        if len(valid_list) == 1 and valid_list[0].lower() == search_string.lower():
            return HttpResponseRedirect(reverse('entry', args=[valid_list[0]]))
        else :
            return render(request, 'encyclopedia/index.html', {
            "entries": valid_list,
            "random_entry": random_entry,
            "search_form": submitted_search_form,
            "is_anything_searched": True
            })

    else:
        return render(request, 'encyclopedia/index.html', {
            "entries": entries_list,
            "random_entry": random_entry,
            "search_form": submitted_search_form,
            "is_anything_searched": False
        })

