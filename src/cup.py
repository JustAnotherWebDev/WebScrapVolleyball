class Cup:
    def __init__(self, gender, date, category, name, players, link, inform):
        # don't use gender as enum because they might add genders and that would crash the app!
        self.gender = gender
        self.date = date
        self.category = category
        self.name = name
        self.players = players
        self.link = link
        self.id = gender + date.replace(" ", "") + category + name + link
        self.inform = inform

    def __str__(self):
        return str({'gender': self.gender, 'date': self.date, 'category': self.category, 'name': self.name, 'players': self.players, 'link': self.link})

    def __eq__(self, other):
        return (self.gender, self.date, self.category, self.name, self.link) == (other.gender, other.date, other.category, other.name, other.link)

    def __ne__(self, other):
        return not self.__eq__(other)
