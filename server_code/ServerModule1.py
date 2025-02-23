from anvil.tables import app_tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from google import genai
from collections import defaultdict

client = genai.Client(api_key="AIzaSyA3iQXk6-M5XQhzLIMO3SfEAKDPRunTHP8")

@anvil.server.callable
def gemini(text, counter):
  response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents='Wenn ich eine Frage stelel antworte bitte normal. Wenn es keine Frage ist antworte nur mit "FoRtNite". Das hier ist der prompt: ' + text,
    #contents=text,
  )
  app_tables.context.add_row(Speeker="User", Text=text, Number=counter)
  app_tables.context.add_row(Speeker="Gemini", Text=response.text, Number=counter)

  # Alle Einträge holen
  rows = list(app_tables.context.search())

  # Prüfen, ob es mindestens 10 Einträge gibt
  if len(rows) >= 4:
    # Nach "Number" gruppieren
    
    grouped = defaultdict(list)
    
    for row in rows:
        grouped[row['Number']].append(row)

    # Für jede Nummer die zwei niedrigsten Werte löschen
    for num, entries in grouped.items():
        # Nach einem anderen Kriterium sortieren, z.B. 'Wert' oder 'ID'
        entries.sort(key=lambda r: r['Number'])  
        
        # Lösche die zwei mit dem kleinsten Wert
        for row in entries[:2]:
            row.delete()
  #first_row = app_tables.context.get_by_id(1)
  #first_row.delete()
  #row = app_tables.context.get(Speeker="Gemini")
  #print(row.get_id())
  #for row in app_tables.context.search():
    #print(f"{row['Speeker']} is {row['Text']} years old")
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
