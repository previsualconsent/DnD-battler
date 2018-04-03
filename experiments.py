__author__ = 'Matteo'
__doc__ = """
The reason why I wrote the script was to run some tests.
"""

N = "\n"
T = "\t"
# N="<br/>"

import DnD, csv


def cr_appraisal(party):
    """
    Assess the victory probability of each monster in the manual against Creatures in the `party` Encounter
    :param party: a list of creatures
    :return:
    """
    # set to same team
    for pc in party:
        pc.alignment = "players"
    out = csv.DictWriter(open("CR stats.csv", 'w', newline=''),
                         fieldnames=['beast', 'victory'])  # DnD.Encounter().json() is overkill and messy
    out.writeheader()
    # challenge each monster
    for beastname in DnD.Creature.beastiary:
        beast = DnD.Creature(beastname)
        beast.alignment = "opponent"
        party.append(beast)  # seems a bit wrong, but everything gets hard reset
        party.go_to_war(100)
        print(beastname + ": " + str(party.tally['victories']['players']) + "%")
        out.writerow({'beast': beastname, 'victory': party.tally['victories']['players']})
        party.remove(beast)  # will perform a hard reset by default


def commoner_brawl(n=5000):
    achilles = DnD.Creature("Achilles", base='commoner', alignment='Achaeans')
    patrocles = DnD.Creature("Patrocles", base='commoner', alignment='Achaeans')
    hector = DnD.Creature("Hector", base='commoner', alignment='Trojans')
    print(achilles.attacks[0]['damage'])
    ratty= DnD.Creature("giant rat")
    rattie = DnD.Creature("giant rat")
    for d in [DnD.Dice(1, [2], role="damage"),
              DnD.Dice(0, [4], role="damage"),
              DnD.Dice(-1, [6], role="damage"),
              DnD.Dice(-1, [2, 3], role="damage"),
              DnD.Dice(1, [4], role="damage"),
              DnD.Dice(0, [6], role="damage"),
              DnD.Dice(-1, [8], role="damage"),
              DnD.Dice(2, [2], role="damage"),
              DnD.Dice(0, [2, 3], role="damage"),
              DnD.Dice(-1, [3, 4], role="damage")]:
        achilles.attacks[0]['damage'] = d
        print(d,T, T.join([str(DnD.Encounter(*party).go_to_war(n).tally['victories']['Achaeans']) for party in [(achilles, hector),(achilles, ratty),(achilles, patrocles,ratty),(achilles, patrocles,ratty,rattie)]]))

def dice_variance(d):
        return sum([sum([(i+1-(d2+1)/2)**2 for i in range(d2)])/d2 for d2 in d.dice])

def WizardVsGoblin(attack):
#'ability_bonuses': {'int': 0, 'cha': 0, 'dex': 0, 'con': 0, 'str': 0, 'wis': 0},
   wizard = DnD.Creature({
      'name': 'Wizard',
      'alignment': 'player',
      'level': 3,
      'str': 10,
      'dex': 16,
      'con': 10,
      'int': 16,
      'wis': 10,
      'cha': 10,
      'ac': 13,
      'hp': 17,
      'starting_hp': 17,
      'hd': 6,
      'proficiency': 2,
      'attack_parameters': [attack],
      #'attack_parameters': [],
      })
   print attack
   nbattles = 100000
   goblin = DnD.Creature("goblin")
   goblin.alignment = "opponent"
   e = DnD.Encounter(wizard, goblin)
   e.go_to_war(nbattles)
   import numpy as np
   finalhp = np.array([x if x > 0 else 0 for x in wizard.tally['finalhp']])
   bins = range(wizard.hp+1)
   plt.hist(finalhp, bins, alpha=0.5, label=attack[0], normed=1, cumulative=0)
   values, _ =  np.histogram(finalhp, bins)
   print values, bins
   print sum(values/nbattles *bins[1:])
   #e.battle()
   #for line in e.masterlog:
      #print line


if __name__ == "__main__":
    # cr_appraisal(DnD.Encounter('my druid','my barbarian','mega_tank', "netsharpshooter"))
    from matplotlib import pyplot as plt
    WizardVsGoblin(["Dagger", 5, 3, 4])
    WizardVsGoblin(["Firebolt", 5, 0, 10])
    plt.legend(loc="upper left")
    plt.xlabel("Final Wizard HP")
    plt.ylabel("Percent[%]")
    plt.show()
    plt.savefig("attacks.png")
    #print(dice_variance(DnD.Dice(0, [100], role="damage")))
