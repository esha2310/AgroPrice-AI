from functools import lru_cache
import json
import time
from django.conf import settings
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.http import JsonResponse,HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_GET,require_POST
from django.views.decorators.cache import never_cache
from .models import WatchItem

@lru_cache(maxsize=1)
def dataset():return json.loads((settings.BASE_DIR/'data/dashboard.json').read_text(encoding='utf-8'))
@never_cache
@require_GET
def index(request):
 name='login.html' if request.path.rstrip('/').endswith(('login','login.html')) else 'signup.html' if request.path.rstrip('/').endswith(('signup','signup.html')) else 'dashboard.html' if request.path.rstrip('/').endswith(('dashboard','dashboard.html')) else 'index.html'
 text=(settings.BASE_DIR/name).read_text(encoding='utf-8').replace('data-backend="0"','data-backend="1"',1)
 return HttpResponse(text)
@never_cache
@require_GET
def session(request):
 user=request.user
 return JsonResponse({'user':user.username if user.is_authenticated else None,'csrf':get_token(request),'saved':list(WatchItem.objects.filter(user=user).values_list('series_id',flat=True)) if user.is_authenticated else []})
def read(request):
 try:
  d=json.loads(request.body)
  if not isinstance(d,dict):raise ValueError
  return d
 except (ValueError,UnicodeDecodeError):return None

def limited(request):
 # Development/single-process mitigation only. Deployers need a shared atomic limiter.
 key='auth:'+request.META.get('REMOTE_ADDR','unknown')+':'+str(int(time.time()//300))
 count=cache.get(key,0);cache.set(key,count+1,300)
 return count>=15
@require_POST
@never_cache
def signup(request):
 if limited(request):return JsonResponse({'error':'Too many attempts. Try again in five minutes.'},status=429)
 d=read(request)
 if d is None:return JsonResponse({'error':'Invalid JSON.'},status=400)
 name=d.get('username','');pw=d.get('password','')
 if not isinstance(name,str) or not isinstance(pw,str) or len(name)<3 or len(name)>150 or len(pw)>256:return JsonResponse({'error':'Use a username of 3–150 characters and a valid password.'},status=400)
 full=d.get('full_name','');email=d.get('email','')
 if not isinstance(full,str) or not isinstance(email,str) or len(full)>150 or len(email)>254:return JsonResponse({'error':'Check your name and email.'},status=400)
 if 'password_confirm' in d and d['password_confirm']!=pw:return JsonResponse({'error':'The passwords do not match.'},status=400)
 if 'accepted_data_use' in d and d['accepted_data_use'] is not True:return JsonResponse({'error':'Please acknowledge the data and account information.'},status=400)
 User=get_user_model();u=User(username=name,first_name=full,email=email)
 try:
  u.full_clean(exclude=['password']);validate_password(pw,u)
 except ValidationError as exc:return JsonResponse({'error':' '.join(exc.messages)},status=400)
 from django.db import IntegrityError
 try:u.set_password(pw);u.save()
 except IntegrityError:return JsonResponse({'error':'This username is unavailable.'},status=400)
 login(request,u);return JsonResponse({'ok':True})
@require_POST
@never_cache
def signin(request):
 if limited(request):return JsonResponse({'error':'Too many attempts. Try again in five minutes.'},status=429)
 d=read(request)
 if d is None:return JsonResponse({'error':'Invalid JSON.'},status=400)
 name=d.get('username','');pw=d.get('password','')
 if not isinstance(name,str) or not isinstance(pw,str) or len(name)>150 or len(pw)>256:return JsonResponse({'error':'Invalid credentials.'},status=400)
 u=authenticate(request,username=name,password=pw)
 if u is None:return JsonResponse({'error':'Incorrect username or password.'},status=400)
 login(request,u)
 if 'remember_me' in d:request.session.set_expiry(60*60*24*7 if d['remember_me'] is True else 0)
 return JsonResponse({'ok':True})
@require_POST
@never_cache
def signout(request):logout(request);return JsonResponse({'ok':True})
@require_POST
@never_cache
def watchlist(request):
 if not request.user.is_authenticated:return JsonResponse({'error':'Sign in first.'},status=401)
 d=read(request)
 if d is None:return JsonResponse({'error':'Invalid JSON.'},status=400)
 sid=d.get('series_id');add=d.get('add')
 if not isinstance(sid,str) or not isinstance(add,bool) or sid not in {s['id'] for s in dataset()['series']}:return JsonResponse({'error':'Unknown market series or invalid action.'},status=400)
 if add:WatchItem.objects.get_or_create(user=request.user,series_id=sid)
 else:WatchItem.objects.filter(user=request.user,series_id=sid).delete()
 return JsonResponse({'saved':list(WatchItem.objects.filter(user=request.user).values_list('series_id',flat=True))})
