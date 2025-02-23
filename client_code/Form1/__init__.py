from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js.window as window
import anvil.js

SpeechRecognition = window.get("SpeechRecognition") or window.get("webkitSpeechRecognition")
SpeechGrammarList = window.get("SpeechGrammarList") or window.get("webkitSpeechGrammarList")
  
grammar = '#JSGF V1.0; grammar colors; public <color> = aqua | azure | beige | bisque | black | blue | brown | chocolate | coral | crimson | cyan | fuchsia | ghostwhite | gold | goldenrod | gray | green | indigo | ivory | khaki | lavender | lime | linen | magenta | maroon | moccasin | navy | olive | orange | orchid | peru | pink | plum | purple | red | salmon | sienna | silver | snow | tan | teal | thistle | tomato | turquoise | violet | white | yellow ;'

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    recognition = SpeechRecognition()
    speechRecognitionList = SpeechGrammarList()
    speechRecognitionList.addFromString(grammar, 1)
    recognition.grammars = speechRecognitionList
    recognition.continuous = False
    recognition.lang = 'en-US'
    recognition.interimResults = False
    recognition.maxAlternatives = 1
    
    def on_result(event):
      color = event.results[0][0].transcript
      self.hint.text = f"Received: {color}"
      self.card.background = color
      
    def on_speech_end(e):
      recognition.stop()
      self.button_1.text = 'Start'
      self.button_1.icon = 'fa:play'
      self.button_1.enabled = True
      
    def on_no_match(e):
      self.hint.text = "I didn't recognise that"
        
    recognition.onresult = on_result
    recognition.onspeechend = on_speech_end
    recognition.onnomatch = on_no_match
    
    self.recognition = recognition

    # Any code you write here will run when the form opens.
   

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.recognition.start()
    self.button_1.text = "recording"
    self.button_1.icon = "fa:microphone"
    self.button_1.enabled = False
    self.hint.text = 'ready to receive color command'

