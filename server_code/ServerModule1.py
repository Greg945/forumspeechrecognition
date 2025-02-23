import anvil.server
from google import genai

client = genai.Client(api_key="AIzaSyA3iQXk6-M5XQhzLIMO3SfEAKDPRunTHP8")

@anvil.server.callable
def gemini(text):
  response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="antworte mir nur wenn es eine Frage ist, sonst antworte nur mit ""leer"":" + text,
  )
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
