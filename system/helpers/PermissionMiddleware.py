from pickle import TRUE
from django.shortcuts import render,redirect
from django.contrib import messages
from ..models import User,Permission
import re
SKIP_PATHS = ['^[/]{1}$',
              "^/Tickets",
              "^/fieldReservation",
              "^/reservationValidate",
              "^/Profile",
              "^/logout",
              "^/register",
              "^/login",
              "^/registerValidate",
              "^/loginValidate",
              ]

def permissionMiddleware(get_response):
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
            user = User.objects.filter(email=request.session['login']['email']).first()
            roleAllowedPaths = Permission.objects.filter(role=user.role).values_list('path',flat=True)
            bAuthorized = False
            for path in roleAllowedPaths:
                pattern = re.compile('^'+path)
                expression = pattern.match(requestPath)
                if expression:
                    bAuthorized = True
                    break
            if not bAuthorized:
                messages.error(request,'UnAuthorized Access to '+requestPath)
                return redirect('/')
        response = get_response(request)
        
        return response
    return middleware