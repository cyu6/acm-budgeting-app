from google.appengine.ext import ndb

class Goals(ndb.Model):
    salary = ndb.IntegerProperty();
    other_income = ndb.IntegerProperty();
    emergency = ndb.IntegerProperty();
    expenses = ndb.KeyProperty(repeated = True)

# class Expenses(ndb.Model):
#     tuition = ndb.IntegerProperty();
#     rent = ndb.IntegerProperty();
#     food = ndb.IntegerProperty();
#     bills = ndb.IntegerProperty();
#     school_supplies = ndb.IntegerProperty();
#     transportation = ndb.IntegerProperty();
#     clothing = ndb.IntegerProperty();
#     misc = ndb.IntegerProperty();

class Expenses(ndb.Model):
    category = ndb.StringProperty();
    amount = ndb.IntegerProperty();
    actual = ndb.BooleanProperty();

# class ActualExpenses(ndb.Model):
#     a_tuition = ndb.IntegerProperty();
#     a_rent = ndb.IntegerProperty();
#     a_food = ndb.IntegerProperty();
#     a_bills = ndb.IntegerProperty();
#     a_school_supplies = ndb.IntegerProperty();
#     a_transportation = ndb.IntegerProperty();
#     a_clothing = ndb.IntegerProperty();
#     a_misc = ndb.IntegerProperty();
