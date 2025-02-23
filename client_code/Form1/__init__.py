from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js.window as window
import anvil.js

SpeechRecognition = window.get("SpeechRecognition") or window.get("webkitSpeechRecognition")
SpeechGrammarList = window.get("SpeechGrammarList") or window.get("webkitSpeechGrammarList")

class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        self.recognition = SpeechRecognition()
        self.recognition.continuous = True  # Fortlaufende Erkennung
        self.recognition.lang = 'de-DE'
        self.recognition.interimResults = True  # Zeigt Zwischenresultate an
        self.recognition.maxAlternatives = 1
        
        self.recognition.onresult = self.on_result
        self.recognition.onspeechend = self.on_speech_end
        self.recognition.onnomatch = self.on_no_match
        self.recognition.onerror = self.on_error
        self.recognition.onsoundend = self.on_sound_end
        
        self.is_listening = False
    
    def on_result(self, event):
      text = ''
      for result in event.results:
        text += result[0].transcript + ' '
      self.hint.text = f"Live: {text.strip()}"
      #anvil.server.call("gemini", text)
      
    def on_sound_end(slef, event):
      print("speechend")
  
    def on_speech_end(self, event)
      if self.is_listening:
        self.recognition.start()  # Direkt neu starten für kontinuierliche Erkennung
    
    def on_no_match(self, event):
        self.hint.text = "I didn't recognise that"
    
    def on_error(self, event):
        self.hint.text = f"Error: {event.error}"
        if self.is_listening:
            self.recognition.start()
    
    def button_1_click(self, **event_args):
        """Diese Methode wird aufgerufen, wenn der Button geklickt wird"""
        if not self.is_listening:
            self.recognition.start()
            self.button_1.text = "Recording..."
            self.button_1.icon = "fa:microphone"
            self.button_1.enabled = False
            self.is_listening = True
            self.hint.text = 'Listening...'
        else:
            self.recognition.stop()
            self.button_1.text = "Start"
            self.button_1.icon = "fa:play"
            self.button_1.enabled = True
            self.is_listening = False