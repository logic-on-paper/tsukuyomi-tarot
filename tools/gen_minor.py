"""小アルカナ56枚を生成して cards/22.jpg〜77.jpg 用の PNG を作る。使い方: py -3 gen_minor.py [番号...]"""
import sys, time
sys.path.insert(0, ".")
import gen_cards as g

SUITS = {
    "wands": "wooden staffs sprouting green leaves",
    "cups": "ornate golden chalices",
    "swords": "steel swords",
    "pentacles": "large golden coins engraved with pentagrams",
}
SCENES = {
 "wands": [
  "Ace of Wands: a hand emerging from dark clouds holding a single sprouting wooden staff, a castle on a distant hill",
  "Two of Wands: a man on a castle battlement holding a small globe and a staff, a second staff fixed to the wall, looking out over a dark sea",
  "Three of Wands: a merchant standing on a cliff with three staffs planted beside him, watching ships sail on a moonlit sea",
  "Four of Wands: four staffs forming a garland gate, two figures dancing before a castle, a quiet night celebration",
  "Five of Wands: five youths brandishing staffs in a chaotic mock battle on dark ground",
  "Six of Wands: a rider crowned with laurel on a horse holding a staff with a wreath, a crowd with staffs around",
  "Seven of Wands: a man on a hilltop defending himself with a staff against six staffs thrust up from below",
  "Eight of Wands: eight staffs flying diagonally through the night sky over a river and a castle",
  "Nine of Wands: a bandaged weary man leaning on a staff, eight staffs standing behind him like a fence",
  "Ten of Wands: a man bent under the weight of ten staffs carrying them toward a distant town",
  "Page of Wands: a youth in a desert holding a tall sprouting staff, gazing up at it, pyramids in the distance",
  "Knight of Wands: an armored knight on a rearing horse holding a staff, desert pyramids behind",
  "Queen of Wands: a queen on a throne holding a staff and a sunflower, a black cat at her feet, lions carved on the throne",
  "King of Wands: a king on a throne holding a sprouting staff, salamanders and lions carved on the throne, a salamander at his feet",
 ],
 "cups": [
  "Ace of Cups: a hand emerging from clouds holding a chalice overflowing with water, a dove descending, a lotus pond below",
  "Two of Cups: a man and a woman exchanging chalices, a winged lion head above a caduceus between them",
  "Three of Cups: three women dancing in a circle raising chalices in a harvest garden at night",
  "Four of Cups: a young man sitting under a tree with arms crossed, three chalices before him, a hand from a cloud offering a fourth",
  "Five of Cups: a black-cloaked figure mourning three spilled chalices, two upright chalices behind, a bridge and castle in the distance",
  "Six of Cups: a child giving a chalice filled with white flowers to a smaller child in an old stone courtyard",
  "Seven of Cups: a silhouetted figure facing seven chalices floating in clouds holding a castle, jewels, a wreath, a dragon, a serpent and a veiled figure",
  "Eight of Cups: a cloaked figure walking away from eight stacked chalices toward dark mountains under an eclipsed moon",
  "Nine of Cups: a satisfied man seated with arms crossed before nine chalices arranged on a curved shelf",
  "Ten of Cups: a couple with raised arms beneath a rainbow of ten chalices, two children dancing, a cottage by a river",
  "Page of Cups: a youth by the sea holding a chalice from which a fish peeks out",
  "Knight of Cups: a knight on a slowly walking white horse holding a chalice before him, a river in the dark",
  "Queen of Cups: a queen on a throne at the edge of the sea holding an ornate closed chalice, gazing into it",
  "King of Cups: a king on a stone throne floating on a dark sea holding a chalice and a scepter, a ship and a leaping fish behind",
 ],
 "swords": [
  "Ace of Swords: a hand emerging from clouds holding an upright sword crowned with a wreath, barren mountains below",
  "Two of Swords: a blindfolded woman seated holding two crossed swords, a crescent moon and a still sea behind her",
  "Three of Swords: a large heart pierced by three swords under storm clouds and rain",
  "Four of Swords: a knight's stone effigy lying on a tomb in a chapel, three swords on the wall above and one beneath",
  "Five of Swords: a smirking man gathering swords while two defeated figures walk away under a stormy sky",
  "Six of Swords: a ferryman poling a boat carrying a cloaked woman and child across calm water, six swords standing in the boat",
  "Seven of Swords: a man sneaking away from a camp of tents carrying five swords, two swords left behind",
  "Eight of Swords: a bound and blindfolded woman surrounded by eight swords planted in the ground, a castle on a cliff behind",
  "Nine of Swords: a figure sitting up in bed holding their face in despair, nine swords hanging on the dark wall",
  "Ten of Swords: a figure lying face down with ten swords in their back, a black sky with a thin dawn on the horizon",
  "Page of Swords: a youth holding a sword aloft on a windy hill, clouds rushing past",
  "Knight of Swords: a knight charging on a galloping horse with sword raised, storm clouds streaking",
  "Queen of Swords: a stern queen on a throne holding an upright sword, her other hand extended, clouds gathering",
  "King of Swords: a king on a throne holding an upright sword, butterflies carved on the throne, a stormy sky",
 ],
 "pentacles": [
  "Ace of Pentacles: a hand emerging from clouds holding a large golden coin engraved with a pentagram, a garden with an arched gate below",
  "Two of Pentacles: a youth dancing while juggling two coins joined by an infinity ribbon, ships on tall waves behind",
  "Three of Pentacles: a stone mason working in a cathedral while a monk and an architect look on, three pentacles carved in the arch",
  "Four of Pentacles: a man clutching a coin to his chest, one balanced on his head and two under his feet, a city behind",
  "Five of Pentacles: two beggars walking through snow past a lit stained glass church window showing five pentacles",
  "Six of Pentacles: a merchant weighing coins on a scale and giving alms to two kneeling beggars",
  "Seven of Pentacles: a farmer leaning on a hoe gazing at a vine bearing seven golden pentacles",
  "Eight of Pentacles: a craftsman carving pentacles at a workbench, finished coins hung on a post beside him",
  "Nine of Pentacles: an elegant woman in a vineyard with a hooded falcon on her hand, nine pentacles among the vines",
  "Ten of Pentacles: an old man with two dogs beneath an archway, a family beyond, ten pentacles arranged like a tree of life",
  "Page of Pentacles: a youth in a plowed field holding up a golden coin in both hands, gazing at it",
  "Knight of Pentacles: a knight on a still black horse holding a golden coin, plowed fields behind",
  "Queen of Pentacles: a queen on a throne in a garden of roses holding a golden coin, a rabbit nearby",
  "King of Pentacles: a king on a throne carved with bulls holding a coin and a scepter, grapes and vines, a castle behind",
 ],
}

ORDER = ["wands", "cups", "swords", "pentacles"]
PROMPTS = {}
idx = 22
for suit in ORDER:
    for scene in SCENES[suit]:
        PROMPTS[idx] = f"{scene}, the {SUITS[suit]} clearly visible"
        idx += 1
assert idx == 78

g.CARDS.update(PROMPTS)

if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or list(range(22, 78))
    for i in ids:
        t = time.time()
        n = g.generate(i, g.SEED_BASE + i)
        print(f"{i:02d} done {n//1024} KB {time.time()-t:.0f}s", flush=True)
