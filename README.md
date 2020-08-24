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
8. **Repeat steps urls + serialiers + views (4, 5, 6) for API calls** 

Authentication:
1. **Create signup endpoint**
