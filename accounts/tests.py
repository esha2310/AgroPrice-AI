import json
from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .models import WatchItem
from .views import dataset
class AuthenticationAndWatchlistTests(TestCase):
 def setUp(self):cache.clear();self.c=Client(enforce_csrf_checks=True)
 def post(self,path,data):
  token=self.c.get('/api/session/').json()['csrf']
  return self.c.post('/api/'+path,data=json.dumps(data),content_type='application/json',HTTP_X_CSRFTOKEN=token)
 def register(self,name='market_reader'):return self.post('signup/',{'username':name,'password':'River!Harvest_2026_Reader'})
 def test_public_page_and_private_watchlist(self):
  r=self.c.get('/');self.assertEqual(r.status_code,200);self.assertContains(r,'data-backend="1"');self.assertEqual(self.post('watchlist/',{'series_id':dataset()['series'][0]['id'],'add':True}).status_code,401)
 def test_csrf_required_for_registration(self):
  self.assertEqual(self.c.post('/api/signup/',data='{}',content_type='application/json').status_code,403)
 def test_signup_hash_session_and_logout(self):
  self.assertEqual(self.register().status_code,200);u=get_user_model().objects.get(username='market_reader');self.assertNotEqual(u.password,'River!Harvest_2026_Reader');self.assertTrue(u.check_password('River!Harvest_2026_Reader'));self.assertEqual(self.c.get('/api/session/').json()['user'],'market_reader');self.assertEqual(self.post('logout/',{}).status_code,200);self.assertIsNone(self.c.get('/api/session/').json()['user'])
 def test_weak_password_and_duplicate_username_rejected(self):
  self.assertEqual(self.post('signup/',{'username':'reader','password':'12345678'}).status_code,400);self.register();self.assertEqual(self.register().status_code,400)
 def test_bad_login_then_good_login(self):
  self.register();self.post('logout/',{});self.assertEqual(self.post('login/',{'username':'market_reader','password':'wrong'}).status_code,400);self.assertEqual(self.post('login/',{'username':'market_reader','password':'River!Harvest_2026_Reader'}).status_code,200)
 def test_watchlist_dedup_and_user_isolation(self):
  sid=dataset()['series'][0]['id'];self.register();self.post('watchlist/',{'series_id':sid,'add':True});self.post('watchlist/',{'series_id':sid,'add':True});self.assertEqual(WatchItem.objects.count(),1);self.post('logout/',{});self.register('another_reader');self.assertEqual(self.c.get('/api/session/').json()['saved'],[]);self.post('watchlist/',{'series_id':sid,'add':False});self.assertEqual(WatchItem.objects.count(),1)
 def test_invalid_series_and_payload(self):
  self.register();self.assertEqual(self.post('watchlist/',{'series_id':'fake','add':True}).status_code,400);self.assertEqual(self.post('watchlist/',{'series_id':dataset()['series'][0]['id'],'add':'false'}).status_code,400);self.assertEqual(self.post('signup/',[]).status_code,400)
 def test_get_cannot_mutate(self):
  for p in ['signup','login','logout','watchlist']:self.assertEqual(self.c.get('/api/'+p+'/').status_code,405)
 def test_login_throttle(self):
  for i in range(15):self.post('login/',{'username':'x','password':'wrong'})
  self.assertEqual(self.post('login/',{'username':'x','password':'wrong'}).status_code,429)

 def test_separate_html_pages(self):
  for path,word in [('/login/','Welcome Back!'),('/signup/','Create Account'),('/dashboard/','data-page="workspace"'),('/index.html','data-page="welcome"'),('/login.html','Welcome Back!'),('/signup.html','Create Account'),('/dashboard.html','data-page="workspace"')]:
   r=self.c.get(path);self.assertEqual(r.status_code,200);self.assertContains(r,word);self.assertContains(r,'data-backend="1"')
 def test_profile_details_and_password_confirmation(self):
  d={'username':'profile_reader','password':'River!Harvest_2026_Reader','full_name':'Market Reader','email':'reader@example.com','password_confirm':'wrong','accepted_data_use':True}
  self.assertEqual(self.post('signup/',d).status_code,400)
  d['password_confirm']=d['password'];self.assertEqual(self.post('signup/',d).status_code,200)
  u=get_user_model().objects.get(username='profile_reader');self.assertEqual(u.first_name,'Market Reader');self.assertEqual(u.email,'reader@example.com')
 def test_remember_me_session_policy(self):
  self.register();self.post('logout/',{})
  self.assertEqual(self.post('login/',{'username':'market_reader','password':'River!Harvest_2026_Reader','remember_me':False}).status_code,200);self.assertTrue(self.c.session.get_expire_at_browser_close())
  self.post('logout/',{});self.post('login/',{'username':'market_reader','password':'River!Harvest_2026_Reader','remember_me':True});self.assertFalse(self.c.session.get_expire_at_browser_close());self.assertLessEqual(self.c.session.get_expiry_age(),604800)
