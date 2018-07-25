import webapp2
import os
import jinja2
from google.appengine.api import users
from models import *


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

class SplitBillHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("/templates/splitbill.html") #fill this in
        self.response.write(template.render())
    def post(self):
        totalbill = int(self.request.get("totalbill"))
        totalpeople = int(self.request.get("totalpeople"))
        eachpersonpays = totalbill/totalpeople
        print(eachpersonpays)
        template_vars = {
            "totalbill" : totalbill,
            "totalpeople" : totalpeople,
            "eachperson" : eachpersonpays
        }
        template = jinja_current_dir.get_template("/templates/show_splitbill.html") #fill this in
        self.response.write(template.render(template_vars))

class BudgetHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("/templates/budget.html") #fill this in
        self.response.write(template.render())
    def post(self):
        # week of
        week = int(self.request.get("week"))
        # income
        salary = int(self.request.get("salary"))
        other_income = int(self.request.get("other_income"))
        # savings
        emergency = int(self.request.get("emergency"))
        # create expenses
        tuition = int(self.request.get("tuition"))
        tuition_expense = Expenses(category = "tuition", amount = tuition, actual = False)
        rent = int(self.request.get("rent"))
        rent_expense = Expenses(category = "rent", amount = rent, actual = False)
        food = int(self.request.get("food"))
        food_expense = Expenses(category = "food", amount = food, actual = False)
        transportation = int(self.request.get("transportation"))
        transportation_expense = Expenses(category = "transportation", amount = transportation, actual = False)
        clothing = int(self.request.get("clothing"))
        clothing_expense = Expenses(category = "clothing", amount = clothing, actual = False)
        misc = int(self.request.get("misc"))
        misc_expense = Expenses(category = "misc", amount = misc, actual = False)
        goal_expenses = [tuition_expense, rent_expense, food_expense, transportation_expense, clothing_expense, misc_expense]
        goal_expenses_keys = []
        for expense in goal_expenses:
            expense.put()
            goal_expenses_keys.append(expense.key)
        # create goals
        goals = Goals(week = week, salary = salary, other_income = other_income, emergency = emergency, expenses = goal_expenses_keys)
        goals.put()
        # print Goals.query(Goals.week == 1).get().salary
        template_vars = {
            "week": goals.week,
            "salary": goals.salary,
            "other_income": goals.other_income,
            "emergency": goals.emergency,
            "tuition": tuition_expense.amount,
            "rent": rent_expense.amount,
            "food": food_expense.amount,
            "transportation": transportation_expense.amount,
            "clothing": clothing_expense.amount,
            "misc": misc_expense.amount
        }

        template = jinja_current_dir.get_template("/templates/show_budget.html")
        self.response.write(template.render(template_vars))

class SaveBudgetHandler(webapp2.RequestHandler):
    def post(self):
        category = str(self.request.get("payments"))
        add_amount = int(self.request.get("amount"))
        # create payments
        addition = Expenses(category = category, amount = add_amount, actual = True)
        addition.put()
        # template_vars = {
        #     "new_expense": addition,
        #     "salary": Goals.query(Goals.salary).get(),
        #     "other_income": Goals.query(Goals.other_income).get(),
        #     "emergency": Goals.query(Goals.emergency).get(),
        #     "tuition": Expenses.query(Expenses.category == "tuition").get().amount,
        #     "rent": Expenses.query(Expenses.category == "rent").get().amount,
        #     "food": Expenses.query(Expenses.category == "food").get().amount,
        #     "transportation": Expenses.query(Expenses.category == "transportation").get().amount,
        #     "clothing": Expenses.query(Expenses.category == "clothing").get().amount,
        #     "misc": Expenses.query(Expenses.category == "misc").get().amount
        # }
        template = jinja_current_dir.get_template("/templates/show_budget.html")
        self.response.write(template.render(template_vars))




class AccountHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("/templates/account.html") #fill this in
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', LoginHandler),
    ('/home', HomeHandler), #can't be /static.. because it will look in the static folder
    ('/calendar', CalendarHandler),
    ('/billspliter', SplitBillHandler ),
    ('/budget', BudgetHandler),
    ('/savebudget', SaveBudgetHandler),
    ('/account', AccountHandler)

], debug=True)


#dev_appserver.py app.yaml
