import sys

if len(sys.argv) < 2:
    raise ValueError("Provide path to wizInt file.")
if len(sys.argv) < 3:
    inputPath = "./input.txt"
else:
    inputPath = sys.argv[2]


mainFile = open(sys.argv[1], "r")
fin = open(inputPath, "r").read()

class Creature:
    def __init__(self, name):
        self.name = name
        self.stat = 100
        self.scroll = scrolls["none"]
        self.realm = realms["overworld"]
    def findEnemies(self):
        keys = self.realm.keys()
        output = []
        for key in keys:
            if key != self.name:
                output.append(self.realm[key])
        return output
    def act(self):
        return
    def reel(self):
        return
    def die(self):
        del creatures[self.name]
        del self.realm[self.name]
    def setStat(self, stat):
        self.stat = maybeNum(stat)

class Wizard(Creature):
    def __init__(self, name):
        super().__init__(name)
    def act(self):
        enemies = self.findEnemies()
        if len(enemies) > 0:
            self.scroll.cast(self.name, enemies[0], True)

class Goblin(Creature):
    def __init__(self, name):
        super().__init__(name)
        self.faction = "evil"
    def reel(self):
        if self.stat <= 0:
            self.die()

class Zombie(Creature):
    def __init__(self, name):
        super().__init__(name)
    def reel(self):
        if self.stat == 0:
            self.die()

class Scribe(Creature):
    def __init__(self, name):
        super().__init__(name)
        self.stat = ""
    def reel(self):
        print(self.stat.replace("_", " "), end="")

class Oracle(Creature):
    def __init__(self, name):
        super().__init__(name)
        self.stat = fin

class Scroll:
    def __init__(self, name, spells):
        self.spells = spells
        self.name = name
    def cast(self, caster, enemy, protected):
        for spell in self.spells:
            if not protected:
                cast(spell, caster, enemy)
            else:
                try:
                    cast(spell, caster, enemy)
                except Fizzle:
                    break
                

class Fizzle(Exception):
    pass

class Nuke(Exception):
    pass

def summon(creature, name):
    summoned = makeCreature(creature, name)
    creatures[name] = summoned
    summoned.realm[name] = summoned
def give(target, scroll):
    creatures[target].scroll = scrolls[scroll]
def teleport(target, realm):
    if not realm in realms:
        realms[realm] = {}
    realms[realm][target] = creatures[target]
    creatures[target].realm = realms[realm]
def fireball(target, amount):
    creatures[target].stat -= maybeNum(amount)
def bleed(target, amount):
    creatures[target].stat /= maybeNum(amount)
def kill(target):
    creatures[target].die()
def imprint(target, thought):
    creatures[target].setStat(thought)
def curse(target):
    cursed[target] = True
def sling(caster, target, spell):
    scrolls[spell].cast(caster, target, False)
def cast(caster, target, spell):
    scrolls[spell].cast(caster, target, True)
def brew(component, caster, target, spell):
    if component in creatures[caster].realm:
        scrolls[spell].cast(caster, target, False)
def tinker(component, caster, target, spell):
    if component in creatures[caster].realm:
        scrolls[spell].cast(caster, target, True)
def nuke():
    raise Nuke
def fizzle():
    raise Fizzle


creatures = {

}
scrolls = {
    "none": Scroll("none", [])
}
cursed = {

}
spells = {
    "summon": {
        "args": 2,
        "meta": summon
    },
    "give": {
        "args": 2,
        "meta": give
    },
    "teleport": {
        "args": 2,
        "meta": teleport
    },
    "fireball": {
        "args": 2,
        "meta": fireball
    },
    "bleed": {
        "args": 2,
        "meta": bleed
    },
    "kill": {
        "args": 1,
        "meta": kill
    },
    "imprint": {
        "args": 2,
        "meta": imprint
    },
    "curse": {
        "args": 1,
        "meta": curse
    },
    "sling": {
        "args": "s",
        "meta": sling
    },
    "cast": {
        "args": "s",
        "meta": cast
    },
    "brew": {
        "args": "c",
        "meta": brew
    },
    "tinker": {
        "args": "c",
        "meta": tinker
    },
    "nuke": {
        "args": 0,
        "meta": nuke
    },
    "fizzle": {
        "args": 0,
        "meta": fizzle
    }
}
realms = {
    "overworld": {
        
    }
}




def maybeNum(s):
    try:
        return float(s)
    except ValueError:
        return s

def makeCreature(creatureType, name):
    if creatureType == "wizard":
        return Wizard(name)
    elif creatureType == "goblin":
        return Goblin(name)
    elif creatureType == "zombie":
        return Zombie(name)
    elif creatureType == "scribe":
        return Scribe(name)
    elif creatureType == "oracle":
        return Oracle(name)




def loadArchive(name):
    archive = open("./"+name+".lor")
    scrollName = ""
    for line in archive:
        line = line.replace("\n", "")
        if line == "":
            continue
        cmd = line.split(" ")
        if(cmd[0] == "scroll"):
            scrollName = cmd[1]
            scrolls[scrollName] = Scroll(scrollName, [])
            continue
        scrolls[scrollName].spells.append(cmd)

def cast(cmd, caster, enemy):
    spell = cmd[0]
    args = spells[spell]["args"]
    if args == 0:
        spells[spell]["meta"]()
        return

    target = cmd[1]
    if target == "me":
        target = caster
    elif target == "them":
        target = enemy
    if args == 1:
        spells[spell]["meta"](spell, target)
        return
    
    if args == "s":
        spells[spell]["meta"](caster, enemy, target)
        return

    value = cmd[2]
    if value == "me":
        value = creatures[caster].name
    elif value == "them":
        value = creatures[enemy].name
    if args == 2:
        if value in creatures:
            value = creatures[value].stat
        spells[spell]["meta"](target, value)
        return
    
    if args == "c":
        spells[spell]["meta"](value, caster, enemy, target)
        return
    
        

for line in mainFile:
    line = line.replace("\n", "")
    if line == "":
        continue
    cmd = line.split(" ")
    if cmd[0] == "archive":
        loadArchive(cmd[1])
        continue
    cast(cmd, "god", "god")

while True:
    try:
        keys = []
        for key in creatures.keys():
            keys.append(key)
        for key in keys:
            creatures[key].act()

        keys = []
        for key in creatures.keys():
            keys.append(key)
        for key in keys:
            creatures[key].reel()
    except Nuke:
        break
