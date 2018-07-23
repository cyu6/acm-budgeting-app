import webapp2
import os
import jinja2
from google.appengine.api import users


jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')

        else:
            login_url = users.create_login_url('/')
            
        template = jinja_current_dir.get_template("/templates/login.html") #fill this in
        self.response.write(template.render())

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("/templates/home.html") #fill this in
        self.response.write(template.render())

class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("/templates/calendar.html") #fill this in
        self.response.write(template.render())
        #DoStuffHere

class BudgetHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("/templates/budget.html") #fill this in
        self.response.write(template.render())

class AccountHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("/templates/account.html") #fill this in
        self.response.write(template.render())

app = webapp2.WSGIApplication([
<<<<<<< HEAD
    ('/', LoginHandler),
    ('/home.html', HomeHandler), #can't be /static.. because it will look in the static folder
    ('/calendar.html', CalendarHandler),
    ('/budget.html', BudgetHandler),
    ('/account.html', AccountHandler)
=======
    ('/home', HomeHandler), #can't be /static.. because it will look in the static folder
    ('/calendar', CalendarHandler),
    ('/budget', BudgetHandler),
    ('/account', AccountHandler)
>>>>>>> 8ec506d0bc2dc2578200bbc093849d6781f34184
], debug=True)


#dev_appserver.py app.yaml
