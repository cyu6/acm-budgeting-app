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
        nickname = None
        login_url = None
        logout_url = None

        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')

        else:
            login_url = users.create_login_url('/home')
        template_vars = {
            "user" : user,
            "nickname" : nickname,
            "login_url" : login_url,
            "logout_url" : logout_url,
        }
        template = jinja_current_dir.get_template("/templates/login.html") #fill this in
        self.response.write(template.render(template_vars))

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
    def post(self):
        bank_account = self.request.get("bank_account")
        salary = self.request.get("salary")
        other_income = self.request.get("other_income")
        tuition = self.request.get("tuition")
        rent = self.request.get("rent")
        food = self.request.get("food")
        bills = self.request.get("bills")
        school_supplies = self.request.get("school_supplies")
        transportation = self.request.get("transportation")
        clothing = self.request.get("clothing")
        misc = self.request.get("misc")
        emergency = self.request.get("emergency")


class AccountHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("/templates/account.html") #fill this in
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', LoginHandler),
    ('/home', HomeHandler), #can't be /static.. because it will look in the static folder
    ('/calendar', CalendarHandler),
    ('/budget', BudgetHandler),
    ('/account', AccountHandler)

], debug=True)


#dev_appserver.py app.yaml
