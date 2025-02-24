import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from google import genai
from google.genai import types
from collections import defaultdict
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

sys_instruct='Wenn ich eine Frage stelel antworte bitte normal. Wenn es keine Frage ist antworte nur mit "Igonriert".'
client = genai.Client(api_key="AIzaSyA3iQXk6-M5XQhzLIMO3SfEAKDPRunTHP8")

google_search_tool = Tool(
    google_search = GoogleSearch()
)

@anvil.server.callable
def gemini(text, counter, search):
  Context = ""
  for row in app_tables.context.search():
    Context += f"'{row['Speeker']}' : '{row['Text']}',"
  if search == "true":
    response = client.models.generate_content(
      model="gemini-2.0-flash",
      config=types.GenerateContentConfig(system_instruction=sys_instruct, tools=[google_search_tool], response_modalities=["TEXT"]),
      contents=' Hier ist noch der Konversations Verlauf, beachte diesen wenn er notwendig ist: "' +  Context + '" Das hier ist der prompt: ' + text
    )
  else:
    response = client.models.generate_content(
      model="gemini-2.0-flash",
      config=types.GenerateContentConfig(system_instruction=sys_instruct),
      contents=' Hier ist noch der Konversations Verlauf, beachte diesen wenn er notwendig ist: "' +  Context + '" Das hier ist der prompt: ' + text
    )
  app_tables.context.add_row(Speeker="User", Text=text, Number=counter)
  app_tables.context.add_row(Speeker="Gemini", Text=response.text, Number=counter)

  # Context laenge loeschen
  rows = app_tables.context.search()
  if len(rows) >= 20:
    numbers = [r['Number'] for r in app_tables.context.search()]
    rows = app_tables.context.search(Number=min(numbers))
    for row in rows:
      row.delete()

  print(response.text)
  return response.text


# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
