"""ComfyUI (Z-Image Turbo) で大アルカナ22枚をダーク調で生成し cards/NN.png に保存する。
使い方: py -3 gen_cards.py [カード番号...]   (番号省略で全22枚)
"""
import json, sys, time, urllib.request, urllib.parse, random, pathlib

COMFY = "http://127.0.0.1:8188"
OUT = pathlib.Path(r"D:\PWA\tsukuyomi-tarot\cards")
W, H = 784, 1344  # 7:12
STEPS, CFG, SHIFT = 8, 1.0, 3.0
SEED_BASE = 20261001 + int(__import__("os").environ.get("SEED_OFFSET", "0"))

STYLE = (
    "dark gothic tarot card illustration, {subject}, "
    "ornate black and antique gold art nouveau border frame, "
    "moonlit night, deep shadows, chiaroscuro, muted palette of black, charcoal, deep indigo and tarnished gold, "
    "ink and gold leaf painting, occult symbolism, mystical, eerie, melancholic atmosphere, "
    "highly detailed, vertical portrait composition, centered, the card fills the entire image edge to edge, solid black outer margin, no white border, no text, no letters"
)

CARDS = {
    0:  "The Fool: a cloaked wanderer stepping toward a cliff edge under a crescent moon, a black dog at their heels, a white rose in hand, swirling mist below",
    1:  "The Magician: a hooded figure at a stone altar raising a wand toward the sky, a cup, a sword, a pentacle and a staff on the altar, a glowing infinity sign above the head",
    2:  "The High Priestess: a veiled woman seated between two tall pillars, one black one white, holding a closed scroll, a crescent moon at her feet, pomegranate veil behind her",
    3:  "The Empress: a crowned queen reclining on a throne in a dark overgrown forest, wheat and ripe pomegranates, a shield with the venus symbol, twelve stars in her crown",
    4:  "The Emperor: a stern bearded king on a black stone throne carved with ram heads, holding a scepter and an orb, barren crimson mountains behind",
    5:  "The Hierophant: a robed high priest on a cathedral throne between two pillars, raising two fingers in blessing, two kneeling acolytes, crossed keys at his feet",
    6:  "The Lovers: a man and a woman standing beneath a vast dark angel with spread wings, a serpent coiled in a tree behind the woman, a burning tree behind the man",
    7:  "The Chariot: an armored warrior standing in a stone chariot drawn by one black sphinx and one white sphinx, starry canopy above, a walled city behind",
    8:  "Strength: a woman in a flowing gown gently closing the jaws of a lion, an infinity sign above her head, dark wilderness",
    9:  "The Hermit: an old cloaked hermit on a snowy mountain peak holding a lantern with a glowing six-pointed star, leaning on a staff, vast darkness around",
    10: "Wheel of Fortune: a great wheel inscribed with alchemical symbols floating in storm clouds, a sphinx on top, a serpent descending, a jackal-headed figure rising",
    11: "Justice: a crowned figure seated between pillars holding an upright sword and a set of balanced scales, a dark purple veil behind",
    12: "The Hanged Man: a man suspended upside down by one foot from a living T-shaped tree, hands behind his back, a serene face with a glowing halo",
    13: "Death: a skeletal knight in black armor riding a pale horse carrying a black banner with a white rose, a bishop and a child before it, a distant sun rising between two towers",
    14: "Temperance: a winged angel with one foot in a dark pool and one on the shore pouring water between two cups, a path leading to a glowing crown on the horizon",
    15: "The Devil: a horned demon with bat wings perched on a black stone pedestal, an inverted pentagram on its forehead, two chained figures with small horns below, torch held downward",
    16: "The Tower: a tall stone tower on a crag struck by lightning, its crown blown off, flames bursting from the windows, two figures falling into the dark",
    17: "The Star: a nude woman kneeling by a dark pool pouring water from two jugs, one large glowing star and seven smaller stars in the night sky, an ibis in a tree",
    18: "The Moon: a full moon with a sorrowful face dripping dew between two dark towers, a wolf and a dog howling, a crayfish crawling out of a black pool, a winding path",
    19: "The Sun: a dark sun with a solemn face and black rays, a child riding a white horse holding a red banner, sunflowers over a stone wall, somber twilight",
    20: "Judgement: a great angel blowing a trumpet from storm clouds, grey figures rising from open coffins with raised arms, icy mountains in the distance",
    21: "The World: a dancing figure wrapped in a flowing violet sash inside a laurel wreath, holding two wands, a lion, a bull, an eagle and an angel in the four corners",
}


def workflow(idx, seed):
    prompt = STYLE.format(subject=CARDS[idx])
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "zImageTurbo_turbo.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
        "4": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": SHIFT}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": "text, letters, watermark, signature, blurry, low quality, bright, cheerful"}},
        "7": {"class_type": "EmptySD3LatentImage", "inputs": {"width": W, "height": H, "batch_size": 1}},
        "8": {"class_type": "KSampler", "inputs": {
            "model": ["4", 0], "positive": ["5", 0], "negative": ["6", 0], "latent_image": ["7", 0],
            "seed": seed, "steps": STEPS, "cfg": CFG, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": f"tsukuyomi/card_{idx:02d}"}},
    }


def api(path, data=None):
    req = urllib.request.Request(COMFY + path, data=json.dumps(data).encode() if data else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def generate(idx, seed):
    pid = api("/prompt", {"prompt": workflow(idx, seed)})["prompt_id"]
    while True:
        time.sleep(2)
        h = api(f"/history/{pid}")
        if pid in h:
            st = h[pid]["status"]
            if st.get("status_str") == "error":
                raise RuntimeError(json.dumps(st.get("messages"), ensure_ascii=False)[:800])
            img = h[pid]["outputs"]["10"]["images"][0]
            break
    q = urllib.parse.urlencode({"filename": img["filename"], "subfolder": img.get("subfolder", ""), "type": img["type"]})
    with urllib.request.urlopen(COMFY + "/view?" + q, timeout=120) as r:
        data = r.read()
    OUT.mkdir(exist_ok=True)
    (OUT / f"{idx:02d}.png").write_bytes(data)
    return len(data)


if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or list(range(22))
    for i in ids:
        t = time.time()
        n = generate(i, SEED_BASE + i)
        print(f"{i:02d} done {n//1024} KB {time.time()-t:.0f}s", flush=True)
