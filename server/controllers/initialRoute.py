from django.shortcuts import HttpResponseRedirect

def initialRoute( request ):
    return HttpResponseRedirect('/login')