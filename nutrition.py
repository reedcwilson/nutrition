import myfitnesspal
import time
import flask
import sys
import argparse
import os

class Nutrition:

  def __init__(self):
    # create client
    self.client = myfitnesspal.Client('reedcwilson', 'myfitnesspal')

  def format_name(self, name):
    return name.strip().replace("'", "@`")

  def create_json(self, day):
    entries = { self.format_name(entry.name): entry.totals for entry in day.entries }
    meals = { self.format_name(meal.name): meal.totals for meal in day.meals}
    result = {'goals': day.goals, 'current': day.totals, 'meals': meals, 'entries': entries}
    return str(result).replace("'", '"').replace("@`", "'")

  def get_day(self, year, month, day):
    return self.client.get_date(year, month, day)

  def get_data(self, year, month, day):
    d = self.client.get_date(year, month, day)
    return self.create_json(d)

app = flask.Flask(__name__)
nutrition = Nutrition()

@app.route("/")
def get_today():
  year, month, day = time.strftime("%Y:%m:%d").split(':')
  resp = flask.make_response(nutrition.get_data(year, month, day))
  resp.headers['Content-Type'] = 'application/json'
  return resp

@app.route("/day")
def get_day():
  cur_year, cur_month, cur_day = time.strftime("%Y:%m:%d").split(':')
  year = flask.request.args.get('year')
  month = flask.request.args.get('month')
  day = flask.request.args.get('day')
  year = year if year else cur_year
  month = month if month else cur_month
  day = day if day else cur_day
  print year, month, day
  resp = flask.make_response(nutrition.get_data(year, month, day))
  resp.headers['Content-Type'] = 'application/json'
  return resp

def main():
  parser = argparse.ArgumentParser(prog='nutrition', description='An API for MyFitnessPal', add_help=True)
  parser.add_argument('-d', '--debug', action='store_true')
  args = parser.parse_args()
  port = os.environ.get('PORT') 
  port = port if port else 5000
  app.run(debug=args.debug, port=int(port))

if __name__ == "__main__":
  main()
