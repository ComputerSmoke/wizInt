wizInt is a work-in-progress programming language. wizInt.py is its interpreter. 

Usage: "python wizInt.py [main file] [input file, default: input.txt] [output file, default: console]

The language has spells, scrolls, and creatures. Spells are operations defined by the language. Scrolls are a list of spells, to be cast in order. Creatures take an action each tick based on their type.

Creatures have a stat, realm, and scroll. Stat is stored asa string, but converted to a float for mathematical operations.
Having certain stats causes some creatures to die. Each tick has an action phase where creatures take primary actions (such as casting), and a reaction phase where creatures take lower-priority actions (such as a scribe printing to console).

Creature types:

wizard - casts their scroll targeting another creature in the same realm

goblin - dies if stat <= 0

zombie - dies if stat == 0

oracle - copies the text of the input file to their stat on creation

scribe - prints their stat to the console

Scrolls are defined in archives, files ending in .lor. Import an archive in main.inn with "archive [name]"

Spells:

summon [type] [name] - summons a creature of specified name and type.

give [creature] [scroll] - gives a scroll to a creature.

teleport [target] [realm] - teleports target creature to a realm. Realm names can be an int or a string. Wizards will only cast
    spells on creatures who share their realm.

fireball [target] [amount] - reduce target creature's stat by amount.

bleed [target] [amount] - divide target creature's stat by amount.

kill [target] - Kill target creature.

imprint [target] [thought] - Change target's stat to thought. 

curse [target] - Not implemented. Likely to make creature die when current scroll completes execution.

sling [spell] - Cast a spell or scroll, and fizzle this scroll if it fizzles.

cast [spell] - Cast a spell or scroll, taking precautions to avoid fizzling if it does.

brew [spell] [ingredient] - Use a creature to cast a spell. This does not destroy the creature. If the specified creature does not
    exist, the spell is not cast. Not protected from fizzles.

tinker [spell] [ingredient] - Like brew but protected from fizzles.

skim [target] [string] [start] [end] - Set target's state to substring of string, starting at start (inclusive), and ending at end (exclusive)

nuke - a powerful spell that immedietly ends all reality when cast

fizzle - Cause the current scroll to fail, as well as any parent scrolls that did not protect themselves from fizzles.

Notes on spells:
Keywords me and them can be used to in scrolls to refer to the caster of the spell, and the creature in their realm they are casting on.

Do not surround strings with quotation marks. When scribes print, underscores will be replaced with spaces (for now).

Using a creature's name instead of an amount will treat that creature's stat as the amount.

