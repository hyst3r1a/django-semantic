from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from . import models
from . import forms
from summarizer import summarize
from summa import summarizer as texsum
from summa import keywords as keysum

import pymorphy2 as morph

def index(request):
    username = request.user
    summarized_text = ''
    emphasized_text = ''
    keywords = ''
    analyzed_words_text = ''

    if request.method == 'POST':
        form  = forms.SimpleForm(request.POST)
        username = form['entered_text'].value()
    

        analyzer = morph.MorphAnalyzer(lang='uk')
        #text = "Пайтон - інтерпретована об'єктно-орієнтована мова програмування високого рівня зі строгою динамічною типізацією. Розроблена в 1990 році Гвідо ван Россумом. Структури даних високого рівня разом із динамічною семантикою та динамічним зв'язуванням роблять її привабливою для швидкої розробки програм, а також як засіб поєднування наявних компонентів. Python підтримує модулі та пакети модулів, що сприяє модульності та повторному використанню коду. Інтерпретатор Python та стандартні бібліотеки доступні як у скомпільованій, так і у вихідній формі на всіх основних платформах. В мові програмування Python підтримується кілька парадигм програмування, зокрема: об'єктно-орієнтована, процедурна, функціональна та аспектно-орієнтована."
        text = username
        print(summarize("Python", text, 3))

        summarized_text   = str(summarize("Python", text, 3))
        print(texsum.summarize(text))
        emphasized_text = texsum.summarize(text)
        print(keysum.keywords(text))
        s = keysum.keywords(text)
        li = s.split()
        keywords = '\n'.join(li) #str(keysum.keywords(text))
        text = text.split()
        endlist = []
        for val in text:
            p = analyzer.parse(val)[0]
            endlist.append(p.normal_form)
        m_dict = {i:endlist.count(i) for i in endlist}
        for w in sorted(m_dict, key=m_dict.get, reverse=True):
            if analyzer.parse(w)[0].tag.POS != "CONJ":
                analyzed_words_text += w + ' ' + str(analyzer.parse(w)[0].tag.POS) + ' ' + str(m_dict[w]) + '\n'

    context = {
        'username':username,
        'summarized_text':summarized_text,
        'emphasized_text':emphasized_text,
        'keywords':keywords,
        'analyzed_words_text':analyzed_words_text
    }
    return render(request, 'index.html', context)