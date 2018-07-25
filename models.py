from google.appengine.ext import ndb

class Goals(ndb.Model):
    week = ndb.IntegerProperty();
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
