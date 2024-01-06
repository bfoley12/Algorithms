class Cell:
   def __init__(self, previous = None, value = 0):
      self.previous = previous
      self.value = value

   def get_previous(self):
      return self.previous
   
   def get_value(self):
      return self.value
   
   def set_value(self, value):
      self.value = value

   def set_previous(self, previous):
      self.previous = previous