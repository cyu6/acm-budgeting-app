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
        nameofevent = self.request.get("nameofevent")
        date = self.request.get("date")
        eachpersonpays = totalbill/totalpeople
        new_splitter = Splitter(totalbill=totalbill,totalpeople=totalpeople, nameofevent=nameofevent, date=date)
        new_splitter.put()
        all_splitters = Splitter.query().fetch()
        template_vars = {
            "totalbill" : new_splitter.totalbill,
            "totalpeople" : new_splitter.totalpeople,
            "eachperson" : eachpersonpays,
            "date" : new_splitter.date,
            "nameofevent" : new_splitter.nameofevent,
            "splitters" : all_splitters
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
        tuition_expense = Expenses(week = week, category = "tuition", amount = tuition, actual = False)
        rent = int(self.request.get("rent"))
        rent_expense = Expenses(week = week, category = "rent", amount = rent, actual = False)
        food = int(self.request.get("food"))
        food_expense = Expenses(week = week, category = "food", amount = food, actual = False)
        transportation = int(self.request.get("transportation"))
        transportation_expense = Expenses(week = week, category = "transportation", amount = transportation, actual = False)
        clothing = int(self.request.get("clothing"))
        clothing_expense = Expenses(week = week, category = "clothing", amount = clothing, actual = False)
        misc = int(self.request.get("misc"))
        misc_expense = Expenses(week = week, category = "misc", amount = misc, actual = False)
        goal_expenses = [tuition_expense, rent_expense, food_expense, transportation_expense, clothing_expense, misc_expense]
        goal_expenses_keys = []
        for expense in goal_expenses:
            expense.put()
            goal_expenses_keys.append(expense.key)
        # create goals
        goals = Goals(week = week, salary = salary, other_income = other_income, emergency = emergency, expenses = goal_expenses_keys)
        goals.put()

        starting_value = 0

        template_vars = {
            "week": goals.week,
            "starting_actual": starting_value,
            "salary": goals.salary,
            "other_income": goals.other_income,
            "emergency": goals.emergency,
            "tuition": tuition_expense.amount,
            "rent": rent_expense.amount,
            "food": food_expense.amount,
            "transportation": transportation_expense.amount,
            "clothing": clothing_expense.amount,
            "misc": misc_expense.amount,
            "a_tuition": starting_value,
            "a_rent": starting_value,
            "a_food": starting_value,
            "a_transportation": starting_value,
            "a_clothing": starting_value,
            "a_misc": starting_value,
        }
        template = jinja_current_dir.get_template("/templates/show_budget.html")
        self.response.write(template.render(template_vars))

class SaveBudgetHandler(webapp2.RequestHandler):
    def post(self):
        category = str(self.request.get("payments"))
        add_amount = int(self.request.get("amount"))
        week = int(self.request.get("week"))
        starting_value = 0
        # create new expense
        new_expense = Expenses(week = week, category = category, amount = add_amount, actual = True)
        new_expense.put()
        # dictionary for all total amounts
        total_amounts = {
            "tuition": 0,
            "rent": 0,
            "food": 0,
            "transportation": 0,
            "clothing": 0,
            "misc": 0
        }
        # fetch all entries with same category and week
        same_category_expenses = Expenses.query(Expenses.week == week).filter(Expenses.category == category).filter(Expenses.actual == True).fetch()
        # find total actual expense for that category so far this week
        total_amount = 0
        sum = 0
        for expense in same_category_expenses:
            total_amount += expense.amount
        # add total amount to dictionary by running through list of categories
        expense_categories = ["tuition", "rent", "food", "transportation", "clothing", "misc"]
        for expense_category in expense_categories:
            if expense_category == category:
                total_amounts[category] = total_amount
        for expense_category in expense_categories:
            if expense_category == category:
                continue
            else:
                expenses_by_category = Expenses.query(Expenses.week == week).filter(Expenses.category == expense_category).filter(Expenses.actual == True).fetch()
                for expense in expenses_by_category:
                    sum += expense.amount
                print sum
                for key in total_amounts:
                    if expense_category == key:
                        total_amounts[key] = sum
        print total_amounts

        # recall total amounts to dictionary


        template_vars = {
            "week": week,
            "starting_actual": starting_value,
            "salary": Goals.query(Goals.week == week).get().salary,
            "other_income": Goals.query(Goals.week == week).get().other_income,
            "emergency": Goals.query(Goals.week == week).get().emergency,
            "tuition": Expenses.query(Expenses.week == week).filter(Expenses.category=="tuition").get().amount,
            "rent": Expenses.query(Expenses.week == week).filter(Expenses.category=="rent").get().amount,
            "food": Expenses.query(Expenses.week == week).filter(Expenses.category=="food").get().amount,
            "transportation": Expenses.query(Expenses.week == week).filter(Expenses.category=="transportation").get().amount,
            "clothing": Expenses.query(Expenses.week == week).filter(Expenses.category=="clothing").get().amount,
            "misc": Expenses.query(Expenses.week == week).filter(Expenses.category=="misc").get().amount,
            "a_tuition": total_amounts["tuition"],
            "a_rent": total_amounts["rent"],
            "a_food": total_amounts["food"],
            "a_transportation": total_amounts["transportation"],
            "a_clothing": total_amounts["clothing"],
            "a_misc": total_amounts["misc"]
        }
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
    ('/billsplitter', SplitBillHandler ),
    ('/budget', BudgetHandler),
    ('/savebudget', SaveBudgetHandler),
    ('/account', AccountHandler)

], debug=True)


#dev_appserver.py app.yaml
