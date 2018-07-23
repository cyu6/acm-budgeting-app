import webapp2
import os
import jinja2


jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("home.html") #fill this in
        self.response.write(template.render())

class CalendarHandlar(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("calendar.html") #fill this in
        self.response.write(template.render())
        #DoStuffHere

class BudgetHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("budget.html") #fill this in
        self.response.write(template.render())

class AccountHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("account.html") #fill this in
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', HomeHandler), #can't be /static.. because it will look in the static folder
    ('/calendar', CalendarHandler),
    ('/budget', BudgetHandler),
    ('/account', AccountHandler)
], debug=True)
