class DiceSet:
    # dice must be an array of Die objects.
    def __init__(self, dice, theme):
        self.dice = dice
        self.theme = theme

    def throw(self):
        return [die.throw() for die in self.dice]

    def serialize(self):
        return [die.serialize() for die in self.dice]

    def __str__(self):
        return str(self.dice)
