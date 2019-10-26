class DiceSet:
    def __init__(self, dice):
        self.dice = dice

    def throw(self):
        return [die.throw() for die in self.dice]

    def serialize(self):
        return [die.serialize() for die in self.dice]

    def __str__(self):
        return str(self.dice)
