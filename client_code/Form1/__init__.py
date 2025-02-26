from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js.window as window
import anvil.js

counter=0
checked=0
searchchecked=0
sttlang="de-DE"
SpeechRecognition = window.get("SpeechRecognition") or window.get("webkitSpeechRecognition")
navigator = window.navigator

class Form1(Form1Template):
    global sttlang, checked, searchchecked
    def __init__(self, **properties):
        self.init_components(**properties)

        self.language.items = [("Deutsch"), ("Englisch"), ("Französisch")]

        self.recognition = SpeechRecognition()
        self.recognition.continuous = True  # Fortlaufende Erkennung
        self.recognition.lang = sttlang
        self.recognition.interimResults = False  # Zwischenresultate anzeigen
        self.recognition.maxAlternatives = 1

        self.recognition.onresult = self.on_result
        self.recognition.onerror = self.on_error

        self.is_listening = False

        # Nur ein AudioContext für die gesamte Klasse erstellen
        self.audio_context = window.AudioContext()
        self.gain_node = self.audio_context.createGain()
        self.gain_node.gain.value = 3.0  # Lautstärke erhöhen
    
        # Web Audio API zur Mikrofonverstärkung einrichten
        self.setup_audio_processing()

    def setup_audio_processing(self):
        """Initialisiert die Audio-Verarbeitung mit Verstärkung"""
        try:
            stream = window.navigator.mediaDevices.getUserMedia({"audio": True})
            self.process_audio(stream)  # Direkt weiterverarbeiten
        except Exception as e:
            self.on_audio_error(e)


    def process_audio(self, stream):
        """Verbindet das Mikrofon mit dem Verstärker"""
        source = self.audio_context.createMediaStreamSource(stream)
        source.connect(self.gain_node)
        #self.gain_node.connect(self.audio_context.destination)  # Optional zum Mithören

    def on_audio_error(self, error):
        self.hint.text = f"Audio Error: {error}"

    



    def on_result(self, event):
        global counter, searchchecked
        text = ''
        final_text = ''
        
        for i in range(event.results.length):
            transcript = event.results[i][0].transcript
            text += transcript + ' '

            # Wenn das Ergebnis final ist, speichern
            if event.results[i].isFinal:
                final_text = transcript + ' '

        self.hint.text = f"Live: {text.strip()}"

        # Wenn es finalen Text gibt, dann rufe anvil.server.call auf
        if final_text.strip():
          print('Apicall for: ', final_text.strip())
          counter+=1
          if searchchecked == 1:
            response = anvil.server.call("gemini", self.input_box.text, counter, "true")
          else:
            response = anvil.server.call("gemini", self.input_box.text, counter, "false")
          self.output_box.text = response
    
    def on_error(self, event):
        self.hint.text = f"Error: {event.error}"
        #if self.is_listening:
        #    self.recognition.start()

    def button_1_click(self, **event_args):
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

    def delete_alles_click(self, **event_args):
      app_tables.context.delete_all_rows()

    def stop_click(self, **event_args):
      self.recognition.stop()
      self.button_1.text = "Start"
      self.button_1.icon = "fa:play"
      self.button_1.enabled = True
      self.is_listening = False

    def History_change(self, **event_args):
      global checked
      if checked == 0:
        print("changed")
        checked = 1
        Context = ""
        for row in app_tables.context.search():
          Context += f"'{row['Speeker']}' : '{row['Text']}',"
        self.history_box.text = Context
      else:
        checked = 0
        self.history_box.text = ""

  
    def input_box_pressed_enter(self, **event_args):
      global searchchecked
      print('Apicall for: ', self.input_box.text)
      if searchchecked == 1:
        print("test")
        response = anvil.server.call("gemini", self.input_box.text, counter, "true")
      else:
                response = anvil.server.call("gemini", self.input_box.text, counter, "false")
      self.output_box.text = response
      self.input_box.text = ''

    
    def language_change(self, **event_args):
      global sttlang
      if self.language.selected_value == "Deutsch":
        print("deustsch")
        sttlang = "de-DE"
      if self.language.selected_value == "Englisch":
        print("englisch")
        sttlang = "en-UK"
      if self.language.selected_value == "Französisch":
        print("frnace")
        sttlang = "fr-FR"

    def search_lever_change(self, **event_args):
      global searchchecked
      if searchchecked == 0:
        searchchecked = 1
      else:
        searchchecked = 0
      
      
    
      
