class Cup:
  def __init__(self, gender, date, category, name, players, link):
    # TODO: Set gender as enum
    self.gender = gender
    self.date = date
    self.category = category
    self.name = name
    self.players = players
    self.link = link
    self.id = gender + date.replace(" ", "") + category + name + link



  def __str__(self):
    #return 'test'
    # TODO: Hier direkt den sinnvollen Text als String einbauen
    return str({'gender': self.gender, 'date': self.date, 'category': self.category, 'name': self.name, 'players': self.players, 'link': self.link, 'id': self.id})

  def __eq__(self, other):
    return (self.gender, self.date, self.category, self.name, self.link) == (self.gender, self.date, self.category, self.name, self.link)
  