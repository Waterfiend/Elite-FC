from pickle import TRUE
from django.shortcuts import render,redirect
from django.contrib import messages
import re
SKIP_PATHS = ['^[/]{1}$',
              "^/register",
              "^/login",
              "^/registerValidate",
              "^/loginValidate",
              "^/Newsfront",
              "^/articledet",   
              "^/media",
              "^/viewPlayers",
              "^/playerstatisticsFront",
              "^/upcommingMatches",
              "^/matcheResults",
              ]

def authenticationMiddleware(get_response):
    def middleware(request):
        global SKIP_PATHS
        bSkip = False
        requestPath = request.path
        print(requestPath)
        for path in SKIP_PATHS:
            pattern = re.compile(path)
            expression = pattern.match(requestPath)
            if expression:
                bSkip = True
                break
        if not bSkip:
            if 'login' not in request.session:
                messages.error(request,'UnAuthenticated: You need to login access to '+requestPath)
                return redirect('/')
        response = get_response(request)
        
        return response
    return middleware