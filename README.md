API for external TODO project.


---

WORKFLOW:

Setup:
1. **Clone existing project**

GitHub:
1. **Create empty repo in GitHub**
2. **Change origin's URL** - git remote set-url origin http://github.com/new_repo -> (to make sure it was updated) git config --get remote.origin.url 
3. **Push local repo to remote** - git push origin master

API:
1. **Create new api app** - python manage.py startapp api
2. **Add rest_framework & api app to the todowoo/settings.py INSTALLED_APPS**
3. **Include api/urls.py to todowoo/urls.py**
4. **Create api/urls.py and create path**
5. **Create serializer.py with model serialiser**
6. **Create view in api/view.py** - use todo/views.py to see the queryset used for Front-End
7. **Use website login/logout functionality to test API**
8. **Repeat steps urls + serializers + views (4, 5, 6) for API calls** 

Authentication (assigning token for user-password pair):
1. **Add api/signup/ endpoint to api/views.py that works only with POST and generates token**
2. **Add rest_framework.authtoken to the todowoo/settings.py INSTALLED_APPS** - generates migration file
3. **Run migrate to update db with new token table**
4. **Add new section REST_FRAMEWORK with DEFAULT_AUTHENTICATION_CLASSES -> TokenAuthentication** - now using token for auth only
5. **Make POST request to the signup endpoint** - only POST methods are supported, use curl
```
curl -X POST http://localhost:8000/api/signup/ -H "Content-Type: application/json" -d "{ \"username\": \"***\", \"password\": \"***\"}" 
# response {"token": key}
```
*IMPORTANT: use double quotes for cURL ONLY in Windows cmd, single quotes don't work! Escape double quotes with backslash.*
6. **Get token from the response**
7. **Check Token in Admin**
8. **Use token for API requests (user-password pair won't work anymore since we specified TokenAuthentication in settings)**
```
curl http://127.0.0.1:8000/api/todos/ -H "Authorization: Token ***********"
# response list of todos
```
*IMPORTANT: use double quotes for cURL ONLY in Windows cmd, single quotes don't work!*
9. **Create api/login endpoint to get token**
10. **Make call to the login endpoint**
```
curl -X POST http://localhost:8000/api/login/ -H "Content-Type: application/json" -d "{ \"username\": \"***\", \"password\": \"***\"}"
# response {"token": key}
```
