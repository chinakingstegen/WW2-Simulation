#!/usr/bin/env python3
"""
WORLD WAR II: GRAND STRATEGY SIMULATION (Tkinter Edition, v2)
Inspired by classroom simulations like historysimulation.com.

SIMPLIFIED RULES:
- 16 major powers (plus 45 greyed-out minor countries filling the rest of the land) on a real (simplified equirectangular) world map, positioned
  by actual latitude/longitude. Designed for a GROUP playing on one shared
  device (hotseat). Every country is playable - use "Acting as" to switch.
- Everyone on the same side (Axis or Allies) is automatically an ally.
  Neutral countries are free agents: no allies, may attack anyone.
- EVERY COUNTRY IS A TERRITORY ON THE MAP, DIVIDED INTO 3 ZONES (West /
  Center / East, or North / Center / South) and marked with names. Zones
  are colored by political allegiance - RED = Axis, BLUE = Allied,
  YELLOW = Neutral - and flip color once the opposing side's troops
  claim them (troops that just arrive in an unclaimed zone do not change
  its color; they must attack it first). A country's Territory % is the share of its own 3 zones it
  still controls; lose all 3 and it is defeated. A small flag on a zone
  shows who occupies it.
- ARMIES ARE VISIBLE ON THE MAP. Every country starts with forces stationed
  at home. Each force type gets its own box with the owner's FLAG behind it:
    * Army (T) stands on land, on the country.
    * Navy (anchor icon) sits in the waters, at that country's naval base
      out at sea, joined to the country by a dotted line.
    * Air Force (wing icon) hovers in the sky in front of a plane silhouette.
- REINFORCEMENTS: there is no money and nothing to build. At the start of
  every new year, each country whose CENTER zone has not been conquered is
  topped up with troops there until its army matches its real historical size for
  that year (see ARMY_STRENGTH_K; 1 troop = SOLDIERS_PER_TROOP soldiers). Starting
  navy and air forces are x100 (UNIT_SCALE), and navies are x3 on top of that
  (NAVY_SIZE_MULT). France is the exception: it only gains troops in 1941
  (TROOP_GAIN_ONLY_IN_YEARS / YEARLY_TROOP_GAIN_OVERRIDE).
- TERRAIN AND WINTER: every land zone has terrain (plains, forest, hills, mountains, jungle
  or desert; see ZONE_TERRAIN). Rough terrain helps the DEFENDERS (hills +15%, mountains
  +30%, jungle +20%, forest +10%) and desert hurts attackers (supply, -8%). The battle
  panel shows the terrain and clicking a zone names it. In winter (the Nov-Dec and Jan-Feb
  turns; the header shows "(Winter)") attackers fight weaker the further from the equator
  the zone is: cold -8%, harsh -15% (defenders suffer 40% of that). Troops
  from cold countries (USSR, Finland, Canada, Norway, Sweden...) suffer far less
  (WINTER_HARDENED). Bots take both into account when choosing their attacks.
- MOVE / ATTACK: CLICK AND DRAG one of your force boxes (army, navy or air)
  and DROP it on any zone. A window asks how many units to send.
    * There is no separate movement phase: on your side's War Phase you may
      both MOVE and BATTLE. Axis act in the Axis War Phase; Allies and
      Neutrals act in the Allied War Phase.
    * Dropping forces on an enemy zone = ATTACK; sending forces to an ally or
      your own country = REPOSITION.
    * Troops move one zone at a time, only to a zone that shares a border with theirs,
      and can't step straight into another country's center (fight through its border
      zones first; landings by sea or air follow the same rule). Air force can fly up
      to 2 zones in one move.
    * Troops crossing the sea (between Eurasia, Britain, Japan, North
      America, Australia) need Navy to carry them: 1 Navy per 1 troop.
      A fleet can only land troops on zones that BORDER its own sea zone, so
      sail it along the coast first. The troops are ferried from your biggest
      rested stack elsewhere (never from the zone they are landing in).
    * Air force can also AIRLIFT troops: drag an air box onto a land zone within
      range, choose "Airlift troops", and 1 Air carries 1 troop (from the same zone).
      The planes fly there with the troops, and both rest for a turn.
    * A fleet only ferries troops ashore and always stays at sea (it can never be
      sent onto a land zone), so it can land troops again every turn.
    * Distant targets take a few turns to reach; forces en route are drawn
      as a box on a dashed line.
    * A country may launch as many attacks per turn as it has rested forces for.
    * Units that move or attack must REST: they can't be moved again or used
      to attack until a full turn has passed (see MOVE_COOLDOWN_TURNS).
      Newly built units are ready immediately.
      In SINGLE PLAYER, resting units can never attack (no exceptions); only the
      troops that just arrived rest when they join a stack.
- COMBAT: Only troops fight troops (on land) and only navy fights navy (at sea);
  air force never fights, so the winner is decided by troops/navy alone.
  Air force instead BOMBS: each country has 2 bombings in total (BOMBINGS_PER_COUNTRY) and may use only
  1 per battle (tick the box in the battle window); bombings from different
  countries stack (each bombing = -10% enemy power in that battle). DEFENDERS BOMB TOO:
  when a battle is started, every defending country with air force in the zone may bomb
  the attackers the same way - the battle window has a tick box for them next to the
  attackers' (a small window asks you instead when a bot attacks you; bots decide for
  themselves). Defenders can only choose to bomb: nobody can attack or start a battle
  outside their own side's War Phase. Moving forces into a
  zone held by enemy troops does NOT start a fight by itself: the armies just
  stand there (the zone is outlined in red). During a war phase, CLICK the
  contested zone to start the battle. Likewise, moving troops into an undefended
  enemy zone does not claim it (orange dotted outline): they must ATTACK it - click
  the zone in your War Phase - to take it. Resting troops can't attack, but a single
  rested troop is enough. The side whose turn it is (the attacker)
  loses some army rating (ATTACKER_PENALTY), so the defense has the advantage.
  A battle plays out over BATTLE_TICKS ticks (BATTLE_TICK_MS apart): every force in it
  loses numbers a little at a time until the fight ends. Swords swing from the fighting
  countries and clash in sparks; if air force bombs the battle, planes fly over and
  bombs fall from the sky and explode.
  The loser's forces in the battle are destroyed; the winner loses a
  share depending on how close the fight was. Winning against a country
  takes territory and a share of its oil. Undefended countries are simply
  occupied.
- OIL is the only resource. It is produced each year, can be traded to
  friends, and is captured when you win battles.
- The game begins in January 1939 (Axis War Phase). Every time you End Phase
  the calendar advances 2 months (MONTHS_PER_TURN), so 6 turns = 1 year.
  Phases alternate Axis War -> Allied War. Oil production, reinforcements and
  historical events happen each January. The war ends at the start of 1946.
- SMALL COUNTRIES (Belgium, Netherlands) have a single CENTER zone (no West or
  East). Its army and air forces are shown in a box above the country, joined to it
  by a line (the navy sits in the water). Forces sent there arrive instantly. Drop forces on the box (or on the
  country itself) to send them there.
- Each country has a chain of historical objectives that follows its part in the
  war. Only one is shown at a time: achieve it, claim its oil reward during your
  War Phase, and your next objective appears.

GAME MODES (chosen on the welcome screen):
- HOTSEAT: the original mode above; a group plays every country.
- SINGLE PLAYER: pick one country. You can only give orders as that country (the
  "Acting as" box is locked). Every other major power is played by a bot that follows
  the same rules as you. When you press End Phase the calendar advances, the other
  side's bots play their War Phase, and control returns to you. Bots on your own side
  move at the start of your phase. Bots stay home until a war exists (the game's
  scripted declarations, a historical schedule in BOT_WAR_SCHEDULE, or an attack), then
  garrison their borders, attack when the odds are good, march toward the nearest
  enemy, land troops from the sea, and bomb in close battles. Their aggression is tuned
  by BOT_ATTACK_MARGIN. If your country is defeated the game ends with final standings.
  EVERY GAME IS DIFFERENT: historical events and the wars bots fight keep their exact
  dates, but each game gives every bot a fixed attacking style plus a mood each turn, and
  the bots vary their targets, force sizes, landings and marches (BOT_* chances).
  Hotseat mode is unchanged.

Run with:  python3 ww2_gui_simulation.py
(Tkinter ships with standard Python - no extra installs needed.)
"""

import math
import random
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, scrolledtext

# ----------------------------------------------------------------------
# MAP: simplified real-world coastlines (approximate lat/lon polygons)
# ----------------------------------------------------------------------

CONTINENTS = {
    "North America": [
        (-168, 66), (-165, 68), (-155, 71), (-140, 70), (-128, 70), (-110, 74),
        (-95, 78), (-80, 73), (-70, 68), (-65, 60), (-60, 50), (-55, 48),
        (-60, 46), (-64, 45), (-66, 44), (-70, 43), (-70, 41), (-74, 40.5),
        (-75, 39), (-76, 37), (-75.5, 35), (-77, 34), (-79, 33), (-80, 32),
        (-81, 31), (-80.5, 28), (-80, 25.5), (-81, 25), (-83, 29), (-85, 30),
        (-89, 30), (-94, 29.5), (-97, 26), (-97, 22), (-95, 18), (-91, 16),
        (-87, 14), (-83, 9), (-79, 8), (-83, 10), (-86, 12), (-90, 14),
        (-92, 15), (-95, 16), (-97, 18), (-105, 20), (-106, 23), (-109, 23),
        (-114, 28), (-114, 31), (-117, 32), (-118, 34), (-121, 36), (-122, 37),
        (-124, 40), (-124, 44), (-124, 46), (-124, 48), (-123, 49), (-130, 54),
        (-135, 58), (-140, 59), (-150, 60), (-160, 59), (-165, 60), (-168, 66),
    ],
    "South America": [
        (-77, 8), (-79, 2), (-80, -4), (-81, -6), (-81, -10), (-77, -14),
        (-75, -15), (-71, -18), (-70, -20), (-70, -23), (-70, -27), (-71, -30),
        (-71, -33), (-73, -37), (-73, -40), (-72, -43), (-72, -46), (-72, -50),
        (-70, -52), (-68, -54), (-65, -55), (-68, -52), (-66, -48), (-65, -45),
        (-62, -40), (-60, -36), (-58, -35), (-57, -34), (-58, -33), (-56, -30),
        (-54, -25), (-48, -25), (-44, -23), (-41, -18), (-39, -13), (-38, -13),
        (-35, -9), (-35, -6), (-38, -4), (-43, -2), (-48, 0), (-50, 0),
        (-51, 1), (-53, 2), (-58, 6), (-60, 8), (-62, 9), (-67, 10),
        (-71, 11), (-74, 11), (-77, 8),
    ],
    "Eurasia": [
        (-10, 36), (-9, 43), (-1.5, 46), (0, 48.5), (2, 50.5), (4, 53),
        (8, 55), (8.5, 57.5), (11, 59), (10.5, 63), (15, 66), (20, 69.5),
        (25, 70), (30, 70), (40, 68), (50, 68), (60, 70), (75, 72), (90, 73), (110, 74),
        (130, 75), (145, 68), (150, 60), (143, 52), (140, 50), (135, 43),
        (131, 42), (130, 40), (126, 37), (122, 30), (120, 24), (110, 18),
        (108, 10), (105, 8), (102, 4), (100, 8), (98, 12), (95, 15),
        (92, 22), (88, 22), (86, 20), (80, 8), (77, 8), (75, 12), (73, 17),
        (70, 22), (65, 25), (60, 25), (56, 26), (52, 25), (48, 14), (44, 12),
        (43, 16), (38, 20), (35, 28), (32, 31), (34, 34), (36, 36), (30, 36),
        (23, 36), (20, 39), (15, 38), (12, 38), (9, 40), (3, 40), (-2, 36),
        (-10, 36),
    ],
    "Africa": [
        (-17, 21), (-16, 16), (-15, 12), (-11, 7), (-9, 5), (-8, 4.5),
        (-4, 5), (2, 5), (3, 6), (5, 4), (8, 4), (9, 2), (9, -1), (12, -2),
        (12, -5), (13, -6), (12, -9), (13, -13), (13, -17), (14, -22),
        (17, -27), (18, -30), (20, -34), (22, -34), (25, -33.5), (28, -32),
        (30, -30), (31, -26), (32, -25), (33, -23), (35, -20), (40, -17),
        (40, -11), (42, -5), (43, -1), (41, 2), (43, 5), (45, 8), (45, 11),
        (43, 12), (40, 11), (39, 11), (37, 15), (34, 18), (33, 22), (35, 27),
        (32, 31), (30, 31.5), (25, 32), (20, 32), (15, 32), (11, 33), (9, 32),
        (9, 30), (8, 28), (9, 25), (8, 22), (0, 21), (-5, 20), (-10, 20),
        (-15, 20), (-17, 21),
    ],
    "Australia": [
        (113, -22), (114, -26), (114, -29), (115, -33.5), (117, -35),
        (120, -34), (124, -32.5), (129, -31.7), (131, -32), (134, -32.5),
        (136, -35), (138, -35.5), (140, -38), (144, -38.3), (147, -38.5),
        (150, -37), (150, -33.5), (153, -29), (153, -25), (151, -24),
        (149, -21), (146, -19), (145, -16), (143, -14), (141, -11),
        (137, -12), (132, -12), (130, -12), (129, -15), (126, -14),
        (123, -17), (121, -18), (117, -20), (113, -22),
    ],
}

MAP_W, MAP_H = 1200, 600

# Single player: how long the camera stays on each bot move before the next one happens.
BOT_MOVE_DELAY_MS = 1500      # pause on a bot troop movement
BOT_BATTLE_DELAY_MS = 2500    # pause on a bot battle

# Battles are not instant: the losses are spread over this many ticks, one every
# BATTLE_TICK_MS milliseconds, so both armies visibly shrink until the fight ends.
BATTLE_TICKS = 5
BATTLE_TICK_MS = 400
BOMBINGS_PER_COUNTRY = 2      # air force bombings each country has for the whole game
BATTLE_FX_FRAMES = 8          # animation frames per tick (swords swinging, bombs falling)


def project(lon, lat):
    """Equirectangular projection: lon/lat -> canvas x/y."""
    x = (lon + 180) / 360 * MAP_W
    y = (90 - lat) / 180 * MAP_H
    return x, y


# ----------------------------------------------------------------------
# UNITS
# ----------------------------------------------------------------------

UNIT_KEYS = ("army", "navy", "air")

UNIT_TYPES = {
    "army": {"label": "Troops",    "short": "T", "power": 1.0},
    "navy": {"label": "Navy",      "short": "N", "power": 1.0},
    "air":  {"label": "Air Force", "short": "A", "power": 1.0},
}

TROOPS_PER_SHIP = 1       # troops crossing the sea need 1 navy per this many troops
TROOPS_PER_PLANE = 1      # airlift: 1 air force unit carries this many troops
AIR_MOVE_SPACES = 2       # air force can fly this many zones (borders) in one move
NAVY_MOVE_ZONES = 5       # a fleet can sail through at most this many sea zones in one move
GROUND_BORDER_PX = 2.5    # land zones whose outlines come this close (map px) share a border
AIR_GAP_PX = 5            # air force also counts zones across a narrow strait (e.g. the Channel)
# ---- terrain and winter (land battles only) ----
# terrain -> (label, attacker power x, defender power x)
TERRAIN_EFFECTS = {
    "plains":    ("Plains",    1.00, 1.00),
    "forest":    ("Forest",    1.00, 1.10),
    "hills":     ("Hills",     1.00, 1.15),
    "mountains": ("Mountains", 0.95, 1.30),
    "jungle":    ("Jungle",    0.95, 1.20),
    "desert":    ("Desert",    0.92, 1.00),
}
# country -> terrain of its zones: one name for all three, or one per zone (in zone order).
# Countries that aren't listed are plains.
ZONE_TERRAIN = {
    "Germany": ("hills", "hills", "plains"), "France": ("plains", "plains", "hills"),
    "Italy": ("mountains", "hills", "hills"), "Japan": ("hills", "mountains", "hills"),
    "USSR": ("plains", "forest", "forest"), "USA": ("mountains", "plains", "forest"),
    "UK": ("hills", "hills", "plains"), "Poland": ("plains", "plains", "forest"),
    "China": ("desert", "mountains", "plains"), "Belgium": "forest",
    "Romania": "hills", "Finland": "forest", "Canada": ("mountains", "forest", "forest"),
    "Australia": ("desert", "desert", "forest"), "India": ("plains", "hills", "jungle"),
    "Spain": ("hills", "hills", "mountains"), "Norway": "mountains", "Sweden": "forest",
    "Czechoslovakia": "hills", "Yugoslavia": "hills", "Greece": "mountains", "Turkey": "hills",
    "Iraq": ("hills", "desert", "desert"), "Iran": ("mountains", "desert", "desert"),
    "Saudi Arabia": "desert", "Afghanistan": "mountains", "Pakistan": ("desert", "plains", "plains"),
    "Mongolia": ("hills", "desert", "plains"), "Korea": "hills", "Syria": ("hills", "plains", "desert"),
    "Tibet": "mountains", "Burma": "jungle", "Thailand": "jungle", "Indochina": "jungle",
    "Morocco": ("hills", "mountains", "hills"), "Algeria": ("hills", "desert", "desert"),
    "Libya": "desert", "Egypt": "desert", "French West Africa": ("desert", "desert", "plains"),
    "French Equatorial Africa": ("desert", "jungle", "jungle"), "Sudan": ("desert", "plains", "plains"),
    "Ethiopia": "mountains", "Nigeria": ("desert", "jungle", "jungle"), "Belgian Congo": "jungle",
    "British East Africa": ("plains", "hills", "jungle"), "Angola": ("jungle", "plains", "desert"),
    "Mozambique": ("plains", "plains", "jungle"), "South Africa": ("desert", "hills", "hills"),
    "Brazil": "jungle", "Argentina": ("plains", "plains", "mountains"), "Chile": "mountains",
    "Peru": ("mountains", "jungle", "jungle"), "Bolivia": ("jungle", "mountains", "hills"),
    "Colombia": ("jungle", "mountains", "jungle"), "Venezuela": "jungle", "Paraguay": "plains",
    "Mexico": ("desert", "hills", "jungle"), "Alaska": ("mountains", "forest", "forest"),
    "Central America": "jungle", "Portugal": "hills", "Iceland": "mountains",
    "Greenland": "mountains", "Sardinia": "hills", "Cuba": "jungle", "Hispaniola": "jungle",
    "Madagascar": "jungle", "Sri Lanka": "jungle", "Taiwan": "mountains", "Luzon": "jungle",
    "Mindanao": "jungle", "Sumatra": "jungle", "Java": "jungle", "Borneo": "jungle",
    "Sulawesi": "jungle", "New Guinea": "jungle", "New Zealand North": "hills",
    "New Zealand South": "mountains", "Tasmania": "forest", "Kazakhstan": "plains",
}
# Winter: the turns of the year that are winter in the north (0 = Jan-Feb ... 5 = Nov-Dec); the
# southern hemisphere is half a year later. How cold depends on latitude (|lat| >= first value).
WINTER_TURNS_NORTH = (0, 5)
WINTER_TURNS_SOUTH = (2, 3)
WINTER_SEVERITY = ((50, 0.15, "Harsh winter"),
                   (40, 0.08, "Cold winter"))
WINTER_DEFENDER_SHARE = 0.4    # defenders (dug in, supplied) suffer this share of the attackers' penalty
WINTER_HARDENED = {"USSR": 0.35, "Finland": 0.2, "Canada": 0.35, "Norway": 0.35,
                   "Sweden": 0.35, "Mongolia": 0.35, "Iceland": 0.35}  # share of the penalty they suffer

ATTACKER_PENALTY = 0.9    # the side whose turn it is (the attacker) fights at -10%,
                          # so the defending side has the advantage
UNIT_SCALE = 100          # starting forces are multiplied by this
NAVY_SIZE_MULT = 3        # ...and every country's starting navy is this many times bigger still
SEA_COAST_PX = 2.5        # a land zone borders a sea zone when its outline comes this close
SEA_JITTER = 0.22         # sea zone seeds wander this fraction of a cell off the grid (organic shapes)
SEA_WIGGLE = 0.17         # how wavy the borders between sea zones are (fraction of edge length)
SOLDIERS_PER_TROOP = 250  # 1 "troop" in the game = this many real soldiers (see ARMY_STRENGTH_K)
UNIT_BOX_SCALE = 0.75     # size of force boxes on the map (0.75 = three-quarter size)
OIL_REWARD_DIVISOR = 10   # objective_reward / this = oil paid for completing an objective
OIL_DECAY_RATE = 0.10       # share of every country's oil stockpile lost each new year
# Small countries show the forces in their CENTER zone in a box drawn above the country
# and joined to it by a plain line. Forces sent into the center zone arrive instantly.
# nation: (dx, rise). dx = horizontal offset of the box center from the country center;
# rise = how many pixels above the country center the box's bottom edge sits.
SMALL_COUNTRY_BOX = {
    "Belgium": (50, 55),
    "Netherlands": (-45, 70),
}
MOVE_COOLDOWN_TURNS = 1   # units that moved rest for one turn before acting again
START_YEAR = 1939
GERMANY_EXTRA_OPENING_MOVES = 3   # extra peacetime moves the German bot makes per turn before the Poland invasion
END_YEAR = 1946
TURNS_PER_YEAR = 6        # each End Phase = one turn = 2 months
MONTHS_PER_TURN = 12 // TURNS_PER_YEAR
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]


def new_units(army=0, navy=0, air=0):
    return {"army": army, "navy": navy, "air": air}


def units_total(u):
    return sum(u[k] for k in UNIT_KEYS)


def units_power(u, nation=None):
    """Return force power, optionally scaled by the owner's ratings."""
    if nation is None:
        return sum(u[k] * UNIT_TYPES[k]["power"] for k in UNIT_KEYS)
    ratings = {"army": nation.army_rating, "navy": nation.navy_rating,
               "air": nation.air_rating}
    return sum(u[k] * UNIT_TYPES[k]["power"] * ratings[k] / 5 for k in UNIT_KEYS)


def fmt_count(n, compact):
    if compact and n >= 1000:
        return f"{n / 1000:.1f}".rstrip("0").rstrip(".") + "k"
    return str(n)


def units_text(u, compact=False):
    parts = [f"{UNIT_TYPES[k]['short']}{fmt_count(u[k], compact)}"
             for k in UNIT_KEYS if u[k] > 0]
    return " ".join(parts) if parts else "-"


def scale_units(u, keep):
    """Return a new unit dict keeping the given fraction of each unit type."""
    return {k: int(round(u[k] * keep)) for k in UNIT_KEYS}


# ----------------------------------------------------------------------
# DATA: 16 NATIONS
# name, side, (lat, lon), oil, stability, objective text,
# objective_reward (paid as oil, /OIL_REWARD_DIVISOR), goal, starting forces (troops, navy, air)
#
# "goal" describes what must be TRUE before the reward can be claimed.
# Every key present must be satisfied:
#   "beat":      list of nations this country must have won a battle against
#   "wins":      total number of battles this country must have won
#   "zones":     minimum number of your own 3 zones to be holding
#   "oil":       minimum oil stockpile to be holding
#   "year":      the earliest year the goal can be claimed
# ----------------------------------------------------------------------

NATION_DATA = [
    ("Germany",     "Axis",    (51.0, 10.0),   40, 75,
     "Expand Lebensraum and dominate continental Europe.", 400,
     {"beat": ["Poland", "France"]}, (12, 3, 8)),
    ("Italy",       "Axis",    (42.5, 12.5),   15, 50,
     "Build a new Roman Empire around the Mediterranean.", 200,
     {"beat": ["France"]}, (8, 3, 4)),
    ("Japan",       "Axis",    (36.0, 138.0),  30, 70,
     "Secure oil in Asia/Pacific for the empire.", 300,
     {"oil": 50}, (10, 6, 6)),
    ("USSR",        "Allies",  (56.0, 45.0),   80, 60,
     "Defend the homeland and expand influence in Eastern Europe.", 350,
     {"beat": ["Finland"]}, (7, 2, 6)),
    ("USA",         "Allies",  (39.0, -98.0),  100, 85,
     "Support the Allies and project power once drawn into war.", 400,
     {"beat": ["Japan"]}, (8, 6, 6)),
    ("UK",          "Allies",  (54.0, -2.5),   30, 80,
     "Preserve the Empire and defeat Axis aggression in Europe.", 350,
     {"zones": 3, "year": 1944}, (6, 6, 5)),
    ("France",      "Allies",  (47.0, 2.5),    20, 55,
     "Defend the homeland from German aggression.", 250,
     {"zones": 2, "year": 1942}, (10, 2, 3)),
    ("Poland",      "Allies",  (52.0, 19.0),   5, 60,
     "Preserve independence against German and Soviet pressure.", 150,
     {"zones": 2, "year": 1941}, (7, 0, 2)),
    ("China",       "Allies",  (35.0, 105.0),  10, 45,
     "Resist Japanese invasion and unify the nation.", 150,
     {"zones": 2, "year": 1943}, (10, 0, 1)),
    ("Netherlands", "Allies",  (52.2, 5.5),    35, 65,
     "Protect the homeland and the oil-rich colonies.", 150,
     {"zones": 3, "year": 1942}, (3, 1, 1)),
    ("Belgium",     "Allies",  (50.8, 4.4),    5, 60,
     "Maintain independence and defend the homeland.", 120,
     {"zones": 3, "year": 1942}, (3, 0, 1)),
    ("Romania",     "Neutral", (46.0, 25.0),   75, 50,
     "Protect the Ploiesti oil fields amid Axis pressure.", 150,
     {"oil": 75, "zones": 3, "year": 1944}, (4, 0, 1)),
    ("Finland",     "Neutral", (64.0, 26.0),   5, 55,
     "Defend against Soviet aggression and preserve independence.", 120,
     {"zones": 3, "year": 1942}, (3, 0, 1)),
    ("Canada",      "Allies",  (56.0, -106.0), 20, 80,
     "Support the British Commonwealth war effort.", 150,
     {"wins": 1}, (3, 1, 1)),
    ("Australia",   "Allies",  (-25.0, 133.0), 10, 78,
     "Defend Pacific interests and support the Commonwealth.", 150,
     {"beat": ["Japan"]}, (3, 1, 1)),
    ("India",       "Allies",  (21.0, 78.0),   10, 55,
     "Support the British war effort while pressing for independence.", 150,
     {"zones": 3, "year": 1943}, (5, 0, 1)),
]

# minor countries (see FILLER_OUTLINES below): Neutral, 3 zones, no troops, not playable
NATION_DATA += [
    ("Spain", "Neutral", (40.3, -4.3), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Norway", "Neutral", (66.6, 20.1), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Sweden", "Neutral", (59.3, 13.7), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Czechoslovakia", "Neutral", (48.1, 16.5), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Yugoslavia", "Neutral", (44.4, 19.3), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Greece", "Neutral", (40.4, 24.2), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Turkey", "Neutral", (39.6, 35.1), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Iraq", "Neutral", (34.0, 44.9), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Iran", "Neutral", (33.2, 55.1), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Saudi Arabia", "Neutral", (21.6, 47.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Afghanistan", "Neutral", (35.3, 67.1), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Pakistan", "Neutral", (28.2, 69.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Kazakhstan", "Neutral", (46.0, 68.1), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Mongolia", "Neutral", (45.2, 101.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Korea", "Neutral", (37.5, 124.6), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Syria", "Neutral", (35.2, 39.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Tibet", "Neutral", (31.4, 88.6), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Burma", "Neutral", (23.7, 98.5), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Thailand", "Neutral", (13.2, 100.8), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Indochina", "Neutral", (17.7, 106.7), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Morocco", "Neutral", (29.3, -6.9), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Algeria", "Neutral", (27.8, 3.8), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Libya", "Neutral", (25.5, 16.2), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Egypt", "Neutral", (25.8, 29.2), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("French West Africa", "Neutral", (15.1, -5.9), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("French Equatorial Africa", "Neutral", (8.1, 18.2), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Sudan", "Neutral", (13.6, 28.6), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Ethiopia", "Neutral", (7.7, 38.8), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Nigeria", "Neutral", (9.6, 7.9), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Belgian Congo", "Neutral", (-3.1, 23.4), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("British East Africa", "Neutral", (-2.6, 35.4), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Angola", "Neutral", (-13.3, 18.2), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Mozambique", "Neutral", (-15.5, 32.6), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("South Africa", "Neutral", (-26.2, 23.5), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Brazil", "Neutral", (-9.0, -48.9), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Argentina", "Neutral", (-39.6, -65.8), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Chile", "Neutral", (-32.6, -69.4), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Peru", "Neutral", (-8.1, -73.4), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Bolivia", "Neutral", (-15.6, -64.9), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Colombia", "Neutral", (2.6, -73.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Venezuela", "Neutral", (3.7, -63.3), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Paraguay", "Neutral", (-23.4, -56.5), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Mexico", "Neutral", (25.3, -104.6), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Alaska", "Neutral", (64.9, -151.3), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Central America", "Neutral", (13.2, -86.2), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
]

# extra minor countries (islands and small states that were missing from the map)
NATION_DATA += [
    ("Denmark", "Neutral", (56.0, 9.5), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Portugal", "Neutral", (39.5, -8.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Ireland", "Neutral", (53.4, -8.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Iceland", "Neutral", (64.9, -18.5), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Greenland", "Neutral", (72.0, -42.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Sardinia", "Neutral", (40.0, 9.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Cuba", "Neutral", (21.7, -79.5), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Hispaniola", "Neutral", (19.0, -71.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Madagascar", "Neutral", (-19.0, 46.7), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Sri Lanka", "Neutral", (7.8, 80.7), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Taiwan", "Neutral", (23.7, 121.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Luzon", "Neutral", (16.0, 121.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Mindanao", "Neutral", (7.8, 125.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Sumatra", "Neutral", (-0.5, 101.5), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Java", "Neutral", (-7.4, 110.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Borneo", "Neutral", (0.5, 114.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Sulawesi", "Neutral", (-2.0, 121.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("New Guinea", "Neutral", (-5.5, 141.0), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("New Zealand North", "Neutral", (-38.5, 175.5), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("New Zealand South", "Neutral", (-44.0, 170.5), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
    ("Tasmania", "Neutral", (-42.0, 146.5), 5, 50,
     "Stay independent.", 0, {"year": 9999}, (0, 0, 0)),
]

# ----------------------------------------------------------------------
# HISTORICAL ARMY SIZES
# Approximate ground-army strength (land forces only - no navy or air force personnel) at
# the START (January) of each year, in thousands of soldiers. These are rounded estimates
# drawn from commonly cited figures (US Army records, Krivosheev, Muller-Hillebrand, etc.);
# sources differ, so treat them as ballpark numbers. In game, 1 troop = SOLDIERS_PER_TROOP
# soldiers. Each January a country whose center is free is topped up to this historical
# strength; a country already above it keeps what it has. Years past the last entry use
# the last one.
# ----------------------------------------------------------------------
ARMY_STRENGTH_K = {
    #               1938   1939   1940   1941   1942   1943   1944   1945
    "Germany":     (800,  1300,  3900,  4700,  5400,  6100,  6700,  6500),
    "Italy":       (700,   900,  1400,  2000,  2500,  3300,   150,   200),
    "Japan":       (1100, 1400,  1550,  1900,  2300,  2700,  3400,  5000),
    "USSR":        (1500, 1600,  2400,  3360,  4800,  6400,  7600,  8400),   # 1939+ nerfed 20%
    "USA":         (180,   180,   250,   600,  1700,  3600,  5200,  5800),
    "UK":          (350,   450,  1100,  2200,  2700,  3000,  3300,  3700),
    "France":      (700,   900,  4500,   100,   150,   400,   600,  1200),
    "Poland":      (270,   280,    80,    40,    80,   150,   250,   450),
    "China":       (1800, 2500,  3000,  3300,  3500,  3500,  3700,  3900),
    "Netherlands": (70,     90,   280,    85,    20,    15,    20,    40),
    "Belgium":     (90,    100,   600,     3,     4,     6,    20,    60),
    "Romania":     (250,   300,   400,   600,   700,   700,   600,   550),
    "Finland":     (40,     45,   300,   150,   450,   450,   450,   200),
    "Canada":      (50,     55,   140,   260,   400,   560,   690,   700),
    "Australia":   (45,     80,   140,   300,   550,   727,   690,   600),
    "India":       (200,   200,   230,   600,  1000,  1500,  2000,  2500),
}


# Years where a country's yearly reinforcement is a fixed number of troops instead of the
# usual top-up to its historical army size. (country, year) -> troops added that January.
YEARLY_TROOP_GAIN_OVERRIDE = {
    ("France", 1941): 4000,
    ("Germany", 1941): 5800,
}

# Iron needed per rating point of Army rating (was 20: Germany hit 10/10 too fast).
ARMY_RATING_IRON_DIV = 75
# Navy rating: iron and oil needed per rating point.
NAVY_RATING_IRON_DIV = 100
NAVY_RATING_OIL_DIV = 50
# Every country starts with this multiple of its listed oil and iron stockpiles
# (yearly oil income is NOT affected).
START_RESOURCE_MULT = 2
# Nerf applied on top of that to every country's starting oil and iron (0.5 = -50%).
START_RESOURCE_NERF = 0.5
# Share of its STARTING oil and iron a country gains every new year (at 100% territory).
YEARLY_RESOURCE_INCOME_SHARE = 0.20
# Army rating from iron: going from rating 5 to 6 costs ARMY_RATING_IRON_DIV iron (75), and
# every step up costs 20% more than the one before (5-6: 75, 6-7: 90, 7-8: 108 ...). The same
# 20% ladder continues below 5 (4-5 costs 75/1.2, 3-4 costs 75/1.2^2 ... 1-2 costs 75/1.2^4).
ARMY_RATING_STEP_GROWTH = 1.2
ARMY_RATING_BASE_STEP = 5


def army_iron_points(iron):
    """Rating points an iron stockpile buys, under the escalating step costs above.
    Partial progress inside a step counts proportionally (like the old linear formula)."""
    points, step = 0.0, 1
    while iron > 0 and step < 60:
        cost = ARMY_RATING_IRON_DIV * ARMY_RATING_STEP_GROWTH ** (step - ARMY_RATING_BASE_STEP)
        if iron >= cost:
            iron -= cost
            points += 1
        else:
            points += iron / cost
            break
        step += 1
    return points
# Share of the defender's oil AND iron that changes hands whenever one of its own
# (starting) zones is captured. The attacking side splits it between its countries.
ZONE_CAPTURE_RESOURCE_SHARE = 0.20
# Balance nerf: multiplier on a country's starting oil, iron and yearly oil income.
RESOURCE_MULT = {"USSR": 1}
# Flat penalty subtracted from a country's army, navy and air ratings (before the 1-10 clamp).
RATING_PENALTY = {"USSR": 1}
# Countries whose starting oil and iron are rounded to the nearest 10 after all multipliers.
ROUND_START_RESOURCES_TO_10 = {"USSR"}
# Yearly air force / navy reinforcement = this share of (country's starting air or navy
# per starting troop) x the troops it has now.
AIR_NAVY_PER_TROOP_SHARE = 0.75

# Balance nerfs: multiplier on the yearly base reinforcement (1.0 = unchanged).
YEARLY_TROOP_MULT = {
    "Germany": 0.5, "USSR": 0.5, "China": 0.5,
    "Italy": 0.7, "Japan": 0.7, "UK": 0.7,
}

# Countries that only receive yearly troop reinforcements in the listed years. In every
# other year they gain no troops at all (their starting army is all they have until then).
TROOP_GAIN_ONLY_IN_YEARS = {
    "France": {1941},
}


IRON_STOCKPILES = {
    "Germany": 80, "Italy": 30, "Japan": 25, "USSR": 90,
    "USA": 85, "UK": 55, "France": 40, "Poland": 25,
    "China": 30, "Netherlands": 20, "Belgium": 15, "Romania": 25,
    "Finland": 20, "Canada": 55, "Australia": 35, "India": 30,
}

# landmass each country sits on - troops need Navy to cross between regions
REGION = {
    "Germany": "Eurasia", "Italy": "Eurasia", "USSR": "Eurasia",
    "France": "Eurasia", "Poland": "Eurasia", "China": "Eurasia",
    "Netherlands": "Eurasia", "Belgium": "Eurasia",
    "Romania": "Eurasia", "Finland": "Eurasia",
    "India": "Eurasia",
    "UK": "Britain", "Japan": "Japan",
    "USA": "North America", "Canada": "North America",
    "Australia": "Australia",
}

REGION.update({'Spain': 'Eurasia', 'Norway': 'Eurasia', 'Sweden': 'Eurasia', 'Czechoslovakia': 'Eurasia', 'Yugoslavia': 'Eurasia', 'Greece': 'Eurasia', 'Turkey': 'Eurasia', 'Syria': 'Eurasia', 'Iraq': 'Eurasia', 'Iran': 'Eurasia', 'Saudi Arabia': 'Eurasia', 'Afghanistan': 'Eurasia', 'Pakistan': 'Eurasia', 'Kazakhstan': 'Eurasia', 'Mongolia': 'Eurasia', 'Korea': 'Eurasia', 'Tibet': 'Eurasia', 'Burma': 'Eurasia', 'Thailand': 'Eurasia', 'Indochina': 'Eurasia', 'Morocco': 'Africa', 'Algeria': 'Africa', 'Libya': 'Africa', 'Egypt': 'Africa', 'French West Africa': 'Africa', 'French Equatorial Africa': 'Africa', 'Sudan': 'Africa', 'Ethiopia': 'Africa', 'Nigeria': 'Africa', 'Belgian Congo': 'Africa', 'British East Africa': 'Africa', 'Angola': 'Africa', 'Mozambique': 'Africa', 'South Africa': 'Africa', 'Brazil': 'South America', 'Argentina': 'South America', 'Chile': 'South America', 'Peru': 'South America', 'Bolivia': 'South America', 'Colombia': 'South America', 'Venezuela': 'South America', 'Paraguay': 'South America', 'Mexico': 'North America', 'Alaska': 'North America', 'Central America': 'North America'})

SIDE_COLOR = {"Axis": "#e74c3c", "Allies": "#3498db", "Neutral": "#f1c40f"}

# Simplified national flags, drawn behind each unit box. Coordinates are
# fractions of the box (x0, y0, x1, y1). Ops: rect, circle, star, jack.
def _hstripes(*colors):
    n = len(colors)
    return [("rect", 0, i / n, 1, (i + 1) / n, c) for i, c in enumerate(colors)]


def _vstripes(*colors):
    n = len(colors)
    return [("rect", i / n, 0, (i + 1) / n, 1, c) for i, c in enumerate(colors)]


FLAGS = {
    "Germany": _hstripes("#111111", "#ffffff", "#dd0000"),
    "Italy": _vstripes("#009246", "#ffffff", "#ce2b37"),
    "Japan": [("rect", 0, 0, 1, 1, "#ffffff"), ("circle", 0.5, 0.5, 0.3, "#bc002d")],
    "USSR": [("rect", 0, 0, 1, 1, "#cc0000"), ("star", 0.2, 0.32, 0.24, "#ffdf00")],
    "USA": _hstripes(*(["#b22234", "#ffffff"] * 3 + ["#b22234"])) +
           [("rect", 0, 0, 0.45, 4 / 7, "#3c3b6e"), ("star", 0.22, 0.29, 0.16, "#ffffff")],
    "UK": [("jack", 0, 0, 1, 1)],
    "France": _vstripes("#0055a4", "#ffffff", "#ef4135"),
    "Poland": _hstripes("#ffffff", "#dc143c"),
    "China": [("rect", 0, 0, 1, 1, "#de2910"), ("rect", 0, 0, 0.5, 0.5, "#12266d"),
              ("circle", 0.25, 0.25, 0.17, "#ffffff")],
    "Netherlands": _hstripes("#ae1c28", "#ffffff", "#21468b"),
    "Belgium": _vstripes("#000000", "#fdda24", "#ef3340"),
    "Romania": _vstripes("#002b7f", "#fcd116", "#ce1126"),
    "Finland": [("rect", 0, 0, 1, 1, "#ffffff"), ("rect", 0.26, 0, 0.42, 1, "#003580"),
                ("rect", 0, 0.4, 1, 0.62, "#003580")],
    "Canada": [("rect", 0, 0, 0.25, 1, "#d52b1e"), ("rect", 0.25, 0, 0.75, 1, "#ffffff"),
               ("rect", 0.75, 0, 1, 1, "#d52b1e"), ("star", 0.5, 0.52, 0.3, "#d52b1e")],
    "Australia": [("rect", 0, 0, 1, 1, "#012169"), ("jack", 0, 0, 0.5, 0.5),
                  ("star", 0.25, 0.78, 0.17, "#ffffff"), ("star", 0.75, 0.3, 0.14, "#ffffff"),
                  ("star", 0.82, 0.68, 0.13, "#ffffff")],
    "India": _hstripes("#ff9933", "#ffffff", "#138808") + [("circle", 0.5, 0.5, 0.13, "#000080")],
}

# Where each country's navy sits: (lon, lat) out in the water. Chosen to fall
# in open sea on this simplified map. Ships stationed in a country are drawn
# at that country's naval base.
NAVY_ANCHOR = {
    "Germany": (3, 63.5), "Italy": (15, 35.5), "Japan": (147, 32), "USSR": (50, 73),
    "USA": (-64, 36), "UK": (-11, 55), "France": (-12, 44), "Poland": (18, 67.5),
    "China": (127, 26), "Netherlands": (-12, 51), "Belgium": (-12, 47.5),
    "Romania": (27, 33),
    "Finland": (31, 72), "Canada": (-50, 54), "Australia": (135, -40),
    "India": (70, 12),
}

# Air force planes are painted in each country's colors: (fuselage, wings + tail, accent).
PLANE_COLORS = {
    "Germany": ("#2b2b2b", "#dd0000", "#ffffff"),
    "Italy": ("#009246", "#ffffff", "#ce2b37"),
    "Japan": ("#ffffff", "#bc002d", "#bc002d"),
    "USSR": ("#cc0000", "#8f0000", "#ffdf00"),
    "USA": ("#3c3b6e", "#b22234", "#ffffff"),
    "UK": ("#1f3a93", "#c8102e", "#ffffff"),
    "France": ("#0055a4", "#ef4135", "#ffffff"),
    "Poland": ("#ffffff", "#dc143c", "#dc143c"),
    "China": ("#de2910", "#12266d", "#ffffff"),
    "Netherlands": ("#ae1c28", "#21468b", "#ffffff"),
    "Belgium": ("#2b2b2b", "#fdda24", "#ef3340"),
    "Romania": ("#002b7f", "#fcd116", "#ce1126"),
    "Finland": ("#ffffff", "#003580", "#003580"),
    "Canada": ("#d52b1e", "#ffffff", "#d52b1e"),
    "Australia": ("#012169", "#ffffff", "#d52b1e"),
    "India": ("#ff9933", "#138808", "#ffffff"),
}

SEA_NAMES = {
    "Germany": "North Sea",
    "Italy": "Mediterranean Sea",
    "Japan": "Pacific Ocean",
    "USSR": "Arctic Ocean",
    "USA": "Atlantic Ocean",
    "UK": "North Atlantic Ocean",
    "France": "Bay of Biscay",
    "Poland": "Baltic Sea",
    "China": "East China Sea",
    "Netherlands": "North Sea",
    "Belgium": "North Sea",
    "Romania": "Black Sea",
    "Finland": "Baltic Sea",
    "Canada": "North Atlantic Ocean",
    "Australia": "Southern Ocean",
    "India": "Arabian Sea",
}


def lighten(hex_color, amt=0.55):
    """Blend a #rrggbb color toward white."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    r, g, b = (int(v + (255 - v) * amt) for v in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def shade(hex_color, alpha=0.5):
    """Color you get by laying black at `alpha` opacity over `hex_color`. Tk canvas items
    have no real transparency (stipple is ignored on some platforms), so a see-through
    black shadow is drawn as this pre-blended solid color."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    r, g, b = (int(v * (1 - alpha)) for v in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def star_points(cx, cy, r):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts += [cx + rad * math.cos(ang), cy + rad * math.sin(ang)]
    return pts

# ----------------------------------------------------------------------
# TERRITORIES: every country is a region on the map split into 3 zones
# ----------------------------------------------------------------------

# Simplified but real border outlines (lon, lat), traced from each country's
# actual shape rather than a generic ellipse - so Italy reads as a boot, the
# UK as an island, France as a hexagon, etc. Neighbouring countries are then
# cut apart along shared borders (a weighted Voronoi split against each
# other's outline) so they don't overlap, and each is divided into 3 strips
# along its longer side.
COUNTRY_OUTLINES = {
    "Germany": [
        (8, 55.25), (8.25, 55.25), (8.25, 55), (8.75, 55), (8.75, 54.75), (10.25, 54.75),
        (10.25, 54.5), (11.5, 54.5), (11.5, 54.25), (11.75, 54.25), (11.75, 54.5),
        (12.75, 54.5), (12.75, 54.75), (13, 54.75), (13, 54.25), (13.75, 54.25),
        (13.75, 53.75), (14, 53.75), (14, 53.5), (14.5, 53.5), (14.75, 50.75),
        (13.75, 50.25), (13.75, 49.5), (14, 49.5), (14.25, 48.5), (13.25, 47.75),
        (13.25, 47.25), (12.75, 47.25), (12.75, 47), (8.5, 47), (8.5, 46.75), (7.5, 46.75),
        (7.5, 49), (6.25, 49.5), (6.25, 51), (5.75, 51.25), (5.75, 51.5), (6, 51.5),
        (6, 53.5), (5.75, 53.5), (5.75, 54), (6.25, 54), (6.25, 54.25), (6.75, 54.25),
        (6.75, 54.5), (7.75, 54.75),
    ],
    "Italy": [
        (8.5, 47), (12.5, 47), (12.5, 46.75), (12.75, 46.75), (12.75, 46.5), (13.75, 45.75),
        (13.75, 45.5), (13.25, 45.5), (13.25, 45.25), (12.25, 45), (12.25, 44.5),
        (12.5, 44.5), (12.5, 43.5), (12.75, 43.5), (13, 43), (13.5, 43), (14.25, 42),
        (14.75, 42), (14.75, 41.75), (15.25, 41.75), (15.25, 41.5), (15.75, 41.5),
        (15.75, 41.25), (16.25, 41.25), (16.25, 41), (16.75, 40.75), (16.75, 40.25),
        (16.5, 40.25), (16.5, 39.75), (16.25, 39.75), (16.25, 39.25), (16, 39.25),
        (16, 38.75), (15.75, 38.75), (15.75, 38), (12.5, 37.75), (12.75, 38.75), (13.25, 39),
        (13.25, 39.5), (13.5, 39.5), (13.5, 39.75), (14, 40), (14, 40.5), (14.25, 40.5),
        (14.25, 41.25), (14, 41.25), (14, 41.75), (13.75, 41.75), (13.75, 42.25),
        (13.5, 42.25), (13.5, 42.5), (11, 42.5), (10.25, 44), (7.5, 44), (7.5, 44.25),
        (6.75, 44.75), (6.75, 45.75), (6.5, 45.75), (6.5, 46), (6.75, 46), (7, 46.5),
        (7.5, 46.5), (7.5, 46.75), (8.5, 46.75),
    ],
    "Japan": [
        (130, 31), (131, 33), (130.5, 34.5), (133, 34.5), (135, 35.5), (136.9, 35.2),
        (138.7, 35.2), (140.9, 36.5), (141.9, 39.0), (141.5, 40.5), (140.0, 41.5),
        (141.4, 43.0), (145.8, 43.4), (144.0, 44.4), (141.7, 45.5), (140.3, 43.5),
        (139.9, 42.0), (140.0, 39.0), (139.8, 37.0), (136.9, 37.3), (137.4, 36.5),
        (135.8, 34.7), (132.7, 34.4), (131.5, 33.9), (130.4, 33.0), (130, 31),
    ],
    "USSR": [
        (127.5, 75), (130.25, 75), (130.25, 74.75), (130.75, 74.75), (130.75, 74.5),
        (131.25, 74.5), (131.25, 74.25), (131.75, 74.25), (131.75, 74), (132.5, 74),
        (132.5, 73.75), (133, 73.75), (133, 73.5), (133.5, 73.5), (133.5, 73.25),
        (134, 73.25), (134, 73), (134.5, 73), (134.5, 72.75), (135, 72.75), (135, 72.5),
        (135.5, 72.5), (135.5, 72.25), (136.25, 72.25), (136.25, 72), (136.75, 72),
        (136.75, 71.75), (137.25, 71.75), (137.25, 71.5), (137.75, 71.5), (137.75, 71.25),
        (138.25, 71.25), (138.25, 71), (138.75, 71), (138.75, 70.75), (139.25, 70.75),
        (139.25, 70.5), (140, 70.5), (140, 70.25), (140.5, 70.25), (140.5, 70), (141, 70),
        (141, 69.75), (141.5, 69.75), (141.5, 69.5), (142, 69.5), (142, 69.25),
        (142.5, 69.25), (142.5, 69), (143, 69), (143, 68.75), (143.75, 68.75),
        (143.75, 68.5), (144.25, 68.5), (144.25, 68.25), (144.75, 68.25), (144.75, 68),
        (145.25, 68), (145.25, 67.75), (146, 67.75), (146, 67.5), (146.5, 67.5),
        (146.5, 67.25), (147.25, 67.25), (147.25, 67), (147.75, 67), (147.75, 66.75),
        (148.5, 66.75), (148.5, 66.5), (149, 66.5), (149, 66.25), (149.75, 66.25),
        (149.75, 66), (150.25, 66), (150.25, 65.75), (151, 65.75), (151, 65.5),
        (151.5, 65.5), (151.5, 65.25), (152.25, 65.25), (152.25, 65), (152.75, 65),
        (152.75, 64.75), (153.5, 64.75), (153.5, 64.5), (154, 64.5), (154, 64.25),
        (154.75, 64.25), (154.75, 64), (155.25, 64), (155.25, 63.75), (156, 63.75),
        (156, 63.5), (156.5, 63.5), (156.5, 63.25), (157.25, 63.25), (157.25, 63),
        (158.5, 62.75), (158.5, 62.5), (159.75, 62.25), (159.75, 62), (161, 62.25),
        (161, 62.5), (161.5, 62.5), (161.5, 62.75), (162.25, 62.75), (162.25, 63),
        (162.75, 63), (162.75, 63.25), (163.5, 63.25), (163.5, 63.5), (164, 63.5),
        (164, 63.75), (164.75, 63.75), (164.75, 64), (165.25, 64), (165.25, 64.25),
        (166, 64.25), (166, 64.5), (166.5, 64.5), (166.5, 64.75), (167.25, 64.75),
        (167.25, 65), (167.75, 65), (167.75, 65.25), (168.5, 65.25), (168.5, 65.5),
        (169, 65.5), (169, 65.75), (170.5, 66), (170.5, 66.25), (171.75, 66.25),
        (171.75, 66.5), (172.75, 66.5), (172.75, 66.75), (174, 66.75), (174, 67), (175, 67),
        (175, 67.25), (176.25, 67.25), (176.25, 67.5), (177.25, 67.5), (177.25, 67.75),
        (178.5, 67.75), (178.5, 68), (179, 68), (179, 60), (177.75, 60), (177.75, 59.75),
        (175.5, 59.75), (175.5, 59.5), (173, 59.5), (173, 59.25), (170.75, 59.25),
        (170.75, 59), (168.25, 59), (168.25, 58.75), (166, 58.75), (166, 58.5),
        (163.5, 58.5), (163.5, 58.25), (161.25, 58.25), (161.25, 58), (159.75, 58),
        (159.75, 57.75), (159, 57.75), (159, 57.5), (158.25, 57.5), (158.25, 57.25),
        (157.5, 57.25), (157.5, 57), (156, 56.75), (156, 56.5), (155.5, 56.5),
        (155.5, 56.25), (154.75, 56.25), (154.75, 56), (154, 56), (154, 55.75),
        (153.25, 55.75), (153.25, 55.5), (151.75, 55.25), (151.75, 55), (151.25, 55),
        (151.25, 54.75), (150.5, 54.75), (150.5, 54.5), (149.75, 54.5), (149.75, 54.25),
        (149, 54.25), (149, 54), (147.5, 53.75), (147.5, 53.5), (147, 53.5), (147, 53.25),
        (146.25, 53.25), (146.25, 53), (145.5, 53), (145.5, 52.75), (144.75, 52.75),
        (144.75, 52.5), (143.25, 52.25), (143.25, 52), (143, 52), (143, 51.75),
        (142.75, 51.75), (142.75, 51.5), (142.5, 51.5), (142.5, 51.25), (142.25, 51.25),
        (142.25, 51), (142, 51), (142, 50.75), (141, 50), (141, 49.5), (140.75, 49.5),
        (140.75, 49.25), (140.5, 49.25), (140.5, 49), (140.25, 49), (140.25, 48.75),
        (140, 48.75), (140, 48.5), (139, 47.75), (139, 47.25), (138.75, 47.25), (138.75, 47),
        (138.5, 47), (138.5, 46.75), (138.25, 46.75), (138.25, 46.5), (138, 46.5),
        (138, 46.25), (137, 45.5), (137, 45), (136.75, 45), (136.75, 44.75), (136.5, 44.75),
        (136.5, 44.5), (136.25, 44.5), (136.25, 44.25), (136, 44.25), (136, 44),
        (135.75, 44), (135, 43), (134.5, 43), (134.5, 42.75), (133.5, 42.75), (133.5, 42.5),
        (132.5, 42.5), (132.5, 42.25), (131.5, 42.25), (131.5, 42), (131, 42), (131, 41.75),
        (130.75, 41.75), (130.75, 41.25), (130.25, 41.25), (130.25, 41.5), (129.75, 41.5),
        (129.75, 41.75), (129, 41.75), (129, 42), (124.75, 42), (124.75, 41.75),
        (123.5, 41.5), (123.25, 41), (122.5, 41), (122.5, 41.25), (120.5, 41.25),
        (120.5, 41.5), (119.75, 41.5), (119.75, 41.75), (119.5, 41.75), (118.75, 42.75),
        (118.25, 42.75), (118, 43.25), (117.5, 43.25), (117.5, 43.5), (117, 43.5),
        (117, 43.75), (116.5, 43.75), (116.5, 44), (116, 44), (116, 44.25), (114.75, 44.5),
        (114.25, 45.25), (113.75, 45.25), (113.75, 45.5), (113.25, 45.5), (113.25, 45.75),
        (112.75, 45.75), (112.75, 46), (112.25, 46), (112.25, 46.25), (111, 46.5),
        (110.5, 47.25), (110, 47.25), (110, 47.5), (109.5, 47.5), (109.5, 47.75),
        (109, 47.75), (109, 48), (108.5, 48), (108.5, 48.25), (107.75, 48.25),
        (107.75, 48.5), (106.75, 48.75), (106.75, 49), (106.5, 49), (106.25, 49.5),
        (105.75, 49.5), (105.75, 49.75), (104.25, 49.75), (104.25, 50), (102.75, 50),
        (102.75, 49.75), (98.25, 49.75), (98.25, 49.5), (94.25, 49.5), (94.25, 49.25),
        (91, 49.25), (91, 49), (85.5, 49), (85.5, 49.25), (82.5, 49.25), (82.5, 49.5),
        (79.5, 49.5), (79.5, 49.75), (74.5, 50), (74.5, 50.25), (74.25, 50.25),
        (73.5, 51.25), (72.5, 51.5), (71.75, 52.5), (70.75, 52.75), (70, 53.75),
        (69.5, 53.75), (69.25, 54.25), (68.5, 54.25), (68.25, 54.75), (67.5, 54.75),
        (67.5, 54.5), (66.5, 54.25), (66.5, 54), (66.25, 54), (66.25, 53.75), (65.75, 53.75),
        (65.5, 53.25), (64.5, 53), (63.75, 52), (63, 52), (63, 51.75), (62.5, 51.75),
        (61.75, 50.75), (60.5, 50.5), (60, 49.75), (59.25, 49.75), (59.25, 49.5),
        (57.75, 49.25), (57.75, 49), (57.25, 49), (57.25, 48.75), (56.5, 48.75),
        (56.5, 48.5), (56, 48.5), (56, 48.25), (55.25, 48.25), (55, 47.75), (54, 47.75),
        (54, 47.5), (53.75, 47.5), (53.25, 46.75), (52.75, 46.75), (52.75, 46.5), (51, 46.5),
        (51, 46.25), (50.25, 46.25), (50.25, 46), (49.25, 45.25), (49.25, 44.75),
        (48.5, 44.25), (48.5, 43.75), (47.75, 43.25), (47.75, 42.5), (46.75, 42),
        (46.75, 42.25), (46.25, 42.25), (46, 42.75), (45.25, 42.75), (45, 43.25),
        (44.5, 43.25), (44.25, 43.75), (43, 44), (43, 44.25), (41.25, 44.25), (41.25, 44),
        (40, 44), (40, 43.75), (39.25, 43.75), (39.25, 44), (38.75, 44), (38.75, 44.25),
        (38, 44.25), (38, 44), (37.75, 44), (37.75, 44.25), (37, 44.25), (37, 44.5),
        (36.25, 44.5), (36.25, 44.75), (33.25, 44.5), (33.25, 44.75), (33, 44.75),
        (32.5, 45.5), (32, 45.5), (32, 45.75), (30.75, 45.75), (30.75, 46), (29.5, 45.75),
        (29.5, 46), (28.25, 46.25), (28.25, 46.5), (28, 46.5), (28, 47), (27.75, 47),
        (27.75, 47.75), (27.5, 47.75), (27.5, 48), (26.75, 48), (26.75, 48.25), (26, 48.25),
        (26, 48), (24.25, 48), (24.25, 48.25), (23.5, 48.75), (23.5, 49.5), (23.75, 49.5),
        (23.75, 50.25), (24, 50.25), (24, 52), (23.75, 52), (23.75, 52.5), (23.5, 52.5),
        (23.5, 53), (23.25, 53), (23, 54), (22.75, 54), (22.5, 54.5), (22, 54.5),
        (22, 54.75), (21.5, 54.75), (21.5, 55), (21.25, 55), (21.25, 57.25), (21.5, 57.25),
        (21.5, 57.5), (22.5, 57.5), (22.5, 57.25), (24, 57.25), (24, 57.5), (24.25, 57.5),
        (24.25, 58), (23.75, 58), (23.75, 58.25), (23.5, 58.25), (23.5, 59.25), (25, 59.25),
        (25, 59.5), (28.25, 59.5), (28.25, 59.75), (28.75, 59.75), (28.75, 60), (29, 60),
        (28.75, 60.5), (29.75, 61), (29.75, 61.5), (30, 61.5), (30, 62), (30.25, 62),
        (30.25, 64), (30.5, 64), (30.5, 65), (30, 65.25), (29.75, 66.25), (29.25, 66.5),
        (29.25, 69), (29, 69), (29, 70), (30.5, 70), (30.5, 69.75), (31.75, 69.75),
        (31.75, 69.5), (33, 69.5), (33, 69.25), (34.25, 69.25), (34.25, 69), (35.5, 69),
        (35.5, 68.75), (36.75, 68.75), (36.75, 68.5), (38, 68.5), (38, 68.25),
        (39.25, 68.25), (39.25, 68), (50.5, 68), (50.5, 68.25), (51.75, 68.25),
        (51.75, 68.5), (53, 68.5), (53, 68.75), (54.25, 68.75), (54.25, 69), (55.5, 69),
        (55.5, 69.25), (56.75, 69.25), (56.75, 69.5), (58, 69.5), (58, 69.75),
        (59.25, 69.75), (59.25, 70), (61, 70), (61, 70.25), (62.75, 70.25), (62.75, 70.5),
        (64.75, 70.5), (64.75, 70.75), (66.5, 70.75), (66.5, 71), (68.5, 71), (68.5, 71.25),
        (70.25, 71.25), (70.25, 71.5), (72.25, 71.5), (72.25, 71.75), (74, 71.75), (74, 72),
        (80.5, 72.25), (80.5, 72.5), (84.25, 72.5), (84.25, 72.75), (88, 72.75), (88, 73),
        (92.5, 73), (92.5, 73.25), (97.5, 73.25), (97.5, 73.5), (102.5, 73.5),
        (102.5, 73.75), (107.5, 73.75), (107.5, 74), (112.5, 74), (112.5, 74.25),
        (117.5, 74.25), (117.5, 74.5), (127.5, 74.75),
    ],
    "USA": [
        (-95, 49.25), (-94, 49.25), (-94, 49), (-92.75, 49), (-92.75, 48.75), (-91.5, 48.75),
        (-91.5, 48.5), (-90.25, 48.5), (-90.25, 48.25), (-89, 48.25), (-89, 48),
        (-87.75, 48), (-87.75, 47.75), (-86.5, 47.75), (-86.5, 47.5), (-85.25, 47.5),
        (-85.25, 47.25), (-83, 47), (-83, 46.75), (-82.75, 46.75), (-82.75, 46.5),
        (-82.5, 46.5), (-82.5, 46.25), (-82.25, 46.25), (-81.5, 45.25), (-81, 45.25),
        (-81, 45), (-80.75, 45), (-80.75, 44.75), (-80.5, 44.75), (-80.5, 44.5),
        (-80.25, 44.5), (-79.5, 43.5), (-79.25, 43.5), (-79.25, 43.75), (-77.5, 43.75),
        (-77.5, 44), (-75.75, 44), (-75.75, 44.25), (-74.5, 44.25), (-74.5, 44.5),
        (-73.25, 44.5), (-73.25, 44.75), (-72, 44.75), (-72, 45), (-70.75, 45),
        (-70.75, 44.75), (-70, 44.75), (-70, 45), (-69.5, 45), (-69, 45.75), (-67.75, 45.75),
        (-67.75, 46), (-67, 46), (-67, 45.75), (-66.5, 45.75), (-66.25, 45.25),
        (-65.75, 45.25), (-65.75, 45), (-65.5, 45), (-65.5, 44.25), (-65.75, 44.25),
        (-65.75, 44), (-67.5, 43.75), (-67.5, 43.5), (-68.5, 43.5), (-68.5, 43.25),
        (-68.75, 43.25), (-68.75, 43), (-69, 43), (-69, 42.75), (-70, 42), (-70, 41),
        (-71, 41), (-71, 40.75), (-73, 40.75), (-73, 40.5), (-74, 40.5), (-74, 40.25),
        (-74.5, 40), (-74.5, 39.5), (-75, 39.25), (-75, 38.75), (-75.25, 38.75),
        (-75.25, 38.25), (-75.5, 38.25), (-75.5, 37.75), (-75.75, 37.75), (-75.75, 36),
        (-75.5, 36), (-75.5, 35), (-75.75, 35), (-76, 34.5), (-76.5, 34.5), (-76.75, 34),
        (-77.75, 33.75), (-78, 33.25), (-78.5, 33.25), (-79, 32.5), (-79.5, 32.5),
        (-79.5, 32.25), (-79.75, 32.25), (-79.75, 32), (-80, 32), (-80, 31.75), (-81, 31),
        (-81, 30.25), (-80.75, 30.25), (-80.75, 28.75), (-80.5, 28.75), (-80.5, 27.25),
        (-80.25, 27.25), (-80, 25.5), (-80.25, 25.5), (-80.25, 25.25), (-80.75, 25.25),
        (-80.75, 25), (-81.5, 25), (-81.5, 24.75), (-82, 25), (-82, 25.75), (-82.25, 25.75),
        (-82.25, 26.75), (-82.5, 26.75), (-82.5, 27.75), (-82.75, 27.75), (-83, 29),
        (-83.5, 29), (-83.5, 29.25), (-84.5, 29.25), (-84.5, 29.5), (-85.5, 29.5),
        (-85.5, 29.75), (-86.75, 29.75), (-86.75, 30), (-90.25, 30), (-90.25, 29.75),
        (-92.75, 29.75), (-92.75, 29.5), (-94, 29.5), (-94, 29.25), (-94.25, 29.25),
        (-94.25, 29), (-94.5, 29), (-94.5, 28.75), (-95.5, 28), (-95.5, 27.5),
        (-95.75, 27.5), (-95.75, 27.25), (-96, 27.25), (-96, 27), (-97, 26.25), (-97, 25.75),
        (-97.25, 25.75), (-97.25, 26.25), (-97.75, 26.25), (-97.75, 26.5), (-98, 26.5),
        (-98.75, 27.5), (-99.5, 27.5), (-99.5, 27.75), (-100.25, 27.75), (-100.25, 28),
        (-101, 28), (-101, 28.25), (-101.75, 28.25), (-101.75, 28.5), (-102.5, 28.5),
        (-102.5, 28.75), (-103.5, 28.75), (-103.5, 29), (-104.75, 29.25), (-104.75, 29.5),
        (-105.5, 30), (-105.5, 30.5), (-105.75, 30.5), (-106.5, 31.5), (-108, 31.5),
        (-108, 31.25), (-111.75, 31.25), (-111.75, 31.5), (-112.5, 31.5), (-112.5, 31.75),
        (-113.75, 31.75), (-113.75, 31.5), (-115.25, 31.25), (-115.25, 31.5),
        (-116.75, 31.75), (-116.75, 32), (-117.25, 32.25), (-117.25, 32.75), (-117.5, 32.75),
        (-117.5, 33), (-117.75, 33), (-117.75, 33.25), (-118, 33.25), (-118, 33.5),
        (-118.25, 33.5), (-118.25, 33.75), (-118.5, 33.75), (-118.5, 34), (-118.75, 34),
        (-118.75, 34.25), (-119, 34.25), (-119, 34.5), (-119.25, 34.5), (-120, 35.5),
        (-120.5, 35.5), (-120.75, 36), (-121.25, 36), (-121.25, 36.25), (-122, 36.75),
        (-122, 37.25), (-122.5, 37.5), (-122.5, 38), (-123, 38.25), (-123, 38.75),
        (-123.25, 38.75), (-123.25, 39), (-123.5, 39), (-123.5, 39.5), (-124, 39.75),
        (-124, 42.75), (-124.25, 42.75), (-124.25, 45.5), (-124.5, 45.5), (-124.5, 47.75),
        (-124.75, 47.75), (-124.75, 48.5), (-124, 48.5), (-124, 48.75), (-123.25, 48.75),
        (-123.25, 49), (-95, 49),
    ],
    "UK": [
        (-5.7, 50.0), (-4.5, 50.4), (-3.5, 50.6), (-1.5, 50.7), (0.3, 51.0),
        (1.4, 51.4), (1.2, 52.9), (0.0, 53.6), (-0.2, 54.5), (-1.5, 54.6),
        (-2.0, 55.8), (-3.0, 56.0), (-2.5, 57.7), (-4.0, 58.6), (-5.0, 58.5),
        (-5.5, 57.3), (-6.2, 56.8), (-5.3, 55.9), (-4.8, 55.0), (-5.0, 54.6),
        (-4.5, 53.4), (-4.8, 52.8), (-4.2, 52.0), (-5.3, 51.7), (-4.7, 51.2),
        (-5.3, 50.0), (-5.7, 50.0),
    ],
    "France": [
        (1.5, 51), (3, 51), (3, 50.75), (3.25, 50.75), (3.5, 50.25), (4, 50.25), (4.5, 49.5),
        (6.5, 49.5), (6.5, 49.25), (7.25, 49.25), (7.25, 49), (7.5, 49), (7.5, 46.5),
        (7, 46.5), (7, 46.25), (6.5, 46), (6.5, 45.75), (6.75, 45.75), (6.75, 44.75),
        (7, 44.75), (7.5, 44), (7, 43.75), (7, 43.25), (6.75, 43.25), (6.75, 43), (6, 43),
        (6, 43.25), (4.75, 43.25), (4.75, 43.5), (4.5, 43.5), (4.5, 43.25), (4, 43.25),
        (3.5, 42.5), (3, 42.5), (3, 42.25), (3.25, 42.25), (3.25, 41.75), (3, 41.75),
        (3, 41.5), (2.75, 41.5), (2.25, 42.25), (1.75, 42.25), (1.75, 42.5), (0, 42.75),
        (0, 43), (-0.75, 43), (-0.75, 43.25), (-1.75, 43.25), (-1.75, 43.5), (-1.5, 43.5),
        (-1.5, 45.25), (-1.75, 45.25), (-2, 45.75), (-1.75, 45.75), (-1.25, 46.5),
        (-1.75, 46.75), (-1.75, 47.25), (-2.25, 47.25), (-2.25, 47.5), (-3, 47.5),
        (-3, 47.75), (-3.5, 47.75), (-3.5, 48), (-4.75, 48.25), (-4.75, 48.5), (-2.75, 48.5),
        (-2.75, 48.75), (-2, 48.75), (-2, 49), (-1.75, 49), (-1.75, 49.75), (-0.5, 50),
        (-0.5, 50.25), (0.25, 50.25), (0.25, 50.5), (1.5, 50.75),
    ],
    "Poland": [
        (21, 56.75), (21.25, 56.75), (21.25, 55), (21.5, 55), (21.5, 54.75), (22, 54.75),
        (22, 54.5), (22.5, 54.5), (22.5, 54.25), (23, 54), (23, 53.5), (23.25, 53.5),
        (23.25, 53), (23.5, 53), (23.5, 52.5), (23.75, 52.5), (23.75, 52), (24, 52),
        (24, 50.25), (23.75, 50.25), (23.5, 49), (23, 49), (22.75, 48.5), (21.75, 48.25),
        (21.75, 48.5), (21.25, 48.5), (21, 49), (19, 49.25), (18.75, 49.75), (18.25, 49.75),
        (18.25, 50), (17.75, 50), (17.75, 50.25), (16.75, 50.25), (16.75, 50.5),
        (14.75, 50.75), (14.5, 53.5), (14, 53.5), (13.75, 54), (15.5, 54.25), (15.5, 54.5),
        (20, 54.5), (20.25, 55), (20.75, 55), (20.75, 55.25), (21, 55.25),
    ],
    "China": [
        (81.5, 45), (82.25, 45), (82.25, 44.75), (83.75, 44.5), (83.75, 44.25),
        (84.25, 44.25), (84.25, 44), (85.75, 43.75), (85.75, 43.5), (86.25, 43.5),
        (86.25, 43.25), (87.75, 43), (87.75, 42.75), (89, 42.5), (89, 42.25), (89.75, 42.25),
        (89.75, 42), (106, 42), (106, 41.75), (108, 41.75), (108, 41.5), (110, 41.5),
        (110, 41.25), (112, 41.25), (112, 41), (113.25, 41), (113.25, 40.75),
        (113.75, 40.75), (113.75, 40.5), (114.25, 40.5), (114.25, 40.25), (114.75, 40.25),
        (114.75, 40), (115.25, 40), (115.25, 39.75), (115.75, 39.75), (115.75, 39.5),
        (116.25, 39.5), (116.25, 39.25), (116.75, 39.25), (116.75, 39), (117.25, 39),
        (117.5, 39.5), (118, 39.5), (118.25, 40), (118.75, 40), (119, 40.5), (119.5, 40.5),
        (119.75, 41.5), (123.25, 41), (123.25, 40.75), (123.5, 40.75), (123.5, 40.25),
        (124, 40), (124, 39.5), (123, 38.75), (123, 38.25), (122.5, 38), (122.5, 37.25),
        (122.25, 37.25), (122, 36.75), (121.25, 36.75), (121.25, 36.5), (120.75, 36.5),
        (120.75, 36.25), (120.25, 36), (120.25, 34.75), (120.5, 34.75), (120.5, 33.5),
        (120.75, 33.5), (121, 31.75), (121.25, 31.75), (121.25, 31.5), (121.75, 31.5),
        (121.75, 31), (122.5, 31), (122.5, 30.75), (122.25, 30.75), (122.25, 30.25),
        (122, 30.25), (122, 29.75), (121.75, 29.75), (122, 28.75), (121.25, 28.25),
        (121.25, 27.5), (121, 27.5), (121, 26.75), (120.75, 26.75), (120.75, 26),
        (120.5, 26), (120.5, 25.25), (120.25, 25.25), (120, 24), (119.75, 24),
        (119.75, 23.75), (119.25, 23.75), (119, 23.25), (118, 23), (117.75, 22.5),
        (116.75, 22.25), (116.5, 21.75), (115.5, 21.5), (115.5, 21.25), (115.25, 21.25),
        (115.25, 21), (114.75, 21), (114.75, 20.75), (114, 20.75), (114, 21), (113.75, 21),
        (113.5, 21.5), (113, 21.5), (113, 21.75), (108.75, 22), (108.75, 22.25),
        (107.75, 23), (107.75, 23.75), (107.5, 23.75), (107.5, 24), (106.5, 24.75),
        (106.5, 25.25), (106.25, 25.25), (106.25, 25.5), (105.25, 26.25), (105.25, 26.75),
        (105, 26.75), (105, 27), (104, 27.75), (104, 28.25), (103.75, 28.25), (103.75, 28.5),
        (102.75, 29.25), (102.75, 29.75), (102.5, 29.75), (102.5, 30), (101.5, 30.75),
        (101.5, 31.25), (101.25, 31.25), (101.25, 31.5), (100.25, 32.25), (100.25, 32.75),
        (100, 32.75), (99.25, 33.75), (98.75, 33.75), (98.75, 34), (97.75, 34),
        (97.75, 34.25), (95.5, 34.25), (95.5, 34.5), (93.25, 34.5), (93.25, 34.75),
        (90.75, 34.75), (90.75, 35), (88, 35), (88, 35.25), (85.25, 35.25), (85.25, 35.5),
        (82.5, 35.5), (82.5, 35.75), (80.75, 35.75), (80.75, 36), (79.5, 36), (79.5, 36.25),
        (77.75, 36.5), (77.75, 36.75), (77, 36.75), (77, 37), (76.25, 37), (76.25, 37.25),
        (75.5, 37.25), (75.5, 37.5), (74.25, 37.75), (74.25, 38), (74, 38), (74, 38.75),
        (74.25, 38.75), (74.25, 40), (74.5, 40), (74.5, 41.25), (74.75, 41.25),
        (74.75, 42.5), (75, 42.5), (75, 43), (76.25, 43.25), (76.25, 43.5), (77.25, 43.5),
        (77.25, 43.75), (78, 43.75), (78, 44), (79, 44), (79, 44.25), (79.75, 44.25),
        (79.75, 44.5), (80.75, 44.5), (80.75, 44.75), (81.5, 44.75),
    ],
    "Netherlands": [
        (5.25, 53.75), (5.75, 53.75), (5.75, 53.5), (6, 53.5), (6, 51.5), (5.75, 51.5),
        (5.75, 51.25), (5.5, 51.25), (5.5, 51.5), (5, 51.5), (5, 51.25), (4.75, 51.25),
        (4.75, 51.5), (3, 51.5), (3, 52), (3.25, 52), (3.25, 52.25), (3.5, 52.25),
        (4.25, 53.25), (4.75, 53.25), (4.75, 53.5), (5.25, 53.5),
    ],
    "Belgium": [
        (2.5, 51.1), (3.4, 51.4), (4.5, 51.5), (5.9, 51.0), (6.4, 50.3),
        (5.8, 49.5), (4.8, 49.5), (3.5, 50.4), (2.5, 51.1),
    ],
    "Romania": [
        (23, 49), (23.5, 49), (24.25, 48), (26, 48), (26, 48.25), (27.5, 48), (27.5, 47.75),
        (27.75, 47.75), (28, 46.5), (28.25, 46.5), (28.25, 46.25), (28.75, 46.25),
        (28.75, 46), (29.5, 46), (29.5, 45.75), (29.75, 45.75), (29.75, 45.5), (29.5, 45.5),
        (29.5, 45), (29.25, 45), (29, 43.75), (28.75, 43.75), (28.5, 43.25), (28, 43.25),
        (28, 43.5), (27.5, 43.5), (27.5, 43.75), (27, 43.75), (27, 43.5), (26.5, 43.5),
        (26.5, 43.75), (25.25, 43.75), (25.25, 43.5), (24.5, 43.5), (24.5, 43.75),
        (23.25, 43.75), (23, 44.25), (22.25, 44.25), (22.25, 44.5), (21, 44.75),
        (20.25, 46.25), (20.5, 46.25), (20.5, 46.5), (20.75, 46.5), (20.75, 46.75),
        (21.75, 47.5), (21.75, 48.25), (22.75, 48.5),
    ],
    "Finland": [
        (28.5, 70), (29, 70), (29, 69), (29.25, 69), (29.25, 66.5), (29.75, 66.25),
        (30, 65.25), (30.5, 65), (30.5, 64), (30.25, 64), (30.25, 62), (30, 62), (29.75, 61),
        (29.5, 61), (29.5, 60.75), (29, 60.75), (29, 60.5), (28.75, 60.5), (28.75, 60.25),
        (28.25, 60.25), (28.25, 60), (26.25, 60), (26.25, 59.75), (24.5, 59.75),
        (24.5, 59.5), (22.75, 59.5), (22.75, 59.75), (21.5, 59.75), (21.5, 60), (21, 60),
        (21, 60.25), (21.25, 60.25), (21.25, 60.75), (21.75, 61), (22, 62), (22.5, 62.25),
        (22.75, 63.25), (23.25, 63.5), (23.5, 64.5), (23.75, 64.5), (23.75, 64.75),
        (24, 64.75), (24, 65), (24.25, 65), (24.25, 65.25), (24.5, 65.25), (25.25, 66.25),
        (25.75, 66.25), (26.5, 67.25), (27, 67.25), (27, 67.5), (28, 68.25), (28, 68.75),
        (28.25, 68.75), (28.25, 69.25), (28.5, 69.25),
    ],
    "Canada": [
        (-126.25, 70.5), (-74.75, 70.5), (-74.75, 70.25), (-74.25, 70.25), (-74.25, 70),
        (-73.75, 70), (-73.75, 69.75), (-73.25, 69.75), (-73.25, 69.5), (-72.75, 69.5),
        (-72.75, 69.25), (-72.25, 69.25), (-72.25, 69), (-71.75, 69), (-71.75, 68.75),
        (-71.25, 68.75), (-71.25, 68.5), (-70.25, 68.25), (-70.25, 68), (-69.5, 67.5),
        (-69.25, 66.5), (-68.75, 66.25), (-68.75, 65.75), (-68.25, 65.5), (-68, 64.5),
        (-67.5, 64.25), (-67.5, 63.75), (-67, 63.5), (-66.75, 62.5), (-66.25, 62.25),
        (-66.25, 61.75), (-65.75, 61.5), (-65.5, 60.5), (-65.25, 60.5), (-64.75, 59.75),
        (-64.25, 59.75), (-64.25, 59.5), (-63.75, 59.5), (-63.75, 59.25), (-63.25, 59.25),
        (-63.25, 59), (-62.75, 59), (-62.75, 58.75), (-62.25, 58.75), (-62.25, 58.5),
        (-61.75, 58.5), (-61.75, 58.25), (-60.75, 58), (-60.75, 57.75), (-60.5, 57.75),
        (-59.75, 56.75), (-59.25, 56.75), (-59.25, 56.5), (-59, 56.5), (-59, 56.25),
        (-58.75, 56.25), (-58, 55.25), (-57.5, 55.25), (-57.5, 55), (-57.25, 55),
        (-56.5, 54), (-56, 54), (-56, 53.75), (-58.25, 53.75), (-58.25, 53.5),
        (-59.25, 53.5), (-59.25, 53.25), (-60, 53.25), (-60, 53), (-61, 53), (-61, 52.75),
        (-61.25, 52.75), (-61.25, 52.25), (-61, 52.25), (-61, 51.75), (-60.75, 51.75),
        (-60.75, 51.25), (-60.5, 51.25), (-60.5, 50.75), (-60.25, 50.75), (-60.25, 50.25),
        (-60, 50.25), (-59.75, 49.75), (-59, 49.75), (-59, 49.5), (-58.5, 49.5),
        (-58.5, 49.25), (-57.75, 49.25), (-57.75, 49), (-57.25, 49), (-57.25, 48.75),
        (-56.5, 48.75), (-56.5, 48.5), (-56, 48.5), (-56, 48.25), (-55.25, 48.25),
        (-55.25, 47.75), (-56, 47.75), (-56, 47.5), (-56.5, 47.5), (-56.5, 47.25),
        (-57.25, 47.25), (-57.25, 47), (-57.75, 47), (-57.75, 46.75), (-58.5, 46.75),
        (-58.5, 46.5), (-59.75, 46.25), (-59.75, 46), (-60.5, 46), (-60.5, 45.75),
        (-61.5, 45.75), (-61.5, 45.5), (-62.5, 45.5), (-62.5, 45.25), (-64.25, 45),
        (-64.25, 44.75), (-64.75, 44.75), (-64.75, 44.5), (-65.25, 44.5), (-65.25, 44.25),
        (-65.5, 44.25), (-65.5, 45), (-65.75, 45), (-65.75, 45.25), (-66.25, 45.25),
        (-66.25, 45.5), (-66.5, 45.5), (-66.5, 45.75), (-67, 45.75), (-67, 46), (-67.75, 46),
        (-67.75, 45.75), (-69, 45.75), (-69, 45.5), (-69.25, 45.5), (-69.5, 45), (-70, 45),
        (-70, 44.75), (-70.75, 44.75), (-70.75, 45), (-72, 45), (-72, 44.75),
        (-73.25, 44.75), (-73.25, 44.5), (-74.5, 44.5), (-74.5, 44.25), (-75.75, 44.25),
        (-75.75, 44), (-77.5, 44), (-77.5, 43.75), (-79.25, 43.75), (-79.25, 43.5),
        (-79.5, 43.5), (-79.5, 43.75), (-79.75, 43.75), (-79.75, 44), (-80, 44),
        (-80, 44.25), (-80.25, 44.25), (-81, 45.25), (-81.5, 45.25), (-81.5, 45.5),
        (-81.75, 45.5), (-81.75, 45.75), (-82, 45.75), (-82, 46), (-82.25, 46), (-83, 47),
        (-85.25, 47.25), (-85.25, 47.5), (-86.5, 47.5), (-86.5, 47.75), (-87.75, 47.75),
        (-87.75, 48), (-89, 48), (-89, 48.25), (-90.25, 48.25), (-90.25, 48.5),
        (-91.5, 48.5), (-91.5, 48.75), (-92.75, 48.75), (-92.75, 49), (-94, 49),
        (-94, 49.25), (-95, 49.25), (-95, 49), (-123.25, 49), (-123.25, 49.25),
        (-123.75, 49.25), (-123.75, 49.5), (-124.25, 49.5), (-124.25, 49.75), (-125.25, 50),
        (-125.25, 50.25), (-125.5, 50.25), (-125.5, 50.5), (-125.75, 50.5), (-125.75, 50.75),
        (-126, 50.75), (-126, 51), (-126.25, 51), (-127, 52), (-127.5, 52), (-128, 52.75),
        (-128.5, 52.75), (-128.5, 53), (-128.75, 53), (-128.75, 53.25), (-129.25, 53.25),
        (-129.75, 54), (-130.25, 54), (-131, 55), (-131.5, 55), (-131.5, 55.25),
        (-131.75, 55.25), (-132.25, 56), (-132.75, 56), (-133.5, 57), (-134, 57),
        (-134.25, 57.5), (-134.75, 57.5), (-134.75, 57.75), (-135.25, 57.75), (-135.25, 58),
        (-135.75, 58), (-135.75, 58.25), (-138.25, 58.5), (-138.25, 58.75), (-138.75, 58.75),
        (-138.75, 59.75), (-139, 59.75), (-138.75, 61), (-138.5, 61), (-138.5, 61.5),
        (-138.25, 61.5), (-138.25, 62), (-138, 62), (-138, 62.75), (-137.75, 62.75),
        (-137.75, 63.25), (-137.5, 63.25), (-137.5, 63.75), (-137.25, 63.75),
        (-137.25, 64.5), (-137, 64.5), (-137, 65), (-136.75, 65), (-136.75, 65.75),
        (-136.5, 65.75), (-136.5, 66.25), (-136.25, 66.25), (-136.25, 66.75), (-136, 66.75),
        (-136, 67.5), (-135.75, 67.5), (-135.75, 68), (-135.5, 68), (-135.5, 68.5),
        (-135.25, 68.5), (-135.25, 68.75), (-135.5, 68.75), (-135.25, 70), (-127.5, 70),
        (-127.5, 70.25), (-126.25, 70.25),
    ],
    "Australia": [
        (140.5, -11), (141, -11), (141.25, -11.5), (141.5, -11.5), (141.75, -11),
        (142.25, -11.25), (142.25, -12), (142.5, -12), (142.75, -13.5), (143, -13.5),
        (143, -14), (143.25, -14), (143.25, -14.25), (143.5, -14.25), (143.5, -14.5),
        (143.75, -14.5), (143.75, -14.75), (144, -14.75), (144, -15), (145, -15.75),
        (146, -19), (146.25, -19), (146.25, -19.25), (146.75, -19.25), (146.75, -19.5),
        (147.25, -19.5), (147.25, -19.75), (147.75, -19.75), (147.75, -20), (148, -20),
        (148, -20.25), (148.25, -20.25), (148.25, -20.5), (148.5, -20.5), (148.5, -20.75),
        (149.5, -21.5), (149.5, -22), (150, -22.25), (150, -22.75), (150.5, -23),
        (150.5, -23.5), (150.75, -23.5), (151.25, -24.25), (151.75, -24.25), (151.75, -24.5),
        (152.25, -24.5), (152.25, -24.75), (152.75, -24.75), (152.75, -25), (153, -25),
        (153, -29.25), (152.5, -29.5), (152.5, -30), (152, -30.25), (152, -30.75),
        (151.5, -31), (151.5, -31.5), (151, -31.75), (151, -32.25), (150.75, -32.25),
        (150.75, -32.5), (150.5, -32.5), (150.5, -33), (150, -33.25), (150, -37),
        (149.75, -37), (149.75, -37.25), (149.25, -37.25), (149.25, -37.5), (148.75, -37.5),
        (148.75, -37.75), (148.25, -37.75), (148.25, -38), (147.75, -38), (147.75, -38.25),
        (147.25, -38.25), (147.25, -38.5), (140, -38), (140, -37.75), (139, -37),
        (139, -36.5), (138.75, -36.5), (138, -35.5), (136, -35), (136, -34.75), (135, -34),
        (135, -33.5), (134.75, -33.5), (134, -32.5), (133.25, -32.5), (133.25, -32.25),
        (131.75, -32.25), (131.75, -32), (130.25, -32), (130.25, -31.75), (128, -31.75),
        (128, -32), (126.25, -32), (126.25, -32.25), (125.25, -32.25), (125.25, -32.5),
        (124.75, -32.5), (124.75, -32.75), (124.25, -32.75), (124.25, -33), (123.75, -33),
        (123.75, -33.25), (123.25, -33.25), (123.25, -33.5), (122.75, -33.5),
        (122.75, -33.75), (122.25, -33.75), (122.25, -34), (120.5, -34.25), (120.5, -34.5),
        (119.5, -34.5), (119.5, -34.75), (118.5, -34.75), (118.5, -35), (117.5, -35),
        (117.5, -34.75), (117.25, -34.75), (117.25, -35), (116.75, -35), (116.5, -34.5),
        (116, -34.5), (116, -34.25), (115.25, -34.25), (115.25, -34), (115, -34),
        (115, -33.5), (114.75, -33.5), (114.75, -32.25), (114.5, -32.25), (114.5, -31),
        (114.25, -31), (114.25, -29.75), (114, -29.75), (114, -28.75), (113.75, -28.75),
        (113.75, -28), (113.5, -28), (113.5, -27.25), (113.25, -27.25), (113.25, -26.5),
        (113, -26.5), (113, -25.5), (113.25, -25.5), (113.25, -24.5), (113.5, -24.5),
        (113.5, -23.5), (113.25, -23.5), (113.25, -22.5), (113, -22.5), (113, -22),
        (113.25, -22), (113.25, -21.75), (113.75, -21.75), (113.75, -21.5), (114.25, -21.5),
        (114.25, -21.25), (114.75, -21.25), (114.75, -21), (115.25, -21), (115.25, -20.75),
        (115.75, -20.75), (115.75, -20.5), (116.25, -20.5), (116.25, -20.25),
        (116.75, -20.25), (116.75, -20), (117.25, -20), (117.25, -19.75), (117.75, -19.75),
        (117.75, -19.5), (118.25, -19.5), (118.25, -19.25), (118.75, -19.25), (118.75, -19),
        (119.25, -19), (119.25, -18.75), (119.75, -18.75), (119.75, -18.5), (120.25, -18.5),
        (120.25, -18.25), (120.75, -18.25), (120.75, -18), (121.25, -18), (121.25, -17.75),
        (121.75, -17.75), (121.75, -17.5), (122.75, -17.25), (122.75, -17), (123, -17),
        (123, -16.75), (123.25, -16.75), (123.25, -16.5), (123.5, -16.5), (123.5, -16.25),
        (123.75, -16.25), (123.75, -16), (124, -16), (124, -15.75), (124.25, -15.75),
        (124.25, -15.5), (124.5, -15.5), (124.5, -15.25), (124.75, -15.25), (124.75, -15),
        (125, -15), (125.75, -14), (126.5, -14), (126.5, -14.25), (127.25, -14.25),
        (127.25, -14.5), (128, -14.5), (128, -14.75), (128.75, -14.75), (128.75, -15),
        (129, -15), (129, -14.5), (129.25, -14.5), (129.25, -13.75), (129.5, -13.75),
        (129.5, -13), (129.75, -13), (129.75, -12.25), (130, -12.25), (130, -12),
        (137.5, -12), (137.5, -11.75), (138.5, -11.75), (138.5, -11.5), (139.5, -11.5),
        (139.5, -11.25), (140.5, -11.25),
    ],
    "India": [
        (74, 34), (78, 34), (78, 33.75), (78.5, 33.5), (78.5, 33), (79, 32.75), (79, 32.25),
        (79.5, 32), (79.5, 31.5), (80, 31.25), (80, 31), (79.5, 30.75), (79.5, 30.25),
        (78.75, 29.75), (78.75, 29.25), (79.25, 29), (79.25, 28.5), (79.5, 28.5),
        (79.75, 28), (80.5, 28), (80.5, 27.75), (81.25, 27.75), (81.25, 27.5), (82, 27.5),
        (82, 27.25), (83, 27.25), (83, 27), (83.75, 27), (83.75, 26.75), (84.5, 26.75),
        (84.5, 26.5), (87.25, 26.75), (87.25, 27), (89, 27), (89, 27.25), (91, 27.25),
        (91, 27.5), (93.25, 27.5), (93.25, 27.25), (95.75, 27.25), (95.75, 27), (97, 27),
        (97, 26.75), (96.75, 26.75), (96.75, 26.5), (96.5, 26.5), (96.5, 26.25),
        (96.25, 26.25), (96.25, 26), (96, 26), (96, 25.75), (95.75, 25.75), (95.75, 25.5),
        (95.5, 25.5), (95.5, 25.25), (95.25, 25.25), (95.25, 25), (95, 25), (94.25, 24),
        (93.75, 24), (93.75, 23.75), (93.5, 23.75), (93.5, 23.5), (92.5, 22.75),
        (92.5, 22.25), (92.25, 22.25), (92.25, 22), (88, 21.75), (88, 21.5), (87.25, 21.5),
        (87.25, 21.25), (87, 21.25), (87, 21), (86, 20.25), (86, 19.75), (85.75, 19.75),
        (85.75, 19.25), (85.5, 19.25), (85.5, 18.75), (85.25, 18.75), (85.25, 18.25),
        (85, 18.25), (85, 17.75), (84.75, 17.75), (84.75, 17.25), (84.5, 17.25),
        (84.5, 16.75), (84.25, 16.75), (84.25, 16.25), (84, 16.25), (84, 15.75),
        (83.75, 15.75), (83.75, 15.25), (83.5, 15.25), (83.5, 14.75), (83.25, 14.75),
        (83.25, 14.25), (83, 14.25), (83, 13.75), (82.75, 13.75), (82.75, 13.25),
        (82.5, 13.25), (82.5, 12.75), (82.25, 12.75), (82.25, 12.25), (82, 12.25),
        (82, 11.75), (81.75, 11.75), (81.75, 11.25), (81.5, 11.25), (81.5, 10.75),
        (81.25, 10.75), (81.25, 10.25), (81, 10.25), (81, 9.75), (80.75, 9.75),
        (80.75, 9.25), (80.5, 9.25), (80.5, 8.75), (80.25, 8.75), (80.25, 8.25), (80, 8.25),
        (80, 8), (77, 8), (77, 8.25), (76.75, 8.25), (76.75, 8.75), (76.5, 8.75),
        (76.5, 9.25), (76.25, 9.25), (76.25, 9.75), (76, 9.75), (76, 10.25), (75.75, 10.25),
        (75.75, 10.75), (75.5, 10.75), (75.5, 11.25), (75.25, 11.25), (75.25, 11.75),
        (75, 11.75), (75, 12.25), (74.75, 12.25), (74.75, 13), (74.5, 13), (74.5, 13.5),
        (74.25, 13.5), (74.25, 14.25), (74, 14.25), (74, 14.75), (73.75, 14.75),
        (73.75, 15.5), (73.5, 15.5), (73.5, 16), (73.25, 16), (73, 17.25), (72.5, 17.5),
        (72.5, 18), (72.25, 18), (72.25, 18.5), (71.75, 18.75), (71.5, 19.75), (71, 20),
        (70.75, 21), (70.5, 21), (70.5, 21.25), (70.25, 21.25), (70.25, 21.75), (69.75, 22),
        (69.75, 22.5), (70, 22.5), (70, 24), (70.25, 24), (70.25, 24.25), (70.75, 24.25),
        (71, 24.75), (71.5, 24.75), (71.5, 25), (72.5, 25.25), (72.75, 25.75),
        (73.25, 25.75), (73.25, 26), (74.25, 26.25), (74.5, 26.75), (75, 26.75), (75, 27),
        (76, 27.25), (76.25, 27.75), (76.75, 27.75), (76.75, 28), (77.75, 28.75),
        (77.75, 29.75), (77.5, 29.75), (77.5, 30.25), (77, 30.25), (77, 30.5), (76.75, 30.5),
        (76.75, 30.75), (76.5, 30.75), (76.5, 31), (76.25, 31), (76.25, 31.25), (76, 31.25),
        (75.25, 32.25), (74, 32.5),
    ],
}

# ----------------------------------------------------------------------
# MINOR COUNTRIES: every bit of land that used to be plain green map is now a country.
# They are Neutral, greyed out, split into 3 zones like the major powers, start with NO
# troops and aren't in the "Acting as" list - they are places to march through, occupy
# and fight over. Borders were traced
# from the leftover land, so they fit snugly against the 16 major powers.
# ----------------------------------------------------------------------
FILLER_OUTLINES = {
    "Spain": [
        (-2.5, 45.75), (-2, 45.75), (-2, 45.5), (-1.5, 45.25), (-1.5, 43.5), (-1.75, 43.5),
        (-1.75, 43.25), (-0.75, 43.25), (-0.75, 43), (0, 43), (0, 42.75), (1, 42.75),
        (1, 42.5), (1.75, 42.5), (1.75, 42.25), (2.25, 42.25), (2.25, 42), (2.75, 41.75),
        (2.75, 41.25), (2.5, 41.25), (2.5, 41), (2.25, 41), (2.25, 40.75), (2, 40.75),
        (2, 40.5), (1, 39.75), (1, 39.25), (0.75, 39.25), (0.75, 38.75), (0.5, 38.75),
        (0.5, 38), (0.25, 38), (-0.5, 37), (-1, 37), (-1.75, 36), (-10, 36), (-10, 37),
        (-9.75, 37), (-9.75, 39.5), (-9.5, 39.5), (-9.5, 40.75), (-9.25, 40.75),
        (-9.25, 42.25), (-9, 42.25), (-9, 43), (-8.75, 43), (-8.75, 43.25), (-8, 43.25),
        (-8, 43.5), (-7.5, 43.5), (-7.5, 43.75), (-7, 43.75), (-7, 44), (-6.25, 44),
        (-6.25, 44.25), (-5.75, 44.25), (-5.75, 44.5), (-5, 44.5), (-5, 44.75),
        (-4.5, 44.75), (-4.5, 45), (-4, 45), (-4, 45.25), (-2.5, 45.5),
    ],
    "Norway": [
        (22.5, 70), (28.5, 70), (28.5, 69.25), (28.25, 69.25), (28, 68.25), (27.75, 68.25),
        (27, 67.25), (26.5, 67.25), (25.75, 66.25), (25.25, 66.25), (25, 65.75),
        (22.5, 65.75), (22.5, 65.5), (22, 65.5), (22, 65.25), (21.75, 65.25), (21.25, 64.5),
        (20.75, 64.5), (20.75, 64.25), (20, 64.25), (20, 64.5), (19.75, 64.5),
        (19.75, 64.25), (18, 64.25), (18, 64), (17, 64), (17, 63.75), (16, 63.75),
        (16, 63.5), (15, 63.5), (15, 63.25), (14, 63.25), (14, 63), (13, 63), (13, 62.75),
        (12, 62.75), (12, 62.5), (11, 62.5), (11, 62.25), (10.5, 62.25), (10.5, 63),
        (10.75, 63), (11, 63.5), (11.5, 63.5), (11.5, 63.75), (11.75, 63.75), (11.75, 64),
        (12.25, 64), (12.75, 64.75), (13.25, 64.75), (13.5, 65.25), (14, 65.25), (14, 65.5),
        (14.5, 65.5), (14.75, 66), (15.25, 66), (15.5, 66.5), (16, 66.5), (16.75, 67.5),
        (17.75, 67.75), (18, 68.25), (18.5, 68.25), (18.5, 68.5), (18.75, 68.5), (19, 69),
        (19.5, 69), (19.75, 69.5), (22.5, 69.75),
    ],
    "Sweden": [
        (19.75, 64.5), (20, 64.5), (20.25, 64), (19.5, 64), (19.5, 63.75), (18.5, 63.5),
        (18.5, 63.25), (18.25, 63.25), (18.25, 62.75), (17.25, 62), (17.25, 61.5),
        (17.5, 61.5), (17.5, 60.5), (17.75, 60.5), (18, 60), (18.5, 60), (18.5, 59.75),
        (18.75, 59.75), (18.75, 59.25), (16.5, 57.75), (16.25, 56.25), (14.25, 56.25),
        (14.25, 55.25), (13, 55.25), (13, 55.5), (12.5, 55.5), (12.5, 55.25), (12.75, 55.25),
        (12.75, 54.5), (11.75, 54.5), (11.75, 54.25), (11.5, 54.25), (11.5, 54.5),
        (10.25, 54.5), (10.25, 54.75), (8.75, 54.75), (8.75, 55), (8.25, 55), (8.25, 55.25),
        (8, 55.25), (8.5, 57.5), (8.75, 57.5), (9, 58), (9.5, 58), (9.5, 58.25), (10, 58.25),
        (10.25, 58.75), (10.75, 58.75), (10.75, 59), (11, 59), (10.5, 62.25), (11, 62.25),
        (11, 62.5), (12, 62.5), (12, 62.75), (13, 62.75), (13, 63), (14, 63), (14, 63.25),
        (15, 63.25), (15, 63.5), (16, 63.5), (16, 63.75), (17, 63.75), (17, 64), (18, 64),
        (18, 64.25), (19.75, 64.25),
    ],
    "Czechoslovakia": [
        (14.5, 50.75), (15.75, 50.75), (15.75, 50.5), (17.75, 50.25), (17.75, 50),
        (18.75, 49.75), (19, 49.25), (21, 49), (21.25, 48.5), (21.75, 48.5), (21.75, 48),
        (21, 48), (21, 47.75), (20.25, 47.75), (20.25, 47.5), (18.75, 47.25), (18.75, 47),
        (18.25, 47), (18.25, 46.75), (17.75, 46.75), (17.75, 46.5), (17.25, 46.5),
        (17.25, 46.25), (16.75, 46.25), (16.75, 46), (16.25, 46), (16.25, 45.75), (15, 45.5),
        (15, 45.25), (14.5, 45.25), (14.5, 45), (14.25, 45), (14.25, 45.25), (14, 45.25),
        (14, 45.5), (13.75, 45.5), (13.75, 45.75), (13.5, 45.75), (13.5, 46), (13.25, 46),
        (12.5, 47), (12.75, 47), (12.75, 47.25), (13.25, 47.25), (13.25, 47.75),
        (14.25, 48.5), (14.25, 49), (14, 49), (14, 49.5), (13.75, 49.5), (13.75, 50.25),
        (14, 50.25), (14, 50.5), (14.5, 50.5),
    ],
    "Yugoslavia": [
        (21, 48), (21.75, 48), (21.75, 47.5), (21.5, 47.5), (21.5, 47.25), (21.25, 47.25),
        (21.25, 47), (20.25, 46.25), (20.25, 46), (20.5, 46), (20.5, 45.5), (20.75, 45.5),
        (20.75, 45), (21, 45), (21, 44.75), (21.5, 44.75), (21.5, 44.5), (23, 44.25),
        (23.25, 43.75), (24.5, 43.75), (24.5, 43.5), (25, 43.5), (25, 43.25), (24.25, 43.25),
        (24.25, 43), (23.5, 43), (23.5, 42.75), (21.75, 42.5), (21.75, 42.25), (21, 42.25),
        (21, 42), (20.25, 42), (20.25, 41.75), (19, 41.5), (18.75, 42), (18, 42),
        (17.5, 42.75), (17, 42.75), (16.5, 43.5), (16, 43.5), (15.75, 44), (15.25, 44),
        (15.25, 44.25), (14.5, 44.75), (14.5, 45.25), (15.75, 45.5), (15.75, 45.75),
        (16.25, 45.75), (16.25, 46), (16.75, 46), (16.75, 46.25), (17.25, 46.25),
        (17.25, 46.5), (17.75, 46.5), (17.75, 46.75), (18.25, 46.75), (18.25, 47),
        (18.75, 47), (18.75, 47.25), (19.5, 47.25), (19.5, 47.5), (20.25, 47.5),
        (20.25, 47.75), (21, 47.75),
    ],
    "Greece": [
        (25.25, 43.75), (26.5, 43.75), (26.5, 43.5), (27.5, 43.75), (27.5, 43.5), (28, 43.5),
        (28, 43.25), (28.25, 43.25), (28.25, 43), (28, 43), (28, 41.25), (28.75, 41.25),
        (28.25, 36.75), (27.75, 36.75), (27.75, 37), (27.25, 37), (27.25, 37.25),
        (27, 37.25), (27, 37.75), (26.75, 37.75), (26.75, 38.25), (26.5, 38.25),
        (26.5, 38.75), (26.25, 38.75), (26, 40.25), (24.25, 40.25), (24.25, 39.25),
        (24, 39.25), (24, 37.5), (23.5, 37.25), (23.25, 36.25), (22.75, 36), (22.75, 36.25),
        (22.5, 36.25), (22.5, 36.5), (22.25, 36.5), (22.25, 36.75), (21.25, 37.5),
        (21, 38.5), (20.5, 38.5), (20.5, 38.75), (19.75, 39.25), (19.25, 41.5), (19.5, 41.5),
        (19.5, 41.75), (20.25, 41.75), (20.25, 42), (21, 42), (21, 42.25), (21.75, 42.25),
        (21.75, 42.5), (22.75, 42.5), (22.75, 42.75), (23.5, 42.75), (23.5, 43), (25, 43.25),
    ],
    "Turkey": [
        (41.25, 44.25), (43, 44.25), (43, 44), (43.75, 44), (43.75, 43.75), (44.25, 43.75),
        (44.5, 43.25), (45, 43.25), (45, 43), (45.5, 42.75), (45.5, 42.25), (45, 42.25),
        (45, 42), (44.5, 42), (44.5, 41.75), (44, 41.75), (44, 41.5), (42.75, 41.25),
        (42.25, 40.5), (41, 40.25), (40.5, 39.5), (40, 39.5), (40, 39.25), (39.5, 39.25),
        (39.5, 39), (39, 39), (39, 38.75), (38.25, 38.75), (37.75, 38), (37.25, 38),
        (36.5, 37), (36, 37), (36, 36.75), (35.75, 36.75), (35.5, 36.25), (35, 36.25),
        (35, 36), (28.25, 36), (28.25, 37.75), (28.5, 37.75), (28.5, 40), (28.75, 40),
        (28.75, 41.25), (30.75, 41.25), (30.75, 41), (31, 41), (31, 41.25), (32.25, 41.5),
        (32.25, 41.75), (32.75, 41.75), (32.75, 42), (35.5, 42), (35.5, 41.75),
        (36.25, 41.75), (36.25, 41.5), (37, 41.5), (37, 41.25), (38.25, 41.25), (38.25, 41),
        (41.25, 41.25), (41.25, 41.5), (41.5, 41.5), (41.5, 42), (41.75, 42), (41.75, 42.5),
        (41.25, 42.5), (41, 43), (40.5, 43), (40.25, 43.5), (39.75, 43.5), (40, 44),
        (41.25, 44),
    ],
    "Iraq": [
        (47.75, 42.75), (48, 42.75), (48, 42.5), (48.5, 42.5), (48.5, 42.25), (49.5, 41.5),
        (49.5, 41), (50, 40.75), (49.75, 40.25), (49.25, 40.25), (49.25, 40), (49, 40),
        (48.75, 30.5), (48.5, 30.5), (48.5, 29.75), (48.25, 29.75), (48.75, 28.75), (38, 28),
        (38, 28.25), (38.25, 28.25), (38.25, 28.75), (38.5, 28.75), (38.5, 29.5),
        (38.75, 29.5), (38.75, 30), (39, 30), (39, 30.5), (39.25, 30.5), (39.25, 31),
        (39.5, 31), (39.5, 31.5), (39.75, 31.5), (40, 32.75), (41, 33.5), (41, 34.25),
        (41.25, 34.25), (41.25, 34.75), (42, 35.25), (42, 35.75), (42.5, 36), (42.5, 36.5),
        (42.75, 36.5), (43, 37.5), (43.25, 37.5), (43.25, 37.75), (43.5, 37.75),
        (43.5, 38.25), (43.75, 38.25), (43.75, 38.5), (44.75, 39.25), (44.75, 39.75),
        (45.5, 40.25), (45.5, 40.75), (45.75, 40.75), (45.75, 41), (46, 41), (46, 41.25),
        (46.25, 41.25), (47, 42.25), (47.5, 42.25),
    ],
    "Iran": [
        (53.25, 42.75), (58.75, 40), (58.75, 39.25), (59, 39.25), (59, 38), (59.25, 38),
        (59.25, 36.75), (59.5, 36.75), (59.5, 35.5), (59.75, 35.5), (59.75, 34.25),
        (60, 34.25), (60, 32.5), (60.25, 32.5), (60.25, 31.25), (60.5, 31.25), (60.5, 27.75),
        (60.25, 27.75), (60, 26.5), (59.75, 26.5), (59.75, 25.25), (58.5, 25.25),
        (58.5, 25.5), (56.5, 25.75), (56.5, 26), (56.75, 26), (56.5, 27), (55.5, 27),
        (55.5, 26.75), (54, 26.75), (54, 27), (53.25, 27), (53.25, 27.25), (52.25, 27.5),
        (51.75, 28.25), (51.25, 28.25), (51.25, 28.5), (51, 28.5), (51, 28.75),
        (50.75, 28.75), (50.75, 29), (50.5, 29), (50.5, 29.25), (50.25, 29.25),
        (49.5, 30.25), (49.25, 30.25), (49.25, 30), (48.5, 30), (48.5, 30.5), (48.75, 30.5),
        (48.75, 35.5), (49, 35.5), (49, 37.5), (49.25, 37.5), (49.25, 37.25), (50, 37.25),
        (50, 37), (50.5, 37), (50.5, 36.75), (53.5, 37), (54, 40.25), (53.75, 40.25),
        (53.75, 40.75), (53.5, 40.75), (53.5, 41.25), (53.25, 41.25), (53.25, 41.75),
        (53, 41.75), (53, 42.5), (53.25, 42.5),
    ],
    "Saudi Arabia": [
        (46.75, 28.75), (48.75, 28.75), (48.75, 28.5), (49.75, 27.75), (49.75, 27), (50, 27),
        (50, 26.75), (50.25, 26.75), (50.25, 26.5), (51.25, 25.75), (51.25, 25),
        (51.75, 24.75), (51.75, 24.25), (54.25, 24.25), (54.25, 24.5), (54.75, 24.5),
        (55, 25), (55.5, 25), (55.75, 25.5), (56.25, 25.5), (56.25, 25), (56.5, 25),
        (56.5, 24.5), (56.75, 24.5), (57, 24), (57.5, 24), (57.5, 23.75), (58, 23.75),
        (58.25, 23.25), (59.25, 23), (59.75, 22.25), (59.25, 22), (59, 21), (58.75, 21),
        (58.75, 20.75), (58.5, 20.75), (58.5, 20.5), (58.25, 20.5), (58.25, 20.25),
        (58, 20.25), (58, 20), (57.75, 20), (57.75, 19.75), (57.5, 19.75), (57.5, 19.5),
        (57.25, 19.5), (57.25, 19.25), (57, 19.25), (57, 19), (56.75, 19), (56.75, 18.75),
        (56.5, 18.75), (56.5, 18.5), (56.25, 18.5), (55.5, 17.5), (55, 17.5), (55, 17.25),
        (54.5, 17.25), (54.5, 17), (54, 17), (54, 16.75), (53.5, 16.75), (53.5, 16.5),
        (53, 16.5), (53, 16.25), (52.25, 16.25), (52.25, 16), (51.75, 16), (51.75, 15.75),
        (51.25, 15.75), (51.25, 15.5), (50.75, 15.5), (50.75, 15.25), (50.25, 15.25),
        (50.25, 15), (49.75, 15), (49.75, 14.75), (49.25, 14.75), (49.25, 14.5),
        (48.75, 14.5), (48.75, 14.25), (48.25, 14.25), (48.25, 14), (47.75, 14),
        (47.75, 13.75), (47.25, 13.75), (47.25, 13.5), (46.75, 13.5), (46.75, 13.25),
        (46.25, 13.25), (46.25, 13), (45.75, 13), (45.75, 12.75), (45.25, 12.75),
        (45.25, 12.5), (44.75, 12.5), (44.75, 12.25), (44.25, 12.25), (44.25, 12), (44, 12),
        (43, 16), (42.75, 16), (42, 17), (41.5, 17), (40.75, 18), (40.25, 18), (39.5, 19),
        (39, 19), (39, 19.25), (38.75, 19.25), (38.75, 19.5), (37.75, 20.25), (37.5, 21.75),
        (37.25, 21.75), (37.25, 22.25), (37, 22.25), (37, 23.5), (37.25, 23.5), (37.25, 26),
        (37.5, 26), (37.5, 27.5), (37.75, 27.5), (37.75, 28), (39.75, 28), (39.75, 28.25),
        (43.25, 28.25), (43.25, 28.5), (46.75, 28.5),
    ],
    "Afghanistan": [
        (58.75, 39.75), (74.25, 39), (74.25, 38.75), (74, 38.75), (74, 38), (74.25, 38),
        (74.25, 37.75), (78.25, 36.5), (78.25, 33.75), (78, 33.75), (78, 34), (74, 34),
        (74, 33.75), (73.5, 33.75), (73.5, 33.5), (73, 33.5), (73, 33.25), (72, 33.25),
        (72, 33), (70.5, 32.75), (70.5, 32.5), (70, 32.5), (70, 32.25), (69.25, 32.25),
        (69.25, 32), (68.75, 32), (68.75, 31.75), (67.25, 31.5), (67.25, 31.25), (66, 31),
        (66, 30.75), (65.5, 30.75), (65.5, 30.5), (64.75, 30.5), (64.75, 30.25), (64, 30.25),
        (64, 30), (63.5, 30), (63.5, 29.75), (62.75, 29.75), (62.5, 29.25), (61.75, 29.25),
        (61.75, 29), (60.5, 28.75), (60.5, 31.25), (60.25, 31.25), (60, 34.25),
        (59.75, 34.25), (59.75, 35.5), (59.5, 35.5), (59.5, 36.75), (59.25, 36.75),
        (59.25, 38), (59, 38), (59, 39.25), (58.75, 39.25),
    ],
    "Pakistan": [
        (73.5, 33.75), (74, 33.75), (74, 32.5), (75.25, 32.25), (75.25, 32), (75.5, 32),
        (75.5, 31.75), (75.75, 31.75), (75.75, 31.5), (76, 31.5), (76, 31.25),
        (76.25, 31.25), (77, 30.25), (77.5, 30.25), (77.5, 29.75), (77.75, 29.75),
        (77.75, 28.75), (77.5, 28.75), (76.75, 27.75), (76.25, 27.75), (76, 27.25),
        (75.5, 27.25), (75.5, 27), (74.5, 26.75), (74.25, 26.25), (73.75, 26.25),
        (73.75, 26), (72.75, 25.75), (72.5, 25.25), (72, 25.25), (72, 25), (71, 24.75),
        (70.75, 24.25), (70.25, 24.25), (70.25, 24), (70, 24), (70, 22.5), (69.75, 22.5),
        (69.75, 22.25), (69.25, 22.25), (69, 22.75), (68, 23), (68, 23.25), (67.75, 23.25),
        (67.75, 23.5), (67.25, 23.5), (67.25, 23.75), (66.5, 23.75), (66.5, 24), (66.25, 24),
        (66, 24.5), (65.5, 24.5), (65.25, 25), (59.5, 25), (59.5, 25.25), (59.75, 25.25),
        (59.75, 26.5), (60, 26.5), (60, 27.25), (60.25, 27.25), (60.25, 27.75),
        (60.5, 27.75), (60.5, 28.75), (61.75, 29), (61.75, 29.25), (62.5, 29.25),
        (62.75, 29.75), (63.5, 29.75), (63.5, 30), (64, 30), (64, 30.25), (65.5, 30.5),
        (65.5, 30.75), (66.75, 31), (66.75, 31.25), (67.25, 31.25), (67.25, 31.5),
        (68.75, 31.75), (68.75, 32), (70, 32.25), (70, 32.5), (70.5, 32.5), (70.5, 32.75),
        (71.25, 32.75), (71.25, 33), (72, 33), (72, 33.25), (73, 33.25), (73, 33.5),
        (73.5, 33.5),
    ],
    "Kazakhstan": [
        (67.5, 54.75), (68.25, 54.75), (68.5, 54.25), (69.25, 54.25), (69.5, 53.75),
        (70, 53.75), (70.75, 52.75), (71.75, 52.5), (72.5, 51.5), (73.5, 51.25), (73.5, 51),
        (73.75, 51), (74.5, 50), (79.5, 49.75), (79.5, 49.5), (82.5, 49.5), (82.5, 49.25),
        (85.25, 49.25), (85.5, 44), (85, 43.75), (85, 44), (84.25, 44), (84.25, 44.25),
        (83.75, 44.25), (83.75, 44.5), (83, 44.5), (83, 44.75), (81.5, 45), (81.5, 44.75),
        (80.75, 44.75), (80.75, 44.5), (79.75, 44.5), (79.75, 44.25), (79, 44.25), (79, 44),
        (78, 44), (78, 43.75), (77.25, 43.75), (77.25, 43.5), (75.5, 43.25), (75.5, 43),
        (75, 43), (75, 42.5), (74.75, 42.5), (74.75, 41.25), (74.5, 41.25), (74.25, 39),
        (58.75, 39.75), (58.5, 40.25), (58, 40.25), (58, 40.5), (57.5, 40.5), (57.5, 40.75),
        (57, 40.75), (57, 41), (56.5, 41), (56.5, 41.25), (56, 41.25), (56, 41.5),
        (55.5, 41.5), (55.5, 41.75), (55, 41.75), (55, 42), (54.5, 42), (54.5, 42.25),
        (53.5, 42.5), (53.5, 42.75), (53.25, 42.75), (53.25, 43.5), (53.5, 43.5),
        (53.5, 44.25), (53.75, 44.25), (53.75, 45), (54, 45), (54, 45.25), (53.5, 45.5),
        (53.5, 46), (53.25, 46), (52.75, 46.75), (53.25, 46.75), (54, 47.75), (55, 47.75),
        (55.25, 48.25), (56, 48.25), (56, 48.5), (57.25, 48.75), (57.25, 49), (57.75, 49),
        (57.75, 49.25), (58.5, 49.25), (58.5, 49.5), (60, 49.75), (60.5, 50.5),
        (61.75, 50.75), (62.5, 51.75), (63.75, 52), (64.5, 53), (65.5, 53.25),
        (65.75, 53.75), (66.25, 53.75), (66.5, 54.25), (67, 54.25), (67, 54.5), (67.5, 54.5),
    ],
    "Mongolia": [
        (102.75, 50), (105.75, 49.75), (105.75, 49.5), (106.25, 49.5), (106.75, 48.75),
        (107.25, 48.75), (107.25, 48.5), (107.75, 48.5), (107.75, 48.25), (108.5, 48.25),
        (108.5, 48), (109, 48), (109, 47.75), (109.5, 47.75), (109.5, 47.5), (110.5, 47.25),
        (111, 46.5), (112.25, 46.25), (112.25, 46), (112.75, 46), (112.75, 45.75),
        (113.25, 45.75), (113.25, 45.5), (114.25, 45.25), (114.75, 44.5), (116, 44.25),
        (116, 44), (116.5, 44), (116.5, 43.75), (117, 43.75), (117, 43.5), (118, 43.25),
        (118.25, 42.75), (118.75, 42.75), (118.75, 42.5), (119.75, 41.75), (119.5, 40.5),
        (119, 40.5), (118.75, 40), (118.25, 40), (118, 39.5), (117.5, 39.5), (117.25, 39),
        (116.75, 39), (116.75, 39.25), (116.25, 39.25), (116.25, 39.5), (115.75, 39.5),
        (115.75, 39.75), (115.25, 39.75), (115.25, 40), (114.75, 40), (114.75, 40.25),
        (114.25, 40.25), (114.25, 40.5), (113.75, 40.5), (113.75, 40.75), (113.25, 40.75),
        (113.25, 41), (112, 41), (112, 41.25), (110, 41.25), (110, 41.5), (108, 41.5),
        (108, 41.75), (106, 41.75), (106, 42), (89.75, 42), (89.75, 42.25), (89, 42.25),
        (89, 42.5), (88.25, 42.5), (88.25, 42.75), (87.75, 42.75), (87.75, 43), (87, 43),
        (87, 43.25), (86.25, 43.25), (86.25, 43.5), (85.25, 43.75), (85.25, 44), (85.5, 44),
        (85.25, 49.25), (85.5, 49.25), (85.5, 49), (91, 49), (91, 49.25), (98.25, 49.5),
        (98.25, 49.75), (102.75, 49.75),
    ],
    "Korea": [
        (124.75, 42), (129, 42), (129, 41.75), (130.25, 41.5), (130.25, 41.25),
        (130.5, 41.25), (130.5, 40.75), (130.25, 40.75), (130.25, 40.25), (130, 40.25),
        (129.25, 39.25), (128.75, 39.25), (128.25, 38.5), (127.75, 38.5), (127.25, 37.75),
        (126.75, 37.75), (126.75, 37.5), (125.75, 36.75), (125.75, 36.25), (125.25, 36),
        (125.25, 35.5), (125, 35.5), (124.75, 34.5), (124.25, 34.25), (124.25, 33.75),
        (124, 33.75), (124, 33.25), (123.75, 33.25), (123.5, 32.25), (123, 32), (122.75, 31),
        (121.75, 31), (121.75, 31.5), (121.25, 31.5), (121.25, 31.75), (121, 31.75),
        (121, 32.5), (120.75, 32.5), (120.5, 34.75), (120.25, 34.75), (120.25, 36),
        (120.5, 36), (120.75, 36.5), (122, 36.75), (122, 37), (122.5, 37.25), (122.5, 38),
        (122.75, 38), (122.75, 38.25), (123, 38.25), (123, 38.75), (124, 39.5), (124, 40),
        (123.5, 40.25), (123.25, 41.25), (123.5, 41.25), (123.5, 41.5), (124, 41.5),
        (124, 41.75), (124.75, 41.75),
    ],
    "Syria": [
        (45.5, 42.75), (46, 42.75), (46.25, 42.25), (46.75, 42.25), (46.75, 41.75),
        (46.5, 41.75), (46.5, 41.5), (45.5, 40.75), (45.5, 40.25), (44.75, 39.75),
        (44.75, 39.25), (44.5, 39.25), (44.5, 39), (43.5, 38.25), (43.5, 37.75), (43, 37.5),
        (43, 37), (42.75, 37), (42.5, 36), (42.25, 36), (42.25, 35.75), (42, 35.75),
        (42, 35.25), (41.25, 34.75), (41, 33.5), (40, 32.75), (39.75, 31.5), (39.5, 31.5),
        (39.5, 31), (39.25, 31), (39.25, 30.5), (39, 30.5), (39, 30), (38.75, 30),
        (38.5, 28.75), (38.25, 28.75), (38.25, 28.25), (38, 28.25), (38, 28), (37.25, 28),
        (37.25, 28.25), (37, 28.25), (36.25, 29.25), (35.75, 29.25), (35, 30.25),
        (34.5, 30.25), (34.5, 30.5), (33.5, 30.75), (33.25, 31.25), (32.5, 31.25),
        (32.5, 32), (32.75, 32), (32.75, 32.25), (33, 32.25), (33, 32.75), (33.5, 33),
        (33.75, 34), (34, 34), (34, 34.25), (34.25, 34.25), (34.25, 34.5), (34.5, 34.5),
        (34.5, 34.75), (35.5, 35.5), (35.5, 36), (35, 36), (35, 36.25), (35.5, 36.25),
        (36, 37), (36.5, 37), (36.5, 37.25), (36.75, 37.25), (37.25, 38), (37.75, 38),
        (38.25, 38.75), (39, 38.75), (39, 39), (39.5, 39), (39.5, 39.25), (40.5, 39.5),
        (41, 40.25), (42.25, 40.5), (42.75, 41.25), (44, 41.5), (44, 41.75), (44.5, 41.75),
        (44.5, 42), (45.5, 42.25),
    ],
    "Tibet": [
        (78.25, 36.5), (79.5, 36.25), (79.5, 36), (80.75, 36), (80.75, 35.75), (82.5, 35.75),
        (82.5, 35.5), (85.25, 35.5), (85.25, 35.25), (88, 35.25), (88, 35), (90.75, 35),
        (90.75, 34.75), (93.25, 34.75), (93.25, 34.5), (97.75, 34.25), (97.75, 34),
        (98.75, 34), (98.75, 33.75), (99.25, 33.75), (99.25, 33.5), (100.25, 32.75),
        (100.25, 32.25), (100.5, 32.25), (100.5, 32), (101.5, 31.25), (101.5, 30.75),
        (100.75, 30.75), (100.75, 30.5), (100.25, 30.5), (100.25, 30.25), (99.75, 30.25),
        (99.75, 30), (99.25, 30), (99.25, 29.75), (98.75, 29.75), (98.75, 29.5),
        (98.25, 29.5), (98.25, 29.25), (97.75, 29.25), (97.75, 29), (97.25, 29),
        (97.25, 28.75), (96.75, 28.75), (96.75, 28.5), (95.75, 28.25), (95.5, 27.75),
        (95, 27.75), (95, 27.25), (91, 27.5), (91, 27.25), (89, 27.25), (89, 27),
        (87.25, 27), (87.25, 26.75), (84.5, 26.5), (84.5, 26.75), (83.75, 26.75),
        (83.75, 27), (83, 27), (83, 27.25), (82, 27.25), (82, 27.5), (81.25, 27.5),
        (81.25, 27.75), (79.75, 28), (79.75, 28.25), (79.25, 28.5), (79.25, 29),
        (78.75, 29.25), (78.75, 29.75), (79.5, 30.25), (79.5, 30.75), (79.75, 30.75),
        (80, 31.25), (79.5, 31.5), (79.5, 32), (79, 32.25), (79, 32.75), (78.75, 32.75),
        (78.75, 33), (78.5, 33), (78.5, 33.5), (78.25, 33.5),
    ],
    "Burma": [
        (100.75, 30.75), (101.75, 30.75), (101.75, 30.5), (102.75, 29.75), (102.75, 29.25),
        (103, 29.25), (103, 29), (104, 28.25), (104, 27.75), (104.25, 27.75), (104.25, 27.5),
        (105.25, 26.75), (105.5, 25.75), (104.75, 25.25), (104.75, 24.75), (104.25, 24.5),
        (104, 23.5), (103.75, 23.5), (103.75, 23.25), (103.5, 23.25), (103.5, 22.75),
        (102.75, 22.25), (102.75, 21.75), (102.25, 21.5), (102.25, 21), (102, 21),
        (102, 20.75), (101.25, 20.75), (101.25, 20.5), (101, 20.5), (100.25, 19.5),
        (99.75, 19.5), (99.75, 19.25), (99.5, 19.25), (98.75, 18.25), (98, 18.25),
        (97.5, 17.5), (97, 17.5), (96.25, 16.5), (95.75, 16.5), (95.75, 16.25),
        (94.75, 15.5), (94.75, 15.75), (94.5, 15.75), (94.5, 16.25), (94.25, 16.25),
        (94.25, 16.75), (94, 16.75), (94, 17.25), (93.75, 17.25), (93.75, 18.25),
        (93.5, 18.25), (93.5, 18.75), (93, 19), (93, 20), (92.75, 20), (92.75, 20.5),
        (92.5, 20.5), (92.5, 21), (92.25, 21), (92.25, 21.75), (92, 21.75), (92, 22),
        (92.5, 22.25), (92.5, 22.75), (92.75, 22.75), (92.75, 23), (93, 23), (93.75, 24),
        (94.25, 24), (94.25, 24.25), (94.5, 24.25), (94.5, 24.5), (94.75, 24.5),
        (94.75, 24.75), (95, 24.75), (95, 25), (95.25, 25), (95.25, 25.25), (95.5, 25.25),
        (95.5, 25.5), (95.75, 25.5), (95.75, 25.75), (96, 25.75), (96, 26), (97, 26.75),
        (97, 27), (95.75, 27), (95.75, 27.25), (95, 27.25), (95, 27.75), (95.5, 27.75),
        (95.75, 28.25), (96.25, 28.25), (96.25, 28.5), (96.75, 28.5), (96.75, 28.75),
        (97.25, 28.75), (97.25, 29), (97.75, 29), (97.75, 29.25), (98.25, 29.25),
        (98.25, 29.5), (98.75, 29.5), (98.75, 29.75), (99.25, 29.75), (99.25, 30),
        (99.75, 30), (99.75, 30.25), (100.25, 30.25), (100.25, 30.5), (100.75, 30.5),
    ],
    "Thailand": [
        (102, 21), (102.5, 20.75), (102.5, 20), (102.75, 20), (103, 17.5), (103.25, 17.5),
        (103.25, 16.5), (103.5, 16.5), (103.5, 15.25), (103.75, 15.25), (104, 12.75),
        (104.25, 12.75), (104.5, 10.5), (104.75, 10.5), (104.75, 9.25), (105, 9.25),
        (105, 7.75), (104.25, 7.25), (104.25, 6.75), (103.75, 6.5), (103.75, 6),
        (102.75, 5.25), (102.75, 4.75), (102.5, 4.75), (102.25, 4.25), (101.75, 4.25),
        (101.75, 4.75), (101.5, 4.75), (101.25, 5.75), (100.75, 6), (100.75, 6.5),
        (100.5, 6.5), (100.5, 7), (100.25, 7), (100.25, 7.75), (100, 7.75), (100, 8.25),
        (99.75, 8.25), (99.75, 8.75), (99.5, 8.75), (99.5, 9.25), (99.25, 9.25),
        (99.25, 9.75), (99, 9.75), (99, 10.25), (98.75, 10.25), (98.75, 10.75),
        (98.5, 10.75), (98.25, 11.75), (98, 11.75), (98, 12), (97.75, 12), (97.75, 12.25),
        (97.5, 12.25), (97.5, 12.5), (97.25, 12.5), (97.25, 12.75), (97, 12.75), (97, 13),
        (96.75, 13), (96.75, 13.25), (96.5, 13.25), (96.5, 13.5), (96.25, 13.5),
        (96.25, 13.75), (96, 13.75), (96, 14), (95, 14.75), (95, 15.25), (94.75, 15.25),
        (94.75, 15.5), (95, 15.5), (95.75, 16.5), (96.25, 16.5), (97, 17.5), (97.5, 17.5),
        (98, 18.25), (98.75, 18.25), (98.75, 18.5), (99, 18.5), (99.75, 19.5),
        (100.25, 19.5), (100.25, 19.75), (100.5, 19.75), (101.25, 20.75), (102, 20.75),
    ],
    "Indochina": [
        (105.5, 26), (105.75, 26), (105.75, 25.75), (106.5, 25.25), (106.5, 24.75),
        (106.75, 24.75), (106.75, 24.5), (107.75, 23.75), (107.75, 23), (108, 23),
        (108.75, 22), (113, 21.75), (113, 21.5), (113.5, 21.5), (114.25, 20.5), (114, 20.5),
        (114, 20.25), (113.5, 20.25), (113.5, 20), (113, 20), (112.75, 19.5),
        (111.75, 19.25), (111.25, 18.5), (110.75, 18.5), (110.75, 18.25), (110.25, 18.25),
        (110.25, 18), (110, 18), (110, 17.5), (109.75, 17.5), (109.75, 16.5), (109.5, 16.5),
        (109.5, 15.5), (109.25, 15.5), (109.25, 14.5), (109, 14.5), (109, 13.5),
        (108.75, 13.5), (108.75, 12.5), (108.5, 12.5), (108.5, 11.5), (108.25, 11.5),
        (108.25, 10.5), (108, 10.5), (108, 10), (107.75, 10), (107.5, 9.5), (107, 9.5),
        (106.75, 9), (106.25, 9), (106, 8.5), (105.5, 8.5), (105.5, 8.25), (105, 8),
        (105, 9.25), (104.75, 9.25), (104.5, 11.75), (104.25, 11.75), (104.25, 12.75),
        (104, 12.75), (104, 14), (103.75, 14), (103.75, 15.25), (103.5, 15.25),
        (103.5, 16.5), (103.25, 16.5), (103.25, 17.5), (103, 17.5), (103, 18.75),
        (102.75, 18.75), (102.75, 20), (102.5, 20), (102.25, 21.5), (102.5, 21.5),
        (102.5, 21.75), (102.75, 21.75), (102.75, 22.25), (103.5, 22.75), (103.5, 23.25),
        (104, 23.5), (104.25, 24.5), (104.75, 24.75), (104.75, 25.25), (105, 25.25),
    ],
    "Morocco": [
        (2.25, 36.75), (3, 36.75), (3, 36.25), (2.75, 36.25), (2.75, 36), (2.5, 36),
        (2.5, 35.75), (1.5, 35), (1.5, 34.25), (1.25, 34.25), (1.25, 34), (1, 34),
        (1, 33.75), (0.75, 33.75), (0.75, 33.5), (-0.25, 32.75), (-0.25, 32.25), (-1, 31.75),
        (-1, 31), (-2, 30.25), (-2.25, 29.25), (-3, 28.75), (-3.25, 27.75), (-4, 27.25),
        (-4, 26.75), (-4.25, 26.75), (-4.5, 25.75), (-5, 25.5), (-5, 25), (-5.25, 25),
        (-5.25, 24.5), (-5.5, 24.5), (-5.5, 24), (-5.75, 24), (-5.75, 23.75), (-6.75, 23.75),
        (-6.75, 23.5), (-8.5, 23.5), (-8.5, 23.25), (-10, 23.25), (-10, 23), (-11.25, 23),
        (-11.25, 22.75), (-12.5, 22.75), (-12.5, 22.5), (-16.25, 22.25), (-16.25, 22.5),
        (-16, 22.5), (-16, 23), (-15.5, 23.25), (-15.25, 24.25), (-14.5, 24.75),
        (-14.25, 25.75), (-13.75, 26), (-13.5, 27), (-13.25, 27), (-13.25, 27.25),
        (-13, 27.25), (-13, 27.5), (-12.75, 27.5), (-12.75, 27.75), (-12.5, 27.75),
        (-12.5, 28), (-12.25, 28), (-12.25, 28.25), (-12, 28.25), (-12, 28.5),
        (-11.75, 28.5), (-11.75, 28.75), (-11.5, 28.75), (-11.5, 29), (-11.25, 29),
        (-11.25, 29.25), (-11, 29.25), (-11, 29.5), (-10.75, 29.5), (-10.75, 29.75),
        (-9.75, 30.5), (-9.5, 33), (-9, 33), (-9, 33.25), (-8.75, 33.25), (-8.75, 33.5),
        (-8.5, 33.5), (-8.5, 33.75), (-8.25, 33.75), (-8.25, 34), (-8, 34), (-8, 34.25),
        (-7.75, 34.25), (-7.75, 34.5), (-7.5, 34.5), (-6.75, 35.5), (-6.25, 35.5),
        (-6.25, 35.75), (-4.5, 35.75), (-4.5, 35.5), (-3.25, 35.5), (-3.25, 35.25),
        (-1.5, 35.25), (-1.5, 35.5), (-0.75, 35.5), (-0.75, 35.75), (0, 35.75), (0, 36),
        (0.75, 36), (0.75, 36.25), (1.5, 36.25), (1.5, 36.5), (2.25, 36.5),
    ],
    "Algeria": [
        (3.75, 37), (6.5, 37), (6.5, 36.75), (7, 36.75), (7, 36.5), (7.75, 36.5),
        (7.75, 36.25), (8.5, 36.25), (8.5, 36), (9.5, 36), (9.5, 19.25), (9.25, 19.25),
        (9.25, 19), (8.5, 19), (8.5, 18.75), (7.25, 19), (7.25, 19.25), (6.25, 19.25),
        (6.25, 19.5), (5, 19.75), (5, 20), (4.25, 20), (4, 20.5), (3.25, 20.5),
        (3.25, 20.75), (2.25, 20.75), (2.25, 21), (2, 21), (2, 21.25), (1.5, 21.25),
        (1.5, 21.5), (0.25, 21.5), (0.25, 21.75), (-0.5, 21.75), (-0.5, 22), (-0.75, 22),
        (-0.75, 22.25), (-1.25, 22.25), (-1.25, 22.5), (-2, 22.5), (-2, 22.75), (-3.75, 23),
        (-3.75, 23.25), (-4.5, 23.25), (-4.5, 23.5), (-5.75, 23.75), (-5.75, 24), (-5.5, 24),
        (-5.5, 24.5), (-5.25, 24.5), (-5.25, 25), (-5, 25), (-5, 25.5), (-4.5, 25.75),
        (-4.5, 26.25), (-4.25, 26.25), (-4, 27.25), (-3.25, 27.75), (-3.25, 28.25),
        (-3, 28.25), (-3, 28.75), (-2.25, 29.25), (-2, 30.25), (-1, 31), (-1, 31.75),
        (-0.75, 31.75), (-0.75, 32), (-0.25, 32.25), (-0.25, 32.75), (0, 32.75), (0, 33),
        (0.25, 33), (0.25, 33.25), (0.5, 33.25), (0.5, 33.5), (1.5, 34.25), (1.5, 35),
        (1.75, 35), (1.75, 35.25), (2, 35.25), (2, 35.5), (3, 36.25), (3, 36.75),
        (3.75, 36.75),
    ],
    "Libya": [
        (9.75, 36.25), (11, 36.25), (11, 33), (11.5, 33), (11.5, 32.75), (12.5, 32.75),
        (12.5, 32.5), (13.5, 32.5), (13.5, 32.25), (14.5, 32.25), (14.5, 32), (24.5, 32),
        (22.25, 19.75), (21.75, 19.75), (21, 18.75), (20.5, 18.75), (20.5, 18.5),
        (20.25, 18.5), (19.5, 17.5), (14, 17.25), (13.75, 17.75), (12.5, 17.75), (12.5, 18),
        (12, 18), (12, 18.25), (11.5, 18.25), (11.5, 18.5), (10.75, 18.5), (10.75, 18.75),
        (10.25, 18.75), (10.25, 19), (9.5, 19), (9.5, 36), (9.75, 36),
    ],
    "Egypt": [
        (24.5, 32), (26.25, 32), (26.25, 31.75), (29, 31.75), (29, 31.5), (30.75, 31.5),
        (30.75, 31.25), (31.5, 31.25), (31.5, 31), (32, 31), (32, 31.25), (32.5, 31.5),
        (32.5, 31.25), (33.25, 31.25), (33.5, 30.75), (34, 30.75), (34, 30.5), (35, 30.25),
        (35, 30), (35.25, 30), (35.75, 29.25), (36.25, 29.25), (36.25, 29), (36.5, 29),
        (37.25, 28), (37.75, 28), (37.75, 27.5), (37.5, 27.5), (37.5, 26), (37.25, 26),
        (37.25, 23.5), (37, 23.5), (37, 23), (36.75, 23), (36.75, 23.75), (36.5, 23.75),
        (36.5, 24.25), (36.25, 24.25), (36.25, 25), (36, 25), (36, 25.5), (35.75, 25.5),
        (35.75, 26), (35.5, 26), (35.25, 27.75), (35, 27.75), (35, 28), (34.75, 28),
        (34.75, 28.25), (34.5, 28.25), (34.5, 28.5), (34.25, 28.5), (34.25, 28.75),
        (34, 28.75), (34, 29), (33.75, 29), (33.75, 29.25), (32.75, 30), (32.75, 29.75),
        (33, 29.75), (33, 29.5), (33.25, 29.5), (33.25, 29.25), (34.25, 28.5), (34.5, 27.5),
        (35, 27.25), (34.75, 26), (34.5, 26), (34.5, 25.25), (34.25, 25.25), (34.25, 24.5),
        (34, 24.5), (34, 24), (33.75, 24), (33.75, 23.5), (33.5, 23.5), (33.5, 23),
        (33.25, 23), (33.25, 22.25), (33, 22.25), (33.5, 20), (22.25, 20), (22.25, 20.5),
        (22.5, 20.5), (22.5, 21.75), (22.75, 21.75), (22.75, 23.25), (23, 23.25),
        (23.25, 26), (23.5, 26), (23.5, 27.25), (23.75, 27.25), (23.75, 28.5), (24, 28.5),
        (24, 30), (24.25, 30), (24.25, 31.25), (24.5, 31.25),
    ],
    "French West Africa": [
        (-6.75, 23.75), (-5.25, 23.75), (-5.25, 23.5), (-4.5, 23.5), (-4.5, 23.25),
        (-3.75, 23.25), (-3.75, 23), (-2.75, 23), (-2.75, 22.75), (-1.25, 22.5),
        (-1.25, 22.25), (-0.75, 22.25), (-0.5, 21.75), (0.25, 21.75), (0.25, 21.5),
        (1.5, 21.5), (1.5, 21.25), (2, 21.25), (2.25, 20.75), (4, 20.5), (4.25, 20), (5, 20),
        (5, 19.75), (5.75, 19.75), (5.75, 19.5), (6.25, 19.5), (6.25, 19.25), (7.25, 19.25),
        (7.25, 19), (8, 19), (8, 18.75), (7.75, 18.75), (7.75, 18), (7.5, 18), (7.5, 17.75),
        (7.25, 17.75), (7.25, 17.5), (7, 17.5), (7, 17.25), (6.75, 17.25), (6.75, 17),
        (6.5, 17), (6.5, 16.75), (6.25, 16.75), (6.25, 16.5), (5.25, 15.75), (5.25, 15.25),
        (5, 15.25), (5, 15), (4.25, 14.5), (4.25, 14), (3.25, 13.25), (3.25, 12.75),
        (2.75, 12.5), (2.5, 11.5), (2.25, 11.5), (2.25, 11.25), (2, 11.25), (2, 11),
        (1, 10.25), (1, 9.75), (0.75, 9.75), (0.75, 9.5), (0.25, 9.25), (0.25, 8.75),
        (-0.5, 8.25), (-0.5, 7.5), (-0.75, 7.5), (-0.75, 7.25), (-1, 7.25), (-1, 7),
        (-2, 6.25), (-2, 5.75), (-2.25, 5.75), (-2.25, 5.25), (-2.5, 5.25), (-2.5, 5),
        (-5, 5), (-5, 4.75), (-6.5, 4.75), (-6.5, 4.5), (-8.25, 4.5), (-8.25, 4.75),
        (-9.25, 5), (-9.25, 5.25), (-9.5, 5.25), (-9.5, 5.5), (-9.75, 5.5), (-9.75, 5.75),
        (-10, 5.75), (-10, 6), (-10.25, 6), (-10.25, 6.25), (-10.5, 6.25), (-10.5, 6.5),
        (-10.75, 6.5), (-10.75, 6.75), (-11, 6.75), (-11, 7), (-12, 7.75), (-12, 8.5),
        (-13, 9.25), (-13, 9.75), (-13.25, 9.75), (-13.25, 10), (-14, 10.5), (-14, 11),
        (-15, 11.75), (-15, 12.25), (-15.25, 12.25), (-15.25, 13.25), (-15.5, 13.25),
        (-15.5, 14.25), (-15.75, 14.25), (-15.75, 15), (-16, 15), (-16, 16), (-16.25, 16),
        (-16.25, 17.25), (-16.5, 17.25), (-16.5, 18.5), (-16.75, 18.5), (-16.75, 19.75),
        (-17, 19.75), (-17, 21.25), (-16.5, 21.5), (-16.5, 22), (-16.25, 22),
        (-16.25, 22.25), (-12.5, 22.5), (-12.5, 22.75), (-11.25, 22.75), (-11.25, 23),
        (-10, 23), (-10, 23.25), (-8.5, 23.25), (-8.5, 23.5), (-6.75, 23.5),
    ],
    "French Equatorial Africa": [
        (16.75, 17.5), (19.5, 17.5), (19.5, 17.25), (20.25, 16.75), (20.25, 16.25),
        (21, 15.75), (21, 15), (21.5, 14.75), (21.5, 14.25), (22, 14), (22, 13.5),
        (22.75, 13), (22.75, 12.5), (23, 12.5), (23, 11.75), (23.25, 11.75), (23.5, 10.75),
        (24.5, 10), (24.75, 8.75), (25.75, 8), (25.75, 7.5), (26, 7.5), (26, 7), (26.25, 7),
        (26.25, 6.5), (26.5, 6.5), (26.5, 6), (26.75, 6), (26.75, 5.5), (27, 5.5),
        (27, 5.25), (12, -2.25), (12, -1), (12.25, -1), (12.25, 1.5), (12.5, 1.5), (12.5, 4),
        (12.75, 4), (12.75, 6.5), (13, 6.5), (13, 9.25), (13.25, 9.25), (13.25, 11.75),
        (13.5, 11.75), (13.5, 14.25), (13.75, 14.25), (13.75, 16.25), (14, 16.25),
        (14, 17.25), (16.75, 17.25),
    ],
    "Sudan": [
        (22.25, 20), (33.5, 20), (33.5, 19.5), (33.75, 19.5), (33.75, 18.5), (34, 18.5),
        (34, 17.75), (34.25, 17.75), (34.25, 17.5), (34.5, 17.5), (34.5, 17.25),
        (34.75, 17.25), (34.75, 17), (35, 17), (35, 16.75), (35.25, 16.75), (35.25, 16.5),
        (35.5, 16.5), (35.5, 16.25), (35.75, 16.25), (35.75, 16), (36, 16), (36, 15.75),
        (36.25, 15.75), (36.25, 15.5), (37.25, 14.75), (37.25, 14), (36.25, 13.25),
        (36, 12.25), (35.5, 12), (35.25, 11), (34.75, 10.75), (34.5, 9.75), (34, 9.5),
        (33.75, 8.5), (33.25, 8.25), (33, 7.25), (32.5, 7), (32.25, 6), (32, 6),
        (31.5, 5.25), (30.25, 5), (30.25, 4.75), (29.5, 4.75), (29.5, 4.5), (28.5, 4.5),
        (28.5, 4.75), (27, 5), (27, 5.5), (26.75, 5.5), (26.75, 6), (26.5, 6), (26.5, 6.5),
        (26.25, 6.5), (26.25, 7), (26, 7), (25.75, 8), (24.75, 8.75), (24.5, 10),
        (23.5, 10.75), (23.5, 11.25), (23.25, 11.25), (23.25, 11.75), (23, 11.75),
        (22.75, 13), (22, 13.5), (22, 14), (21.75, 14), (21.75, 14.25), (21.5, 14.25),
        (21.5, 14.75), (21, 15), (21, 15.75), (20.75, 15.75), (20.75, 16), (20.25, 16.25),
        (20.25, 16.75), (19.5, 17.25), (19.5, 17.75), (19.75, 17.75), (20.5, 18.75),
        (21, 18.75), (21.75, 19.75), (22.25, 19.75),
    ],
    "Ethiopia": [
        (37.25, 14.25), (37.75, 14), (37.75, 13.5), (38, 13.5), (38, 13), (38.25, 13),
        (38.25, 12.25), (38.5, 12.25), (38.5, 11.75), (38.75, 11.75), (38.75, 11.25),
        (39, 11.25), (39, 11), (40.25, 11), (40.25, 11.25), (41, 11.25), (41, 11.5),
        (41.75, 11.5), (41.75, 11.75), (42.5, 11.75), (42.5, 12), (44, 11.75),
        (44.25, 11.25), (44.75, 11.25), (44.75, 11), (45, 11), (45, 7.75), (44.75, 7.75),
        (44.75, 7.25), (44, 6.75), (44, 6.25), (43.5, 6), (43.5, 5.5), (43, 5.25),
        (43, 4.75), (42.5, 4.5), (42.5, 4), (42, 3.75), (42, 3.25), (41.5, 3), (41.5, 2.5),
        (41, 2.25), (41, 1.75), (40.75, 1.75), (40.75, 2), (40, 2), (40, 2.25), (39.5, 2.25),
        (39.5, 2.5), (38.75, 2.5), (38.75, 2.75), (38.25, 2.75), (38.25, 3), (37.5, 3),
        (37.5, 3.25), (37, 3.25), (37, 3.5), (36.25, 3.5), (36.25, 3.75), (34.75, 4),
        (34.75, 4.25), (34.25, 4.25), (34, 4.75), (33, 4.75), (32.75, 5.25), (32, 5.25),
        (32, 5.5), (31.75, 5.5), (31.75, 5.75), (32.25, 6), (32.5, 7), (33, 7.25),
        (33.25, 8.25), (33.75, 8.5), (34, 9.5), (34.5, 9.75), (34.75, 10.75), (35.25, 11),
        (35.5, 12), (36, 12.25), (36.25, 13.25), (36.5, 13.25),
    ],
    "Nigeria": [
        (9.25, 19.25), (9.5, 19.25), (9.5, 19), (10.25, 19), (10.25, 18.75), (10.75, 18.75),
        (10.75, 18.5), (11.5, 18.5), (11.5, 18.25), (12, 18.25), (12, 18), (12.5, 18),
        (12.5, 17.75), (13.75, 17.75), (13.75, 17.5), (14, 17.5), (14, 16.25),
        (13.75, 16.25), (13.75, 14.25), (13.5, 14.25), (13.5, 11.75), (13.25, 11.75),
        (13.25, 9.25), (13, 9.25), (13, 6.5), (12.75, 6.5), (12.75, 4), (12.5, 4),
        (12.5, 1.5), (12.25, 1.5), (12.25, -1), (12, -1), (12, -2), (11.5, -2),
        (11.5, -1.75), (10.75, -1.75), (10.75, -1.5), (10, -1.5), (10, -1.25), (9.25, -1.25),
        (9.25, -1), (9, -1), (9, 2.25), (8.75, 2.25), (8.75, 2.75), (8.5, 2.75), (8.5, 3.25),
        (8.25, 3.25), (8.25, 3.75), (8, 3.75), (8, 4), (4.75, 4), (4.75, 4.25), (4.5, 4.25),
        (4.5, 4.5), (4.25, 4.5), (4.25, 4.75), (4, 4.75), (4, 5), (3.75, 5), (3, 6),
        (2.75, 6), (2, 5), (-2.5, 5), (-2.5, 5.25), (-2.25, 5.25), (-2.25, 5.75), (-2, 5.75),
        (-2, 6.25), (-1.75, 6.25), (-1.75, 6.5), (-1.5, 6.5), (-1.5, 6.75), (-0.5, 7.5),
        (-0.5, 8.25), (0.25, 8.75), (0.25, 9.25), (1, 9.75), (1, 10.25), (1.25, 10.25),
        (1.25, 10.5), (1.5, 10.5), (1.5, 10.75), (2.5, 11.5), (2.75, 12.5), (3, 12.5),
        (3, 12.75), (3.25, 12.75), (3.25, 13.25), (4.25, 14), (4.25, 14.5), (5.25, 15.25),
        (5.25, 15.75), (5.5, 15.75), (5.5, 16), (5.75, 16), (5.75, 16.25), (6, 16.25),
        (6, 16.5), (6.25, 16.5), (6.25, 16.75), (6.5, 16.75), (6.5, 17), (6.75, 17),
        (6.75, 17.25), (7.75, 18), (7.75, 18.75), (8.5, 18.75), (8.5, 19), (9.25, 19),
    ],
    "Belgian Congo": [
        (26.75, 5.25), (27, 5.25), (27, 5), (27.75, 5), (27.75, 4.75), (29, 4.5), (29, 3),
        (29.25, 3), (29.25, 0), (29.5, 0), (29.5, -2.75), (29.75, -2.75), (29.75, -5.75),
        (30, -5.75), (30, -9.25), (29.75, -9.25), (29.75, -9.5), (29.5, -9.5), (29.5, -9.75),
        (29.25, -9.75), (29.25, -10), (29, -10), (29, -10.25), (28.75, -10.25), (28, -11.25),
        (27.5, -11.25), (27.25, -11.75), (26.5, -11.75), (26.5, -11.5), (26, -11.5),
        (26, -11.25), (25.5, -11.25), (25.5, -11), (24.5, -10.75), (24.5, -10.5),
        (24.25, -10.5), (24, -10), (23.5, -10), (23, -9.25), (22, -9), (21.75, -8.5),
        (21.25, -8.5), (21, -8), (20.5, -8), (20.25, -7.5), (19.75, -7.5), (19.5, -7),
        (19, -7), (18.75, -6.5), (18.25, -6.5), (18, -6), (17.5, -6), (17.25, -5.5),
        (16.75, -5.5), (16.5, -5), (16, -5), (15.75, -4.5), (15.25, -4.5), (15, -4),
        (14.5, -4), (14.25, -3.5), (13.75, -3.5), (13.75, -3.25), (13.25, -3.25),
        (13, -2.75), (12.5, -2.75), (12.5, -2.5), (12.25, -2.5), (12.25, -2), (12.75, -2),
        (12.75, -1.75), (13.25, -1.75), (13.25, -1.5), (13.75, -1.5), (13.75, -1.25),
        (14.25, -1.25), (14.25, -1), (14.75, -1), (14.75, -0.75), (15.25, -0.75),
        (15.25, -0.5), (15.75, -0.5), (15.75, -0.25), (16.25, -0.25), (16.25, 0), (16.75, 0),
        (16.75, 0.25), (17.25, 0.25), (17.25, 0.5), (17.75, 0.5), (17.75, 0.75),
        (18.25, 0.75), (18.25, 1), (18.75, 1), (18.75, 1.25), (19.25, 1.25), (19.25, 1.5),
        (19.75, 1.5), (19.75, 1.75), (20.25, 1.75), (20.25, 2), (20.75, 2), (20.75, 2.25),
        (21.25, 2.25), (21.25, 2.5), (21.75, 2.5), (21.75, 2.75), (22.25, 2.75), (22.25, 3),
        (22.75, 3), (22.75, 3.25), (23.25, 3.25), (23.25, 3.5), (23.75, 3.5), (23.75, 3.75),
        (24.25, 3.75), (24.25, 4), (24.75, 4), (24.75, 4.25), (25.25, 4.25), (25.25, 4.5),
        (25.75, 4.5), (25.75, 4.75), (26.25, 4.75), (26.25, 5), (26.75, 5),
    ],
    "British East Africa": [
        (31.5, 5.5), (32.75, 5.25), (33, 4.75), (34, 4.75), (34, 4.5), (34.25, 4.5),
        (34.25, 4.25), (34.75, 4.25), (34.75, 4), (35.5, 4), (35.5, 3.75), (37, 3.5),
        (37, 3.25), (37.5, 3.25), (37.5, 3), (38.25, 3), (38.25, 2.75), (38.75, 2.75),
        (38.75, 2.5), (39.5, 2.5), (39.5, 2.25), (40, 2.25), (40, 2), (41.25, 1.75),
        (41.25, 1.5), (41.5, 1.5), (41.5, 1), (42, 0.75), (42, 0.25), (42.5, 0),
        (42.5, -0.5), (43, -0.75), (43, -2), (42.75, -2), (42.75, -2.75), (42.5, -2.75),
        (42.5, -3.5), (42.25, -3.5), (42.25, -4.5), (42, -4.5), (42, -5.25), (41.75, -5.25),
        (41.75, -6), (41.5, -6), (41.25, -7.75), (41, -7.75), (41, -8.5), (40.75, -8.5),
        (40.5, -9.75), (30, -9.25), (30, -5.75), (29.75, -5.75), (29.75, -2.75),
        (29.5, -2.75), (29.5, 0), (29.25, 0), (29.25, 3), (29, 3), (29, 4.5), (30.25, 4.75),
        (30.25, 5), (31, 5), (31, 5.25), (31.5, 5.25),
    ],
    "Angola": [
        (12, -2.25), (12.25, -2.25), (12.5, -2.75), (13, -2.75), (13.25, -3.25),
        (14.25, -3.5), (14.5, -4), (15, -4), (15.25, -4.5), (15.75, -4.5), (16, -5),
        (16.5, -5), (16.75, -5.5), (17.25, -5.5), (17.5, -6), (18, -6), (18.25, -6.5),
        (18.75, -6.5), (19, -7), (19.5, -7), (19.75, -7.5), (20.25, -7.5), (20.5, -8),
        (21, -8), (21.25, -8.5), (21.75, -8.5), (22, -9), (23, -9.25), (23, -9.5),
        (23.25, -9.5), (23.5, -10), (24, -10), (24.5, -10.75), (25, -10.75), (25, -11),
        (25.5, -11), (25.5, -11.25), (26, -11.25), (26, -11.5), (26.5, -11.5),
        (26.5, -11.75), (26.75, -11.75), (26.75, -12.25), (26.5, -12.25), (26.5, -13.5),
        (26.25, -13.5), (26.25, -14.5), (26, -14.5), (26, -15.25), (25.75, -15.25),
        (25.5, -16.5), (25.25, -16.5), (25.25, -17), (25, -17), (25, -18.25),
        (24.75, -18.25), (24.75, -18.5), (23.5, -18.75), (23.5, -19), (23, -19),
        (22.75, -19.5), (21.75, -19.5), (21.75, -19.75), (20.75, -20), (20.5, -20.5),
        (19.5, -20.5), (19.5, -20.75), (19, -20.75), (18.75, -21.25), (17.25, -21.5),
        (17, -22), (15.75, -22.25), (15.75, -22.5), (15, -22.5), (15, -22.75),
        (14.25, -22.75), (14.25, -22.5), (14, -22.5), (14, -21.75), (13.75, -21.75),
        (13.75, -20.5), (13.5, -20.5), (13.5, -19.5), (13.25, -19.5), (13.25, -18.25),
        (13, -18.25), (13, -12.5), (12.75, -12.5), (12.5, -10.5), (12.25, -10.5),
        (12.25, -9.75), (12, -9.75), (12, -8.25), (12.25, -8.25), (12.25, -7.5),
        (12.5, -7.5), (12.5, -7), (12.75, -7), (12.75, -6.25), (13, -6.25), (13, -6),
        (12, -5.25),
    ],
    "Mozambique": [
        (29.75, -9.25), (40.25, -9.75), (40.25, -11.5), (40, -11.5), (40, -17), (39.75, -17),
        (39.75, -17.25), (39.25, -17.25), (39, -17.75), (38.5, -17.75), (38, -18.5),
        (37.25, -18.5), (37.25, -18.75), (36.75, -18.75), (36.5, -19.25), (35.5, -19.5),
        (35.5, -19.75), (34.75, -20.25), (34.75, -20.75), (34, -21.25), (34, -21.75),
        (33.5, -22), (33.5, -22.5), (33, -22.75), (33, -23.25), (32.75, -23.25),
        (32.5, -24.25), (32.25, -24.25), (32.25, -24), (31.75, -24), (31.5, -23.5),
        (31, -23.5), (30.25, -22.5), (29.5, -22.5), (29.5, -22.25), (29.25, -22.25),
        (29.25, -22), (29, -22), (29, -21.75), (28.75, -21.75), (28.75, -21.5),
        (28.5, -21.5), (27.75, -20.5), (27.25, -20.5), (27.25, -20.25), (27, -20.25),
        (26.25, -19.25), (25.75, -19.25), (25.75, -19), (25, -18.5), (25, -17), (25.25, -17),
        (25.5, -15.75), (25.75, -15.75), (25.75, -15.25), (26, -15.25), (26, -14.5),
        (26.25, -14.5), (26.25, -13.5), (26.5, -13.5), (26.5, -12.25), (26.75, -12.25),
        (26.75, -11.75), (27.25, -11.75), (27.5, -11.25), (28, -11.25), (28, -11),
        (28.25, -11), (28.25, -10.75), (28.5, -10.75), (28.5, -10.5), (28.75, -10.5),
        (28.75, -10.25), (29, -10.25),
    ],
    "South Africa": [
        (24.75, -18.25), (25, -18.25), (25.75, -19.25), (26.25, -19.25), (26.25, -19.5),
        (26.5, -19.5), (27.25, -20.5), (27.75, -20.5), (27.75, -20.75), (28, -20.75),
        (28, -21), (28.25, -21), (28.25, -21.25), (28.5, -21.25), (28.5, -21.5),
        (28.75, -21.5), (29.5, -22.5), (30.25, -22.5), (31, -23.5), (31.5, -23.5),
        (31.75, -24), (32.25, -24), (32.25, -24.75), (32, -24.75), (32, -25), (31, -25.75),
        (31, -26.5), (30.75, -26.5), (30.75, -27.5), (30.5, -27.5), (30.5, -28.5),
        (30.25, -28.5), (30.25, -29.5), (30, -29.5), (30, -30), (29.75, -30),
        (29.75, -30.25), (29.5, -30.25), (29.5, -30.5), (29.25, -30.5), (29.25, -30.75),
        (29, -30.75), (29, -31), (28.75, -31), (28.75, -31.25), (28.5, -31.25),
        (28.5, -31.5), (28.25, -31.5), (27.5, -32.5), (26.75, -32.5), (26.75, -32.75),
        (26.25, -32.75), (26.25, -33), (25.75, -33), (25.75, -33.25), (25.25, -33.25),
        (25.25, -33.5), (24.5, -33.5), (24.5, -33.75), (22.75, -33.75), (22.75, -34),
        (20, -34), (20, -33.75), (19.75, -33.75), (19.75, -33.25), (19.25, -33),
        (19.25, -32.5), (19, -32.5), (19, -32), (18.75, -32), (18.75, -31.5), (18.5, -31.5),
        (18.5, -31), (18.25, -31), (18, -30), (17.75, -30), (17.75, -29.25), (17.5, -29.25),
        (17.5, -28.25), (17.25, -28.25), (17, -26.75), (16.25, -26.25), (16.25, -25.75),
        (16, -25.75), (15.75, -24.75), (15.25, -24.5), (15.25, -24), (15, -24), (15, -23.5),
        (14.75, -23.5), (14.75, -23), (14.5, -23), (14.5, -22.75), (15.75, -22.5),
        (15.75, -22.25), (16.5, -22.25), (16.5, -22), (17, -22), (17.25, -21.5),
        (18.75, -21.25), (18.75, -21), (19, -21), (19, -20.75), (19.5, -20.75),
        (19.5, -20.5), (20.5, -20.5), (20.75, -20), (21.25, -20), (21.25, -19.75),
        (21.75, -19.75), (21.75, -19.5), (22.75, -19.5), (23, -19), (24.25, -18.75),
        (24.25, -18.5), (24.75, -18.5),
    ],
    "Brazil": [
        (-54.25, 2.75), (-53.75, 2.75), (-53.5, 2.25), (-53, 2.25), (-53, 2), (-52.5, 2),
        (-52.5, 1.75), (-51.5, 1.5), (-51.5, 1.25), (-51.25, 1.25), (-51.25, 1), (-51, 1),
        (-50.25, 0), (-47.75, 0), (-47.75, -0.25), (-47, -0.25), (-47, -0.5),
        (-45.75, -0.75), (-45.75, -1), (-45.25, -1), (-45.25, -1.25), (-44.5, -1.25),
        (-44.5, -1.5), (-44, -1.5), (-44, -1.75), (-43.25, -1.75), (-43.25, -2),
        (-42.75, -2), (-42.75, -2.25), (-42, -2.25), (-42, -2.5), (-41.5, -2.5),
        (-41.5, -2.75), (-40.75, -2.75), (-40.75, -3), (-40, -3), (-40, -3.25),
        (-38.5, -3.5), (-38.5, -3.75), (-38, -3.75), (-37.75, -4.25), (-37.25, -4.25),
        (-37, -4.75), (-36.5, -4.75), (-36.25, -5.25), (-35.75, -5.25), (-35.75, -5.5),
        (-35, -6), (-35, -9.25), (-35.25, -9.25), (-35.25, -9.75), (-36, -10.25),
        (-36, -10.75), (-37, -11.5), (-37, -12), (-37.25, -12), (-38, -13), (-39, -13),
        (-39, -13.25), (-39.25, -13.25), (-39.25, -14), (-39.5, -14), (-39.75, -15.25),
        (-40, -15.25), (-40, -15.75), (-40.25, -15.75), (-40.25, -16.5), (-40.5, -16.5),
        (-40.75, -18), (-41.25, -18.25), (-41.5, -19.25), (-42, -19.5), (-42, -20),
        (-42.5, -20.25), (-42.5, -20.75), (-42.75, -20.75), (-42.75, -21.25), (-43, -21.25),
        (-43.25, -21.75), (-43.5, -21.75), (-43.5, -21.5), (-44, -21.5), (-44, -21.25),
        (-44.75, -21.25), (-44.75, -21), (-45.25, -21), (-45.25, -20.75), (-45.75, -20.75),
        (-45.75, -20.5), (-46.5, -20.5), (-46.5, -20.25), (-47, -20.25), (-47, -20),
        (-47.5, -20), (-47.5, -19.75), (-48, -19.75), (-48, -19.5), (-48.75, -19.5),
        (-48.75, -19.25), (-49.25, -19.25), (-49.25, -19), (-49.75, -19), (-49.75, -18.75),
        (-50.5, -18.75), (-50.5, -18.5), (-51, -18.5), (-51, -18.25), (-51.5, -18.25),
        (-51.5, -18), (-52.25, -18), (-52.25, -17.75), (-52.75, -17.75), (-52.75, -17.5),
        (-53.25, -17.5), (-53.25, -17.25), (-53.75, -17.25), (-53.75, -17), (-54.5, -17),
        (-54.5, -16.75), (-55, -16.75), (-55, -16.5), (-55.5, -16.5), (-55.5, -16.25),
        (-56.75, -16), (-56.75, -15.75), (-57.25, -15.5), (-57.25, -15), (-58, -14.5),
        (-58, -14), (-58.25, -14), (-58.25, -13.5), (-58.5, -13.5), (-58.5, -13),
        (-58.75, -13), (-58.75, -12.5), (-59, -12.5), (-59.25, -11.5), (-60, -11),
        (-60, -10.5), (-60.25, -10.5), (-60.25, -10), (-60.5, -10), (-60.5, -9.5),
        (-60.75, -9.5), (-60.75, -9), (-61, -9), (-61, -8.5), (-61.25, -8.5), (-61.5, -7.5),
        (-62, -7.25), (-62, -6.75), (-62.25, -6.75), (-62.5, -5.75), (-62.75, -5.75),
        (-62.75, -5.5), (-63, -5.5), (-63, -5), (-63.25, -5), (-63.25, -4.5), (-62.75, -4.5),
        (-62.75, -4.25), (-62.5, -4.25), (-62.5, -4), (-62.25, -4), (-62.25, -3.75),
        (-62, -3.75), (-62, -3.5), (-61.75, -3.5), (-61.75, -3.25), (-61.5, -3.25),
        (-60.75, -2.25), (-60, -2.25), (-59.25, -1.25), (-58.75, -1.25), (-58, -0.25),
        (-57.5, -0.25), (-56.75, 0.75), (-56.25, 0.75), (-56.25, 1), (-56, 1), (-55.5, 1.75),
        (-55, 1.75),
    ],
    "Argentina": [
        (-65.25, -28.25), (-65, -28.25), (-65, -28.5), (-64.25, -28.5), (-64.25, -28.75),
        (-63.5, -28.75), (-63.5, -29), (-62.75, -29), (-62.75, -29.25), (-62, -29.25),
        (-62, -29.5), (-61.25, -29.5), (-61.25, -29.75), (-60.5, -29.75), (-60.5, -30),
        (-60, -30), (-59.75, -30.5), (-59, -30.5), (-59, -30.75), (-57.75, -30.75),
        (-57.75, -31), (-57.25, -31), (-57.25, -31.25), (-57, -31.25), (-57, -31.75),
        (-57.25, -31.75), (-57.25, -32), (-57.5, -32), (-57.5, -32.5), (-58, -32.75),
        (-58, -33.25), (-57.25, -33.75), (-57.25, -34.25), (-57.5, -34.25), (-58.25, -35.25),
        (-58.75, -35.25), (-58.75, -35.5), (-59.25, -35.5), (-59.5, -36), (-60, -36),
        (-60, -36.25), (-60.25, -36.25), (-60.25, -36.75), (-60.5, -36.75), (-60.5, -37.25),
        (-60.75, -37.25), (-60.75, -37.75), (-61, -37.75), (-61, -38.25), (-61.25, -38.25),
        (-61.25, -38.75), (-61.5, -38.75), (-61.75, -40), (-62.5, -40.5), (-62.75, -41.5),
        (-63, -41.5), (-63, -41.75), (-63.25, -41.75), (-63.25, -42.25), (-63.5, -42.25),
        (-63.5, -43), (-63.75, -43), (-63.75, -43.25), (-64.25, -43.5), (-64.25, -44),
        (-64.75, -44.25), (-65, -45.5), (-65.25, -45.5), (-65.25, -46.25), (-65.5, -46.25),
        (-65.5, -47), (-65.75, -47), (-65.75, -47.75), (-66, -47.75), (-66, -48.5),
        (-66.25, -48.5), (-66.25, -49), (-66.5, -49), (-66.5, -49.5), (-66.75, -49.5),
        (-66.75, -50), (-67, -50), (-67, -50.5), (-67.25, -50.5), (-67.5, -51.5),
        (-68, -51.75), (-68, -52.25), (-67.75, -52.25), (-67.75, -52.5), (-67.5, -52.5),
        (-67.5, -52.75), (-67.25, -52.75), (-67.25, -53), (-67, -53), (-67, -53.25),
        (-66.75, -53.25), (-66.75, -53.5), (-66.5, -53.5), (-66.5, -53.75), (-65.5, -54.5),
        (-65.5, -54.75), (-66.25, -54.75), (-66.25, -54.5), (-67, -54.5), (-67, -54.25),
        (-68.25, -54), (-68.25, -53.75), (-68.5, -53.75), (-68.5, -53.5), (-68.75, -53.5),
        (-68.75, -53.25), (-69, -53.25), (-69, -53), (-69.25, -53), (-69.25, -52.75),
        (-69.5, -52.75), (-69.5, -52.5), (-69.75, -52.5), (-69.75, -52.25), (-70, -52.25),
        (-70, -52), (-70.25, -52), (-70.25, -51.75), (-70.5, -51.75), (-70.5, -51.5),
        (-70.75, -51.5), (-70.75, -51.25), (-71, -51.25), (-71, -51), (-72, -50.25),
        (-72.25, -41.75), (-71.25, -41), (-71.25, -40.5), (-71, -40.5), (-70.75, -39.5),
        (-70.25, -39.25), (-70.25, -38.75), (-70, -38.75), (-69.75, -37.75), (-68.75, -37),
        (-68.75, -36.5), (-68.5, -36.5), (-68.5, -36), (-68.25, -36), (-68.25, -35.5),
        (-68, -35.5), (-68, -35), (-67.75, -35), (-67.75, -34.5), (-67.5, -34.5),
        (-67.5, -33.75), (-67.25, -33.75), (-67.25, -33.25), (-67, -33.25), (-67, -32.75),
        (-66.75, -32.75), (-66.75, -32.25), (-66.5, -32.25), (-66.5, -31.75),
        (-66.25, -31.75), (-66.25, -31), (-66, -31), (-66, -30.25), (-65.75, -30.25),
        (-65.75, -29.5), (-65.5, -29.5),
    ],
    "Chile": [
        (-70, -24.75), (-69.75, -24.75), (-69.75, -25), (-69, -25), (-69, -25.25),
        (-67.75, -25.5), (-67.75, -25.75), (-67.5, -25.75), (-67.5, -26), (-67.25, -26),
        (-67.25, -26.25), (-67, -26.25), (-67, -26.5), (-66.75, -26.5), (-66.75, -26.75),
        (-66.5, -26.75), (-66.5, -27), (-66.25, -27), (-66.25, -27.25), (-65.25, -28),
        (-65.25, -28.75), (-65.5, -28.75), (-65.5, -29.5), (-65.75, -29.5), (-65.75, -30.25),
        (-66, -30.25), (-66.25, -31.75), (-66.5, -31.75), (-66.5, -32.25), (-66.75, -32.25),
        (-66.75, -32.75), (-67, -32.75), (-67, -33.25), (-67.25, -33.25), (-67.25, -33.75),
        (-67.5, -33.75), (-67.5, -34.5), (-67.75, -34.5), (-67.75, -35), (-68, -35),
        (-68, -35.5), (-68.25, -35.5), (-68.25, -36), (-68.5, -36), (-68.75, -37),
        (-69.75, -37.75), (-69.75, -38.25), (-70, -38.25), (-70.25, -39.25), (-70.75, -39.5),
        (-70.75, -40), (-71, -40), (-71.25, -41), (-71.5, -41), (-71.5, -41.25),
        (-72.5, -42), (-72.75, -40.75), (-73, -40.75), (-73, -36.75), (-72.75, -36.75),
        (-72.75, -36.25), (-72.5, -36.25), (-72.5, -35.75), (-72.25, -35.75),
        (-72.25, -35.25), (-72, -35.25), (-72, -34.75), (-71.75, -34.75), (-71.75, -34.25),
        (-71.5, -34.25), (-71.5, -33.75), (-71.25, -33.75), (-71.25, -33.25), (-71, -33.25),
        (-71, -29.25), (-70.75, -29.25), (-70.5, -28), (-70.25, -28), (-70.25, -27.25),
        (-70, -27.25),
    ],
    "Peru": [
        (-79.75, -1.75), (-78.75, -1.75), (-78.75, -2), (-77, -2), (-77, -2.25),
        (-75.25, -2.25), (-75.25, -2.5), (-73.25, -2.5), (-73.25, -2.75), (-71.5, -2.75),
        (-71.5, -3), (-67.75, -3.25), (-67.75, -3.5), (-66, -3.5), (-66, -3.75),
        (-64.75, -3.75), (-64.75, -4), (-64.25, -4), (-64, -4.5), (-63.5, -4.5),
        (-63.75, -5.5), (-64.75, -6.25), (-64.75, -6.75), (-65, -6.75), (-65, -7),
        (-65.5, -7.25), (-65.5, -7.75), (-66.25, -8.25), (-66.25, -8.75), (-66.75, -9),
        (-67, -10), (-67.25, -10), (-67.25, -10.25), (-67.5, -10.25), (-67.5, -10.5),
        (-68.5, -11.25), (-68.75, -12.25), (-69, -12.25), (-69, -12.5), (-69.25, -12.5),
        (-69.25, -12.75), (-69.5, -12.75), (-69.5, -13), (-69.75, -13), (-69.75, -13.25),
        (-70.75, -14), (-70.75, -14.5), (-71, -14.5), (-71, -14.75), (-72, -15.5),
        (-72, -16), (-72.5, -16.25), (-72.5, -16.75), (-72.75, -16.75), (-72.75, -16.5),
        (-73.25, -16.5), (-73.75, -15.75), (-74.25, -15.75), (-74.75, -15), (-75.25, -15),
        (-75.25, -14.75), (-75.75, -14.75), (-75.75, -14.5), (-76.25, -14.5),
        (-76.25, -14.25), (-77, -14.25), (-77, -14), (-77.25, -14), (-77.25, -13.75),
        (-77.5, -13.75), (-77.5, -13.5), (-77.75, -13.5), (-77.75, -13.25), (-78, -13.25),
        (-78, -13), (-78.25, -13), (-78.25, -12.75), (-78.5, -12.75), (-78.5, -12.5),
        (-78.75, -12.5), (-78.75, -12.25), (-79, -12.25), (-79, -12), (-79.25, -12),
        (-79.25, -11.75), (-79.5, -11.75), (-79.5, -11.5), (-79.75, -11.5), (-79.75, -11.25),
        (-80, -11.25), (-80, -11), (-81, -10.25), (-81, -5.75), (-80.75, -5.75),
        (-80.75, -5.25), (-80.5, -5.25), (-80.5, -4.75), (-80.25, -4.75), (-80.25, -4.25),
        (-80, -4.25),
    ],
    "Bolivia": [
        (-63.5, -4.75), (-63.25, -4.75), (-63.25, -5), (-63, -5), (-63, -5.5),
        (-62.5, -5.75), (-62.5, -6.25), (-62.25, -6.25), (-62, -7.25), (-61.5, -7.5),
        (-61.5, -8), (-61.25, -8), (-61.25, -8.5), (-61, -8.5), (-61, -9), (-60.75, -9),
        (-60.75, -9.5), (-60.5, -9.5), (-60.5, -10), (-60.25, -10), (-60, -11),
        (-59.25, -11.5), (-59.25, -12), (-59, -12), (-59, -12.5), (-58.75, -12.5),
        (-58.75, -13), (-58.5, -13), (-58.5, -13.5), (-58.25, -13.5), (-58, -14.5),
        (-57.25, -15), (-57, -16), (-57.25, -16), (-57.25, -16.25), (-57.5, -16.25),
        (-57.5, -16.5), (-57.75, -16.5), (-57.75, -16.75), (-58, -16.75), (-58, -17),
        (-58.25, -17), (-58.25, -17.25), (-58.5, -17.25), (-58.5, -17.5), (-58.75, -17.5),
        (-58.75, -17.75), (-59, -17.75), (-59, -18), (-59.25, -18), (-59.25, -18.25),
        (-59.5, -18.25), (-59.5, -18.5), (-59.75, -18.5), (-59.75, -18.75), (-60, -18.75),
        (-60, -19), (-60.25, -19), (-61, -20), (-61.75, -20), (-61.75, -20.25),
        (-62, -20.25), (-62, -20.5), (-62.25, -20.5), (-63, -21.5), (-63.5, -21.5),
        (-63.5, -21.75), (-63.75, -21.75), (-64.5, -22.75), (-65, -22.75), (-65.75, -23.75),
        (-66.25, -23.75), (-66.25, -24), (-66.5, -24), (-67.25, -25), (-67.75, -25),
        (-67.75, -25.25), (-68.25, -25.5), (-68.25, -25.25), (-69, -25.25), (-69, -25),
        (-69.75, -25), (-69.75, -24.75), (-70, -24.75), (-70, -19.75), (-70.25, -19.75),
        (-70.25, -19.25), (-70.5, -19.25), (-70.75, -18.25), (-71, -18.25), (-71.75, -17.25),
        (-72.25, -17.25), (-72.25, -17), (-72.5, -17), (-72.5, -16.25), (-72.25, -16.25),
        (-72.25, -16), (-72, -16), (-72, -15.5), (-71.75, -15.5), (-71.75, -15.25),
        (-70.75, -14.5), (-70.75, -14), (-70.5, -14), (-70.5, -13.75), (-70.25, -13.75),
        (-70.25, -13.5), (-70, -13.5), (-70, -13.25), (-69.75, -13.25), (-69.75, -13),
        (-68.75, -12.25), (-68.5, -11.25), (-68.25, -11.25), (-68.25, -11), (-68, -11),
        (-68, -10.75), (-67, -10), (-66.75, -9), (-66.5, -9), (-66.5, -8.75),
        (-66.25, -8.75), (-66.25, -8.25), (-65.5, -7.75), (-65.5, -7.25), (-64.75, -6.75),
        (-64.75, -6.25), (-63.75, -5.5), (-63.75, -5), (-63.5, -5),
    ],
    "Colombia": [
        (-74.25, 11), (-72.5, 11), (-72.5, 10.75), (-72, 10.75), (-72, 10.5), (-71.75, 10.5),
        (-71.75, 10), (-71.5, 10), (-71.5, 9.5), (-71.25, 9.5), (-71.25, 9), (-71, 9),
        (-71, 8.5), (-70.75, 8.5), (-70.75, 8), (-70.5, 8), (-70.5, 7.5), (-70.25, 7.5),
        (-70.25, 7), (-70, 7), (-70, 6.5), (-69.75, 6.5), (-69.75, 6), (-69.5, 6),
        (-69.5, 5.5), (-69.25, 5.5), (-69.25, 5), (-69, 5), (-69, 4.5), (-68.75, 4.5),
        (-68.75, 4), (-68.5, 4), (-68.5, 3.25), (-68.25, 3.25), (-68.25, 2.75), (-68, 2.75),
        (-68, 2.25), (-67.75, 2.25), (-67.75, 1.75), (-67.5, 1.75), (-67.5, 1.25),
        (-67.25, 1.25), (-67.25, 0.75), (-67, 0.75), (-67, 0.25), (-66.75, 0.25),
        (-66.75, -0.25), (-66.5, -0.25), (-66.5, -0.75), (-66.25, -0.75), (-66.25, -1.25),
        (-66, -1.25), (-66, -1.75), (-65.75, -1.75), (-65.75, -2.25), (-65.5, -2.25),
        (-65.5, -2.75), (-65.25, -2.75), (-65, -3.75), (-66, -3.75), (-66, -3.5),
        (-67.75, -3.5), (-67.75, -3.25), (-69.5, -3.25), (-69.5, -3), (-71.5, -3),
        (-71.5, -2.75), (-73.25, -2.75), (-73.25, -2.5), (-75.25, -2.5), (-75.25, -2.25),
        (-77, -2.25), (-77, -2), (-78.75, -2), (-78.75, -1.75), (-79.5, -1.75),
        (-79.5, -0.25), (-79.25, -0.25), (-79, 2.75), (-78.75, 2.75), (-78.75, 3.5),
        (-78.5, 3.5), (-78.5, 4.25), (-78.25, 4.25), (-78.25, 5), (-78, 5), (-78, 5.75),
        (-77.75, 5.75), (-77.75, 6.5), (-77.5, 6.5), (-77.25, 8), (-77, 8), (-77, 8.25),
        (-76.75, 8.25), (-76.75, 8.5), (-76.5, 8.5), (-76.5, 8.75), (-76.25, 8.75),
        (-76.25, 9), (-76, 9), (-76, 9.25), (-75.75, 9.25), (-75.75, 9.5), (-75.5, 9.5),
        (-75.5, 9.75), (-75.25, 9.75), (-75.25, 10), (-75, 10),
    ],
    "Venezuela": [
        (-72.5, 11), (-70, 11), (-70, 10.75), (-69.25, 10.75), (-69.25, 10.5), (-68.5, 10.5),
        (-68.5, 10.25), (-67.5, 10.25), (-67.5, 10), (-66.5, 10), (-66.5, 9.75),
        (-65.25, 9.75), (-65.25, 9.5), (-64, 9.5), (-64, 9.25), (-62.75, 9.25), (-62.75, 9),
        (-61, 8.75), (-61, 8.5), (-60.5, 8.5), (-60.5, 8.25), (-60.25, 8.25), (-60.25, 8),
        (-60, 8), (-60, 7.75), (-59.75, 7.75), (-59.75, 7.5), (-59.5, 7.5), (-59.5, 7.25),
        (-59.25, 7.25), (-59.25, 7), (-59, 7), (-58.25, 6), (-57.75, 6), (-57, 5),
        (-56.25, 5), (-56.25, 4.75), (-56, 4.75), (-56, 4.5), (-55.75, 4.5), (-55.75, 4.25),
        (-55.5, 4.25), (-55.5, 4), (-55.25, 4), (-54.5, 3), (-54, 3), (-54, 2.75),
        (-54.25, 2.75), (-55, 1.75), (-55.5, 1.75), (-56.25, 0.75), (-56.75, 0.75),
        (-57.5, -0.25), (-58, -0.25), (-58.75, -1.25), (-59.25, -1.25), (-60, -2.25),
        (-60.75, -2.25), (-60.75, -2.5), (-61, -2.5), (-61, -2.75), (-61.25, -2.75),
        (-61.25, -3), (-61.5, -3), (-61.5, -3.25), (-61.75, -3.25), (-61.75, -3.5),
        (-62, -3.5), (-62.75, -4.5), (-63.25, -4.5), (-63.25, -4.75), (-63.5, -4.75),
        (-63.5, -4.5), (-64, -4.5), (-64.25, -4), (-64.75, -4), (-64.75, -3.75),
        (-65, -3.75), (-65, -3.25), (-65.25, -3.25), (-65.25, -2.75), (-65.5, -2.75),
        (-65.5, -2.25), (-65.75, -2.25), (-65.75, -1.75), (-66, -1.75), (-66, -1.25),
        (-66.25, -1.25), (-66.25, -0.75), (-66.5, -0.75), (-66.5, -0.25), (-66.75, -0.25),
        (-66.75, 0.25), (-67, 0.25), (-67, 0.75), (-67.25, 0.75), (-67.25, 1.25),
        (-67.5, 1.25), (-67.5, 1.75), (-67.75, 1.75), (-67.75, 2.25), (-68, 2.25),
        (-68, 2.75), (-68.25, 2.75), (-68.25, 3.25), (-68.5, 3.25), (-68.5, 4), (-68.75, 4),
        (-68.75, 4.5), (-69, 4.5), (-69, 5), (-69.25, 5), (-69.25, 5.5), (-69.5, 5.5),
        (-69.5, 6), (-69.75, 6), (-69.75, 6.5), (-70, 6.5), (-70, 7), (-70.25, 7),
        (-70.25, 7.5), (-70.5, 7.5), (-70.5, 8), (-70.75, 8), (-70.75, 8.5), (-71, 8.5),
        (-71, 9), (-71.25, 9), (-71.25, 9.5), (-71.5, 9.5), (-71.75, 10.5), (-72, 10.5),
        (-72, 10.75), (-72.5, 10.75),
    ],
    "Paraguay": [
        (-57, -15.75), (-56.75, -15.75), (-56.75, -16), (-56.25, -16), (-56.25, -16.25),
        (-55.5, -16.25), (-55.5, -16.5), (-55, -16.5), (-55, -16.75), (-54.5, -16.75),
        (-54.5, -17), (-53.75, -17), (-53.75, -17.25), (-53.25, -17.25), (-53.25, -17.5),
        (-52.75, -17.5), (-52.75, -17.75), (-52.25, -17.75), (-52.25, -18), (-51.5, -18),
        (-51.5, -18.25), (-51, -18.25), (-51, -18.5), (-50.5, -18.5), (-50.5, -18.75),
        (-49.75, -18.75), (-49.75, -19), (-49.25, -19), (-49.25, -19.25), (-48.75, -19.25),
        (-48.75, -19.5), (-48, -19.5), (-48, -19.75), (-47.5, -19.75), (-47.5, -20),
        (-47, -20), (-47, -20.25), (-46.5, -20.25), (-46.5, -20.5), (-45.75, -20.5),
        (-45.75, -20.75), (-45.25, -20.75), (-45.25, -21), (-44, -21.25), (-44, -21.5),
        (-43.5, -21.5), (-43.5, -21.75), (-43.25, -21.75), (-43.25, -22), (-43.75, -22.25),
        (-43.75, -22.75), (-44, -22.75), (-44.5, -23.5), (-45, -23.5), (-45, -23.75),
        (-45.5, -23.75), (-45.5, -24), (-46.25, -24), (-46.25, -24.25), (-46.75, -24.25),
        (-46.75, -24.5), (-47.25, -24.5), (-47.25, -24.75), (-47.75, -24.75), (-47.75, -25),
        (-54, -25), (-54, -25.25), (-54.25, -25.25), (-54.25, -26), (-54.5, -26),
        (-54.5, -26.5), (-54.75, -26.5), (-54.75, -27.25), (-55, -27.25), (-55, -27.75),
        (-55.25, -27.75), (-55.25, -28.5), (-55.5, -28.5), (-55.5, -29), (-55.75, -29),
        (-55.75, -30), (-56.25, -30.25), (-56.25, -30.75), (-56.5, -30.75), (-56.75, -31.25),
        (-57.25, -31.25), (-57.25, -31), (-57.75, -31), (-57.75, -30.75), (-59, -30.75),
        (-59, -30.5), (-59.75, -30.5), (-59.75, -30.25), (-60, -30.25), (-60, -30),
        (-60.5, -30), (-60.5, -29.75), (-61.25, -29.75), (-61.25, -29.5), (-62, -29.5),
        (-62, -29.25), (-62.75, -29.25), (-62.75, -29), (-63.5, -29), (-63.5, -28.75),
        (-65, -28.5), (-65, -28.25), (-65.25, -28.25), (-65.25, -28), (-65.5, -28),
        (-65.5, -27.75), (-65.75, -27.75), (-65.75, -27.5), (-66, -27.5), (-66, -27.25),
        (-66.25, -27.25), (-66.25, -27), (-66.5, -27), (-66.5, -26.75), (-66.75, -26.75),
        (-66.75, -26.5), (-67, -26.5), (-67, -26.25), (-68, -25.5), (-68, -25.25),
        (-67.75, -25.25), (-67.75, -25), (-67.25, -25), (-67.25, -24.75), (-67, -24.75),
        (-66.25, -23.75), (-65.75, -23.75), (-65, -22.75), (-64.5, -22.75), (-64.5, -22.5),
        (-64.25, -22.5), (-63.5, -21.5), (-63, -21.5), (-63, -21.25), (-62.75, -21.25),
        (-62.75, -21), (-62.5, -21), (-61.75, -20), (-61, -20), (-61, -19.75),
        (-60.75, -19.75), (-60.75, -19.5), (-60.5, -19.5), (-60.5, -19.25), (-60.25, -19.25),
        (-60.25, -19), (-60, -19), (-60, -18.75), (-59.75, -18.75), (-59.75, -18.5),
        (-59.5, -18.5), (-59.5, -18.25), (-59.25, -18.25), (-59.25, -18), (-59, -18),
        (-59, -17.75), (-58.75, -17.75), (-58.75, -17.5), (-58.5, -17.5), (-58.5, -17.25),
        (-58.25, -17.25), (-58.25, -17), (-58, -17), (-58, -16.75), (-57.75, -16.75),
    ],
    "Mexico": [
        (-113.75, 31.75), (-112.5, 31.75), (-112.5, 31.5), (-111.75, 31.5), (-111.75, 31.25),
        (-108, 31.25), (-108, 31.5), (-106.5, 31.5), (-106.5, 31.25), (-105.5, 30.5),
        (-105.5, 30), (-105.25, 30), (-104.75, 29.25), (-103.5, 29), (-103.5, 28.75),
        (-102.5, 28.75), (-102.5, 28.5), (-101.75, 28.5), (-101.75, 28.25), (-101, 28.25),
        (-101, 28), (-100.25, 28), (-100.25, 27.75), (-99.5, 27.75), (-99.5, 27.5),
        (-98.75, 27.5), (-98.75, 27.25), (-98.5, 27.25), (-97.75, 26.25), (-97.25, 26.25),
        (-97.25, 25.75), (-97, 25.75), (-97, 21.75), (-96.75, 21.75), (-96.75, 21.25),
        (-96.5, 21.25), (-96.5, 20.75), (-96.25, 20.75), (-96.25, 20.25), (-96, 20.25),
        (-96, 19.75), (-95.75, 19.75), (-95.75, 19.25), (-95.5, 19.25), (-95.25, 18.25),
        (-95, 18.25), (-94.75, 17.75), (-94.25, 17.75), (-94.25, 17.25), (-94.5, 17.25),
        (-94.5, 17), (-95.5, 16.25), (-95.5, 16.5), (-95.75, 16.5), (-95.75, 16.75),
        (-96, 16.75), (-96, 17), (-96.25, 17), (-97, 18), (-98, 18), (-98, 18.25),
        (-99, 18.25), (-99, 18.5), (-99.75, 18.5), (-99.75, 18.75), (-100.75, 18.75),
        (-100.75, 19), (-101.75, 19), (-101.75, 19.25), (-102.75, 19.25), (-102.75, 19.5),
        (-103.5, 19.5), (-103.5, 19.75), (-104.5, 19.75), (-104.5, 20), (-105, 20),
        (-105, 20.25), (-105.25, 20.25), (-105.25, 21), (-105.5, 21), (-105.5, 21.75),
        (-105.75, 21.75), (-106, 23), (-109.25, 23), (-109.25, 23.25), (-109.5, 23.25),
        (-109.5, 23.5), (-109.75, 23.5), (-109.75, 23.75), (-110, 23.75), (-110, 24),
        (-110.25, 24), (-110.25, 24.25), (-110.5, 24.25), (-110.5, 24.5), (-110.75, 24.5),
        (-110.75, 24.75), (-111, 24.75), (-111, 25), (-111.25, 25), (-111.25, 25.25),
        (-111.5, 25.25), (-111.5, 25.5), (-111.75, 25.5), (-111.75, 25.75), (-112, 25.75),
        (-112, 26), (-112.25, 26), (-112.25, 26.25), (-112.5, 26.25), (-112.5, 26.5),
        (-112.75, 26.5), (-112.75, 26.75), (-113, 26.75), (-113, 27), (-114, 27.75),
        (-114, 31), (-114.5, 31), (-114.5, 31.5), (-113.75, 31.5),
    ],
    "Alaska": [
        (-155.75, 71), (-149.5, 70.75), (-149.5, 70.5), (-145.75, 70.5), (-145.75, 70.25),
        (-142, 70.25), (-142, 70), (-135.25, 70), (-135.25, 69.25), (-135.5, 69.25),
        (-135.5, 68.75), (-135.25, 68.75), (-135.25, 68.5), (-135.5, 68.5), (-135.5, 68),
        (-135.75, 68), (-135.75, 67.5), (-136, 67.5), (-136, 66.75), (-136.25, 66.75),
        (-136.25, 66.25), (-136.5, 66.25), (-136.5, 65.75), (-136.75, 65.75), (-136.75, 65),
        (-137, 65), (-137, 64.5), (-137.25, 64.5), (-137.25, 63.75), (-137.5, 63.75),
        (-137.5, 63.25), (-137.75, 63.25), (-137.75, 62.75), (-138, 62.75), (-138, 62),
        (-138.25, 62), (-138.25, 61.5), (-138.5, 61.5), (-138.5, 61), (-138.75, 61),
        (-138.75, 60.25), (-139, 60.25), (-139, 59.75), (-138.75, 59.75), (-138.75, 58.75),
        (-139.5, 58.75), (-139.5, 59), (-142.5, 59), (-142.5, 59.25), (-145, 59.25),
        (-145, 59.5), (-147.5, 59.5), (-147.5, 59.75), (-150, 59.75), (-150, 60),
        (-151.25, 60), (-151.25, 59.75), (-153.75, 59.75), (-153.75, 59.5), (-156.25, 59.5),
        (-156.25, 59.25), (-158.75, 59.25), (-158.75, 59), (-161.25, 59), (-161.25, 59.25),
        (-162, 59.25), (-162, 59.5), (-163.25, 59.5), (-163.25, 59.75), (-164.5, 59.75),
        (-164.5, 60), (-165, 60), (-165, 60.25), (-165.5, 60.5), (-165.5, 61), (-165.75, 61),
        (-165.75, 61.5), (-166, 61.5), (-166, 62), (-166.25, 62), (-166.25, 62.75),
        (-166.5, 62.75), (-166.5, 63.25), (-166.75, 63.25), (-166.75, 63.75), (-167, 63.75),
        (-167, 64.25), (-167.25, 64.25), (-167.25, 64.75), (-167.5, 64.75), (-167.5, 65.25),
        (-167.75, 65.25), (-167.75, 65.75), (-168, 65.75), (-168, 66), (-167.75, 66),
        (-167.5, 66.5), (-167, 66.5), (-166.5, 67.25), (-166, 67.25), (-165.5, 68),
        (-163.75, 68.25), (-163.75, 68.5), (-163, 68.5), (-163, 68.75), (-162, 68.75),
        (-162, 69), (-161.25, 69), (-161.25, 69.25), (-160.75, 69.25), (-160.75, 69.5),
        (-159.5, 69.5), (-159.5, 69.75), (-158.75, 69.75), (-158.75, 70), (-158.25, 70),
        (-158.25, 70.25), (-157, 70.25), (-157, 70.5), (-156.25, 70.5), (-156.25, 70.75),
        (-155.75, 70.75),
    ],
    "Central America": [
        (-90.75, 18), (-88.25, 18), (-88.25, 17.75), (-87.75, 17.5), (-87.75, 17),
        (-87.5, 17), (-87.5, 16.5), (-87.25, 16.5), (-87.25, 16), (-87, 16), (-87, 15.75),
        (-86.25, 15.75), (-86.25, 15.5), (-85.25, 15.5), (-85.25, 15.25), (-84, 15.25),
        (-84, 15), (-83.5, 15), (-83.5, 10.75), (-83.25, 10.75), (-83.25, 10.5), (-83, 10.5),
        (-82.25, 9.5), (-81.75, 9.5), (-81.75, 9.25), (-81.25, 9.25), (-81.25, 9),
        (-77.5, 8.75), (-77.5, 7.5), (-79, 7.5), (-79, 7.25), (-79.75, 7.25), (-79.75, 7.5),
        (-80.75, 7.5), (-80.75, 7.75), (-81.5, 7.75), (-81.5, 8), (-82.5, 8), (-82.5, 8.25),
        (-83.5, 8.5), (-83.75, 9), (-84.25, 9), (-84.5, 9.5), (-85, 9.5), (-85, 9.75),
        (-85.25, 9.75), (-85.25, 10), (-86.25, 10.75), (-86.25, 11.25), (-87, 11.75),
        (-87, 12.25), (-87.25, 12.25), (-87.75, 13), (-89, 13.25), (-89, 13.5), (-90, 13.5),
        (-90, 13.75), (-91, 13.75), (-91, 14), (-91.5, 14), (-91.5, 14.25), (-92, 14.5),
        (-92, 15), (-95.25, 16), (-95.25, 16.5), (-95, 16.5), (-94.25, 17.5), (-93.75, 17.5),
        (-93.75, 17.25), (-93.25, 17.25), (-93.25, 17), (-92.25, 16.75), (-92.25, 17.75),
        (-90.75, 17.75),
    ],
}
# ----------------------------------------------------------------------
# MAP REFINEMENT: redrawn Scandinavia and Iberia, Hudson Bay cut out of Canada, thin gaps
# between neighbouring countries closed, and the islands / small countries that were
# missing. These outlines replace the older ones of the same name (see below).
# ----------------------------------------------------------------------
REBUILT_OUTLINES = {
    "Afghanistan": [
        (58.7, 39.62), (58.75, 39.72), (61.25, 39.69), (61.62, 39.56), (63.75, 39.56), (64.12,
        39.44), (66.38, 39.44), (66.75, 39.31), (69, 39.31), (69.38, 39.19), (71.5, 39.19),
        (71.88, 39.06), (74.12, 39.06), (74.27, 39), (74.31, 38.88), (74.1, 38.62), (74.07,
        38.25), (74.38, 37.73), (78.27, 36.5), (78.31, 33.88), (78.25, 33.73), (78.12, 33.69),
        (77.75, 33.93), (74.25, 33.94), (73.62, 33.81), (73.38, 33.6), (73, 33.52), (72.88,
        33.35), (72.13, 33.31), (71.88, 33.1), (71.25, 33.02), (71.12, 32.85), (70.5, 32.77),
        (70.38, 32.6), (70, 32.52), (69.88, 32.23), (68.75, 32.02), (68.62, 31.73), (67.25,
        31.52), (67.12, 31.35), (66.75, 31.27), (66.62, 30.98), (65.5, 30.77), (65.38, 30.48),
        (64.12, 30.31), (63.88, 30.1), (63.5, 30.02), (63.38, 29.85), (62.75, 29.77), (62.5,
        29.35), (61.75, 29.27), (61.62, 28.98), (60.62, 28.82), (60.5, 28.85), (60.44, 29),
        (60.43, 31), (60.19, 31.38), (60.19, 31.88), (60.06, 32.25), (60.06, 33.38), (59.9,
        34.12), (59.69, 34.38), (59.68, 35.25), (59.44, 35.62), (59.43, 36.5), (59.19, 36.88),
        (59.18, 37.75), (58.94, 38.12), (58.93, 39), (58.73, 39.25),
    ],
    "Alaska": [
        (-155.85, 70.88), (-155.75, 70.98), (-152.75, 70.94), (-152.38, 70.81), (-149.62,
        70.81), (-149.25, 70.57), (-145.88, 70.56), (-145.5, 70.32), (-142.12, 70.31), (-141.75,
        70.07), (-135.75, 70.07), (-135.6, 70.12), (-135.5, 70.4), (-135.25, 70.4), (-135.19,
        69.38), (-135.43, 69), (-135.23, 68.75), (-135.23, 68.5), (-135.4, 68.38), (-135.48,
        68), (-135.65, 67.88), (-135.73, 67.5), (-135.9, 67.38), (-135.98, 66.75), (-136.15,
        66.62), (-136.23, 66.25), (-136.4, 66.12), (-136.48, 65.75), (-136.65, 65.62), (-136.73,
        65), (-136.9, 64.88), (-136.98, 64.5), (-137.15, 64.38), (-137.23, 63.75), (-137.4,
        63.62), (-137.48, 63.25), (-137.65, 63.12), (-137.73, 62.75), (-137.9, 62.62), (-137.98,
        62), (-138.15, 61.88), (-138.23, 61.5), (-138.4, 61.38), (-138.48, 61), (-138.65,
        60.88), (-138.73, 60.25), (-138.9, 60.12), (-138.9, 59.88), (-138.69, 59.62), (-138.73,
        58.38), (-139, 58.35), (-139.12, 58.65), (-139.5, 58.73), (-139.75, 58.93), (-142.38,
        58.94), (-142.75, 59.18), (-144.88, 59.19), (-145.25, 59.43), (-147.38, 59.44),
        (-147.75, 59.68), (-149.88, 59.69), (-150.25, 59.93), (-151, 59.93), (-151.38, 59.69),
        (-153.5, 59.68), (-153.88, 59.44), (-156, 59.43), (-156.38, 59.19), (-158.5, 59.18),
        (-158.88, 58.94), (-161, 58.94), (-161.25, 58.98), (-161.5, 59.18), (-162, 59.23),
        (-162.25, 59.43), (-163.12, 59.44), (-163.5, 59.68), (-164.38, 59.69), (-164.62, 59.9),
        (-165, 59.98), (-165.12, 60.27), (-165.52, 60.5), (-165.85, 61.38), (-166.02, 61.5),
        (-166.1, 61.88), (-166.27, 62), (-166.35, 62.62), (-166.52, 62.75), (-166.6, 63.12),
        (-166.77, 63.25), (-166.85, 63.62), (-167.02, 63.75), (-167.1, 64.12), (-167.27, 64.25),
        (-167.35, 64.62), (-167.52, 64.75), (-167.6, 65.12), (-167.77, 65.25), (-167.85, 65.62),
        (-168.02, 65.75), (-168.02, 66), (-167.73, 66.12), (-167.5, 66.52), (-167, 66.6),
        (-166.5, 67.28), (-166, 67.35), (-165.5, 68.03), (-164, 68.19), (-163.85, 68.25),
        (-163.75, 68.52), (-163.12, 68.6), (-162.88, 68.81), (-162.25, 68.82), (-161.88, 69.06),
        (-161.38, 69.1), (-161.25, 69.27), (-160.88, 69.35), (-160.75, 69.52), (-159.75, 69.57),
        (-159.5, 69.77), (-158.88, 69.85), (-158.75, 70.02), (-158.38, 70.1), (-158.25, 70.27),
        (-157.25, 70.32), (-157, 70.52), (-156.38, 70.6), (-156.25, 70.77),
    ],
    "Algeria": [
        (3.1, 37.12), (3.38, 37.15), (3.5, 36.86), (3.62, 36.86), (3.88, 37.06), (6.38, 37.06),
        (6.62, 36.85), (7, 36.77), (7.12, 36.6), (7.75, 36.52), (7.88, 36.35), (8.5, 36.27),
        (8.75, 36.07), (9.12, 36.1), (9.25, 36.39), (9.38, 36.41), (9.53, 36.25), (9.56, 19.5),
        (9.5, 19.35), (9.25, 19.27), (9.12, 19.1), (8.5, 19.02), (8.25, 18.82), (7.38, 18.94),
        (7, 19.18), (6.25, 19.23), (6.12, 19.52), (5, 19.73), (4.75, 19.93), (4.25, 19.98), (4,
        20.4), (3.38, 20.44), (3, 20.68), (2.25, 20.73), (1.88, 21.15), (1.5, 21.23), (1.37,
        21.4), (0.38, 21.44), (0.12, 21.65), (-0.5, 21.73), (-0.87, 22.15), (-1.25, 22.23),
        (-1.38, 22.4), (-2, 22.48), (-2.12, 22.65), (-3, 22.91), (-3.75, 22.98), (-3.88, 23.15),
        (-4.5, 23.23), (-4.62, 23.52), (-5.64, 23.75), (-5.64, 23.88), (-5.48, 24), (-5.4,
        24.38), (-5.23, 24.5), (-5.15, 24.88), (-4.98, 25), (-4.9, 25.5), (-4.48, 25.75),
        (-4.29, 26.38), (-3.98, 26.75), (-3.91, 27.25), (-3.23, 27.75), (-2.91, 28.75), (-2.23,
        29.25), (-1.88, 30.3), (-0.97, 31), (-0.91, 31.75), (-0.23, 32.25), (-0.12, 32.8),
        (0.67, 33.38), (1.52, 34.25), (1.62, 35.05), (2.42, 35.62), (3.02, 36.25),
    ],
    "Angola": [
        (11.7, -2.38), (12.12, -2.28), (12.5, -2.77), (13, -2.85), (13.25, -3.27), (13.62,
        -3.35), (13.75, -3.52), (14.25, -3.6), (14.5, -4.02), (15, -4.1), (15.25, -4.52),
        (15.75, -4.6), (16, -5.02), (16.5, -5.1), (16.75, -5.52), (17.25, -5.6), (17.5, -6.02),
        (18, -6.1), (18.25, -6.52), (18.75, -6.6), (19, -7.02), (19.5, -7.1), (19.75, -7.52),
        (20.25, -7.6), (20.5, -8.02), (21, -8.1), (21.25, -8.52), (21.75, -8.6), (22, -9.02),
        (22.88, -9.22), (23.45, -10), (24, -10.1), (24.5, -10.77), (25.38, -10.98), (25.5,
        -11.27), (26.38, -11.6), (26.68, -12), (26.44, -12.38), (26.43, -13.25), (26.19,
        -13.62), (26.15, -14.38), (25.98, -14.5), (25.9, -15.12), (25.73, -15.25), (25.65,
        -15.62), (25.48, -15.75), (25.29, -16.62), (24.98, -17), (24.93, -18), (24.62, -18.4),
        (24.25, -18.48), (24.12, -18.77), (23, -18.98), (22.75, -19.4), (21.75, -19.48), (21.62,
        -19.65), (20.75, -19.98), (20.5, -20.4), (19.5, -20.48), (19.38, -20.65), (19, -20.73),
        (18.73, -21), (18.62, -21.27), (17.25, -21.48), (17, -21.9), (16.5, -21.98), (16.25,
        -22.18), (15.75, -22.23), (15.62, -22.52), (14.5, -22.73), (14.31, -23), (14.12,
        -23.09), (13.93, -22), (13.69, -21.62), (13.68, -20.75), (13.44, -20.38), (13.43,
        -19.75), (13.19, -19.38), (13.18, -18.5), (12.94, -18.12), (12.93, -12.75), (12.69,
        -12.38), (12.54, -11), (12.4, -10.62), (12.23, -10.5), (12.15, -9.88), (11.94, -9.62),
        (11.94, -8.38), (12.15, -8.12), (12.23, -7.5), (12.4, -7.38), (12.48, -7), (12.65,
        -6.88), (12.69, -6.38), (12.91, -6), (11.97, -5.25), (11.94, -3.12), (11.77, -2.75),
        (11.61, -2.62),
    ],
    "Argentina": [
        (-65.14, -28.25), (-65, -28.23), (-64.75, -28.43), (-64.25, -28.48), (-64, -28.68),
        (-63.5, -28.73), (-63.38, -28.9), (-62.75, -28.98), (-62.62, -29.15), (-62, -29.23),
        (-61.88, -29.4), (-61.25, -29.48), (-61.12, -29.65), (-60.5, -29.73), (-60.38, -29.9),
        (-60, -29.98), (-59.75, -30.4), (-59.12, -30.44), (-58.75, -30.68), (-57.75, -30.73),
        (-57.62, -30.9), (-57.25, -30.98), (-56.66, -31.62), (-57.12, -31.85), (-57.4, -32.12),
        (-57.48, -32.5), (-57.88, -32.73), (-57.93, -32.88), (-57.88, -33.3), (-57.23, -33.75),
        (-57.23, -34.25), (-57.62, -34.45), (-58.2, -35.25), (-58.62, -35.35), (-58.75, -35.52),
        (-59.25, -35.6), (-59.5, -36.02), (-59.88, -36.1), (-60.15, -36.38), (-60.48, -37.25),
        (-60.65, -37.38), (-60.73, -37.75), (-60.9, -37.88), (-60.98, -38.25), (-61.15, -38.38),
        (-61.23, -38.75), (-61.54, -39.12), (-61.73, -40), (-62.41, -40.5), (-62.73, -41.5),
        (-63.15, -41.88), (-63.23, -42.25), (-63.4, -42.38), (-63.48, -43), (-64.15, -43.5),
        (-64.23, -44), (-64.65, -44.25), (-64.84, -45.12), (-65.18, -45.75), (-65.23, -46.25),
        (-65.4, -46.38), (-65.48, -47), (-65.65, -47.12), (-65.73, -47.75), (-65.9, -47.88),
        (-65.98, -48.5), (-66.15, -48.62), (-66.23, -49), (-66.4, -49.12), (-66.48, -49.5),
        (-66.65, -49.62), (-66.98, -50.5), (-67.28, -50.75), (-67.48, -51.5), (-67.9, -51.75),
        (-67.9, -52.12), (-66.48, -53.5), (-66.3, -53.88), (-65.47, -54.5), (-65.5, -54.77),
        (-66.12, -54.81), (-66.38, -54.6), (-67, -54.52), (-67.12, -54.23), (-68.25, -54.02),
        (-71.02, -51.25), (-71.2, -50.88), (-72.03, -50.25), (-72.06, -48.25), (-72.19, -47.88),
        (-72.19, -44), (-72.31, -43.62), (-72.32, -42.62), (-72.54, -42.38), (-72.27, -41.88),
        (-71.58, -41.38), (-71.23, -41), (-71.04, -40.38), (-70.73, -40), (-70.65, -39.5),
        (-70.23, -39.25), (-70.04, -38.62), (-69.73, -38.25), (-69.66, -37.75), (-68.72, -37),
        (-68.53, -36.25), (-68.23, -36), (-67.9, -35.12), (-67.73, -35), (-67.65, -34.62),
        (-67.48, -34.5), (-67.4, -33.88), (-67.23, -33.75), (-67.15, -33.38), (-66.98, -33.25),
        (-66.9, -32.88), (-66.73, -32.75), (-66.65, -32.38), (-66.48, -32.25), (-66.4, -31.88),
        (-66.23, -31.75), (-66.04, -30.62), (-65.73, -30.25), (-65.68, -29.75), (-65.48, -29.5),
        (-65.43, -29), (-65.23, -28.75),
    ],
    "Belgium": [
        (2.57, 51.5), (2.75, 51.53), (3, 51.38), (3.5, 51.56), (4.38, 51.56), (5.38, 51.29),
        (6.12, 50.92), (6.37, 50.38), (6.33, 50.25), (6.02, 49.62), (5.75, 49.46), (4.75,
        49.47), (3.75, 50.29), (2.38, 51.19), (2.29, 51.38),
    ],
    "Bolivia": [
        (-63.56, -4.88), (-63.25, -4.84), (-63, -4.98), (-62.9, -5.5), (-62.48, -5.75), (-62.4,
        -6.12), (-62.23, -6.25), (-62.09, -6.62), (-62.04, -7), (-61.88, -7.27), (-61.48, -7.5),
        (-61.15, -8.38), (-60.98, -8.5), (-60.9, -8.88), (-60.73, -9), (-60.65, -9.38), (-60.48,
        -9.5), (-60.4, -9.88), (-60.23, -10), (-59.91, -11), (-59.23, -11.5), (-58.9, -12.38),
        (-58.73, -12.5), (-58.65, -12.88), (-58.48, -13), (-58.4, -13.38), (-58.23, -13.5),
        (-57.91, -14.5), (-57.23, -15), (-56.98, -16), (-60, -19.02), (-60.38, -19.2), (-60.95,
        -20), (-61.62, -20.1), (-62, -20.52), (-62.27, -20.62), (-62.95, -21.5), (-63.38,
        -21.6), (-63.5, -21.77), (-63.8, -21.88), (-64.45, -22.75), (-65, -22.84), (-65.7,
        -23.75), (-66.12, -23.85), (-66.25, -24.02), (-66.55, -24.12), (-67.2, -25), (-67.62,
        -25.1), (-68, -25.41), (-68.75, -25.31), (-68.9, -25.25), (-69, -24.98), (-69.5,
        -24.93), (-69.75, -24.73), (-70.4, -24.62), (-70.4, -24.38), (-70.12, -24.27), (-70.07,
        -24.12), (-70.07, -20), (-70.27, -19.75), (-70.35, -19.38), (-70.52, -19.25), (-70.72,
        -18.5), (-71.12, -18.17), (-71.62, -17.45), (-71.75, -17.34), (-72.71, -17.12), (-72.59,
        -16.88), (-72.56, -16.38), (-72.1, -15.88), (-72.02, -15.5), (-71.75, -15.2), (-70.88,
        -14.55), (-70.77, -14), (-69.67, -12.88), (-68.88, -12.3), (-68.52, -11.25), (-67.92,
        -10.62), (-67.12, -10.05), (-66.77, -9), (-66.35, -8.62), (-66.27, -8.25), (-65.62,
        -7.8), (-65.52, -7.25), (-64.88, -6.8), (-64.78, -6.25), (-63.88, -5.55), (-63.77, -5),
    ],
    "Borneo": [
        (116.56, 6.88), (116.75, 7), (116.88, 6.93), (117.75, 6.09), (119.1, 5.38), (118.94,
        5.12), (118.09, 4.38), (117.94, 3.62), (117.81, 2.38), (118.41, 1.25), (118.46, 0.88),
        (116.71, -1.75), (116.12, -3.72), (114.12, -3.56), (113.75, -3.44), (112.88, -3.44),
        (112.5, -3.31), (111.62, -3.31), (110.12, -2.9), (109.96, -2.5), (109.79, -1.5),
        (108.96, 0), (108.97, 1), (110.62, 2.16), (113.38, 3.59), (113.93, 4), (115.19, 5.12),
    ],
    "Brazil": [
        (-53.81, 2.88), (-53.62, 2.96), (-53.5, 2.35), (-53, 2.27), (-52.88, 2.1), (-52.5,
        2.02), (-52.38, 1.73), (-51.5, 1.52), (-50.88, 0.92), (-50.25, 0.09), (-47.75, 0.02),
        (-47.62, -0.15), (-47, -0.23), (-46.88, -0.52), (-45.75, -0.73), (-45.62, -0.9),
        (-45.25, -0.98), (-45.12, -1.15), (-44.5, -1.23), (-44.38, -1.4), (-44, -1.48), (-43.88,
        -1.65), (-43.25, -1.73), (-43.12, -1.9), (-42.75, -1.98), (-42.62, -2.15), (-42, -2.23),
        (-41.88, -2.4), (-41.5, -2.48), (-41.38, -2.65), (-40.88, -2.69), (-40.62, -2.9), (-40,
        -2.98), (-39.88, -3.27), (-38.5, -3.48), (-38.38, -3.65), (-38, -3.73), (-37.75, -4.15),
        (-37.25, -4.23), (-37, -4.65), (-36.5, -4.73), (-36.25, -5.15), (-35.75, -5.23),
        (-35.55, -5.62), (-34.98, -6), (-34.94, -9.12), (-35.15, -9.38), (-35.23, -9.75),
        (-35.88, -10.2), (-36, -10.8), (-36.88, -11.45), (-36.98, -12), (-37.38, -12.2),
        (-37.95, -13), (-38.88, -13.1), (-39.15, -13.38), (-39.23, -14), (-39.54, -14.38),
        (-39.73, -15.25), (-39.9, -15.38), (-39.98, -15.75), (-40.15, -15.88), (-40.23, -16.5),
        (-40.54, -16.88), (-40.73, -18), (-41.15, -18.25), (-41.48, -19.25), (-41.9, -19.5),
        (-41.98, -20), (-42.4, -20.25), (-42.48, -20.75), (-42.65, -20.88), (-42.88, -21.72),
        (-43.38, -21.65), (-43.5, -21.48), (-43.88, -21.4), (-44, -21.23), (-45.12, -21.02),
        (-45.25, -20.73), (-45.62, -20.65), (-45.75, -20.48), (-46.38, -20.4), (-46.5, -20.23),
        (-46.88, -20.15), (-47, -19.98), (-47.38, -19.9), (-47.5, -19.73), (-47.88, -19.65),
        (-48, -19.48), (-48.62, -19.4), (-48.75, -19.23), (-49.12, -19.15), (-49.25, -18.98),
        (-49.62, -18.9), (-49.75, -18.73), (-50.38, -18.65), (-50.5, -18.48), (-51.38, -18.15),
        (-51.5, -17.98), (-52.12, -17.9), (-52.25, -17.73), (-53.12, -17.4), (-53.25, -17.23),
        (-53.62, -17.15), (-53.75, -16.98), (-54.38, -16.9), (-54.5, -16.73), (-54.88, -16.65),
        (-55, -16.48), (-55.38, -16.4), (-55.5, -16.23), (-56.12, -16.15), (-56.25, -15.98),
        (-56.62, -15.9), (-56.75, -15.73), (-57, -15.65), (-57.23, -15), (-57.91, -14.5),
        (-58.23, -13.5), (-58.4, -13.38), (-58.48, -13), (-58.65, -12.88), (-58.73, -12.5),
        (-58.9, -12.38), (-59.23, -11.5), (-59.91, -11), (-60.23, -10), (-60.4, -9.88), (-60.48,
        -9.5), (-60.65, -9.38), (-60.73, -9), (-60.9, -8.88), (-60.98, -8.5), (-61.15, -8.38),
        (-61.48, -7.5), (-61.88, -7.27), (-62.04, -7), (-62.09, -6.62), (-62.23, -6.25), (-62.4,
        -6.12), (-62.48, -5.75), (-62.9, -5.5), (-62.98, -5), (-63.18, -4.75), (-63.12, -4.6),
        (-62.7, -4.5), (-62.12, -3.7), (-61.75, -3.52), (-60.62, -2.35), (-59.95, -2.25),
        (-59.3, -1.38), (-58.7, -1.25), (-58.05, -0.38), (-57.45, -0.25), (-56.8, 0.62), (-56.2,
        0.75), (-55.55, 1.62), (-54.95, 1.75), (-54.38, 2.55),
    ],
    "British East Africa": [
        (31.4, 5.38), (31.62, 5.46), (31.88, 5.4), (32.12, 5.19), (32.75, 5.15), (33, 4.73),
        (34, 4.65), (34.25, 4.23), (34.62, 4.15), (34.75, 3.98), (35.38, 3.91), (35.75, 3.71),
        (36.12, 3.65), (36.25, 3.48), (36.88, 3.4), (37, 3.23), (37.38, 3.15), (37.5, 2.98),
        (38.12, 2.9), (38.25, 2.73), (38.62, 2.65), (38.75, 2.48), (39.38, 2.4), (39.5, 2.23),
        (39.88, 2.15), (40, 1.98), (40.62, 1.9), (40.88, 1.69), (41.38, 2.02), (41.53, 2),
        (41.44, 1.75), (41.6, 1), (42.02, 0.75), (42.1, 0.25), (42.52, 0), (42.6, -0.5), (43.02,
        -0.75), (43.06, -1.88), (42.85, -2.12), (42.77, -2.75), (42.6, -2.88), (42.52, -3.5),
        (42.35, -3.62), (42.31, -4.38), (42.1, -4.62), (42.02, -5.25), (41.85, -5.38), (41.77,
        -6), (41.6, -6.12), (41.46, -6.5), (41.41, -7.25), (41.27, -7.75), (41.1, -7.88),
        (41.02, -8.5), (40.71, -8.88), (40.62, -9.96), (40.25, -9.69), (38, -9.69), (37.62,
        -9.56), (35.38, -9.56), (35, -9.44), (32.75, -9.44), (32.38, -9.31), (29.98, -9.25),
        (29.93, -6), (29.69, -5.62), (29.68, -3), (29.44, -2.62), (29.43, -0.25), (29.19, 0.12),
        (29.18, 2.75), (28.94, 3.12), (28.94, 4.38), (28.98, 4.5), (29.12, 4.56), (30.12, 4.73),
        (30.25, 5.02), (30.88, 5.1), (31, 5.27),
    ],
    "Burma": [
        (100.73, 30.75), (101.75, 30.77), (101.95, 30.38), (102.67, 29.88), (103.12, 28.95),
        (104.03, 28.25), (104.1, 27.88), (104.27, 27.75), (104.38, 27.45), (105.28, 26.75),
        (105.44, 26.25), (105.41, 26), (105.02, 25.38), (104.73, 25.25), (104.65, 24.75),
        (104.23, 24.5), (103.9, 23.5), (103.48, 23.25), (103.41, 22.75), (102.73, 22.25),
        (102.65, 21.88), (102.23, 21.5), (102.25, 20.99), (102, 20.98), (101.75, 20.82),
        (101.25, 20.78), (100.55, 19.88), (100.25, 19.77), (100.12, 19.6), (99.7, 19.5), (99.05,
        18.62), (98.75, 18.52), (98.62, 18.35), (98, 18.28), (97.5, 17.6), (96.95, 17.5), (96.3,
        16.62), (95.7, 16.5), (95.05, 15.62), (94.38, 15.48), (94.31, 15.75), (94.39, 16.12),
        (94.23, 16.25), (94.15, 16.62), (93.98, 16.75), (93.9, 17.12), (93.73, 17.25), (93.68,
        18), (93.48, 18.25), (93.4, 18.75), (92.98, 19), (92.9, 19.88), (92.73, 20), (92.65,
        20.38), (92.48, 20.5), (92.4, 20.88), (92.23, 21), (92.15, 21.5), (91.79, 21.62),
        (91.82, 21.75), (92, 22.02), (92.4, 22.25), (92.48, 22.75), (92.75, 23.02), (93.12,
        23.2), (93.7, 24), (94.12, 24.1), (96.08, 26.12), (96.91, 26.75), (96.89, 26.88),
        (96.75, 26.93), (95.88, 26.94), (95.62, 27.15), (95, 27.23), (94.98, 27.75), (95.5,
        27.85), (95.75, 28.27), (96.12, 28.35), (96.25, 28.52), (96.62, 28.6), (96.75, 28.77),
        (97.12, 28.85), (97.25, 29.02), (97.62, 29.1), (97.75, 29.27), (98.12, 29.35), (98.25,
        29.52), (98.62, 29.6), (98.75, 29.77), (99.12, 29.85), (99.25, 30.02), (99.62, 30.1),
        (99.75, 30.27), (100.12, 30.35), (100.25, 30.52), (100.62, 30.6),
    ],
    "Canada": [
        (-126.27, 70.5), (-125.88, 70.56), (-74.75, 70.52), (-74.62, 70.35), (-74.25, 70.27),
        (-74.12, 70.1), (-73.75, 70.02), (-73.62, 69.85), (-73.25, 69.77), (-73.12, 69.6),
        (-72.75, 69.52), (-72.63, 69.35), (-72.25, 69.27), (-72.12, 69.1), (-71.25, 68.77),
        (-71.12, 68.48), (-70.25, 68.27), (-70.05, 67.88), (-69.5, 67.52), (-69.15, 66.5),
        (-68.73, 66.25), (-68.65, 65.75), (-68.23, 65.5), (-67.9, 64.5), (-67.48, 64.25),
        (-67.4, 63.75), (-66.98, 63.5), (-66.72, 62.62), (-66.75, 62.48), (-67, 62.44), (-70,
        63), (-78.12, 62.94), (-79.38, 63.19), (-80, 63.19), (-80.38, 63.31), (-81.75, 63.44),
        (-86, 64.25), (-87.88, 64.06), (-90.5, 63.29), (-92.38, 62.09), (-94.25, 61.15),
        (-94.31, 60.88), (-94.06, 59.75), (-94.09, 59.38), (-94.28, 58.88), (-94.19, 58.62),
        (-92.5, 56.97), (-89.12, 56.91), (-87.62, 55.96), (-85.38, 55.41), (-80.75, 51.44),
        (-80.62, 51.38), (-79, 51.44), (-78.85, 51.5), (-78.82, 51.62), (-78.94, 52.12),
        (-78.91, 52.62), (-78.54, 53.75), (-77.69, 55.5), (-78.19, 58.38), (-77.34, 60),
        (-77.31, 60.75), (-77.44, 61.12), (-77.38, 61.9), (-77, 61.94), (-71.88, 60.94),
        (-65.75, 60.93), (-65.12, 60.42), (-64.75, 59.85), (-64.25, 59.77), (-64.12, 59.6),
        (-63.75, 59.52), (-63.62, 59.35), (-63.25, 59.27), (-63.12, 59.1), (-62.75, 59.02),
        (-62.62, 58.85), (-61.75, 58.52), (-61.62, 58.23), (-60.75, 58.02), (-60.38, 57.67),
        (-59.8, 56.88), (-59.25, 56.77), (-58.7, 56.25), (-58.05, 55.38), (-57.5, 55.27),
        (-57.12, 54.92), (-56.55, 54.12), (-55.98, 54), (-55.98, 53.75), (-56.12, 53.69), (-58,
        53.68), (-58.25, 53.48), (-59, 53.43), (-59.25, 53.23), (-59.88, 53.15), (-60.12,
        52.94), (-60.75, 52.93), (-61.12, 52.65), (-61.18, 52.5), (-60.98, 52.25), (-60.9,
        51.88), (-60.73, 51.75), (-60.65, 51.38), (-60.48, 51.25), (-60.4, 50.88), (-60.23,
        50.75), (-60.15, 50.38), (-59.98, 50.25), (-59.75, 49.85), (-59, 49.77), (-58.88, 49.6),
        (-58.5, 49.52), (-58.38, 49.35), (-57.75, 49.27), (-57.62, 49.1), (-57.25, 49.02),
        (-57.12, 48.85), (-56.5, 48.77), (-56.38, 48.6), (-56, 48.52), (-55.88, 48.35), (-55.25,
        48.27), (-55.23, 47.75), (-55.88, 47.65), (-56, 47.48), (-56.38, 47.4), (-56.5, 47.23),
        (-57.12, 47.15), (-57.25, 46.98), (-57.62, 46.9), (-57.75, 46.73), (-58.25, 46.68),
        (-58.5, 46.48), (-59.62, 46.27), (-59.75, 45.98), (-60.38, 45.9), (-60.5, 45.73),
        (-61.25, 45.68), (-61.62, 45.44), (-62.25, 45.43), (-62.62, 45.19), (-64.12, 45.02),
        (-64.25, 44.73), (-64.62, 44.65), (-64.75, 44.48), (-65.02, 44.38), (-65.1, 43.88),
        (-65.25, 43.82), (-65.38, 43.85), (-65.43, 44), (-65.48, 45), (-65.73, 45.25), (-66.25,
        45.35), (-66.5, 45.77), (-66.88, 45.85), (-67, 46.02), (-67.5, 46.06), (-67.75, 46.02),
        (-68, 45.82), (-69, 45.78), (-69.5, 45.1), (-70, 45.02), (-70.25, 44.82), (-70.62,
        44.85), (-70.88, 45.06), (-71.88, 45.06), (-72.25, 44.82), (-73.12, 44.81), (-73.5,
        44.57), (-74.38, 44.56), (-74.62, 44.35), (-75.62, 44.31), (-76, 44.07), (-77.38,
        44.06), (-77.75, 43.82), (-79.12, 43.81), (-79.5, 43.59), (-80.12, 44.42), (-81, 45.27),
        (-81.55, 45.38), (-82.12, 46.17), (-83, 47.02), (-85, 47.19), (-85.38, 47.56), (-86.25,
        47.57), (-86.62, 47.81), (-87.5, 47.82), (-87.88, 48.06), (-88.75, 48.07), (-89.12,
        48.31), (-90, 48.32), (-90.38, 48.56), (-91.25, 48.57), (-91.62, 48.81), (-92.5, 48.82),
        (-92.88, 49.06), (-93.75, 49.07), (-94.12, 49.31), (-94.88, 49.31), (-95.12, 49.1),
        (-95.38, 49.06), (-123.12, 49.06), (-123.75, 48.97), (-124.11, 49.12), (-123.88, 49.21),
        (-123.86, 49.37), (-124.25, 49.48), (-124.38, 49.77), (-125.25, 49.98), (-126.38,
        51.08), (-126.95, 51.88), (-127.5, 51.97), (-128, 52.65), (-128.5, 52.73), (-128.88,
        53.15), (-129.25, 53.22), (-129.75, 53.9), (-130.3, 54), (-130.95, 54.88), (-131.5,
        54.98), (-131.88, 55.33), (-132.25, 55.9), (-132.8, 56), (-133.45, 56.88), (-134,
        56.98), (-134.25, 57.4), (-134.75, 57.48), (-134.88, 57.65), (-135.75, 57.98), (-135.85,
        58.25), (-136, 58.31), (-136.88, 58.31), (-137.25, 58.44), (-138.62, 58.35), (-138.69,
        59.62), (-138.93, 60), (-138.73, 60.25), (-138.65, 60.88), (-138.48, 61), (-138.4,
        61.38), (-138.23, 61.5), (-138.15, 61.88), (-137.98, 62), (-137.9, 62.62), (-137.73,
        62.75), (-137.65, 63.12), (-137.48, 63.25), (-137.4, 63.62), (-137.23, 63.75), (-137.15,
        64.38), (-136.98, 64.5), (-136.9, 64.88), (-136.73, 65), (-136.65, 65.62), (-136.48,
        65.75), (-136.4, 66.12), (-136.23, 66.25), (-136.15, 66.62), (-135.98, 66.75), (-135.9,
        67.38), (-135.73, 67.5), (-135.65, 67.88), (-135.48, 68), (-135.4, 68.38), (-135.23,
        68.5), (-135.23, 68.75), (-135.43, 69), (-135.19, 69.38), (-135.12, 70.4), (-134.88,
        70.4), (-134.77, 70.12), (-134.62, 70.07), (-127.88, 70.06), (-127.62, 70.1), (-127.38,
        70.31), (-126.5, 70.32),
    ],
    "Central America": [
        (-90.77, 18), (-90.5, 18.06), (-88.25, 18.02), (-88.12, 17.73), (-87.73, 17.5), (-87.4,
        16.62), (-87.23, 16.5), (-87.15, 16.12), (-86.88, 15.85), (-86.25, 15.77), (-86, 15.57),
        (-85.38, 15.56), (-85, 15.32), (-84.12, 15.31), (-83.88, 15.1), (-83.5, 15.02), (-83.4,
        10.88), (-82.88, 10.42), (-82.3, 9.62), (-81.75, 9.52), (-81.62, 9.35), (-81.25, 9.27),
        (-81.12, 8.98), (-77.5, 8.77), (-77.48, 7.5), (-78.75, 7.43), (-79.12, 7.19), (-79.62,
        7.19), (-79.88, 7.4), (-80.62, 7.44), (-80.88, 7.65), (-81.5, 7.73), (-81.75, 7.93),
        (-82.5, 7.98), (-82.62, 8.27), (-83.5, 8.48), (-83.75, 8.9), (-84.25, 8.98), (-84.5,
        9.4), (-85, 9.48), (-85.27, 9.75), (-85.45, 10.12), (-86.25, 10.7), (-86.34, 11.25),
        (-87.02, 11.75), (-87.1, 12.12), (-87.38, 12.33), (-87.88, 13.03), (-88.88, 13.19),
        (-89.25, 13.43), (-89.88, 13.44), (-90.25, 13.68), (-91, 13.73), (-91.12, 13.9), (-91.5,
        13.98), (-91.62, 14.27), (-92.02, 14.5), (-92.12, 15.02), (-94.5, 15.79), (-95.47,
        15.88), (-95.27, 16.5), (-94.95, 16.62), (-94.38, 17.42), (-93.88, 17.79), (-93.65,
        17.38), (-93.25, 17.27), (-93.12, 16.98), (-92.5, 16.82), (-92.38, 16.85), (-92.32, 17),
        (-92.25, 17.77), (-91, 17.82),
    ],
    "Chile": [
        (-70.4, -24.75), (-69.88, -24.69), (-69.62, -24.9), (-69, -24.98), (-68.88, -25.27),
        (-67.75, -25.48), (-66.23, -27), (-66.05, -27.38), (-65.25, -27.95), (-65.19, -28.62),
        (-65.4, -28.88), (-65.48, -29.5), (-65.65, -29.62), (-65.73, -30.25), (-66.04, -30.62),
        (-66.23, -31.75), (-66.4, -31.88), (-66.48, -32.25), (-66.65, -32.38), (-66.98, -33.25),
        (-67.15, -33.38), (-67.23, -33.75), (-67.4, -33.88), (-67.48, -34.5), (-67.65, -34.62),
        (-67.73, -35), (-67.9, -35.12), (-68.23, -36), (-68.53, -36.25), (-68.72, -37), (-69.66,
        -37.75), (-69.73, -38.25), (-70.04, -38.62), (-70.23, -39.25), (-70.65, -39.5), (-70.73,
        -40), (-71.04, -40.38), (-71.23, -41), (-71.58, -41.38), (-72.25, -41.85), (-72.5,
        -42.27), (-72.62, -42.27), (-72.71, -41.12), (-73.06, -40.62), (-73.06, -36.88),
        (-72.85, -36.62), (-72.77, -36.25), (-72.6, -36.12), (-72.52, -35.75), (-72.35, -35.62),
        (-72.27, -35.25), (-72.1, -35.12), (-72.02, -34.75), (-71.85, -34.62), (-71.77, -34.25),
        (-71.6, -34.12), (-71.52, -33.75), (-71.35, -33.62), (-71.27, -33.25), (-71.07, -33),
        (-71.06, -29.38), (-70.71, -28.88), (-70.66, -28.38), (-70.32, -27.75), (-70.27,
        -27.25), (-70.07, -27), (-70.07, -25.25), (-70.12, -25.1), (-70.4, -25),
    ],
    "China": [
        (81.6, 44.88), (82.12, 44.91), (82.5, 44.71), (82.88, 44.65), (83, 44.48), (83.62,
        44.4), (83.75, 44.23), (84.12, 44.15), (84.25, 43.98), (84.75, 43.93), (85, 43.77),
        (86.12, 43.52), (86.25, 43.23), (86.88, 43.15), (87.12, 42.94), (87.62, 42.9), (87.75,
        42.73), (88.12, 42.65), (88.25, 42.48), (88.88, 42.4), (89, 42.23), (89.62, 42.15),
        (89.88, 41.94), (105.75, 41.93), (106.12, 41.69), (107.75, 41.68), (108.12, 41.44),
        (109.75, 41.43), (110.12, 41.19), (111.75, 41.18), (112.12, 40.94), (113, 40.93),
        (113.25, 40.73), (113.62, 40.65), (113.75, 40.48), (114.12, 40.4), (114.25, 40.23),
        (114.62, 40.15), (114.75, 39.98), (115.12, 39.9), (115.25, 39.73), (115.62, 39.65),
        (115.75, 39.48), (116.12, 39.4), (116.25, 39.23), (116.62, 39.15), (116.88, 38.94),
        (117.25, 38.98), (117.5, 39.4), (118, 39.48), (118.25, 39.9), (118.75, 39.98), (119,
        40.4), (119.5, 40.48), (119.75, 41.4), (120.5, 41.44), (120.88, 41.31), (123.25, 41.02),
        (123.48, 40.25), (123.9, 40), (123.91, 39.5), (123, 38.8), (122.9, 38.38), (122.48, 38),
        (122.4, 37.25), (122, 37.02), (121.88, 36.73), (120.75, 36.52), (120.52, 36.12),
        (120.25, 36.02), (120.19, 35.88), (120.19, 34.88), (120.4, 34.62), (120.54, 34.12),
        (120.56, 33.25), (120.73, 32.5), (120.93, 32.25), (120.98, 31.75), (121.25, 31.48),
        (121.62, 31.4), (121.75, 30.98), (122.62, 30.91), (122.84, 30.62), (122.35, 30.5),
        (122.27, 30.25), (122.1, 30.12), (122.02, 29.75), (121.86, 29.62), (122.02, 28.75),
        (121.34, 28.25), (121.27, 27.5), (121.1, 27.38), (121.02, 26.75), (120.85, 26.62),
        (120.81, 26.12), (120.6, 25.88), (120.52, 25.25), (120.21, 24.88), (120.02, 24),
        (119.75, 23.73), (119.25, 23.65), (119, 23.23), (118.12, 23.03), (117.75, 22.48),
        (116.88, 22.28), (116.5, 21.73), (115.62, 21.52), (115.52, 21.25), (115.25, 20.98),
        (114.85, 20.88), (114.62, 20.46), (114.12, 20.73), (113.55, 21.5), (113.12, 21.6),
        (112.88, 21.81), (111.12, 21.81), (110.75, 21.94), (108.88, 21.97), (108.12, 22.92),
        (107.85, 23.12), (107.75, 23.8), (106.88, 24.45), (106.77, 24.75), (106.6, 24.88),
        (106.52, 25.25), (105.88, 25.73), (105.75, 26.02), (105.48, 26.12), (105.25, 26.8),
        (104.38, 27.45), (104.27, 27.75), (104.1, 27.88), (104, 28.3), (103.12, 28.95), (103.02,
        29.25), (102.85, 29.38), (102.75, 29.8), (101.88, 30.45), (101.77, 30.75), (101.6,
        30.88), (101.5, 31.3), (100.59, 32), (100.52, 32.25), (100.35, 32.38), (100.25, 32.8),
        (99.5, 33.35), (99.25, 33.77), (98.88, 33.85), (98.75, 34.02), (98, 34.07), (97.62,
        34.31), (93.5, 34.44), (93.12, 34.81), (91, 34.82), (90.62, 35.06), (88.25, 35.07),
        (87.88, 35.31), (85.5, 35.32), (85.12, 35.56), (82.75, 35.57), (82.38, 35.81), (81,
        35.82), (80.62, 36.06), (79.75, 36.07), (79.5, 36.27), (78.38, 36.46), (74.38, 37.73),
        (74.27, 38), (74.1, 38.12), (74.07, 38.5), (74.31, 38.88), (74.46, 40.62), (74.6,
        41.12), (74.81, 41.38), (74.82, 42.25), (75.02, 42.5), (75.12, 42.9), (75.5, 42.98),
        (75.62, 43.15), (76.12, 43.21), (76.5, 43.41), (77.25, 43.48), (77.38, 43.65), (78,
        43.73), (78.25, 43.93), (79, 43.98), (79.12, 44.15), (79.75, 44.23), (80, 44.43),
        (80.75, 44.48), (80.88, 44.65), (81.5, 44.73),
    ],
    "Colombia": [
        (-72.77, 11.38), (-72.5, 11.4), (-72.4, 10.88), (-72, 10.77), (-71.73, 10.5), (-71.4,
        9.62), (-71.23, 9.5), (-71.15, 9.12), (-70.98, 9), (-70.9, 8.62), (-70.73, 8.5),
        (-70.65, 8.12), (-70.48, 8), (-70.4, 7.62), (-70.23, 7.5), (-70.15, 7.12), (-69.98, 7),
        (-69.9, 6.62), (-69.73, 6.5), (-69.65, 6.12), (-69.48, 6), (-69.4, 5.62), (-69.23, 5.5),
        (-69.15, 5.12), (-68.98, 5), (-68.9, 4.62), (-68.73, 4.5), (-68.65, 4.12), (-68.48, 4),
        (-68.4, 3.38), (-68.23, 3.25), (-68.15, 2.88), (-67.98, 2.75), (-67.9, 2.38), (-67.73,
        2.25), (-67.65, 1.88), (-67.48, 1.75), (-67.15, 0.88), (-66.98, 0.75), (-66.9, 0.38),
        (-66.73, 0.25), (-66.65, -0.13), (-66.48, -0.25), (-66.4, -0.62), (-66.23, -0.75),
        (-66.15, -1.12), (-65.98, -1.25), (-65.9, -1.62), (-65.73, -1.75), (-65.4, -2.62),
        (-65.23, -2.75), (-64.97, -3.62), (-65, -3.77), (-65.88, -3.81), (-66.25, -3.57),
        (-67.62, -3.56), (-68, -3.32), (-69.38, -3.31), (-69.75, -3.07), (-71.38, -3.06),
        (-71.75, -2.82), (-73.12, -2.81), (-73.5, -2.57), (-75.12, -2.56), (-75.5, -2.32),
        (-76.88, -2.31), (-77.25, -2.07), (-78.62, -2.06), (-78.88, -1.85), (-79.5, -1.77),
        (-79.79, -1.38), (-79.57, -1.12), (-79.56, -0.38), (-79.35, -0.13), (-79.19, 0.62),
        (-79.19, 1.75), (-79.06, 2.12), (-79.06, 2.62), (-78.85, 2.88), (-78.77, 3.5), (-78.6,
        3.62), (-78.52, 4.25), (-78.35, 4.38), (-78.27, 5), (-78.1, 5.12), (-78.02, 5.75),
        (-77.85, 5.88), (-77.77, 6.5), (-77.46, 6.88), (-77.27, 8), (-75.25, 10.02), (-74.88,
        10.2), (-74.3, 11), (-73, 11.07), (-72.85, 11.12),
    ],
    "Cuba": [
        (-83.06, 23), (-82, 23.12), (-80.12, 23.06), (-78, 22.54), (-76, 21.54), (-74.38,
        20.41), (-74.29, 20.25), (-76, 19.94), (-77.5, 19.97), (-78.62, 21.53), (-81.75, 22.31),
        (-82.25, 22.31), (-84, 21.88), (-84.88, 21.95), (-84.96, 22), (-84.93, 22.12), (-84,
        22.91),
    ],
    "Czechoslovakia": [
        (14.48, 50.75), (15.62, 50.81), (16, 50.47), (17.75, 50.27), (17.88, 49.98), (18.75,
        49.77), (19.12, 49.22), (21, 49.02), (21.25, 48.6), (21.77, 48.5), (21.77, 48), (21.12,
        47.9), (20.88, 47.69), (20.38, 47.65), (20.12, 47.44), (18.88, 47.27), (18.75, 46.98),
        (17.87, 46.65), (17.75, 46.48), (17.38, 46.4), (17.25, 46.23), (16.88, 46.15), (16.75,
        45.98), (16.38, 45.9), (16.25, 45.73), (15.75, 45.65), (15.62, 45.48), (15.12, 45.4),
        (15, 45.23), (14.62, 45.15), (14.38, 44.81), (14.12, 44.66), (14.02, 45), (13.73,
        45.12), (13.65, 45.62), (13.12, 46.08), (12.53, 47), (12.75, 47.27), (13.12, 47.35),
        (13.25, 47.8), (14.16, 48.5), (14.15, 48.88), (13.98, 49), (13.9, 49.38), (13.69,
        49.62), (13.69, 50.12), (14, 50.52), (14.38, 50.6),
    ],
    "Denmark": [
        (9.94, 57.62), (10.5, 57.72), (10.55, 57.62), (10.59, 56.88), (10.85, 56.5), (10.32,
        56.12), (10.5, 55.96), (10.75, 55.84), (11.12, 55.81), (11.75, 56.04), (12.5, 56.09),
        (12.54, 55.62), (12, 54.6), (10.38, 54.56), (9.88, 54.81), (8.88, 54.81), (8.23, 55),
        (7.94, 55.62), (8.09, 56.62), (8.5, 57.16),
    ],
    "Egypt": [
        (24.48, 32.38), (24.75, 32.4), (24.85, 32.12), (25, 32.07), (26.12, 32.06), (26.5,
        31.82), (28.88, 31.81), (29.25, 31.57), (30.62, 31.56), (30.88, 31.35), (31.5, 31.27),
        (31.75, 31.07), (32.25, 31.41), (32.38, 31.39), (32.62, 31.19), (33.25, 31.15), (33.5,
        30.73), (33.88, 30.66), (34.38, 30.4), (34.5, 30.23), (35.05, 30.12), (35.7, 29.25),
        (36.25, 29.16), (36.88, 28.33), (37.25, 27.98), (37.75, 27.9), (37.81, 27.75), (37.77,
        27.5), (37.57, 27.25), (37.56, 26.12), (37.32, 25.75), (37.31, 23.62), (37.1, 23.38),
        (37.02, 23), (36.73, 23), (36.65, 23.62), (36.48, 23.75), (36.4, 24.12), (36.23, 24.25),
        (36.15, 24.88), (35.98, 25), (35.9, 25.38), (35.73, 25.5), (35.65, 25.88), (35.48, 26),
        (35.15, 27.62), (34.5, 28.18), (34.46, 27.75), (34.6, 27.5), (35, 27.28), (35.06,
        27.12), (34.91, 26.38), (34.77, 26), (34.6, 25.88), (34.56, 25.38), (34.35, 25.12),
        (34.27, 24.5), (34.1, 24.38), (33.77, 23.5), (33.6, 23.38), (33.52, 23), (33.35, 22.88),
        (33.31, 22.38), (33.09, 22), (33.48, 20.38), (33.88, 20.27), (33.88, 19.98), (22.25,
        19.98), (22.19, 20.38), (22.4, 20.62), (22.44, 21.62), (22.68, 22), (22.69, 23.12),
        (22.9, 23.38), (23.06, 24.12), (23.06, 25.12), (23.19, 25.88), (23.43, 26.25), (23.44,
        27.12), (23.65, 27.38), (23.69, 28.38), (23.93, 28.75), (23.94, 29.88), (24.18, 30.25),
        (24.19, 31.12), (24.43, 31.5),
    ],
    "Ethiopia": [
        (37.2, 14.25), (37.62, 14.34), (37.85, 13.62), (38.02, 13.5), (38.1, 13.12), (38.27,
        13), (38.35, 12.38), (38.52, 12.25), (38.85, 11.38), (39.13, 11.1), (40, 11.07), (40.25,
        11.27), (40.88, 11.35), (41, 11.52), (41.62, 11.6), (41.75, 11.77), (42.25, 11.82),
        (42.5, 11.98), (44, 11.77), (44.25, 11.35), (44.75, 11.27), (45.02, 11), (45.02, 7.75),
        (44.85, 7.62), (44.77, 7.25), (44.09, 6.75), (44.02, 6.25), (43.6, 6), (43.52, 5.5),
        (43.1, 5.25), (43.02, 4.75), (42.6, 4.5), (42.52, 4), (42.1, 3.75), (42.02, 3.25),
        (41.6, 3), (41.52, 2.5), (41.21, 2.25), (41.49, 2.12), (41, 1.72), (40.75, 1.73), (40.5,
        1.93), (40, 1.98), (39.87, 2.15), (39.5, 2.23), (39.38, 2.4), (38.75, 2.48), (38.62,
        2.65), (38.25, 2.73), (38.12, 2.9), (37.5, 2.98), (37.38, 3.15), (37, 3.23), (36.88,
        3.4), (36.25, 3.48), (36.12, 3.65), (35.75, 3.71), (35.38, 3.91), (34.75, 3.98), (34.62,
        4.15), (34.25, 4.23), (34, 4.65), (33, 4.73), (32.75, 5.15), (32, 5.23), (31.73, 5.5),
        (31.73, 5.75), (32.12, 5.98), (32.29, 6.25), (32.48, 7), (32.88, 7.23), (33.04, 7.5),
        (33.23, 8.25), (33.65, 8.5), (33.98, 9.5), (34.4, 9.75), (34.73, 10.75), (35.15, 11),
        (35.48, 12), (35.9, 12.25), (36.23, 13.25), (36.62, 13.45),
    ],
    "Finland": [
        (26.94, 70), (28, 70.03), (28.91, 69.12), (29.16, 68.5), (29.22, 68), (29.79, 67.5),
        (30.04, 66.62), (29.94, 65.38), (30.25, 64.88), (30.06, 64.12), (30.09, 63.88), (30.38,
        63.59), (31.52, 63), (31.52, 62.38), (30.25, 61.91), (29.73, 61.5), (29.5, 61.1),
        (28.38, 60.58), (28.25, 60.72), (27.62, 60.44), (26, 60.44), (22.88, 59.88), (22.25,
        60.09), (21.22, 60.88), (21.31, 61.75), (21.19, 62.5), (21.6, 63.38), (23.75, 64.54),
        (25.21, 65.12), (24.75, 65.66), (24.5, 65.65), (24.25, 65.44), (24.1, 65.5), (23.91,
        66.5), (23.46, 67), (23.16, 67.62), (22.5, 68.44), (22.38, 68.54), (21.12, 68.84),
        (20.64, 69.12), (21.5, 69.25), (22.5, 68.81), (24.75, 68.81),
    ],
    "France": [
        (2.07, 51.25), (2.12, 51.34), (2.25, 51.3), (3.8, 50.25), (4.75, 49.47), (5.62, 49.44),
        (6.12, 49.6), (6.25, 49.48), (7.38, 49.02), (7.43, 48.88), (7.4, 46.62), (7, 46.52),
        (6.77, 46.12), (6.5, 46.02), (6.44, 45.88), (6.68, 45.5), (6.73, 44.75), (7.41, 44.25),
        (7.47, 43.62), (7.12, 43.52), (7.02, 43.25), (6.62, 42.94), (6.12, 42.94), (5.75,
        43.18), (4.88, 43.19), (4.62, 43.31), (4, 43.15), (3.72, 42.75), (3.62, 41.95), (2.88,
        41.34), (2.5, 41.16), (2.44, 41.38), (2.59, 41.75), (3.29, 42.38), (3, 42.5), (2,
        42.44), (1.38, 42.79), (0.5, 42.94), (-0.62, 42.94), (-1.55, 43.25), (-1.81, 43.62),
        (-1.77, 43.88), (-1.57, 44.12), (-1.57, 45), (-1.91, 45.5), (-1.97, 45.75), (-1.73,
        45.88), (-1.46, 46.25), (-1.4, 46.5), (-1.77, 46.75), (-1.88, 47.15), (-2.25, 47.23),
        (-2.5, 47.43), (-3, 47.48), (-3.12, 47.65), (-3.5, 47.73), (-3.62, 48.02), (-4.62,
        48.19), (-4.77, 48.25), (-4.81, 48.38), (-4.77, 48.5), (-4.62, 48.56), (-3, 48.57),
        (-2.75, 48.77), (-2.12, 48.85), (-1.85, 49.12), (-1.75, 49.77), (-0.62, 49.98), (-0.5,
        50.27), (0.12, 50.35), (0.25, 50.52), (1.38, 50.73), (1.5, 51.02), (2, 51.1),
    ],
    "French West Africa": [
        (-6.65, 23.62), (-5.38, 23.69), (-4.62, 23.52), (-4.5, 23.23), (-3.88, 23.15), (-3.62,
        22.94), (-3, 22.91), (-2.12, 22.65), (-1.88, 22.44), (-1.38, 22.4), (-1.25, 22.23),
        (-0.88, 22.15), (-0.5, 21.73), (0.12, 21.65), (0.38, 21.44), (1.38, 21.4), (1.5, 21.23),
        (1.88, 21.15), (2.25, 20.73), (3, 20.68), (3.38, 20.44), (4, 20.4), (4.25, 19.98),
        (4.75, 19.93), (5, 19.73), (6.12, 19.52), (6.25, 19.23), (7, 19.18), (7.25, 18.98),
        (7.72, 18.88), (7.62, 17.95), (6.83, 17.38), (5.23, 15.75), (5.12, 15.2), (4.22, 14.5),
        (4.12, 13.95), (3.25, 13.3), (3.15, 12.88), (2.73, 12.5), (2.38, 11.45), (1.58, 10.88),
        (0.98, 10.25), (0.88, 9.7), (0.23, 9.25), (0.12, 8.7), (-0.52, 8.25), (-0.62, 7.45),
        (-1.42, 6.88), (-2.02, 6.25), (-2.35, 5.38), (-2.52, 5.25), (-2.6, 4.62), (-2.75, 4.57),
        (-2.88, 4.6), (-2.98, 4.88), (-3.12, 4.93), (-4.75, 4.93), (-5.12, 4.69), (-6.25, 4.68),
        (-6.62, 4.44), (-8.12, 4.44), (-8.27, 4.5), (-8.38, 4.77), (-9.25, 4.98), (-11.02,
        6.75), (-11.2, 7.12), (-12, 7.7), (-12.12, 8.55), (-13, 9.2), (-13.1, 9.62), (-13.27,
        9.75), (-13.38, 10.05), (-14.02, 10.5), (-14.12, 11.05), (-15.03, 11.75), (-15.1,
        12.12), (-15.31, 12.38), (-15.35, 13.12), (-15.56, 13.38), (-15.6, 14.12), (-15.77,
        14.25), (-15.85, 14.88), (-16.06, 15.12), (-16.07, 15.75), (-16.31, 16.12), (-16.32,
        17), (-16.56, 17.38), (-16.57, 18.25), (-16.77, 18.5), (-16.82, 19.5), (-17.06, 19.88),
        (-17.06, 21.12), (-17, 21.27), (-16.6, 21.5), (-16.69, 22), (-16.62, 22.27), (-16.25,
        22.22), (-16, 22.31), (-14.5, 22.31), (-14.12, 22.44), (-12.62, 22.44), (-12.25, 22.68),
        (-11.38, 22.69), (-11.12, 22.9), (-10.12, 22.94), (-9.75, 23.18), (-8.62, 23.19),
        (-8.25, 23.43), (-6.88, 23.44),
    ],
    "Germany": [
        (7.98, 55.25), (8.12, 55.27), (8.23, 55), (8.38, 54.94), (8.88, 54.81), (9.88, 54.81),
        (10.38, 54.56), (11.38, 54.56), (11.62, 54.44), (11.88, 54.56), (12.5, 54.57), (12.88,
        54.81), (13.02, 54.75), (13.12, 54.36), (13.5, 54.44), (14.02, 54.38), (14.03, 54.25),
        (13.78, 54), (13.79, 53.88), (13.98, 53.5), (14.38, 53.4), (14.43, 53.25), (14.68, 51),
        (14.38, 50.6), (14, 50.52), (13.73, 50.25), (13.69, 49.62), (13.9, 49.38), (13.98, 49),
        (14.15, 48.88), (14.16, 48.5), (13.25, 47.8), (13.12, 47.35), (12.75, 47.27), (12.5,
        47.07), (8.62, 47.06), (8.25, 46.82), (7.48, 46.88), (7.4, 49), (6.25, 49.48), (6.13,
        49.75), (6.37, 50.38), (6.16, 50.88), (5.82, 51.25), (6.06, 51.62), (6.06, 53.38),
        (5.54, 54.12), (6.5, 54.32), (6.75, 54.52), (7.62, 54.72),
    ],
    "Greece": [
        (25.35, 43.62), (26.25, 43.68), (26.5, 43.48), (26.88, 43.44), (27.25, 43.68), (27.5,
        43.48), (27.88, 43.4), (28, 43.23), (28.38, 43.16), (28.55, 43), (28.59, 42.88), (28.13,
        42.77), (28.07, 42.62), (28.1, 41.38), (28.38, 41.35), (28.48, 41.62), (28.62, 41.68),
        (28.75, 41.65), (28.81, 41.5), (28.81, 40.88), (28.69, 40.5), (28.69, 39.75), (28.56,
        39.38), (28.56, 38.62), (28.44, 38.25), (28.44, 37.5), (28.28, 36.75), (27.88, 36.41),
        (27.62, 36.9), (27.25, 36.98), (26.98, 37.25), (26.65, 38.12), (26.48, 38.25), (26.4,
        38.62), (26.23, 38.75), (26.04, 39.88), (25.88, 40.15), (24.5, 40.18), (24.35, 40.12),
        (24.31, 39.38), (24.07, 39), (24.02, 37.5), (23.6, 37.25), (23.27, 36.25), (22.75,
        36.02), (22.23, 36.5), (22.05, 36.88), (21.25, 37.45), (21, 38.3), (20.88, 38.41),
        (20.5, 38.48), (20.3, 38.88), (19.73, 39.25), (19.46, 40.12), (19.41, 40.62), (19.27,
        41), (19.03, 41.12), (19.04, 41.25), (19.25, 41.53), (20.25, 41.73), (20.38, 41.9), (21,
        41.98), (21.25, 42.18), (21.75, 42.23), (21.88, 42.52), (23.38, 42.69), (23.62, 42.9),
        (24.25, 42.98), (24.38, 43.15), (25, 43.23),
    ],
    "Greenland": [
        (-31.69, 83.38), (-30, 83.5), (-29.25, 83.44), (-28.12, 83.19), (-26.75, 83.06),
        (-25.62, 82.81), (-25.12, 82.81), (-23.12, 82.44), (-22.62, 82.44), (-22.25, 82.31),
        (-21.75, 82.31), (-20, 82.02), (-18.47, 79), (-19.59, 76.25), (-20.09, 75.25), (-21.88,
        72.58), (-25, 70.46), (-29.62, 68.66), (-35, 65.96), (-40.38, 64.53), (-41.66, 62.5),
        (-43, 59.9), (-43.62, 59.94), (-44.62, 60.19), (-48, 60.72), (-51.69, 64.12), (-53.54,
        66.5), (-54.06, 68.88), (-53.92, 69.12), (-52.21, 70.38), (-52.15, 70.5), (-52.5,
        70.79), (-55.55, 72.5), (-58.12, 75.53), (-59.5, 75.56), (-59.88, 75.69), (-61.25,
        75.69), (-61.62, 75.81), (-62.88, 75.81), (-63.25, 75.94), (-64.5, 75.94), (-64.88,
        76.06), (-66.25, 76.06), (-66.62, 76.19), (-67.88, 76.19), (-71.75, 77.84), (-71.91,
        78), (-71.38, 78.29), (-63.88, 81.06), (-62.5, 81.06), (-62.12, 81.19), (-60.75, 81.19),
        (-60.38, 81.31), (-59, 81.31), (-58.62, 81.44), (-57.25, 81.44), (-56.88, 81.56),
        (-55.5, 81.56), (-55.12, 81.69), (-53.75, 81.69), (-53.38, 81.81), (-50.25, 81.94),
        (-49.88, 82.06), (-46.88, 82.19), (-46.5, 82.31), (-45.25, 82.31), (-44.88, 82.44),
        (-43.62, 82.44), (-43.25, 82.56), (-41.88, 82.56), (-41.5, 82.69), (-40.25, 82.69),
        (-39.88, 82.81), (-38.62, 82.81), (-38.25, 82.94), (-36.88, 82.94), (-36.5, 83.06),
        (-35.25, 83.06), (-34.88, 83.19), (-33.62, 83.19), (-33.25, 83.31),
    ],
    "Hispaniola": [
        (-72.7, 19.88), (-72.5, 20), (-70, 19.91), (-68.7, 18.88), (-68.54, 18.62), (-69.12,
        18.34), (-71.5, 17.63), (-73.88, 18.09), (-74.47, 18.5), (-74.42, 18.62),
    ],
    "Iceland": [
        (-22.31, 66.38), (-22, 66.5), (-19.62, 66.19), (-17.25, 66.19), (-16.88, 66.31),
        (-15.12, 66.31), (-14, 65.44), (-13.65, 65), (-15, 64.21), (-16.12, 63.96), (-18.62,
        63.44), (-20.88, 63.44), (-22.52, 63.88), (-22.09, 65), (-22.12, 65.14), (-23.91,
        65.62), (-23.75, 65.78),
    ],
    "India": [
        (74.1, 33.88), (74.38, 33.94), (77.88, 33.9), (78.4, 33.38), (78.48, 33), (78.9, 32.62),
        (78.98, 32.25), (79.4, 32), (79.48, 31.5), (79.89, 31.25), (79.77, 30.88), (79.48,
        30.75), (79.38, 30.2), (78.73, 29.75), (78.73, 29.25), (79.15, 29), (79.23, 28.5),
        (79.62, 28.27), (79.75, 27.98), (81.12, 27.77), (81.25, 27.48), (81.88, 27.4), (82,
        27.23), (82.75, 27.18), (83, 26.98), (83.62, 26.9), (83.75, 26.73), (84.25, 26.68),
        (84.5, 26.52), (87.12, 26.69), (87.5, 26.93), (88.88, 26.94), (89.25, 27.18), (90.88,
        27.19), (91.25, 27.43), (94.75, 27.31), (95.62, 27.15), (95.88, 26.94), (96.89, 26.88),
        (96.8, 26.62), (96.08, 26.12), (94.12, 24.1), (93.75, 24.03), (93.62, 23.92), (93.12,
        23.2), (92.75, 23.02), (92.48, 22.75), (92.4, 22.25), (92, 22.02), (91.75, 21.7),
        (91.62, 21.66), (91.52, 21.88), (91.38, 21.93), (90.38, 21.94), (90, 21.81), (88.25,
        21.81), (88.1, 21.75), (88, 21.48), (87.38, 21.4), (86.92, 20.88), (86.12, 20.3),
        (86.02, 19.75), (85.85, 19.62), (85.77, 19.25), (85.6, 19.12), (85.52, 18.75), (85.35,
        18.62), (85.27, 18.25), (85.1, 18.12), (85.02, 17.75), (84.85, 17.62), (84.77, 17.25),
        (84.6, 17.12), (84.52, 16.75), (84.35, 16.62), (84.27, 16.25), (84.1, 16.12), (84.02,
        15.75), (83.85, 15.62), (83.77, 15.25), (83.6, 15.12), (83.52, 14.75), (83.35, 14.62),
        (83.27, 14.25), (83.1, 14.12), (83.02, 13.75), (82.85, 13.62), (82.77, 13.25), (82.6,
        13.12), (82.52, 12.75), (82.35, 12.62), (82.27, 12.25), (82.1, 12.12), (82.02, 11.75),
        (81.85, 11.62), (81.77, 11.25), (81.6, 11.12), (81.52, 10.75), (81.35, 10.62), (81.27,
        10.25), (81.1, 10.12), (80.77, 9.25), (80.5, 9.13), (79.75, 9.47), (79.66, 8.5), (79.52,
        8), (79.38, 7.94), (77.12, 7.94), (76.73, 8.25), (76.4, 9.12), (76.23, 9.25), (76.15,
        9.62), (75.98, 9.75), (75.9, 10.12), (75.73, 10.25), (75.65, 10.62), (75.48, 10.75),
        (75.4, 11.12), (75.23, 11.25), (75.15, 11.62), (74.98, 11.75), (74.9, 12.12), (74.73,
        12.25), (74.65, 12.88), (74.48, 13), (74.4, 13.38), (74.23, 13.5), (74.15, 14.12),
        (73.98, 14.25), (73.9, 14.62), (73.73, 14.75), (73.65, 15.38), (73.48, 15.5), (73.4,
        15.88), (73.23, 16), (72.9, 17.25), (72.48, 17.5), (72.4, 17.88), (72.23, 18), (72.15,
        18.5), (71.73, 18.75), (71.54, 19.5), (71.38, 19.77), (70.98, 20), (70.78, 20.75),
        (70.23, 21.25), (70.15, 21.75), (69.54, 21.88), (70.06, 22.62), (70.1, 23.88), (70.38,
        24.15), (70.75, 24.23), (71.08, 24.75), (72, 24.98), (72.12, 25.15), (72.5, 25.23),
        (72.88, 25.78), (73.75, 25.98), (73.88, 26.15), (74.25, 26.23), (74.62, 26.78), (75.5,
        26.98), (75.62, 27.15), (76, 27.23), (76.25, 27.65), (76.8, 27.75), (77.35, 28.5),
        (77.77, 28.75), (77.81, 29.62), (77.6, 29.88), (77.52, 30.25), (76.95, 30.38), (76.38,
        31.17), (75.25, 32.27), (74.1, 32.5),
    ],
    "Indochina": [
        (105.45, 26), (105.75, 26.02), (105.88, 25.73), (106.52, 25.25), (106.6, 24.88),
        (106.77, 24.75), (106.84, 24.5), (107.75, 23.8), (107.85, 23.12), (108.12, 22.92),
        (108.88, 21.97), (110.75, 21.94), (111.12, 21.81), (112.88, 21.81), (113.12, 21.6),
        (113.55, 21.5), (114.1, 20.75), (114.52, 20.5), (114.5, 20.36), (113.62, 20.15), (113.5,
        19.98), (113, 19.9), (112.75, 19.48), (111.88, 19.28), (111.3, 18.5), (110.38, 18.15),
        (110.1, 17.88), (110.02, 17.5), (109.82, 17.25), (109.77, 16.5), (109.57, 16.25),
        (109.56, 15.62), (109.32, 15.25), (109.31, 14.62), (109.07, 14.25), (109.06, 13.62),
        (108.82, 13.25), (108.81, 12.62), (108.57, 12.25), (108.56, 11.62), (108.32, 11.25),
        (108.27, 10.5), (108.1, 10.38), (108.02, 10), (107.73, 9.88), (107.5, 9.48), (107, 9.4),
        (106.75, 8.98), (106.25, 8.9), (106, 8.48), (105.6, 8.38), (105.38, 7.91), (105.09,
        8.12), (105.06, 9.12), (104.82, 9.5), (104.81, 10.38), (104.57, 10.75), (104.31, 12.62),
        (104.1, 12.88), (103.96, 13.38), (103.81, 15.12), (103.57, 15.5), (103.56, 16.38),
        (103.35, 16.62), (103.31, 17.38), (103.1, 17.62), (102.94, 18.25), (102.94, 19.12),
        (102.81, 19.88), (102.6, 20.12), (102.52, 20.75), (102.35, 20.88), (102.19, 21.38),
        (102.65, 21.88), (102.73, 22.25), (103.41, 22.75), (103.48, 23.25), (103.9, 23.5),
        (104.23, 24.5), (104.65, 24.75), (104.73, 25.25), (105.02, 25.38),
    ],
    "Iran": [
        (52.85, 42.75), (53.25, 42.79), (54.38, 42.29), (58.77, 40), (58.69, 39.38), (58.93,
        39), (58.94, 38.12), (59.18, 37.75), (59.19, 36.88), (59.43, 36.5), (59.44, 35.62),
        (59.68, 35.25), (59.69, 34.38), (59.9, 34.12), (60.06, 33.38), (60.06, 32.25), (60.19,
        31.88), (60.19, 31.38), (60.43, 31), (60.43, 28), (60.23, 27.75), (60.15, 27.38),
        (59.98, 27.25), (59.9, 26.62), (59.69, 26.38), (59.65, 25.38), (59.25, 24.95), (59.12,
        24.91), (59, 25.15), (58.5, 25.23), (58.4, 25.5), (58.25, 25.56), (57.62, 25.56),
        (57.12, 25.69), (56.75, 25.64), (56.62, 25.5), (56.5, 25.57), (56.28, 25.88), (56.62,
        26.11), (56.66, 26.25), (56.53, 26.75), (56.38, 26.91), (55.75, 26.93), (55.38, 26.69),
        (54.12, 26.69), (53.88, 26.9), (53.25, 26.98), (53.12, 27.27), (52.2, 27.5), (51.75,
        28.15), (51.25, 28.23), (50.12, 29.33), (49.5, 30.16), (49, 29.9), (48.88, 29.71),
        (48.59, 30), (48.6, 30.38), (48.81, 30.62), (48.81, 32.75), (48.94, 33.12), (48.97,
        37.5), (49.12, 37.66), (49.38, 37.72), (49.5, 37.35), (50, 37.27), (50.12, 37.1), (50.5,
        37.02), (50.75, 36.82), (51.75, 36.81), (52.12, 36.94), (53.4, 37), (53.93, 40), (53.73,
        40.25), (53.65, 40.62), (53.48, 40.75), (53.4, 41.12), (53.23, 41.25), (53.15, 41.62),
        (52.98, 41.75),
    ],
    "Iraq": [
        (48.1, 43), (48.17, 43), (48.23, 42.62), (48.52, 42.5), (48.62, 42.2), (49.5, 41.55),
        (49.6, 41), (49.97, 40.75), (49.77, 40.25), (49.38, 40.15), (49.07, 39.75), (49.07,
        38.12), (49.12, 37.98), (49.34, 37.88), (49, 37.55), (48.94, 37.38), (48.94, 33.12),
        (48.81, 32.75), (48.81, 30.62), (48.57, 30.25), (48.59, 30), (48.78, 29.75), (48.77,
        29.62), (48.5, 29.52), (48.47, 29.38), (48.62, 29.1), (49.12, 29.02), (49.15, 28.75),
        (47.25, 28.69), (46.88, 28.56), (45.38, 28.56), (45, 28.44), (43.62, 28.44), (43.25,
        28.31), (41.88, 28.31), (41.5, 28.19), (40, 28.19), (39.62, 28.06), (38.21, 28.12),
        (38.35, 28.62), (38.52, 28.75), (38.66, 29.12), (38.71, 29.62), (39.02, 30), (39.35,
        30.88), (39.52, 31), (39.6, 31.38), (39.77, 31.5), (40.09, 32.75), (41.03, 33.5),
        (41.34, 34.75), (42.02, 35.25), (42.1, 35.62), (42.52, 36), (42.71, 36.62), (43.02, 37),
        (43.1, 37.5), (43.52, 37.75), (43.59, 38.25), (44.42, 38.88), (44.77, 39.25), (44.88,
        39.8), (45.52, 40.25), (45.59, 40.75), (46.42, 41.38), (46.77, 41.75), (46.88, 42.17),
        (47, 42.28), (47.5, 42.35), (47.73, 42.75),
    ],
    "Ireland": [
        (-7.8, 55.25), (-7.5, 55.37), (-6.5, 55.28), (-5.94, 54.62), (-5.88, 54.5), (-6.19,
        53.38), (-6.19, 53), (-5.98, 52.25), (-6.88, 52.16), (-8.62, 51.56), (-9.75, 51.5),
        (-10.31, 51.75), (-10.47, 51.88), (-10.42, 52), (-9.96, 52.38), (-9.65, 53.12), (-10.15,
        53.5), (-10.02, 54.25), (-8.88, 54.34), (-8.55, 54.75),
    ],
    "Italy": [
        (8.48, 47), (12.38, 47.03), (13.12, 46.08), (13.65, 45.62), (13.62, 44.96), (13.12,
        45.19), (12.35, 45), (12.35, 44.62), (12.56, 44.38), (12.6, 43.62), (12.77, 43.5), (13,
        43.1), (13.55, 43), (14.25, 42.09), (14.75, 42.02), (14.88, 41.85), (15.25, 41.77),
        (15.38, 41.6), (16.25, 41.27), (16.35, 41), (16.75, 40.77), (16.81, 40.62), (16.77,
        40.25), (16.6, 40.12), (16.52, 39.75), (16.35, 39.62), (16.27, 39.25), (16.1, 39.12),
        (16.02, 38.75), (15.85, 38.62), (15.75, 37.98), (14.38, 37.94), (14, 37.81), (12.5,
        37.82), (12.73, 38.75), (13.15, 39), (13.23, 39.5), (13.9, 40), (13.98, 40.5), (14.18,
        40.75), (14.15, 41.12), (13.98, 41.25), (13.9, 41.62), (13.73, 41.75), (13.65, 42.12),
        (13.38, 42.4), (11, 42.48), (10.27, 43.87), (10.12, 43.93), (8, 43.93), (7.85, 43.88),
        (7.75, 43.61), (7.5, 43.7), (7.38, 44.3), (6.73, 44.75), (6.68, 45.5), (6.48, 45.75),
        (6.48, 46), (6.77, 46.12), (7, 46.52), (7.38, 46.6), (7.62, 46.81), (8.38, 46.85),
    ],
    "Java": [
        (106.44, -6.12), (106.75, -6), (108.75, -6.44), (110.88, -6.44), (112.12, -6.71),
        (112.62, -6.84), (114.5, -7.73), (114.54, -8.12), (114.38, -8.59), (113.5, -8.56),
        (112.25, -8.31), (111.62, -8.31), (109.5, -7.94), (108.12, -7.81), (106, -7.41),
        (105.21, -6.88), (105.15, -6.75),
    ],
    "Kazakhstan": [
        (67.48, 54.75), (68.25, 54.77), (68.5, 54.35), (69.25, 54.27), (69.5, 53.85), (70,
        53.78), (70.83, 52.75), (71.75, 52.53), (72.58, 51.5), (73.5, 51.27), (74.62, 49.97),
        (76.88, 49.94), (77.25, 49.81), (79.38, 49.81), (79.75, 49.57), (82.38, 49.56), (82.75,
        49.32), (85.12, 49.27), (85.19, 48.12), (85.31, 47.75), (85.31, 45.5), (85.44, 45.12),
        (85.4, 44.12), (85, 43.78), (84.75, 43.93), (84.25, 43.98), (84.12, 44.15), (83.75,
        44.23), (83.62, 44.4), (83.12, 44.44), (82.88, 44.65), (82.5, 44.71), (82.12, 44.91),
        (81.75, 44.93), (81.5, 44.73), (80.88, 44.65), (80.62, 44.44), (80, 44.43), (79.75,
        44.23), (79.12, 44.15), (78.88, 43.94), (78.25, 43.93), (78, 43.73), (77.38, 43.65),
        (77.12, 43.44), (76.5, 43.41), (76.12, 43.21), (75.62, 43.15), (75.5, 42.98), (75.12,
        42.9), (75.02, 42.5), (74.85, 42.38), (74.81, 41.38), (74.57, 41), (74.44, 40.5),
        (74.41, 39.62), (74.27, 39.12), (74.12, 39.07), (71.88, 39.06), (71.5, 39.19), (69.38,
        39.19), (69, 39.31), (66.75, 39.31), (66.38, 39.44), (64.12, 39.44), (63.75, 39.56),
        (61.62, 39.56), (61.25, 39.69), (59, 39.69), (58.85, 39.75), (58.75, 40.02), (58.5,
        40.16), (54.62, 42.09), (54.38, 42.29), (53.25, 42.79), (52.88, 42.85), (52.85, 43.12),
        (53.12, 43.23), (53.23, 43.5), (53.4, 43.62), (53.48, 44.25), (53.65, 44.38), (53.69,
        44.88), (53.89, 45.25), (53.48, 45.5), (53.38, 45.9), (52.78, 46.12), (52.78, 46.75),
        (53.3, 46.88), (53.95, 47.75), (55, 47.85), (55.25, 48.27), (55.75, 48.32), (56, 48.52),
        (57.12, 48.73), (57.25, 49.02), (57.62, 49.1), (57.88, 49.31), (58.38, 49.35), (58.5,
        49.52), (59.88, 49.72), (60.5, 50.53), (61.62, 50.72), (62.5, 51.78), (63.62, 51.97),
        (64.45, 53), (65.38, 53.22), (65.75, 53.77), (66.25, 53.85), (66.5, 54.27), (66.88,
        54.35), (67, 54.52), (67.38, 54.6),
    ],
    "Korea": [
        (124.73, 42), (128.88, 42.06), (129.02, 42), (129.12, 41.73), (130.25, 41.52), (130.84,
        40.88), (130.35, 40.62), (130.27, 40.25), (129.88, 40.05), (129.3, 39.25), (128.75,
        39.15), (128.3, 38.5), (127.75, 38.4), (127.3, 37.75), (126.88, 37.65), (126.67, 37.38),
        (125.88, 36.8), (125.77, 36.25), (125.35, 36), (125.27, 35.5), (124.97, 35.25), (124.77,
        34.5), (124.35, 34.25), (124.27, 33.75), (124.1, 33.62), (124.02, 33.25), (123.72, 33),
        (123.52, 32.25), (123.12, 32.02), (122.96, 31.75), (122.88, 30.79), (122.5, 30.94),
        (121.88, 30.94), (121.73, 31), (121.62, 31.4), (121.25, 31.48), (120.98, 31.75),
        (120.93, 32.25), (120.73, 32.5), (120.56, 33.25), (120.54, 34.12), (120.4, 34.62),
        (120.19, 34.88), (120.19, 35.88), (120.25, 36.02), (120.52, 36.12), (120.75, 36.52),
        (121.88, 36.73), (122, 37.02), (122.4, 37.25), (122.48, 38), (122.9, 38.38), (122.97,
        38.75), (123.91, 39.5), (123.9, 40), (123.48, 40.25), (123.23, 41.25), (123.5, 41.52),
        (123.88, 41.6), (124.12, 41.81), (124.62, 41.85),
    ],
    "Libya": [
        (9.53, 36.38), (9.75, 36.43), (10.12, 36.31), (11.02, 36.25), (11.07, 33.25), (11.12,
        33.1), (11.5, 33.02), (11.75, 32.82), (12.38, 32.81), (12.75, 32.57), (13.38, 32.56),
        (13.75, 32.32), (14.5, 32.27), (14.75, 32.07), (23.88, 32.07), (24.02, 32.12), (24.12,
        32.4), (24.4, 32.38), (24.43, 31.5), (24.23, 31.25), (24.18, 30.25), (23.94, 29.88),
        (23.93, 28.75), (23.69, 28.38), (23.68, 27.5), (23.44, 27.12), (23.43, 26.25), (23.23,
        26), (23.06, 25.12), (23.06, 24.12), (22.9, 23.38), (22.69, 23.12), (22.68, 22), (22.44,
        21.62), (22.43, 20.75), (22.23, 20.5), (22.15, 19.88), (21.7, 19.75), (21, 18.84),
        (20.45, 18.75), (19.88, 17.95), (19.5, 17.77), (19.38, 17.6), (16.88, 17.56), (16.5,
        17.32), (14.25, 17.32), (13.75, 17.77), (12.62, 17.85), (12.5, 18.02), (11.62, 18.35),
        (11.5, 18.52), (10.88, 18.6), (10.75, 18.77), (10.38, 18.85), (10.25, 19.02), (9.6,
        19.12),
    ],
    "Luzon": [
        (120.48, 18.5), (120.88, 18.56), (122.15, 18.5), (122.19, 17.75), (122.06, 17.38),
        (122.06, 16.5), (121.59, 15.12), (121.57, 14.12), (121.62, 13.98), (123.38, 13.02),
        (123.45, 12.88), (121, 13.59), (120.5, 14.43), (119.97, 14.88), (120.31, 16.25),
        (120.31, 17.12), (120.44, 17.5),
    ],
    "Madagascar": [
        (49.09, -12.12), (49.25, -12.03), (49.41, -12.25), (50.41, -14.88), (50.41, -15.12),
        (49.59, -17.25), (48.91, -20.12), (47.66, -24.25), (47.5, -24.52), (47.25, -24.66),
        (45.13, -25.5), (44.96, -25.38), (43.71, -23.5), (43.22, -21.62), (44.31, -19.38),
        (44.07, -17.12), (44.12, -16.98), (46.31, -15.5), (47.88, -13.93),
    ],
    "Mexico": [
        (-113.77, 31.75), (-112.62, 31.81), (-112.38, 31.6), (-111.75, 31.52), (-111.5, 31.32),
        (-108.25, 31.32), (-107.88, 31.56), (-106.62, 31.56), (-106.48, 31.5), (-106.25, 31.1),
        (-105.5, 30.55), (-105.4, 30.12), (-105.12, 29.92), (-104.62, 29.22), (-103.62, 29.06),
        (-103.25, 28.82), (-102.62, 28.81), (-102.38, 28.6), (-101.75, 28.52), (-101.62, 28.35),
        (-101, 28.27), (-100.88, 28.1), (-100.25, 28.02), (-100.13, 27.85), (-99.5, 27.77),
        (-99.38, 27.6), (-98.75, 27.52), (-98.38, 27.17), (-97.8, 26.38), (-97.25, 26.27),
        (-97.12, 25.85), (-96.6, 25.75), (-96.6, 25.5), (-96.88, 25.4), (-96.93, 25.25), (-96.9,
        21.88), (-96.73, 21.75), (-96.65, 21.38), (-96.48, 21.25), (-96.4, 20.88), (-96.23,
        20.75), (-96.15, 20.38), (-95.98, 20.25), (-95.65, 19.38), (-95.48, 19.25), (-95.28,
        18.5), (-94.98, 18.25), (-94.75, 17.9), (-94.12, 17.93), (-93.98, 17.88), (-94, 17.71),
        (-94.38, 17.42), (-94.95, 16.62), (-95.27, 16.5), (-95.47, 16), (-95.62, 15.91),
        (-95.85, 16.62), (-96.38, 17.08), (-97, 17.91), (-97.88, 17.94), (-98.25, 18.18),
        (-98.88, 18.19), (-99.12, 18.4), (-99.75, 18.48), (-100, 18.68), (-100.62, 18.69),
        (-101, 18.93), (-101.62, 18.94), (-102, 19.18), (-102.62, 19.19), (-102.88, 19.4),
        (-103.5, 19.48), (-103.62, 19.65), (-104.38, 19.69), (-104.62, 19.9), (-105, 19.98),
        (-105.27, 20.25), (-105.35, 20.88), (-105.52, 21), (-105.6, 21.62), (-105.77, 21.75),
        (-105.96, 22.62), (-106.12, 22.9), (-109.25, 22.98), (-113.02, 26.75), (-113.2, 27.12),
        (-114.03, 27.75), (-114.07, 30.75), (-114.12, 30.9), (-114.74, 31), (-114.5, 31.52),
        (-113.88, 31.6),
    ],
    "Mindanao": [
        (124.94, 9.75), (125.12, 9.87), (125.25, 9.8), (126.04, 8.75), (126.53, 7.12), (126.5,
        6.95), (125.62, 5.94), (125.5, 5.88), (123.88, 6.54), (122.04, 7), (122.19, 7.25),
        (123.62, 8.69),
    ],
    "Morocco": [
        (2.73, 37.12), (3.02, 37.12), (3.02, 36.25), (2.42, 35.62), (1.62, 35.05), (1.52,
        34.25), (0.67, 33.38), (-0.12, 32.8), (-0.23, 32.25), (-0.91, 31.75), (-0.97, 31),
        (-1.88, 30.3), (-2.23, 29.25), (-2.91, 28.75), (-3.23, 27.75), (-3.91, 27.25), (-3.98,
        26.75), (-4.29, 26.37), (-4.48, 25.75), (-4.9, 25.5), (-4.98, 25), (-5.15, 24.88),
        (-5.48, 24), (-5.75, 23.73), (-6.5, 23.68), (-6.88, 23.44), (-8.25, 23.43), (-8.62,
        23.19), (-9.75, 23.18), (-10.12, 22.94), (-11.12, 22.9), (-11.38, 22.69), (-12.25,
        22.68), (-12.62, 22.44), (-14.12, 22.44), (-14.5, 22.31), (-16, 22.31), (-16.25, 22.22),
        (-16.64, 22.38), (-16.55, 22.62), (-16.12, 22.73), (-16, 23.02), (-15.6, 23.25),
        (-15.27, 24.25), (-14.59, 24.75), (-14.27, 25.75), (-13.88, 25.98), (-13.71, 26.25),
        (-13.52, 27), (-10.67, 29.88), (-9.84, 30.5), (-9.52, 33), (-9.12, 33.1), (-7.75,
        34.52), (-7.45, 34.62), (-6.8, 35.5), (-6.38, 35.6), (-6.12, 35.81), (-4.62, 35.81),
        (-4.25, 35.57), (-3.25, 35.52), (-3, 35.32), (-1.75, 35.32), (-1.5, 35.52), (-0.88,
        35.6), (-0.75, 35.77), (-0.12, 35.85), (0, 36.02), (0.62, 36.1), (0.75, 36.27), (1.37,
        36.35), (1.5, 36.52), (2.12, 36.6), (2.25, 36.77), (2.62, 36.85),
    ],
    "Mozambique": [
        (29.59, -9.38), (29.75, -9.25), (32.38, -9.31), (32.75, -9.44), (35, -9.44), (35.38,
        -9.56), (40.25, -9.69), (40.4, -9.75), (40.59, -10.12), (40.35, -10.25), (40.31,
        -11.38), (40.07, -11.75), (40.02, -17), (39.75, -17.27), (39.25, -17.35), (39, -17.77),
        (38.5, -17.85), (38, -18.53), (37.5, -18.57), (37.25, -18.77), (36.75, -18.85), (36.5,
        -19.27), (35.62, -19.48), (35.5, -19.77), (34.95, -20.12), (34.84, -20.25), (34.77,
        -20.75), (34.12, -21.2), (34.02, -21.75), (33.6, -22), (33.52, -22.5), (33.1, -22.75),
        (33.02, -23.25), (32.72, -23.5), (32.62, -24.46), (32.25, -24.27), (32.12, -24.1),
        (31.75, -24.02), (31.5, -23.6), (30.95, -23.5), (30.25, -22.59), (29.5, -22.52), (28.38,
        -21.42), (27.8, -20.62), (27.25, -20.52), (26.88, -20.17), (26.3, -19.38), (25.75,
        -19.27), (25.62, -18.95), (25, -18.52), (24.94, -18.38), (24.94, -17.12), (25.29,
        -16.62), (25.48, -15.75), (25.65, -15.62), (25.73, -15.25), (25.9, -15.12), (25.98,
        -14.5), (26.15, -14.38), (26.19, -13.62), (26.43, -13.25), (26.44, -12.38), (26.65,
        -12.12), (26.73, -11.75), (27.25, -11.65), (27.5, -11.23), (27.88, -11.15), (28.75,
        -10.23), (29.12, -10.05),
    ],
    "Netherlands": [
        (5.32, 54), (5.38, 54.09), (5.5, 54.05), (6.06, 53.38), (6.06, 51.62), (5.75, 51.16),
        (4.38, 51.56), (3.5, 51.56), (3, 51.38), (2.65, 51.62), (3.25, 52.27), (3.62, 52.45),
        (4.2, 53.25), (5.12, 53.6),
    ],
    "New Guinea": [
        (132.94, -0.75), (134, -0.63), (134.5, -0.71), (140.62, -2.34), (145.25, -4.59),
        (147.52, -6), (147.84, -7.5), (150.36, -10.25), (149.38, -10.31), (149, -10.19), (148,
        -10.16), (145.88, -8.46), (144, -7.69), (141, -9), (139.12, -8.21), (138.75, -8.19),
        (138, -8.34), (137.81, -7.5), (137.81, -6.38), (137.62, -5.48), (134.88, -4.34), (133,
        -4.03), (131.84, -2.62), (131.09, -1.25), (131.03, -1),
    ],
    "New Zealand North": [
        (172.73, -34.62), (172.75, -34.55), (172.88, -34.58), (174.45, -36), (175.5, -36.69),
        (176.12, -37.77), (177.12, -37.81), (177.62, -37.69), (178.42, -37.75), (177.79,
        -38.88), (177.06, -39.75), (175.12, -41.43), (175, -41.46), (174.84, -41.12), (174.54,
        -39.75), (174.4, -39.5), (173.75, -39.27), (173.72, -39.12), (174.66, -37), (173,
        -35.18),
    ],
    "New Zealand South": [
        (172.44, -40.62), (172.62, -40.5), (172.75, -40.54), (174.02, -41.12), (174.04, -41.38),
        (173.79, -42.38), (173.62, -42.8), (172.75, -43.81), (171.23, -44.62), (170.62, -46.02),
        (169, -46.62), (166.54, -46), (166.57, -45.88), (168, -44.44), (171.25, -41.94),
    ],
    "Nigeria": [
        (9.23, 19.25), (9.38, 19.31), (9.62, 19.1), (10.25, 19.02), (10.38, 18.85), (10.75,
        18.77), (10.88, 18.6), (11.5, 18.52), (11.62, 18.35), (12.5, 18.02), (12.62, 17.85),
        (13.75, 17.77), (14.06, 17.38), (14.06, 16.38), (13.82, 16), (13.81, 14.38), (13.57,
        14), (13.56, 11.88), (13.32, 11.5), (13.31, 9.38), (13.07, 9), (13.06, 6.62), (12.82,
        6.25), (12.81, 4.12), (12.57, 3.75), (12.56, 1.62), (12.32, 1.25), (12.31, -0.88),
        (12.07, -1.25), (12.03, -2), (11.62, -2.34), (11.38, -1.85), (10.75, -1.77), (10.62,
        -1.6), (10, -1.52), (9.75, -1.32), (9.25, -1.27), (8.98, -1), (8.93, 2), (8.73, 2.25),
        (8.65, 2.62), (8.48, 2.75), (8.4, 3.12), (8.23, 3.25), (8.15, 3.62), (7.88, 3.9), (4.75,
        3.98), (3.62, 5.08), (3.12, 5.8), (2.88, 5.93), (2.62, 5.8), (2, 4.97), (-2, 4.93),
        (-2.15, 4.88), (-2.25, 4.6), (-2.38, 4.57), (-2.5, 4.6), (-2.56, 4.75), (-2.52, 5.25),
        (-2.35, 5.37), (-2.02, 6.25), (-1.42, 6.88), (-0.62, 7.45), (-0.52, 8.25), (0.12, 8.7),
        (0.23, 9.25), (0.88, 9.7), (0.98, 10.25), (1.58, 10.88), (2.38, 11.45), (2.73, 12.5),
        (3.15, 12.88), (3.25, 13.3), (4.12, 13.95), (4.25, 14.55), (5.12, 15.2), (5.23, 15.75),
        (6.75, 17.3), (7.62, 17.95), (7.75, 18.77), (8.38, 18.85), (8.5, 19.02), (9.12, 19.1),
    ],
    "Norway": [
        (23.44, 71), (25.75, 71.12), (27.88, 71.06), (28.25, 70.94), (29.88, 70.81), (31, 70.4),
        (31.22, 70.12), (31, 69.84), (30.62, 69.79), (29.25, 69.21), (29, 69.19), (28.75,
        69.31), (28, 70.03), (27.12, 70.06), (25.75, 69.41), (25.12, 68.96), (24.75, 68.81),
        (22.5, 68.81), (21.5, 69.25), (20.62, 69.19), (19.38, 68.46), (16.5, 67.54), (15.5,
        66.91), (14.62, 66.19), (13.84, 65.38), (13.38, 64.45), (12.46, 63.5), (12.07, 62.5),
        (12.41, 61.62), (12.41, 61.38), (11.96, 60.5), (11.91, 60), (11.55, 59.38), (10.88,
        58.97), (10.73, 59), (10.64, 59.38), (10.5, 59.41), (10.12, 58.97), (9.12, 58.66), (8,
        58.09), (7, 58), (6.12, 58.46), (5.34, 59.12), (5.09, 59.62), (4.94, 60.25), (5.19,
        61.38), (5.03, 62), (5.75, 62.54), (8.88, 63.59), (11.38, 64.96), (13.62, 67.06),
        (15.12, 68.29), (16.62, 68.84), (19, 70.04), (21, 70.54),
    ],
    "Pakistan": [
        (73.48, 33.75), (73.75, 33.81), (74.02, 33.75), (74.12, 32.48), (75.25, 32.27), (76.38,
        31.17), (76.95, 30.38), (77.52, 30.25), (77.6, 29.88), (77.81, 29.62), (77.77, 28.75),
        (77.35, 28.5), (76.8, 27.75), (76.25, 27.65), (76, 27.23), (75.62, 27.15), (75.5,
        26.98), (74.62, 26.78), (74.25, 26.23), (73.88, 26.15), (73.75, 25.98), (72.88, 25.78),
        (72.5, 25.23), (72.12, 25.15), (72, 24.98), (71.08, 24.75), (70.75, 24.23), (70.38,
        24.15), (70.1, 23.88), (70.02, 22.5), (69.5, 21.95), (69.38, 21.91), (69.04, 22.62),
        (68.88, 22.78), (68, 22.98), (67.62, 23.4), (67.25, 23.48), (67.12, 23.65), (66.5,
        23.73), (66, 24.4), (65.5, 24.48), (65.27, 24.88), (65.12, 24.93), (60, 24.94), (59.62,
        24.81), (59.29, 24.88), (59.48, 25.25), (59.65, 25.38), (59.69, 26.38), (59.9, 26.62),
        (59.98, 27.25), (60.15, 27.38), (60.23, 27.75), (60.4, 27.88), (60.5, 28.77), (61.62,
        28.98), (61.75, 29.27), (62.5, 29.35), (62.75, 29.77), (63.37, 29.85), (63.5, 30.02),
        (63.88, 30.1), (64.12, 30.31), (65.38, 30.48), (65.5, 30.77), (66.62, 30.98), (66.75,
        31.27), (67.12, 31.35), (67.25, 31.52), (68.62, 31.73), (68.75, 32.02), (69.88, 32.23),
        (70, 32.52), (70.38, 32.6), (70.5, 32.77), (71.12, 32.85), (71.25, 33.02), (71.88,
        33.1), (72.12, 33.31), (72.88, 33.35), (73, 33.52), (73.38, 33.6),
    ],
    "Paraguay": [
        (-56.96, -15.75), (-56.75, -15.73), (-56.62, -15.9), (-56.25, -15.98), (-56.13, -16.15),
        (-55.5, -16.23), (-55.38, -16.4), (-54.5, -16.73), (-54.38, -16.9), (-53.75, -16.98),
        (-53.62, -17.15), (-53.25, -17.23), (-53.12, -17.4), (-52.75, -17.48), (-52.63, -17.65),
        (-52.25, -17.73), (-52.12, -17.9), (-51.5, -17.98), (-51.38, -18.15), (-50.5, -18.48),
        (-50.38, -18.65), (-49.75, -18.73), (-49.62, -18.9), (-48.75, -19.23), (-48.62, -19.4),
        (-48, -19.48), (-47.88, -19.65), (-47, -19.98), (-46.88, -20.15), (-46.5, -20.23),
        (-46.38, -20.4), (-45.88, -20.44), (-45.62, -20.65), (-45.25, -20.73), (-45.12, -21.02),
        (-44, -21.23), (-43.88, -21.4), (-43.5, -21.48), (-43.38, -21.65), (-43, -21.72),
        (-42.84, -21.88), (-42.88, -22.02), (-43.38, -22.09), (-43.62, -22.23), (-43.73,
        -22.75), (-44.02, -22.88), (-44.5, -23.53), (-44.88, -23.6), (-45, -23.77), (-45.38,
        -23.85), (-45.5, -24.02), (-46.12, -24.1), (-46.25, -24.27), (-46.62, -24.35), (-46.75,
        -24.52), (-47.12, -24.6), (-47.25, -24.77), (-47.62, -24.85), (-47.88, -25.06), (-53.88,
        -25.1), (-54.15, -25.38), (-54.23, -26), (-54.4, -26.12), (-54.48, -26.5), (-54.65,
        -26.62), (-54.73, -27.25), (-54.9, -27.38), (-54.98, -27.75), (-55.15, -27.88), (-55.23,
        -28.5), (-55.4, -28.62), (-55.48, -29), (-55.65, -29.12), (-55.73, -30), (-56.15,
        -30.25), (-56.23, -30.75), (-56.52, -30.88), (-56.62, -31.46), (-57.25, -30.98),
        (-57.62, -30.9), (-57.75, -30.73), (-58.75, -30.68), (-59.12, -30.44), (-59.75, -30.4),
        (-60, -29.98), (-60.38, -29.9), (-60.5, -29.73), (-61.12, -29.65), (-61.25, -29.48),
        (-61.75, -29.43), (-62, -29.23), (-62.62, -29.15), (-62.75, -28.98), (-63.38, -28.9),
        (-63.5, -28.73), (-64.12, -28.65), (-64.25, -28.48), (-64.88, -28.4), (-65.33, -27.88),
        (-66.12, -27.3), (-66.23, -27), (-67.81, -25.38), (-67.62, -25.1), (-67.25, -25.03),
        (-67.12, -24.92), (-66.55, -24.12), (-66.25, -24.02), (-66.12, -23.85), (-65.7, -23.75),
        (-65.05, -22.88), (-64.45, -22.75), (-63.8, -21.88), (-63.5, -21.77), (-63.38, -21.6),
        (-62.95, -21.5), (-62.27, -20.62), (-62, -20.52), (-61.62, -20.1), (-60.95, -20),
        (-60.38, -19.2), (-60, -19.02), (-56.98, -16),
    ],
    "Peru": [
        (-79.89, -1.5), (-79.75, -1.47), (-79.5, -1.77), (-78.88, -1.85), (-78.62, -2.06),
        (-77.25, -2.07), (-76.88, -2.31), (-75.5, -2.32), (-75.12, -2.56), (-73.5, -2.57),
        (-73.12, -2.81), (-71.75, -2.82), (-71.38, -3.06), (-69.75, -3.07), (-69.38, -3.31),
        (-68, -3.32), (-67.62, -3.56), (-66.25, -3.57), (-65.88, -3.81), (-65, -3.82), (-64.75,
        -4.02), (-64.25, -4.1), (-64, -4.52), (-63.6, -4.62), (-63.6, -4.88), (-63.77, -5),
        (-63.88, -5.55), (-64.75, -6.2), (-64.88, -6.8), (-65.52, -7.25), (-65.59, -7.75),
        (-66.27, -8.25), (-66.35, -8.62), (-66.77, -9), (-67.09, -10), (-67.92, -10.62),
        (-68.52, -11.25), (-68.88, -12.3), (-69.75, -12.95), (-70.77, -14), (-70.88, -14.55),
        (-71.67, -15.12), (-72.02, -15.5), (-72.1, -15.88), (-72.52, -16.25), (-72.59, -16.88),
        (-72.75, -17.05), (-72.88, -17.09), (-72.98, -16.62), (-73.38, -16.42), (-73.73,
        -15.88), (-74.3, -15.75), (-74.75, -15.1), (-75.25, -15.02), (-75.38, -14.85), (-75.75,
        -14.77), (-75.88, -14.6), (-76.25, -14.52), (-76.38, -14.35), (-77, -14.27), (-80.02,
        -11.25), (-80.2, -10.88), (-81.03, -10.25), (-81.06, -5.88), (-80.85, -5.63), (-80.77,
        -5.25), (-80.6, -5.12), (-80.52, -4.75), (-80.35, -4.62), (-80.27, -4.25), (-80.1,
        -4.12), (-79.96, -3.62), (-79.94, -2.62), (-79.84, -2.38), (-79.94, -2),
    ],
    "Poland": [
        (20.86, 57), (21, 57.03), (21.28, 56.75), (21.35, 55.12), (21.63, 54.85), (22.5, 54.52),
        (22.62, 54.23), (23.02, 54), (23.1, 53.62), (23.27, 53.5), (23.35, 53.12), (23.52, 53),
        (23.6, 52.62), (23.77, 52.5), (23.85, 52.12), (24.06, 51.88), (24.06, 50.38), (23.71,
        49.88), (23.66, 49.38), (23.52, 49.12), (23, 49.02), (22.62, 48.47), (22, 48.32),
        (21.75, 48.52), (21.25, 48.6), (21, 49.02), (19.12, 49.22), (18.75, 49.77), (17.88,
        49.98), (17.75, 50.27), (16.12, 50.44), (15.95, 50.5), (15.75, 50.77), (14.75, 50.85),
        (14.56, 51.62), (14.56, 52.62), (14.43, 53.25), (14.38, 53.4), (13.98, 53.5), (13.78,
        54), (14.12, 54.29), (14.38, 54.07), (14.75, 54.19), (15.25, 54.19), (15.62, 54.56),
        (20, 54.6), (20.25, 55.02), (20.62, 55.1), (20.9, 55.38),
    ],
    "Portugal": [
        (-9.02, 42.12), (-8.25, 42.25), (-7.75, 42.19), (-7, 42.04), (-6.23, 41.62), (-6.34,
        41.25), (-6.91, 40.25), (-6.96, 39.75), (-7.37, 38.88), (-7, 38.25), (-7.09, 38),
        (-7.48, 37.25), (-8.12, 36.94), (-9.02, 37), (-9.07, 38.38), (-9.12, 38.52), (-9.5,
        38.73), (-9.56, 38.88), (-9.54, 39.38), (-8.81, 40.75), (-8.81, 41.25),
    ],
    "Romania": [
        (22.98, 49), (23.5, 49.03), (24.23, 48.12), (24.38, 48.07), (25.75, 48.07), (26, 48.23),
        (27.5, 48.02), (27.77, 47.75), (27.96, 46.88), (28.38, 46.35), (28.75, 46.27), (29,
        46.07), (29.5, 46.02), (29.62, 45.85), (30.05, 45.62), (30.09, 45.5), (29.6, 45.38),
        (29.52, 45), (29.21, 44.62), (29.02, 43.75), (28.73, 43.63), (28.62, 43.04), (28,
        43.23), (27.88, 43.4), (27.5, 43.48), (27.25, 43.68), (26.88, 43.44), (26.5, 43.48),
        (26.38, 43.65), (26.12, 43.69), (25.5, 43.68), (25.12, 43.47), (24.62, 43.6), (24.38,
        43.81), (23.38, 43.82), (23.23, 43.88), (23, 44.27), (21.75, 44.47), (21.5, 44.77),
        (21.12, 44.85), (20.85, 45.12), (20.77, 45.5), (20.6, 45.62), (20.52, 46), (20.36,
        46.12), (20.34, 46.25), (21.17, 46.88), (21.77, 47.5), (21.85, 48.25), (22.62, 48.47),
    ],
    "Sardinia": [
        (8.56, 41.12), (9.13, 41.25), (9.78, 40.5), (9.52, 39.25), (9, 39), (8.38, 39.23),
        (8.32, 39.38), (8.44, 40.12), (8.11, 41),
    ],
    "Saudi Arabia": [
        (47.06, 28.62), (49.12, 28.65), (49.25, 28.2), (49.78, 27.75), (49.85, 27.12), (50.27,
        26.75), (50.45, 26.38), (51.28, 25.75), (51.35, 25), (51.77, 24.75), (51.88, 24.35),
        (54.12, 24.35), (54.25, 24.52), (54.75, 24.6), (55, 25.02), (55.5, 25.1), (55.73, 25.5),
        (56, 25.6), (56.12, 25.84), (56.55, 25.5), (56.59, 25.38), (56.36, 25.25), (56.36,
        25.12), (56.52, 25), (56.6, 24.62), (56.77, 24.5), (56.98, 24.12), (57.5, 24.02),
        (57.62, 23.85), (58, 23.77), (58.38, 23.22), (59.25, 23.03), (59.66, 22.5), (59.72,
        22.25), (59.35, 22), (59.02, 21), (56.5, 18.48), (56.12, 18.3), (55.5, 17.47), (55.12,
        17.4), (55, 17.23), (54.62, 17.15), (54.5, 16.98), (54.12, 16.9), (54, 16.73), (53.62,
        16.65), (53.5, 16.48), (53.12, 16.4), (53, 16.23), (52.37, 16.15), (52.25, 15.98),
        (51.88, 15.9), (51.75, 15.73), (51.38, 15.65), (51.25, 15.48), (50.88, 15.4), (50.75,
        15.23), (50.38, 15.15), (50.25, 14.98), (49.88, 14.9), (49.75, 14.73), (49.38, 14.65),
        (49.25, 14.48), (48.88, 14.4), (48.75, 14.23), (48.38, 14.15), (48.25, 13.98), (47.88,
        13.9), (47.75, 13.73), (47.38, 13.65), (47.25, 13.48), (46.87, 13.4), (46.75, 13.23),
        (46.38, 13.15), (46.25, 12.98), (45.88, 12.9), (45.75, 12.73), (45.38, 12.65), (45.25,
        12.48), (44.88, 12.4), (44.75, 12.23), (44.38, 12.15), (44.12, 11.94), (43.98, 12),
        (43.84, 12.38), (43, 15.8), (42.62, 16.08), (42.05, 16.88), (41.45, 17), (40.8, 17.88),
        (40.2, 18), (39.55, 18.88), (39, 18.98), (38.73, 19.25), (38.55, 19.62), (37.72, 20.25),
        (37.54, 21.38), (37.23, 21.75), (37.15, 22.12), (36.98, 22.25), (36.94, 22.5), (37.1,
        23.38), (37.31, 23.62), (37.32, 25.75), (37.56, 26.12), (37.57, 27.25), (37.77, 27.5),
        (37.85, 27.88), (38.25, 28.06), (39.62, 28.06), (40, 28.19), (41.5, 28.19), (41.88,
        28.31), (43.25, 28.31), (43.62, 28.44), (45, 28.44), (45.38, 28.56),
    ],
    "South Africa": [
        (24.73, -18.25), (24.88, -18.23), (25, -18.52), (25.55, -18.88), (25.75, -19.27), (26.3,
        -19.38), (26.88, -20.17), (27.25, -20.52), (27.8, -20.62), (28.38, -21.42), (29.5,
        -22.52), (30.25, -22.59), (30.95, -23.5), (31.5, -23.6), (31.75, -24.02), (32.12,
        -24.1), (32.59, -24.62), (32.12, -24.85), (31.92, -25.12), (31.09, -25.75), (31.06,
        -26.38), (30.82, -26.75), (30.81, -27.38), (30.57, -27.75), (30.56, -28.38), (30.32,
        -28.75), (30.31, -29.38), (30.1, -29.62), (30.02, -30), (28.5, -31.52), (28.12, -31.7),
        (27.55, -32.5), (26.88, -32.6), (26.75, -32.77), (26.38, -32.85), (26.25, -33.02),
        (25.38, -33.35), (25.25, -33.52), (24.62, -33.6), (24.38, -33.81), (23, -33.82), (22.62,
        -34.06), (20.12, -34.06), (19.73, -33.75), (19.65, -33.25), (19.23, -33), (18.9,
        -32.12), (18.73, -32), (18.65, -31.62), (18.48, -31.5), (18.4, -31.12), (18.23, -31),
        (18.03, -30.25), (17.73, -30), (17.65, -29.38), (17.44, -29.12), (17.43, -28.5), (17.19,
        -28.12), (16.91, -26.75), (16.23, -26.25), (15.65, -24.75), (15.23, -24.5), (14.9,
        -23.62), (14.73, -23.5), (14.62, -23.23), (14.29, -23.12), (14.32, -23), (14.5, -22.73),
        (15.62, -22.52), (15.75, -22.23), (16.25, -22.18), (16.5, -21.98), (17, -21.9), (17.25,
        -21.48), (18.62, -21.27), (18.73, -21), (19, -20.73), (19.38, -20.65), (19.5, -20.48),
        (20.5, -20.4), (20.75, -19.98), (21.62, -19.65), (21.75, -19.48), (22.62, -19.43),
        (22.77, -19.38), (23, -18.98), (24.12, -18.77), (24.25, -18.48), (24.62, -18.4),
    ],
    "Spain": [
        (-2.15, 43.88), (-1.88, 43.9), (-1.75, 43.45), (-1.25, 43.09), (-0.62, 42.94), (0.5,
        42.94), (1.38, 42.79), (2, 42.44), (3, 42.5), (3.29, 42.38), (2.62, 41.8), (2.38,
        41.16), (2.12, 41.4), (1.88, 41.41), (1.25, 41.16), (0.56, 40.5), (-0.28, 39.5), (-0.46,
        38.38), (-0.84, 37.75), (-1.12, 37.46), (-2.25, 36.75), (-4.38, 36.79), (-5.62, 36),
        (-6.38, 36.48), (-6.5, 36.9), (-7.12, 37.09), (-7.38, 37.23), (-7.41, 37.38), (-7,
        38.25), (-7.37, 38.87), (-6.96, 39.75), (-6.91, 40.25), (-6.34, 41.25), (-6.23, 41.62),
        (-7, 42.04), (-8.25, 42.25), (-9, 42.22), (-9.16, 42.38), (-9.41, 43), (-9, 43.41),
        (-7.75, 43.75), (-6.12, 43.69), (-5.75, 43.56), (-2.5, 43.56), (-2.25, 43.6),
    ],
    "Sri Lanka": [
        (79.7, 9.38), (79.75, 9.47), (80, 9.41), (81.5, 8.4), (81.66, 8.12), (81.91, 7), (80.88,
        5.97), (80, 5.98), (79.84, 6.38), (79.56, 7.5),
    ],
    "Sudan": [
        (22.19, 19.88), (22.5, 19.94), (33.88, 19.9), (33.93, 19.75), (33.81, 19.38), (33.82,
        18.75), (34.02, 18.5), (34.1, 17.88), (36.27, 15.75), (36.45, 15.38), (37.38, 14.71),
        (37.64, 14.62), (37.62, 14.46), (37.12, 14.17), (36.55, 13.38), (36.23, 13.25), (36.04,
        12.5), (35.88, 12.23), (35.48, 12), (35.15, 11), (34.73, 10.75), (34.4, 9.75), (33.98,
        9.5), (33.65, 8.5), (33.23, 8.25), (32.9, 7.25), (32.48, 7), (32.15, 6), (31.75, 5.77),
        (31.62, 5.53), (31.38, 5.35), (31, 5.27), (30.75, 5.07), (30.25, 5.02), (30.15, 4.75),
        (30, 4.69), (29.38, 4.56), (28.62, 4.56), (28, 4.72), (27.75, 5.02), (27.12, 5.1),
        (26.73, 5.5), (26.4, 6.38), (26.23, 6.5), (26.15, 6.88), (25.98, 7), (25.66, 8), (24.75,
        8.7), (24.41, 10), (23.47, 10.75), (23.4, 11.12), (23.23, 11.25), (23.15, 11.62),
        (22.98, 11.75), (22.84, 12.12), (22.66, 13), (21.98, 13.5), (21.9, 13.88), (21.48,
        14.25), (21.4, 14.75), (20.98, 15), (20.9, 15.62), (20.73, 15.75), (20.62, 16.02),
        (20.23, 16.25), (20.12, 16.8), (19.48, 17.25), (19.48, 17.75), (19.88, 17.95), (20.45,
        18.75), (21, 18.84), (21.7, 19.75),
    ],
    "Sulawesi": [
        (123.69, 1.38), (124.75, 1.47), (124.97, 1), (123.12, 0.53), (121.94, -0.62), (121.79,
        -0.88), (123, -0.94), (123.15, -1), (123.18, -1.12), (123.06, -3), (122.66, -4.62),
        (122.5, -4.97), (121.12, -4.57), (120.98, -4.62), (120.38, -5.53), (119.5, -5.52),
        (119.44, -5.25), (119.69, -3.88), (119.56, -1.38), (119.44, -1), (119.46, -0.5),
        (119.59, -0.25), (120.5, 1.03), (121.38, 1.06), (121.75, 1.19),
    ],
    "Sumatra": [
        (95.33, 5.5), (96.25, 5.56), (96.62, 5.44), (97.5, 5.41), (98.56, 4), (100.38, 2.06),
        (103.05, 0.5), (104.56, -1), (106.03, -3), (105.94, -4.88), (105.75, -5.77), (104.5,
        -5.87), (104.38, -5.81), (102.06, -3.88), (100.34, -1.62), (98.75, 0.8), (96.84, 3),
        (95.71, 4.75),
    ],
    "Sweden": [
        (20.2, 69), (20.75, 69.04), (21.12, 68.84), (22.5, 68.44), (23.16, 67.62), (23.46, 67),
        (23.91, 66.5), (24.06, 66), (24.02, 65.5), (23.75, 65.48), (23.65, 65.75), (23.5,
        65.81), (22.12, 65.66), (20.88, 64.31), (20.25, 63.84), (18.5, 62.96), (17.38, 62.52),
        (17.19, 61.5), (17.23, 60.75), (18.62, 60.02), (18.77, 59.5), (18.12, 59.41), (17.12,
        58.71), (16.6, 58.5), (16.56, 57.88), (16.69, 57.12), (16.38, 56.71), (14.25, 55.59),
        (13.62, 55.44), (13, 55.48), (12.79, 56), (12.34, 56.5), (11.79, 57.75), (11.21, 58.5),
        (11.15, 58.75), (10.84, 58.88), (11.66, 59.5), (11.91, 60), (11.96, 60.5), (12.41,
        61.38), (12.41, 61.62), (12.07, 62.5), (12.46, 63.5), (13.38, 64.45), (13.94, 65.5),
        (15.5, 66.91), (16.5, 67.54), (19.38, 68.46),
    ],
    "Syria": [
        (45.6, 42.75), (46, 42.77), (46.25, 42.35), (46.75, 42.27), (46.77, 41.75), (46.42,
        41.38), (45.62, 40.8), (45.52, 40.25), (44.88, 39.8), (44.77, 39.25), (44.5, 38.95),
        (43.62, 38.3), (43.52, 37.75), (43.1, 37.5), (43.02, 37), (42.71, 36.62), (42.52, 36),
        (42.1, 35.62), (42.02, 35.25), (41.34, 34.75), (41.03, 33.5), (40.09, 32.75), (39.77,
        31.5), (39.6, 31.38), (39.52, 31), (39.35, 30.88), (39.02, 30), (38.71, 29.62), (38.66,
        29.12), (38.52, 28.75), (38.35, 28.62), (38.27, 28.25), (38, 27.98), (37.25, 27.98),
        (36.88, 28.33), (36.3, 29.12), (35.7, 29.25), (35, 30.16), (34.5, 30.23), (34.38,
        30.52), (33.5, 30.73), (33.25, 31.15), (32.48, 31.25), (32.48, 32), (32.9, 32.38),
        (32.98, 32.75), (33.4, 33), (33.73, 34), (34.58, 34.88), (35.29, 35.38), (35.34, 35.5),
        (35.12, 35.6), (35.07, 35.75), (35.12, 36.15), (35.5, 36.23), (35.73, 36.62), (36,
        36.73), (36.12, 36.9), (36.55, 37), (37.25, 37.91), (37.8, 38), (38.25, 38.65), (39,
        38.73), (39.12, 38.9), (39.5, 38.98), (39.62, 39.15), (40, 39.23), (40.12, 39.4), (40.5,
        39.47), (41.08, 40.25), (42.25, 40.47), (42.88, 41.28), (44, 41.48), (44.12, 41.65),
        (44.5, 41.73), (44.62, 41.9), (45.5, 42.23),
    ],
    "Taiwan": [
        (121.69, 25.25), (122, 25.37), (122.42, 25.12), (122.53, 24.88), (122.04, 23), (121.54,
        22.12), (121.38, 22), (121.06, 22.25), (120.59, 22.88), (120.44, 23.88), (121.12, 24.92),
    ],
    "Tasmania": [
        (144.58, -40.75), (146.25, -40.69), (146.62, -40.81), (148.25, -40.85), (148.28,
        -42.12), (147.56, -43), (147, -43.5), (145.38, -42.42),
    ],
    "Thailand": [
        (101.9, 20.88), (102, 20.98), (102.12, 20.96), (102.52, 20.75), (102.6, 20.12), (102.81,
        19.88), (102.96, 18.12), (103.1, 17.62), (103.31, 17.38), (103.35, 16.62), (103.56,
        16.38), (103.57, 15.5), (103.81, 15.12), (103.96, 13.38), (104.1, 12.88), (104.31,
        12.62), (104.57, 10.75), (104.81, 10.38), (104.82, 9.5), (105.06, 9.12), (105.09, 8.12),
        (105.34, 7.75), (104.88, 7.66), (104.38, 7.3), (104.27, 6.75), (103.85, 6.5), (103.75,
        5.95), (102.95, 5.38), (102.84, 5.25), (102.77, 4.75), (102.48, 4.62), (102.25, 4.23),
        (102, 4.19), (101.73, 4.25), (101.15, 5.75), (100.73, 6), (100.4, 6.88), (100.23, 7),
        (100.15, 7.62), (99.98, 7.75), (99.65, 8.62), (99.48, 8.75), (99.4, 9.12), (99.23,
        9.25), (99.15, 9.62), (98.98, 9.75), (98.9, 10.12), (98.73, 10.25), (98.65, 10.62),
        (98.48, 10.75), (98.28, 11.5), (95.98, 13.75), (95.8, 14.12), (95, 14.7), (94.88,
        15.15), (94.38, 15.23), (94.36, 15.38), (94.62, 15.54), (95.05, 15.62), (95.7, 16.5),
        (96.3, 16.62), (96.95, 17.5), (97.5, 17.6), (98, 18.28), (98.62, 18.35), (98.75, 18.52),
        (99.05, 18.62), (99.62, 19.42), (100.55, 19.88), (101.2, 20.75),
    ],
    "Turkey": [
        (41.23, 44.25), (42.88, 44.31), (43.12, 44.1), (43.75, 44.02), (43.88, 43.85), (44.25,
        43.77), (44.5, 43.35), (45, 43.27), (45.12, 42.98), (45.5, 42.77), (45.56, 42.5), (45.5,
        42.23), (44.62, 41.9), (44.5, 41.73), (44.12, 41.65), (44, 41.48), (42.88, 41.28),
        (42.25, 40.47), (41.08, 40.25), (40.5, 39.47), (40.12, 39.4), (40, 39.23), (39.12,
        38.9), (39, 38.73), (38.25, 38.65), (37.8, 38), (37.25, 37.91), (36.55, 37), (36.12,
        36.9), (36, 36.73), (35.73, 36.62), (35.5, 36.23), (35.12, 36.15), (35, 35.6), (34.75,
        35.6), (34.65, 35.87), (34.5, 35.93), (28.23, 36), (28.03, 36.38), (28.28, 36.75),
        (28.44, 37.5), (28.44, 38.25), (28.56, 38.62), (28.56, 39.38), (28.69, 39.75), (28.69,
        40.5), (28.88, 41.65), (29.12, 41.65), (29.23, 41.37), (29.38, 41.32), (30.62, 41.31),
        (30.88, 41.19), (31.12, 41.31), (32.12, 41.48), (32.25, 41.77), (32.62, 41.85), (32.88,
        42.06), (35.38, 42.06), (35.62, 41.85), (36.25, 41.77), (36.38, 41.6), (37, 41.52),
        (37.12, 41.35), (38.12, 41.31), (38.5, 41.07), (41, 41.19), (41.15, 41.25), (41.23,
        41.5), (41.4, 41.62), (41.48, 42), (41.65, 42.12), (41.65, 42.38), (41.25, 42.48), (41,
        42.9), (40.5, 42.98), (40.25, 43.35), (39.54, 43.38), (40, 44.02), (41, 44.07),
    ],
    "USA": [
        (-95.02, 49.25), (-94.12, 49.31), (-93.75, 49.07), (-92.88, 49.06), (-92.5, 48.82),
        (-91.62, 48.81), (-91.25, 48.57), (-90.38, 48.56), (-90, 48.32), (-89.12, 48.31),
        (-88.75, 48.07), (-87.88, 48.06), (-87.5, 47.82), (-86.62, 47.81), (-86.25, 47.57),
        (-85.38, 47.56), (-85, 47.19), (-83, 47.02), (-82.12, 46.17), (-81.55, 45.38), (-81,
        45.27), (-80.12, 44.42), (-79.5, 43.59), (-79.12, 43.81), (-77.75, 43.82), (-77.38,
        44.06), (-76, 44.07), (-75.62, 44.31), (-74.75, 44.32), (-74.38, 44.56), (-73.5, 44.57),
        (-73.25, 44.77), (-72.25, 44.82), (-71.88, 45.06), (-70.88, 45.06), (-70.62, 44.85),
        (-70.25, 44.82), (-70, 45.02), (-69.5, 45.1), (-69, 45.78), (-68, 45.82), (-67.62,
        46.06), (-67, 46.02), (-66.88, 45.85), (-66.5, 45.77), (-66.25, 45.35), (-65.75, 45.27),
        (-65.48, 45), (-65.5, 43.85), (-66.38, 43.94), (-66.75, 43.81), (-67.25, 43.81), (-67.4,
        43.75), (-67.5, 43.48), (-68.38, 43.4), (-69.08, 42.62), (-69.91, 42), (-70, 40.98),
        (-70.75, 40.93), (-71.12, 40.69), (-72.75, 40.68), (-73.12, 40.44), (-73.88, 40.4),
        (-74, 40.23), (-74.4, 40), (-74.48, 39.5), (-74.9, 39.25), (-74.98, 38.75), (-75.15,
        38.62), (-75.23, 38.25), (-75.4, 38.12), (-75.48, 37.75), (-75.68, 37.5), (-75.68,
        36.25), (-75.44, 35.88), (-75.48, 35), (-75.77, 34.88), (-76, 34.48), (-76.5, 34.4),
        (-76.75, 33.98), (-77.62, 33.78), (-78, 33.23), (-78.5, 33.15), (-78.95, 32.5), (-79.38,
        32.4), (-80.08, 31.62), (-80.91, 31), (-80.93, 30.5), (-80.69, 30.12), (-80.68, 29),
        (-80.44, 28.62), (-80.43, 27.5), (-80.19, 27.12), (-79.94, 25.75), (-79.98, 25.5),
        (-80.25, 25.23), (-80.62, 25.15), (-80.75, 24.98), (-81.25, 24.93), (-81.5, 24.77),
        (-82.02, 25), (-82.1, 25.62), (-82.31, 25.88), (-82.32, 26.5), (-82.56, 26.88), (-82.57,
        27.5), (-82.77, 27.75), (-82.96, 28.62), (-83.12, 28.9), (-83.5, 28.98), (-83.75,
        29.18), (-84.5, 29.23), (-84.75, 29.43), (-85.38, 29.44), (-85.75, 29.68), (-86.62,
        29.69), (-87, 29.93), (-90, 29.93), (-90.38, 29.69), (-92.5, 29.68), (-92.88, 29.44),
        (-93.88, 29.4), (-94.58, 28.62), (-95.38, 28.05), (-95.48, 27.5), (-96, 26.95), (-96.77,
        26.37), (-96.77, 26.25), (-96.6, 26.12), (-96.6, 25.88), (-97, 25.82), (-97.15, 25.88),
        (-97.25, 26.27), (-97.8, 26.38), (-98.38, 27.17), (-98.75, 27.52), (-99.38, 27.6),
        (-99.5, 27.77), (-100.12, 27.85), (-100.25, 28.02), (-100.88, 28.1), (-101, 28.27),
        (-101.62, 28.35), (-101.75, 28.52), (-102.38, 28.6), (-102.62, 28.81), (-103.25, 28.82),
        (-103.62, 29.06), (-104.62, 29.22), (-105.12, 29.92), (-105.4, 30.12), (-105.5, 30.55),
        (-106.25, 31.1), (-106.48, 31.5), (-106.62, 31.56), (-107.88, 31.56), (-108.25, 31.32),
        (-111.5, 31.32), (-111.75, 31.52), (-112.38, 31.6), (-112.62, 31.81), (-113.62, 31.81),
        (-113.88, 31.6), (-114.5, 31.52), (-114.62, 31.2), (-114.88, 31.04), (-115, 31.27),
        (-115.25, 31.28), (-115.38, 31.52), (-116.75, 31.73), (-116.88, 32.02), (-117.27,
        32.25), (-117.35, 32.62), (-119.38, 34.58), (-119.95, 35.38), (-120.5, 35.48), (-120.75,
        35.9), (-121.25, 35.98), (-121.45, 36.38), (-122.02, 36.75), (-122.1, 37.25), (-122.52,
        37.5), (-122.6, 38), (-123.02, 38.25), (-123.1, 38.62), (-123.52, 39), (-123.6, 39.5),
        (-124.02, 39.75), (-124.07, 42.5), (-124.31, 42.88), (-124.32, 45.25), (-124.56, 45.62),
        (-124.57, 47.5), (-124.77, 47.75), (-124.81, 48), (-124.77, 48.5), (-124.12, 48.61),
        (-124.12, 49.02), (-123.62, 48.94), (-123.12, 49.06), (-95.38, 49.06), (-95.12, 49.1),
    ],
    "USSR": [
        (127.48, 75), (127.75, 75.06), (130.25, 75.02), (130.38, 74.85), (130.75, 74.77),
        (130.88, 74.6), (131.25, 74.52), (131.38, 74.35), (131.75, 74.27), (131.88, 74.1),
        (132.5, 74.02), (132.62, 73.85), (133, 73.77), (133.12, 73.6), (133.5, 73.52), (133.62,
        73.35), (134, 73.27), (134.12, 73.1), (134.5, 73.02), (134.62, 72.85), (135, 72.77),
        (135.12, 72.6), (135.5, 72.52), (135.62, 72.35), (136.25, 72.27), (136.38, 72.1),
        (136.75, 72.02), (136.88, 71.85), (137.25, 71.77), (137.38, 71.6), (138.25, 71.27),
        (138.38, 71.1), (138.75, 71.02), (138.88, 70.85), (139.25, 70.77), (139.38, 70.6), (140,
        70.52), (140.12, 70.35), (140.5, 70.27), (140.62, 70.1), (141.5, 69.77), (141.62, 69.6),
        (142, 69.52), (142.12, 69.35), (142.5, 69.27), (142.62, 69.1), (143, 69.02), (143.12,
        68.85), (143.75, 68.77), (143.87, 68.6), (144.75, 68.27), (144.88, 68.1), (145.25,
        68.02), (145.37, 67.85), (146, 67.77), (146.12, 67.6), (146.5, 67.52), (146.62, 67.35),
        (147.25, 67.27), (147.38, 67.1), (147.75, 67.02), (147.88, 66.85), (148.5, 66.77),
        (148.62, 66.6), (149, 66.52), (149.12, 66.35), (149.75, 66.27), (149.88, 66.1), (150.25,
        66.02), (150.38, 65.85), (151, 65.77), (151.12, 65.6), (151.5, 65.52), (151.62, 65.35),
        (152.25, 65.27), (152.38, 65.1), (152.75, 65.02), (152.88, 64.85), (153.5, 64.77),
        (153.62, 64.6), (154, 64.52), (154.12, 64.35), (154.75, 64.27), (154.87, 64.1), (155.25,
        64.02), (155.38, 63.85), (156, 63.77), (156.12, 63.6), (156.5, 63.52), (156.62, 63.35),
        (157.25, 63.27), (157.38, 62.98), (158.5, 62.77), (158.62, 62.48), (159.75, 62.27),
        (160, 62.07), (160.88, 62.23), (161, 62.52), (161.38, 62.6), (161.5, 62.77), (162.12,
        62.85), (162.25, 63.02), (162.62, 63.1), (162.75, 63.27), (163.38, 63.35), (163.5,
        63.52), (163.88, 63.6), (164, 63.77), (164.62, 63.85), (164.75, 64.02), (165.12, 64.1),
        (165.25, 64.27), (165.87, 64.35), (166, 64.52), (166.38, 64.6), (166.5, 64.77), (167.12,
        64.85), (167.25, 65.02), (167.62, 65.1), (167.75, 65.27), (168.38, 65.35), (168.5,
        65.52), (168.88, 65.6), (169, 65.77), (170.38, 65.98), (170.48, 66.25), (170.62, 66.31),
        (171.5, 66.32), (171.75, 66.52), (172.5, 66.57), (172.88, 66.81), (173.75, 66.82),
        (174.12, 67.06), (174.75, 67.07), (175.12, 67.31), (176, 67.32), (176.38, 67.56), (177,
        67.57), (177.38, 67.81), (178.25, 67.82), (178.62, 68.06), (179, 68.02), (179.06,
        67.88), (179.06, 60.25), (179, 59.98), (178, 59.93), (177.62, 59.69), (175.75, 59.68),
        (175.38, 59.44), (173.25, 59.43), (172.88, 59.19), (171, 59.18), (170.62, 58.94),
        (168.5, 58.93), (168.12, 58.69), (166.25, 58.68), (165.88, 58.44), (163.75, 58.43),
        (163.38, 58.19), (161.5, 58.18), (161.12, 57.94), (160, 57.93), (159.75, 57.73),
        (159.12, 57.65), (159, 57.48), (158.38, 57.4), (158.25, 57.23), (157.62, 57.15),
        (157.38, 56.94), (156.12, 56.77), (156, 56.48), (155.62, 56.4), (155.5, 56.23), (154.87,
        56.15), (154.75, 55.98), (154.12, 55.9), (154, 55.73), (153.38, 55.65), (153.25, 55.48),
        (151.88, 55.27), (151.75, 54.98), (151.38, 54.9), (151.25, 54.73), (150.62, 54.65),
        (150.5, 54.48), (149.88, 54.4), (149.75, 54.23), (149.12, 54.15), (148.88, 53.94),
        (147.62, 53.77), (147.5, 53.48), (147.12, 53.4), (147, 53.23), (146.38, 53.15), (146.25,
        52.98), (145.62, 52.9), (145.5, 52.73), (144.88, 52.65), (144.62, 52.44), (143.38,
        52.27), (143.27, 52), (141.92, 50.62), (141.12, 50.05), (141.02, 49.5), (139.92, 48.38),
        (139.12, 47.8), (139.02, 47.25), (137.92, 46.12), (137.12, 45.55), (137.02, 45), (136,
        43.98), (135.62, 43.8), (135.05, 43), (134.62, 42.9), (134.38, 42.69), (133.62, 42.65),
        (133.38, 42.44), (132.62, 42.4), (132.38, 42.19), (131.62, 42.15), (131.5, 41.98),
        (131.1, 41.88), (130.96, 41.62), (130.88, 41.04), (130.25, 41.52), (129.12, 41.73),
        (129.02, 42), (128.88, 42.06), (124.88, 42.06), (124.62, 41.85), (124.12, 41.81),
        (123.88, 41.6), (123.5, 41.52), (123, 41.07), (119.88, 41.48), (119.75, 41.8), (119,
        42.35), (118.75, 42.77), (118.25, 42.85), (118, 43.27), (117.12, 43.48), (117, 43.77),
        (116.12, 44.1), (116, 44.27), (114.88, 44.47), (114.25, 45.28), (113.38, 45.48),
        (113.25, 45.77), (112.38, 46.1), (112.25, 46.27), (111.12, 46.47), (110.5, 47.28),
        (109.62, 47.48), (109.5, 47.77), (108.62, 48.1), (108.5, 48.27), (107.88, 48.35),
        (107.75, 48.52), (107.38, 48.6), (107.25, 48.77), (106.75, 48.85), (106.3, 49.5),
        (105.88, 49.6), (105.62, 49.81), (102.75, 49.98), (102.5, 49.82), (98.38, 49.81), (98,
        49.44), (91.12, 49.31), (90.75, 49.07), (85.88, 49.06), (85.62, 49.1), (85.38, 49.31),
        (82.75, 49.32), (82.38, 49.56), (79.75, 49.57), (79.38, 49.81), (77.25, 49.81), (76.88,
        49.94), (74.62, 49.97), (73.5, 51.27), (72.62, 51.47), (71.8, 52.5), (70.88, 52.72),
        (70.05, 53.75), (69.5, 53.85), (69.25, 54.27), (68.5, 54.35), (68.25, 54.77), (68,
        54.81), (67.5, 54.77), (67.38, 54.6), (66.5, 54.27), (66.25, 53.85), (65.75, 53.77),
        (65.38, 53.22), (64.5, 53.03), (63.62, 51.97), (62.5, 51.78), (61.62, 50.72), (60.5,
        50.53), (59.88, 49.72), (58.62, 49.56), (58.38, 49.35), (57.75, 49.27), (57.62, 49.1),
        (57.25, 49.02), (57.12, 48.73), (56, 48.52), (55.75, 48.32), (55.25, 48.27), (55,
        47.85), (54, 47.78), (53.3, 46.88), (52.78, 46.75), (52.78, 46.25), (52.62, 46.09),
        (52.5, 46.11), (52.3, 46.38), (52.12, 46.44), (51.25, 46.43), (51, 46.23), (50.38,
        46.15), (50.17, 45.88), (49.38, 45.3), (49.27, 44.75), (48.62, 44.3), (48.52, 43.75),
        (47.96, 43.38), (47.91, 43.25), (48.24, 43.12), (47.73, 42.75), (47.5, 42.35), (46.88,
        42.25), (46.38, 42.32), (46.23, 42.38), (46, 42.77), (45.38, 42.84), (45.1, 43), (45,
        43.27), (44.5, 43.35), (44.25, 43.77), (43.88, 43.85), (43.62, 44.06), (43.12, 44.1),
        (42.88, 44.31), (41.38, 44.31), (41, 44.07), (40.12, 44.06), (39.98, 44), (39.75, 43.6),
        (39.38, 43.41), (39.15, 43.88), (38.75, 43.98), (38.62, 44.15), (38.25, 44.18), (37.88,
        43.94), (37.62, 44.15), (37, 44.23), (36.88, 44.4), (36.25, 44.48), (36, 44.68), (33.25,
        44.52), (32.88, 44.83), (32.5, 45.4), (32, 45.48), (31.88, 45.65), (30.88, 45.69),
        (30.5, 45.93), (30.25, 45.9), (30.12, 45.66), (29.62, 45.85), (29.5, 46.02), (29,
        46.07), (28.75, 46.27), (28.38, 46.35), (27.96, 46.88), (27.77, 47.75), (27.5, 48.02),
        (26, 48.23), (25.75, 48.07), (24.25, 48.1), (23.71, 48.75), (23.57, 49.12), (23.71,
        49.88), (24.06, 50.38), (24.02, 52), (23.85, 52.12), (23.77, 52.5), (23.6, 52.62),
        (23.52, 53), (23.35, 53.12), (23.02, 54), (22.62, 54.23), (22.5, 54.52), (21.62, 54.85),
        (21.35, 55.12), (21.31, 56.62), (20.96, 57.12), (21.62, 57.56), (22.38, 57.56), (22.75,
        57.32), (23.88, 57.35), (24.18, 57.75), (24.12, 57.9), (23.75, 57.98), (23.48, 58.25),
        (23.5, 59.27), (24.75, 59.32), (25.12, 59.56), (28.12, 59.6), (28.25, 59.77), (28.62,
        59.85), (28.85, 60.12), (28.75, 60.39), (28.45, 60.38), (28.5, 60.65), (29.5, 61.1),
        (29.73, 61.5), (30.25, 61.91), (31.52, 62.38), (31.52, 63), (30.38, 63.59), (30.09,
        63.88), (30.07, 64.12), (30.25, 64.88), (29.94, 65.38), (30.04, 66.62), (29.79, 67.5),
        (29.22, 68), (29.16, 68.5), (28.97, 69), (29, 69.14), (30.62, 69.79), (31, 69.84),
        (31.38, 70.09), (31.5, 69.85), (32, 69.57), (32.88, 69.56), (33.25, 69.32), (34.12,
        69.31), (34.5, 69.07), (35.38, 69.06), (35.75, 68.82), (36.62, 68.81), (37, 68.57),
        (37.88, 68.56), (38.25, 68.32), (39.25, 68.27), (39.5, 68.07), (50.25, 68.07), (50.62,
        68.31), (51.5, 68.32), (51.88, 68.56), (52.75, 68.57), (53.12, 68.81), (54, 68.82),
        (54.38, 69.06), (55.25, 69.07), (55.62, 69.31), (56.5, 69.32), (56.88, 69.56), (57.75,
        69.57), (58, 69.77), (59, 69.82), (59.38, 70.06), (60.75, 70.07), (61.12, 70.31), (62.5,
        70.32), (62.88, 70.56), (64.5, 70.57), (64.88, 70.81), (66.25, 70.82), (66.62, 71.06),
        (68.25, 71.07), (68.62, 71.31), (70, 71.32), (70.38, 71.56), (72, 71.57), (72.38,
        71.81), (73.75, 71.82), (74.12, 72.06), (80.25, 72.19), (80.62, 72.56), (84, 72.57),
        (84.38, 72.81), (87.75, 72.82), (88.12, 73.06), (92.25, 73.07), (92.62, 73.31), (97.25,
        73.32), (97.62, 73.56), (102.25, 73.57), (102.62, 73.81), (107.25, 73.82), (107.62,
        74.06), (112.25, 74.07), (112.62, 74.31), (117.25, 74.32), (117.62, 74.56), (127.25,
        74.69), (127.4, 74.75),
    ],
    "Venezuela": [
        (-72.4, 11.38), (-72.12, 11.4), (-72, 11.23), (-71.38, 11.06), (-70.12, 11.06), (-69.88,
        10.85), (-69.25, 10.77), (-69.12, 10.6), (-68.5, 10.52), (-68.25, 10.32), (-67.62,
        10.31), (-67.38, 10.1), (-66.62, 10.06), (-66.25, 9.82), (-65.38, 9.81), (-65, 9.57),
        (-64.12, 9.56), (-63.75, 9.32), (-62.88, 9.31), (-62.5, 8.94), (-61, 8.77), (-60.88,
        8.6), (-60.48, 8.5), (-58.88, 6.92), (-58.3, 6.12), (-57.7, 6), (-57.05, 5.12), (-56.25,
        5.02), (-55.12, 3.92), (-54.55, 3.12), (-53.75, 3.17), (-53.66, 3.12), (-53.7, 3), (-54,
        2.71), (-54.37, 2.55), (-54.95, 1.75), (-55.55, 1.62), (-56.2, 0.75), (-56.8, 0.62),
        (-57.45, -0.25), (-58.05, -0.38), (-58.7, -1.25), (-59.3, -1.38), (-59.95, -2.25),
        (-60.62, -2.35), (-61.75, -3.52), (-62.12, -3.7), (-62.7, -4.5), (-63.12, -4.6),
        (-63.25, -4.77), (-63.5, -4.77), (-63.62, -4.6), (-64, -4.52), (-64.25, -4.1), (-64.75,
        -4.02), (-64.91, -3.75), (-65.23, -2.75), (-65.4, -2.62), (-65.48, -2.25), (-65.65,
        -2.12), (-65.73, -1.75), (-65.9, -1.62), (-66.23, -0.75), (-66.4, -0.62), (-66.48,
        -0.25), (-66.65, -0.12), (-66.98, 0.75), (-67.15, 0.88), (-67.23, 1.25), (-67.4, 1.38),
        (-67.48, 1.75), (-67.65, 1.88), (-67.73, 2.25), (-67.9, 2.38), (-67.98, 2.75), (-68.15,
        2.88), (-68.23, 3.25), (-68.4, 3.38), (-68.48, 4), (-68.65, 4.12), (-68.73, 4.5),
        (-68.9, 4.62), (-68.98, 5), (-69.15, 5.12), (-69.23, 5.5), (-69.4, 5.62), (-69.48, 6),
        (-69.65, 6.12), (-69.73, 6.5), (-69.9, 6.62), (-69.98, 7), (-70.15, 7.12), (-70.23,
        7.5), (-70.4, 7.62), (-70.48, 8), (-70.65, 8.12), (-70.73, 8.5), (-70.9, 8.62), (-70.98,
        9), (-71.15, 9.12), (-71.23, 9.5), (-71.4, 9.62), (-71.73, 10.5), (-72, 10.77), (-72.4,
        10.88),
    ],
    "Yugoslavia": [
        (21.1, 47.88), (21.75, 47.9), (21.81, 47.62), (21.17, 46.88), (20.34, 46.25), (20.36,
        46.12), (20.52, 46), (20.6, 45.62), (20.77, 45.5), (20.85, 45.12), (21.12, 44.85),
        (21.5, 44.77), (21.75, 44.47), (23, 44.27), (23.25, 43.85), (24.5, 43.77), (24.62,
        43.6), (25.02, 43.5), (25, 43.23), (24.38, 43.15), (24.25, 42.98), (23.62, 42.9),
        (23.38, 42.69), (21.88, 42.52), (21.75, 42.23), (21.25, 42.18), (21, 41.98), (20.38,
        41.9), (20.25, 41.73), (19.25, 41.53), (18.88, 41.16), (18.75, 41.9), (18, 41.97),
        (17.5, 42.65), (16.95, 42.75), (16.5, 43.4), (16, 43.48), (15.75, 43.9), (15.25, 43.98),
        (15, 44.41), (14.29, 44.62), (14.62, 45.15), (15, 45.23), (15.12, 45.4), (15.62, 45.48),
        (15.75, 45.65), (16.25, 45.73), (16.38, 45.9), (16.75, 45.98), (16.88, 46.15), (17.25,
        46.23), (17.38, 46.4), (17.75, 46.48), (17.88, 46.65), (18.75, 46.98), (18.88, 47.27),
        (20.12, 47.44), (20.38, 47.65), (21, 47.73),
    ],
}
NEW_MINOR_COUNTRIES = ['Denmark', 'Portugal', 'Ireland', 'Iceland', 'Greenland', 'Sardinia', 'Cuba', 'Hispaniola', 'Madagascar', 'Sri Lanka', 'Taiwan', 'Luzon', 'Mindanao', 'Sumatra', 'Java', 'Borneo', 'Sulawesi', 'New Guinea', 'New Zealand North', 'New Zealand South', 'Tasmania']
MINOR_SINGLE_ZONE = {'Ireland', 'Tasmania', 'Taiwan', 'Hispaniola', 'Sri Lanka', 'Sardinia'}      # tiny islands: one Center zone only
for _n in NEW_MINOR_COUNTRIES:
    FILLER_OUTLINES[_n] = REBUILT_OUTLINES[_n]
COUNTRY_OUTLINES.update(FILLER_OUTLINES)
COUNTRY_OUTLINES.update(REBUILT_OUTLINES)
MINOR_COUNTRIES = set(FILLER_OUTLINES)
SINGLE_ZONE_COUNTRIES = set(SMALL_COUNTRY_BOX) | MINOR_SINGLE_ZONE   # one Center zone only
REGION.update({'Denmark': 'Eurasia', 'Portugal': 'Eurasia'})   # the rest are islands
MINOR_GREY = "#c4c9ce"        # unplayable countries are greyed out until someone occupies them
MINOR_TEXT = "#5f6b76"

# zone colours: blue = only Allied troops, red = only Axis troops
ZONE_COLORS = {"Allies": "#7fb3e0", "Axis": "#e88d8d", "Neutral": "#b5bdc2"}
ZONE_EMPTY = "#e6eedb"      # no troops in the zone
ZONE_MIXED = "#c39bd3"      # troops from different sides (shouldn't normally happen)
SEA_ZONE_FILL = "#bfe3f5"       # light blue sea
SEA_BORDER = "#2b2b2b"          # thin solid line between named sea zones
SEA_MINOR_OUTLINE = "#8fc3dc"   # faint outline around each minor (coastal) sea box
SEA_GRID_LON = 10
SEA_GRID_LAT = 10
SEA_OPEN_GRID_LON = 30
SEA_OPEN_GRID_LAT = 20


def _clip_halfplane(poly, a, b, c):
    """Keep the part of a convex polygon where a*x + b*y <= c."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        dp = a * p[0] + b * p[1] - c
        dq = a * q[0] + b * q[1] - c
        if dp <= 0:
            out.append(p)
        if (dp < 0 and dq > 0) or (dp > 0 and dq < 0):
            t = dp / (dp - dq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def polygon_area(poly):
    a = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        a += x0 * y1 - x1 * y0
    return abs(a) / 2


def polygon_centroid(poly):
    a = cx = cy = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        cr = x0 * y1 - x1 * y0
        a += cr
        cx += (x0 + x1) * cr
        cy += (y0 + y1) * cr
    if abs(a) < 1e-9:
        return (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))
    return (cx / (3 * a), cy / (3 * a))


def point_in_polygon(x, y, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi:
            inside = not inside
        j = i
    return inside


def _split3(poly, use_x):
    """Cut a convex polygon into three strips along x (west->east) or y (north->south)."""
    vals = [p[0] if use_x else p[1] for p in poly]
    lo, hi = min(vals), max(vals)
    t1, t2 = lo + (hi - lo) / 3, lo + 2 * (hi - lo) / 3
    if use_x:
        return [_clip_halfplane(poly, 1, 0, t1),
                _clip_halfplane(_clip_halfplane(poly, -1, 0, -t1), 1, 0, t2),
                _clip_halfplane(poly, -1, 0, -t2)]
    return [_clip_halfplane(poly, 0, 1, t1),
            _clip_halfplane(_clip_halfplane(poly, 0, -1, -t1), 0, 1, t2),
            _clip_halfplane(poly, 0, -1, -t2)]


def _bbox_center_and_half_size(outline):
    lons = [p[0] for p in outline]
    lats = [p[1] for p in outline]
    cx, cy = (min(lons) + max(lons)) / 2, (min(lats) + max(lats)) / 2
    rx, ry = (max(lons) - min(lons)) / 2, (max(lats) - min(lats)) / 2
    return cx, cy, rx, ry


def smooth_polygon(pts, passes=3, chaikin=1):
    """Round off the staircase look of a traced outline. A few light averaging passes
    flatten the 0.25-degree steps into gentle curves, then Chaikin corner cutting
    rounds what is left. Neighbouring countries share the same border points, so they
    smooth the same way and stay lined up."""
    pts = list(pts)
    if len(pts) > 1 and pts[0] == pts[-1]:
        pts.pop()                                  # drop the repeated closing point
    if len(pts) < 5:
        return pts
    for _ in range(passes):
        n = len(pts)
        pts = [(0.25 * pts[i - 1][0] + 0.5 * pts[i][0] + 0.25 * pts[(i + 1) % n][0],
                0.25 * pts[i - 1][1] + 0.5 * pts[i][1] + 0.25 * pts[(i + 1) % n][1])
               for i in range(n)]
    for _ in range(chaikin):
        n = len(pts)
        out = []
        for i in range(n):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
            out.append((0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1))
            out.append((0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1))
        pts = out
    return pts


def compute_zone_adjacency(zones, near):
    """zone id -> set of neighbouring land zones. Two zones of the same country are
    neighbours if they sit side by side (West-Center-East); zones of different countries
    are neighbours if their outlines come within `near` map pixels of each other."""
    land = {z: info for z, info in zones.items() if not info.get("sea")}
    step, cell = max(1.0, near / 2), float(near)
    pts, grid = {}, {}
    for z, info in land.items():
        poly, out = info["poly"], []
        for i in range(len(poly)):
            (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % len(poly)]
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) // step))
            for k in range(n):
                t = k / n
                out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
        pts[z] = out
        for x, y in out:
            grid.setdefault((int(x // cell), int(y // cell)), []).append((z, x, y))
    adj = {z: set() for z in land}
    n2 = near * near
    for z, out in pts.items():
        nation = land[z]["nation"]
        for x, y in out:
            gx, gy = int(x // cell), int(y // cell)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for z2, x2, y2 in grid.get((gx + dx, gy + dy), ()):
                        if (z2 != z and land[z2]["nation"] != nation
                                and (x - x2) ** 2 + (y - y2) ** 2 <= n2):
                            adj[z].add(z2)
    for z, info in land.items():
        for z2, info2 in land.items():
            if (z != z2 and info["nation"] == info2["nation"]
                    and abs(info["idx"] - info2["idx"]) == 1):
                adj[z].add(z2)
    return adj


def rasterize_polygons(polys, width, height):
    """Even-odd fill of map-pixel polygons into a width*height bytearray (1 = inside)."""
    mask = bytearray(width * height)
    for poly in polys:
        rows, n = {}, len(poly)
        for i in range(n):
            (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
            if y0 == y1:
                continue
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            for y in range(max(0, int(y0 + 0.5)), min(height - 1, int(y1 - 0.5)) + 1):
                rows.setdefault(y, []).append(x0 + (x1 - x0) * (y + 0.5 - y0) / (y1 - y0))
        for y, xs in rows.items():
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                a, b = max(0, int(xs[k] + 0.5)), min(width, int(xs[k + 1] + 0.5))
                if b > a:
                    mask[y * width + a:y * width + b] = b"\x01" * (b - a)
    return mask


class SeaIndex:
    """Which sea zone is at a map point? (Buckets the zone polygons into a coarse grid.)"""

    def __init__(self, zones, bucket=40.0):
        self.bucket, self.grid, self.box, self.poly, self.seed = bucket, {}, {}, {}, {}
        for z, info in zones.items():
            if not info.get("sea"):
                continue
            xs, ys = [p[0] for p in info["poly"]], [p[1] for p in info["poly"]]
            self.box[z] = (min(xs), min(ys), max(xs), max(ys))
            self.poly[z], self.seed[z] = info["poly"], info["centroid"]
            for gx in range(int(min(xs) // bucket), int(max(xs) // bucket) + 1):
                for gy in range(int(min(ys) // bucket), int(max(ys) // bucket) + 1):
                    self.grid.setdefault((gx, gy), []).append(z)

    def at(self, x, y):
        near = self.grid.get((int(x // self.bucket), int(y // self.bucket)), ())
        for z in near:
            x0, y0, x1, y1 = self.box[z]
            if x0 <= x <= x1 and y0 <= y <= y1 and point_in_polygon(x, y, self.poly[z]):
                return z
        # a hairline gap between two wavy borders: take the closest zone
        pool = near or self.seed
        return min(pool, key=lambda z: (self.seed[z][0] - x) ** 2 + (self.seed[z][1] - y) ** 2,
                   default=None)


def compute_sea_land_adjacency(zones, land_outlines, near):
    """sea zone id -> set of land zones that border it. A land zone borders a sea zone
    when the zone's COAST touches open water that belongs to that sea zone.

    Sea zones are free-form regions that may reach under the land, and the map has blank
    gaps (countries that aren't in the game), so two checks keep this honest: the water
    must be at least a few pixels deep (not a hairline gap between two outlines), and it
    must be connected - through water of the same sea zone - to that zone's own seed
    point. An inland zone therefore never borders the sea, and a zone's fleet can only
    land where its own water really touches the coast."""
    B = 3                                                  # coarse blocks of 3 x 3 pixels
    land_mask = rasterize_polygons(land_outlines, MAP_W, MAP_H)
    index = SeaIndex(zones)
    gw, gh = -(-MAP_W // B), -(-MAP_H // B)
    water = bytearray(gw * gh)                            # block is water if all its pixels are
    owner = {}                                            # water block -> sea zone it lies in
    for by in range(gh):
        rows = [land_mask[y * MAP_W:(y + 1) * MAP_W] for y in range(by * B, min(MAP_H, by * B + B))]
        for bx in range(gw):
            x0, x1 = bx * B, min(MAP_W, bx * B + B)
            if not any(any(r[x0:x1]) for r in rows):
                water[by * gw + bx] = 1
                owner[by * gw + bx] = index.at(x0 + B / 2, by * B + B / 2)
    # the part of each sea zone's water that is connected to its seed
    connected = bytearray(gw * gh)
    for z, info in zones.items():
        if not info.get("sea"):
            continue
        sbx, sby = int(info["centroid"][0] // B), int(info["centroid"][1] // B)
        start = None
        for rad in range(4):
            for dby in range(-rad, rad + 1):
                for dbx in range(-rad, rad + 1):
                    bx, by = sbx + dbx, sby + dby
                    if (start is None and 0 <= bx < gw and 0 <= by < gh
                            and owner.get(by * gw + bx) == z):
                        start = by * gw + bx
            if start is not None:
                break
        if start is None:
            continue
        connected[start] = 1
        stack = [start]
        while stack:
            cur = stack.pop()
            bx, by = cur % gw, cur // gw
            for nb, ok in ((cur - 1, bx > 0), (cur + 1, bx < gw - 1),
                           (cur - gw, by > 0), (cur + gw, by < gh - 1)):
                if ok and not connected[nb] and owner.get(nb) == z:
                    connected[nb] = 1
                    stack.append(nb)

    adj = {z: set() for z, info in zones.items() if info.get("sea")}
    ring = [(math.cos(a * math.pi / 4), math.sin(a * math.pi / 4)) for a in range(8)]
    reach = (near + 2.0, near + 1.0, near, 1.5)           # water must run this far outward

    def is_water(px, py):
        return 0 <= px < MAP_W and 0 <= py < MAP_H and not land_mask[int(py) * MAP_W + int(px)]

    for z, info in zones.items():
        if info.get("sea"):
            continue
        poly = info["poly"]
        for i in range(len(poly)):
            (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % len(poly)]
            n = max(1, int(math.hypot(x1 - x0, y1 - y0)))
            for k in range(n + 1):
                x, y = x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n
                for ux, uy in ring:
                    if all(is_water(x + ux * r, y + uy * r) for r in reach):
                        fx, fy = x + ux * reach[0], y + uy * reach[0]
                        bi = int(fy // B) * gw + int(fx // B)
                        if connected[bi]:
                            adj[owner[bi]].add(z)
    return adj


def build_zones():
    """Returns (zones, cells, nation_zones, capital_zone):
    zones[zone_id]  = {nation, idx, name, poly, centroid}   (poly in map units)
    cells[nation]   = the whole country outline (its real, clipped border)
    nation_zones    = nation -> its 3 zone ids;  capital_zone = nation -> home zone id.

    Each country uses its real simplified border (COUNTRY_OUTLINES); the outlines
    are drawn so neighbours meet along shared borders without overlapping."""
    bounds, cells = {}, {}
    for name, outline in COUNTRY_OUTLINES.items():
        cx, cy, rx, ry = _bbox_center_and_half_size(outline)
        bounds[name] = (rx, ry)
        cells[name] = smooth_polygon([project(lon, lat) for lon, lat in outline])

    zones, nation_zones, capital_zone = {}, {}, {}
    for row in NATION_DATA:
        name, (lat, lon) = row[0], row[2]
        rx, ry = bounds[name]
        use_x = rx >= ry
        ids = []
        if name in SINGLE_ZONE_COUNTRIES:  # Belgium / Netherlands / minors: one Center zone
            zid = f"{name}:0"
            poly = cells[name]
            zones[zid] = {"nation": name, "idx": 0, "name": f"{name} (Center)",
                          "poly": poly, "centroid": polygon_centroid(poly)}
            ids.append(zid)
            nation_zones[name] = ids
            capital_zone[name] = ids[0]
            continue
        dirs = ["West", "Center", "East"] if use_x else ["North", "Center", "South"]
        for i, (poly, d) in enumerate(zip(_split3(cells[name], use_x), dirs)):
            zid = f"{name}:{i}"
            zones[zid] = {"nation": name, "idx": i, "name": f"{name} ({d})",
                          "poly": poly, "centroid": polygon_centroid(poly)}
            ids.append(zid)
        nation_zones[name] = ids
        capital_zone[name] = ids[1]       # home base = the country's Center zone
    return zones, cells, nation_zones, capital_zone


def _clip_cell(poly, tags, a, b, c, tag):
    """Clip a convex polygon to the half-plane a*x + b*y <= c. tags[i] says which
    neighbouring cell the edge leaving vertex i borders; the new cut edge gets `tag`."""
    out, out_tags, n = [], [], len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if fp <= 0:
            out.append(p)
            out_tags.append(tags[i])
            if fq > 0:
                t = fp / (fp - fq)
                out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
                out_tags.append(tag)
        elif fq <= 0:
            t = fp / (fp - fq)
            out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
            out_tags.append(tags[i])
    keep = [i for i in range(len(out))
            if abs(out[i][0] - out[(i + 1) % len(out)][0]) + abs(out[i][1] - out[(i + 1) % len(out)][1]) > 1e-6]
    return [out[i] for i in keep], [out_tags[i] for i in keep]


def _wiggle_edge(p, q):
    """A wavy line from p to q (both ends exact), made by repeated midpoint displacement.
    It is generated from the edge's endpoints in a fixed order, so the two zones that
    share an edge get exactly the same curve and no gap opens between them."""
    key = lambda pt: (round(pt[0], 2), round(pt[1], 2))
    lo, hi = (p, q) if key(p) <= key(q) else (q, p)
    length = math.hypot(hi[0] - lo[0], hi[1] - lo[1])
    pts = [lo, hi]
    if length >= 5:
        rnd = random.Random(f"{lo[0]:.1f},{lo[1]:.1f},{hi[0]:.1f},{hi[1]:.1f}")
        amp = length * SEA_WIGGLE
        for _ in range(3 if length > 22 else 2):
            nxt = [pts[0]]
            for a, b in zip(pts, pts[1:]):
                dx, dy = b[0] - a[0], b[1] - a[1]
                seg = math.hypot(dx, dy) or 1.0
                off = rnd.uniform(-1, 1) * amp
                nxt.append(((a[0] + b[0]) / 2 - dy / seg * off, (a[1] + b[1]) / 2 + dx / seg * off))
                nxt.append(b)
            pts = nxt
            amp *= 0.55
    return pts if (lo is p) else pts[::-1]


def build_sea_zones():
    """Create the sea zones: small coastal zones and larger open-ocean zones.

    Instead of rectangles of a lat/lon grid, every zone is a free-form region: the
    ocean is split between jittered seed points (a weighted Voronoi diagram, so the
    big open-ocean zones stay big) and the shared borders are given a gentle wave. The
    zones tile the whole map; land is simply drawn on top of them."""
    boxes = []
    for outline in COUNTRY_OUTLINES.values():
        lons_ = [point[0] for point in outline]
        lats_ = [point[1] for point in outline]
        boxes.append((min(lons_), max(lons_), min(lats_), max(lats_)))

    def near_land(lon, lat, margin=10):
        mx, my = margin + 6, margin + 1        # open cells are 30 x 20 degrees
        return any(x0 - mx <= lon <= x1 + mx and y0 - my <= lat <= y1 + my
                   for x0, x1, y0, y1 in boxes)

    def on_land(x, y):
        lon, lat = x / MAP_W * 360 - 180, 90 - y / MAP_H * 180
        return any(point_in_polygon(lon, lat, outline) for outline in COUNTRY_OUTLINES.values())

    specs = []

    def add_spec(prefix, lon, lat, width, height, seed_at=None, weight_mult=1.0):
        center_lon, center_lat = lon + width / 2, lat + height / 2
        if seed_at is None and any(point_in_polygon(center_lon, center_lat, outline)
                                   for outline in COUNTRY_OUTLINES.values()):
            return None
        sx, sy = width / 360 * MAP_W, height / 180 * MAP_H
        zone_id = f"sea:{prefix}:{lon + 180}:{lat + 90}"
        if seed_at is not None:                  # box centre is on land: seed it in its water
            seed = seed_at
        else:
            cx, cy = project(center_lon, center_lat)
            rnd = random.Random(zone_id)
            seed, jitter = (cx, cy), SEA_JITTER
            for _ in range(6):                   # wander off the grid, but stay at sea
                x = cx + rnd.uniform(-1, 1) * jitter * sx
                y = cy + rnd.uniform(-1, 1) * jitter * sy
                if 1 <= x <= MAP_W - 1 and 1 <= y <= MAP_H - 1 and not on_land(x, y):
                    seed = (x, y)
                    break
                jitter /= 2
        specs.append({"id": zone_id, "name": sea_name_at(center_lon, center_lat),
                      "seed": seed, "weight": 0.25 * sx * sy * weight_mult,
                      "bounds": (lon, lat, width, height)})
        return zone_id

    def water_seed(lon, lat, width, height):
        """Nearest open-water point inside a grid square whose centre is on land (or None
        if the square is all land), so coastal water there still gets its own box."""
        cx, cy = project(lon + width / 2, lat + height / 2)
        x0, y0 = project(lon, lat + height)
        x1, y1 = project(lon + width, lat)
        best = None
        n = 7
        for i in range(n):
            for j in range(n):
                x = x0 + (i + 0.5) / n * (x1 - x0)
                y = y0 + (j + 0.5) / n * (y1 - y0)
                if 1 <= x <= MAP_W - 1 and 1 <= y <= MAP_H - 1 and not on_land(x, y):
                    d = (x - cx) ** 2 + (y - cy) ** 2
                    if best is None or d < best[0]:
                        best = (d, (x, y))
        return best[1] if best else None

    # Open-ocean zones are larger, but only where their center is well away from land.
    open_rects = []
    for lat in range(-80, 80, SEA_OPEN_GRID_LAT):
        for lon in range(-180, 180, SEA_OPEN_GRID_LON):
            center_lon, center_lat = lon + SEA_OPEN_GRID_LON / 2, lat + SEA_OPEN_GRID_LAT / 2
            if near_land(center_lon, center_lat):
                continue
            if add_spec("open", lon, lat, SEA_OPEN_GRID_LON, SEA_OPEN_GRID_LAT):
                open_rects.append([project(lon, lat), project(lon + SEA_OPEN_GRID_LON, lat),
                                   project(lon + SEA_OPEN_GRID_LON, lat + SEA_OPEN_GRID_LAT),
                                   project(lon, lat + SEA_OPEN_GRID_LAT)])

    # Smaller zones fill the coastlines and all spaces not claimed by open-ocean zones.
    for lat in range(-90, 90, SEA_GRID_LAT):
        for lon in range(-180, 180, SEA_GRID_LON):
            center = project(lon + SEA_GRID_LON / 2, lat + SEA_GRID_LAT / 2)
            if any(point_in_polygon(center[0], center[1], poly) for poly in open_rects):
                continue
            if not add_spec("coast", lon, lat, SEA_GRID_LON, SEA_GRID_LAT):
                # centre is on land: still give the square's coastal water a box of its own
                seed = water_seed(lon, lat, SEA_GRID_LON, SEA_GRID_LAT)
                if seed:
                    add_spec("coast", lon, lat, SEA_GRID_LON, SEA_GRID_LAT, seed, 0.4)

    # ---- the weighted Voronoi cell of every seed ----
    n = len(specs)
    cells = []
    for i, a in enumerate(specs):
        xi, yi = a["seed"]
        poly = [(0.0, 0.0), (float(MAP_W), 0.0), (float(MAP_W), float(MAP_H)), (0.0, float(MAP_H))]
        tags = [None] * 4                      # None = edge on the edge of the map
        r2 = None
        for j in sorted((j for j in range(n) if j != i),
                        key=lambda j: (specs[j]["seed"][0] - xi) ** 2 + (specs[j]["seed"][1] - yi) ** 2):
            xj, yj = specs[j]["seed"]
            if r2 is not None:                 # too far away to touch this cell: skip it
                d, r = math.hypot(xj - xi, yj - yi), math.sqrt(r2)
                if d > r and (d - r) ** 2 - specs[j]["weight"] >= r2 - a["weight"]:
                    continue
            poly, tags = _clip_cell(poly, tags, 2 * (xj - xi), 2 * (yj - yi),
                                    xj * xj + yj * yj - xi * xi - yi * yi + a["weight"] - specs[j]["weight"], j)
            r2 = max((px - xi) ** 2 + (py - yi) ** 2 for px, py in poly)
        cells.append((poly, tags))

    zones = {}
    for i, a in enumerate(specs):
        poly, tags = cells[i]
        wavy, edges = [], {}
        for k in range(len(poly)):
            p, q = poly[k], poly[(k + 1) % len(poly)]
            if tags[k] is None:
                wavy.append(p)                 # the edge of the map stays straight
            else:
                line = _wiggle_edge(p, q)
                wavy.extend(line[:-1])
                edges[specs[tags[k]]["id"]] = line
        zones[a["id"]] = {
            "nation": "Ocean",
            "name": a["name"],
            "poly": wavy,
            "centroid": a["seed"],
            "sea": True,
            "bounds": a["bounds"],             # lon/lat of the grid square it grew from
            "edges": edges,                    # neighbouring zone id -> shared wavy border
        }
    return zones


def chain_polylines(pieces):
    """Join polylines that meet end to end (at points where exactly two meet) into
    longer lines, so they can be drawn as one smooth curve."""
    key = lambda pt: (round(pt[0], 1), round(pt[1], 1))
    ends = {}
    for i, pts in enumerate(pieces):
        for e in (pts[0], pts[-1]):
            ends.setdefault(key(e), []).append(i)
    used = [False] * len(pieces)

    def grow(chain, forward):
        while True:
            node = key(chain[-1] if forward else chain[0])
            cand = [i for i in ends.get(node, ()) if not used[i]]
            if len(ends.get(node, ())) != 2 or not cand:
                return
            used[cand[0]] = True
            pts = pieces[cand[0]]
            if key(pts[0]) != node:
                pts = pts[::-1]
            if forward:
                chain.extend(pts[1:])
            else:
                chain[:0] = pts[::-1][:-1]

    chains = []
    for i, pts in enumerate(pieces):
        if used[i]:
            continue
        used[i] = True
        chain = list(pts)
        grow(chain, True)
        grow(chain, False)
        chains.append(chain)
    return chains


def sea_name_at(lon, lat):
    """Name of the sea / ocean region (a 'zone' on the map) that a point belongs to.
    Specific seas are tested first, then the big oceans."""
    def box(lat0, lat1, lon0, lon1):
        return lat0 <= lat < lat1 and lon0 <= lon < lon1

    if lat >= 66:
        return "Arctic Ocean"
    if lat < -55:
        return "Southern Ocean"
    if box(40, 48, 26, 42):
        return "Black Sea"
    if box(53, 66, 10, 31):
        return "Baltic Sea"
    if box(50, 62, -4, 10):
        return "North Sea"
    if box(62, 66, -12, 20):
        return "Norwegian Sea"
    if box(30, 47, -6, 14):
        return "West Mediterranean Sea"
    if box(30, 41, 14, 37):
        return "East Mediterranean Sea"
    if box(12, 28, 32, 44):
        return "Red Sea"
    if box(22, 31, 47, 58):
        return "Persian Gulf"
    if box(5, 28, 50, 76):
        return "Arabian Sea"
    if box(5, 24, 78, 98):
        return "Bay of Bengal"
    if box(0, 24, 98, 122):
        return "South China Sea"
    if box(24, 34, 118, 132):
        return "East China Sea"
    if box(34, 52, 126, 144):
        return "Sea of Japan"
    if box(50, 66, 135, 162):
        return "Sea of Okhotsk"
    if lat >= 52 and (lon >= 160 or lon < -160):
        return "Bering Sea"
    if box(51, 66, -96, -76):
        return "Hudson Bay"
    if box(17, 31, -98, -80):
        return "Gulf of Mexico"
    if box(7, 23, -88, -60):
        return "Caribbean Sea"
    if box(40, 50, -10, 0):
        return "Bay of Biscay"
    if -100 <= lon < 20 and not (lon < -80 and lat < 17):     # Atlantic
        return "North Atlantic Ocean" if lat >= 0 else "South Atlantic Ocean"
    if 20 <= lon < 120 and lat < 30:
        return "Indian Ocean"
    # Pacific, split like the wall-map zones
    if lat < 0:
        return "South Pacific Ocean"
    if 120 <= lon < 165:
        return "West Pacific Ocean"
    if lon >= 165 or lon < -140:
        return "Central Pacific Ocean"
    return "East Pacific Ocean"


# ---- light theme: black text on light backgrounds for easy reading ----
BG_MAIN = "#e8ecf1"
BG_PANEL = "#f4f6f9"
BG_CARD = "#ffffff"
BORDER = "#cfd6df"
HEADER_BG = "#16222f"
HEADER_FG = "#ffffff"
ACCENT = "#1f5f8b"
GOOD = "#1e8449"
BAD = "#c0392b"
DIM = "#6b7785"
FG_TEXT = "#111827"
OCEAN_COLOR = "#bfe3f5"
LAND_COLOR = "#b7d8a1"
LAND_OUTLINE = "#6f9a54"
GRID_COLOR = "#a3cde6"
UI_FONT = "Segoe UI"
MONO_FONT = "Consolas"
# darker side colors for text on white backgrounds
SIDE_DARK = {"Axis": "#b03a2e", "Allies": "#21618c", "Neutral": "#9a7d0a"}
# quick-send presets offered in the send-forces window
PRESETS = (("10%", 0.10), ("25%", 0.25), ("50%", 0.50), ("All", 1.0))

_BUTTON_KINDS = {
    "normal": ("#e3e8ee", "#d3dae3", FG_TEXT),
    "quiet": ("#eef1f5", "#dde3ea", FG_TEXT),
    "primary": ("#b7d8a1", "#a4c98b", FG_TEXT),
    "accent": ("#c7dceb", "#b2cde0", FG_TEXT),
    "danger": ("#f2c3bd", "#e6aaa2", FG_TEXT),
}


def make_button(parent, text, command, kind="normal", font_size=10, padx=10, pady=5):
    """Flat button with a hover color."""
    bg, hover, fg = _BUTTON_KINDS[kind]
    b = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                  activebackground=hover, activeforeground=fg,
                  disabledforeground="#9aa5b1", relief="flat", bd=0,
                  cursor="hand2", font=(UI_FONT, font_size, "bold"),
                  padx=padx, pady=pady, highlightthickness=0)

    b._rest_bg = bg

    def on_enter(e):
        if getattr(b, "_dimmed", 0):
            return                        # window is dimmed behind a dialog: stay dark
        if str(b.cget("state")) != "disabled":
            b.config(bg=hover)

    def on_leave(e):
        if getattr(b, "_dimmed", 0):
            return
        b.config(bg=bg)

    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)
    return b


def make_card(parent, title=None):
    """A white bordered panel with an optional small heading."""
    outer = tk.Frame(parent, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    if title:
        tk.Label(outer, text=title.upper(), bg=BG_CARD, fg=ACCENT,
                 font=(UI_FONT, 8, "bold")).pack(anchor="w", padx=10, pady=(8, 2))
    return outer



# every this many kilometers of distance adds one turn of travel time
KM_PER_TRAVEL_TURN = 3500
MAX_TRAVEL_TURNS = 4
MAX_ONE_SPACE_MOVE_KM = 1500

# ---- single-player bots ----
# A bot only attacks when its force (after the attacker penalty) is at least this many
# times the defenders' power. Lower = more reckless.
BOT_DEFAULT_MARGIN = 1.25
BOT_ATTACK_MARGIN = {"Germany": 1.0, "Japan": 1.0, "Italy": 1.1, "USSR": 1.1}
BOT_AMPHIBIOUS_MARGIN = 1.3     # landings from the sea are riskier, so demand more
BOT_BOMB_COMFORT = 1.4          # bots skip bombing when their power beats the enemy's by
                                # margin x this much - the win looks safe without it
# Who bots may fight, and from when (year as a fraction: 1940.8 = Nov 1940). From the
# given date every country in the first group may fight every country in the second.
# This supplements the game's own scripted war declarations and the wars the human
# player starts. Outside of these, a bot stays home.
_WESTERN_ALLIES = {"UK", "France", "Poland", "Belgium", "Netherlands",
                   "Canada", "Australia", "India"}
# Each entry is (date, attackers, targets, tag). The tag names the historical event whose
# date the war follows (see event_shift).
BOT_WAR_SCHEDULE = (
    (1939.0, {"Japan"}, {"China"}, "china_war"),                       # Sino-Japanese War
    (1939.6666666667, {"Germany"}, _WESTERN_ALLIES, "poland"),        # invasion of Poland (Sept 1939)
    (1939.8, {"USSR"}, {"Finland"}, "winter_war"),                     # Winter War
    (1940.4, {"Italy"}, _WESTERN_ALLIES, "italy_war"),                 # Italy enters the war
    (1941.0, {"Germany", "Italy", "Romania"}, {"USSR"}, "barbarossa"), # Barbarossa
    (1941.0, {"Japan"}, _WESTERN_ALLIES | {"USA"}, "pearl_harbor"),    # Pearl Harbor
    (1941.0, {"Germany", "Italy"}, {"USA"}, "pearl_harbor"),
)

# ---- single-player variation: "mostly the script, but every game is different" ----
# Historical dates never change; the variation is in how the bots behave.
BOT_STYLE_RANGE = (0.9, 1.15)      # each bot's attack margin is scaled by a roll in this range
BOT_MOOD_CHOICES = ((0.85, 15), (1.0, 70), (1.25, 15))   # (margin scale, weight): bold / normal / cautious turn
BOT_MIN_MARGIN = 0.85              # no bot ever attacks at worse odds than this
BOT_HESITATE_CHANCE = 0.08         # chance a bot sits out its attack step on a turn
BOT_RANDOM_TARGET_CHANCE = 0.3     # chance it picks any workable target, not the weakest one
BOT_HOLD_CHANCE = 0.1              # chance a stack stays put instead of marching on
BOT_AMPHIBIOUS_SKIP_CHANCE = 0.25  # chance a bot doesn't try a landing this turn

def haversine_km(latlon1, latlon2):
    """Great-circle distance in kilometers between two (lat, lon) points."""
    lat1, lon1 = latlon1
    lat2, lon2 = latlon2
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (math.sin(dphi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    return 2 * r * math.asin(min(1.0, math.sqrt(a)))


# ----------------------------------------------------------------------
# OBJECTIVE CHAINS
# Each country has an ordered list of objectives that walks it through its part in the real
# war. Only ONE is shown at a time: achieve it, claim the oil reward, and the next one
# appears. Each entry is (text, reward, goal); the reward is paid as oil (reward /
# OIL_REWARD_DIVISOR). Besides the goal keys listed at NATION_DATA there are:
#   "date":    (year, month_index) - earliest turn the goal can be met (0 = January ... 11 = December)
#   "occupy":  minimum number of foreign zones this country is currently occupying
#   "at_war":  list of nations this country must be at war with
# Countries not listed here (the unplayable minors) just use their single NATION_DATA goal.
# ----------------------------------------------------------------------

OBJECTIVE_CHAINS = {
    "Germany": [
        ("Rearm the Reich and hold all 3 German zones through the Munich crisis (autumn 1939).",
         60, {"zones": 3, "date": (1939, 8)}),
        ("Invade Poland: win a battle against Poland.", 100, {"beat": ["Poland"]}),
        ("Strike west through the Low Countries: win battles against Belgium and the Netherlands.",
         120, {"beat": ["Belgium", "Netherlands"]}),
        ("Defeat France: win a battle against France.", 150, {"beat": ["France"]}),
        ("Launch Operation Barbarossa: win a battle against the USSR.", 200, {"beat": ["USSR"]}),
        ("Drive deep into the East: occupy 6 foreign zones.", 200, {"occupy": 6}),
        ("Hold out as the Reich collapses: still control at least 2 of your 3 zones in 1946.",
         150, {"zones": 2, "date": (1946, 0)}),
    ],
    "Italy": [
        ("Seal the Pact of Steel: reach September 1940 with all 3 Italian zones intact.",
         40, {"zones": 3, "date": (1940, 8)}),
        ("Enter the war as France reels: be at war with France.", 60, {"at_war": ["France"]}),
        ("Strike across the Alps: win a battle against France.", 100, {"beat": ["France"]}),
        ("Build the new Roman Empire: occupy 2 foreign zones.", 120, {"occupy": 2}),
        ("Survive the Allied landings: keep at least 2 of your 3 zones into late 1944.",
         100, {"zones": 2, "date": (1944, 8)}),
    ],
    "Japan": [
        ("Press the war in China: win a battle against China.", 80, {"beat": ["China"]}),
        ("Secure oil for the empire: hold at least 50 oil.", 100, {"oil": 50}),
        ("Strike at Pearl Harbor and the Pacific: win a battle against the USA.",
         150, {"beat": ["USA"]}),
        ("Build the Co-Prosperity Sphere: occupy 4 foreign zones.", 150, {"occupy": 4}),
        ("Threaten the southern flank: win a battle against Australia.", 120,
         {"beat": ["Australia"]}),
        ("Fight to the last: keep at least 2 of your 3 zones into 1946.", 100,
         {"zones": 2, "date": (1946, 0)}),
    ],
    "USSR": [
        ("Win the Winter War: win a battle against Finland.", 80, {"beat": ["Finland"]}),
        ("Survive Operation Barbarossa: be at war with Germany and keep at least 2 of your "
         "3 zones into mid-1942.", 120,
         {"at_war": ["Germany"], "zones": 2, "date": (1942, 6)}),
        ("Hold the line at Stalingrad: win a battle against Germany.", 200,
         {"beat": ["Germany"]}),
        ("Launch the great counter-offensive: occupy 4 foreign zones.", 200, {"occupy": 4}),
        ("Drive on to Berlin: occupy 6 foreign zones by 1946.", 250,
         {"occupy": 6, "date": (1946, 0)}),
    ],
    "USA": [
        ("Be the Arsenal of Democracy: reach 1942 with all 3 American zones intact.", 60,
         {"zones": 3, "date": (1942, 0)}),
        ("Pearl Harbor brings America in: be at war with Japan.", 80, {"at_war": ["Japan"]}),
        ("Turn the tide at Midway: win a battle against Japan.", 150, {"beat": ["Japan"]}),
        ("Land in Sicily: win a battle against Italy.", 150, {"beat": ["Italy"]}),
        ("Open the Second Front on D-Day: win a battle against Germany.", 200,
         {"beat": ["Germany"]}),
        ("Finish the war: occupy 4 foreign zones.", 200, {"occupy": 4}),
    ],
    "UK": [
        ("Keep the guarantee to Poland: be at war with Germany.", 60, {"at_war": ["Germany"]}),
        ("Stand alone in the Battle of Britain: hold all 3 British zones into 1942.", 120,
         {"zones": 3, "date": (1942, 0)}),
        ("Fight for the Mediterranean: win a battle against Italy.", 150, {"beat": ["Italy"]}),
        ("Return to the Continent: win a battle against Germany.", 200, {"beat": ["Germany"]}),
        ("Win the war in Europe: occupy 3 foreign zones.", 200, {"occupy": 3}),
    ],
    "France": [
        ("Honor the guarantee to Poland: be at war with Germany.", 60, {"at_war": ["Germany"]}),
        ("Man the Maginot Line: hold all 3 French zones through late 1940.", 100,
         {"zones": 3, "date": (1940, 10)}),
        ("Fight on after the invasion: keep at least 2 of your 3 zones into 1942.", 120,
         {"zones": 2, "date": (1942, 0)}),
        ("Liberate France: win a battle against Germany.", 150, {"beat": ["Germany"]}),
    ],
    "Poland": [
        ("Stand against the German threat: hold all 3 Polish zones into late 1939.", 40,
         {"zones": 3, "date": (1939, 10)}),
        ("Resist the invasion: win a battle against Germany.", 100, {"beat": ["Germany"]}),
        ("Never surrender: keep at least 2 of your 3 zones into 1941.", 100,
         {"zones": 2, "date": (1941, 0)}),
        ("Fight on beside the Allies: win 3 battles.", 100, {"wins": 3}),
    ],
    "China": [
        ("Resist the Japanese invasion: win a battle against Japan.", 80, {"beat": ["Japan"]}),
        ("Hold the heartland: keep at least 2 of your 3 zones into 1942.", 100,
         {"zones": 2, "date": (1942, 0)}),
        ("Keep fighting alongside the Allies: win 3 battles.", 100,
         {"wins": 3, "date": (1943, 0)}),
        ("Take back what was lost: occupy 2 foreign zones.", 150, {"occupy": 2}),
    ],
    "Netherlands": [
        ("Hold the neutral line: keep your homeland through September 1940.", 30,
         {"zones": 3, "date": (1940, 8)}),
        ("Defend against the German assault: win a battle against Germany.", 80,
         {"beat": ["Germany"]}),
        ("Never give in: still hold your homeland in 1942.", 80, {"zones": 3, "date": (1942, 0)}),
    ],
    "Belgium": [
        ("Hold the neutral line: keep your homeland through September 1940.", 30,
         {"zones": 3, "date": (1940, 8)}),
        ("Defend against the German assault: win a battle against Germany.", 80,
         {"beat": ["Germany"]}),
        ("Never give in: still hold your homeland in 1942.", 80, {"zones": 3, "date": (1942, 0)}),
    ],
    "Romania": [
        ("Guard the Ploiesti oil fields: hold at least 80 oil.", 60, {"oil": 80}),
        ("Sign the Tripartite Pact: join the Axis and be at war with the UK.", 80,
         {"at_war": ["UK"], "date": (1941, 10)}),
        ("Join the invasion of the East: win a battle against the USSR.", 150,
         {"beat": ["USSR"]}),
        ("Hang on as the front collapses: keep at least 2 of your 3 zones into 1945.", 100,
         {"zones": 2, "date": (1945, 0)}),
    ],
    "Finland": [
        ("Hold the Mannerheim Line: keep all 3 zones through the Winter War (to March 1941).",
         80, {"zones": 3, "date": (1941, 2)}),
        ("Hit back at the Soviets: win a battle against the USSR.", 100, {"beat": ["USSR"]}),
        ("Stay independent: keep at least 2 of your 3 zones into 1945.", 100,
         {"zones": 2, "date": (1945, 0)}),
    ],
    "Canada": [
        ("Join the Commonwealth war effort: win 1 battle.", 60, {"wins": 1}),
        ("Fight in the Mediterranean: win a battle against Italy.", 100, {"beat": ["Italy"]}),
        ("Storm the beaches of Normandy: win a battle against Germany.", 150,
         {"beat": ["Germany"]}),
    ],
    "Australia": [
        ("Defend the homeland: hold all 3 Australian zones into 1942.", 60,
         {"zones": 3, "date": (1942, 0)}),
        ("Turn back Japan: win a battle against Japan.", 150, {"beat": ["Japan"]}),
        ("Take the offensive in the Pacific: occupy 2 foreign zones.", 150, {"occupy": 2}),
    ],
    "India": [
        ("Hold the subcontinent: keep all 3 zones into 1943.", 60,
         {"zones": 3, "date": (1943, 0)}),
        ("Defend the Burma frontier: win a battle against Japan.", 120, {"beat": ["Japan"]}),
        ("Push the Japanese back: occupy 2 foreign zones.", 150, {"occupy": 2}),
    ],
}


# ----------------------------------------------------------------------
# NATION MODEL
# ----------------------------------------------------------------------

class Nation:
    def __init__(self, name, side, latlon, oil, stability,
                 objective, objective_reward, goal, start_forces):
        self.name = name
        self.side = side          # "Axis", "Allies", "Neutral"
        self.latlon = latlon      # (lat, lon)
        res_mult = RESOURCE_MULT.get(name, 1.0) * START_RESOURCE_MULT * START_RESOURCE_NERF
        self.oil = int(round(oil * res_mult))
        self.iron = int(round(IRON_STOCKPILES.get(name, 10) * res_mult))
        if name in ROUND_START_RESOURCES_TO_10:      # tidy starting numbers
            self.oil = int(round(self.oil / 10.0)) * 10
            self.iron = int(round(self.iron / 10.0)) * 10
        # yearly income = a share of the STARTING stockpiles, for both oil and iron
        self.oil_rate = max(1, int(round(self.oil * YEARLY_RESOURCE_INCOME_SHARE)))
        self.iron_rate = max(1, int(round(self.iron * YEARLY_RESOURCE_INCOME_SHARE)))
        self.stability = stability
        # ordered objectives; only the current one is active (see OBJECTIVE_CHAINS)
        self.objectives = list(OBJECTIVE_CHAINS.get(name)
                               or [(objective, objective_reward, goal)])
        self.objective_index = 0
        self.zones_occupied = 0       # foreign zones this country is currently occupying
        self.start_forces = start_forces
        self.victories_over = set()   # nations this country has beaten in battle
        self.battles_won = 0
        self.zone_count = 1 if name in SINGLE_ZONE_COUNTRIES else 3   # Belgium/Netherlands: 1
        self.zones_held = self.zone_count   # how many of its own zones it still controls
        self.at_war_with = set()
        self.alive = True
        self.last_attack_tick = None   # turn number of this country's last attack order
        self.bombing_uses = BOMBINGS_PER_COUNTRY

    @staticmethod
    def _rating(value):
        return max(1, min(10, int(round(value))))

    @property
    def army_rating(self):
        return self._rating(1 + army_iron_points(self.iron) + self.start_forces[0] / 5
                            - RATING_PENALTY.get(self.name, 0))

    @property
    def navy_rating(self):
        return self._rating(1 + self.iron / NAVY_RATING_IRON_DIV + self.oil / NAVY_RATING_OIL_DIV
                            + self.start_forces[1] / 3 - RATING_PENALTY.get(self.name, 0))

    @property
    def air_rating(self):
        return self._rating(1 + self.oil / 50 + self.start_forces[2] / 3
                            - RATING_PENALTY.get(self.name, 0))

    @property
    def territory(self):
        """Territory % = share of the country's own 3 zones it still controls."""
        return int(round(self.zones_held * 100 / self.zone_count))

    def oil_income(self):
        return int(round(self.oil_rate * self.territory / 100))

    def iron_income(self):
        return int(round(self.iron_rate * self.territory / 100))

    def has_oil_field(self):
        return self.oil >= 30

    # ---- the current objective (one at a time) ----
    @property
    def objective_claimed(self):
        """True once EVERY objective in the chain has been completed and claimed."""
        return self.objective_index >= len(self.objectives)

    @property
    def objective(self):
        if self.objective_claimed:
            return "All objectives complete."
        return self.objectives[self.objective_index][0]

    @property
    def objective_reward(self):
        return 0 if self.objective_claimed else self.objectives[self.objective_index][1]

    @property
    def goal(self):
        return {} if self.objective_claimed else self.objectives[self.objective_index][2]

    def claim_objective(self):
        """The current objective is claimed: the next one in the chain appears."""
        if not self.objective_claimed:
            self.objective_index += 1

    @staticmethod
    def _date_months(year, month_index):
        return (year - START_YEAR) * 12 + month_index

    @staticmethod
    def _date_label(months):
        return f"{START_YEAR + months // 12} {MONTH_NAMES[months % 12]}"

    def objective_progress(self, year):
        """Return a list of (requirement text, is_met) for this nation's current goal."""
        g = self.goal
        checks = []
        now_months = int(round((year - START_YEAR) * 12))
        for name in g.get("at_war", []):
            checks.append((f"Be at war with {name}", name in self.at_war_with))
        if "occupy" in g:
            checks.append((f"Occupy at least {g['occupy']} foreign zone(s) "
                           f"(now {self.zones_occupied})",
                           self.zones_occupied >= g["occupy"]))
        if "date" in g:
            target = self._date_months(*g["date"])
            checks.append((f"Reach {self._date_label(target)} "
                           f"(now {self._date_label(now_months)})",
                           now_months >= target))
        for name in g.get("beat", []):
            checks.append((f"Win a battle against {name}",
                           name in self.victories_over))
        if "wins" in g:
            checks.append((f"Win {g['wins']} battle(s) ({self.battles_won} so far)",
                           self.battles_won >= g["wins"]))
        if "zones" in g:
            need = min(g["zones"], self.zone_count)
            checks.append((f"Control at least {need} of your {self.zone_count} zone(s) "
                           f"(now {self.zones_held})",
                           self.zones_held >= need))
        if "oil" in g:
            checks.append((f"Hold at least {g['oil']} oil (now {self.oil})",
                           self.oil >= g["oil"]))
        if "year" in g:
            checks.append((f"Reach the year {g['year']} (now {int(year)})",
                           year >= g["year"]))
        return checks

    def objective_met(self, year):
        if self.objective_claimed:
            return False
        return all(met for _, met in self.objective_progress(year))


# ----------------------------------------------------------------------
# MAIN APPLICATION
# ----------------------------------------------------------------------

class WW2Sim(tk.Tk):
    SIDE_ORDER = {"Axis": 0, "Allies": 1, "Neutral": 2}

    def __init__(self):
        super().__init__()
        self.title("World War II: Grand Strategy Simulation")
        self.geometry(f"{min(1600, self.winfo_screenwidth() - 40)}x"
                      f"{min(1080, self.winfo_screenheight() - 80)}")
        self.configure(bg=BG_MAIN)
        self.setup_styles()

        self.setup_world()
        self.current = self.nations["Germany"]   # turn starts as Axis
        self.phase = "Axis War Phase"
        self.selected_target = None                       # a zone id (for the info panel)
        self.selected_force_loc = self.capital_zone["Germany"]
        self.force_locs = []
        self.drag = None                                  # drag-and-drop state

        # single-player mode: player_name is None in hotseat mode
        self.player_name = None
        self.game_over = False
        self.bot_running = False
        self.player_turn_active = True                   # single-player: human may issue orders now
        self.battle_busy = False                          # a battle is playing out tick by tick
        self.bot_skip = False                             # 'Skip' pressed: no more pauses this run
        self._bot_wait = None                             # variable the pause waits on
        self._bot_last_shown = None
        self._bot_arrow = None                            # (from_zone, to_zone) shown briefly
        self.mode_var = tk.StringVar()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # zoom / pan view state for the map
        self.zoom = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0
        self._pan_start = None

        self.build_ui()
        self.welcome_dialog()

    def setup_styles(self):
        """Consistent ttk look (tables, combobox, scrollbars)."""
        st = ttk.Style(self)
        try:
            st.theme_use("clam")
        except tk.TclError:
            pass
        st.configure("Treeview", background=BG_CARD, fieldbackground=BG_CARD,
                     foreground=FG_TEXT, rowheight=26, font=(UI_FONT, 10), borderwidth=0)
        st.configure("Treeview.Heading", background=HEADER_BG, foreground="#ffffff",
                     font=(UI_FONT, 10, "bold"), relief="flat", padding=6)
        st.configure("Compact.Treeview", background=BG_CARD, fieldbackground=BG_CARD,
                 foreground=FG_TEXT, rowheight=20, font=(UI_FONT, 9), borderwidth=0)
        st.configure("Compact.Treeview.Heading", background=HEADER_BG, foreground="#ffffff",
                 font=(UI_FONT, 9, "bold"), relief="flat", padding=3)
        st.map("Treeview.Heading", background=[("active", ACCENT)])
        st.map("Treeview", background=[("selected", ACCENT)],
               foreground=[("selected", "#ffffff")])
        st.configure("TCombobox", padding=4, fieldbackground=BG_CARD, background=BG_CARD)
        st.configure("Vertical.TScrollbar", background="#c4ccd6", troughcolor=BG_PANEL,
                     bordercolor=BG_PANEL, arrowcolor=FG_TEXT)
        self.option_add("*TCombobox*Listbox.font", (UI_FONT, 10))

    def setup_world(self):
        """Create nations, the 3-zone territories and every country's starting forces."""
        self.nations = {}
        for row in NATION_DATA:
            n = Nation(*row)
            self.nations[n.name] = n
        self.zones, self.cells, self.nation_zones, self.capital_zone = build_zones()
        self.land_adj = compute_zone_adjacency(self.zones, GROUND_BORDER_PX)   # ground moves
        self.air_adj = compute_zone_adjacency(self.zones, AIR_GAP_PX)          # air moves
        self.sea_zones = build_sea_zones()
        self.zones.update(self.sea_zones)
        # sea zone -> land zones it borders (the only places its fleet can land troops)
        self.sea_index = SeaIndex(self.zones)
        self.sea_land_adj = compute_sea_land_adjacency(self.zones, self.cells.values(), SEA_COAST_PX)
        navy_size = {n.name: n.start_forces[1] * UNIT_SCALE * NAVY_SIZE_MULT
                     for n in self.nations.values() if n.name not in MINOR_COUNTRIES}
        self.sea_zone = {}
        placed = {}                                  # nation with a fleet -> its sea zone
        # Every fleet starts in a sea zone of its own, on its country's coast (any coast
        # if it has none), and never in the same named sea as a hostile fleet - so a
        # country never starts out sharing waters with an enemy. The biggest fleets pick
        # first; each picks the free zone nearest its anchor.
        for name in sorted(NAVY_ANCHOR, key=lambda nm: -navy_size.get(nm, 0)):
            ax, ay = project(*NAVY_ANCHOR[name])
            own = set(self.nation_zones.get(name, ()))
            free = [z for z in self.sea_land_adj if z not in placed.values()]
            quiet = [z for z in free if not any(
                self.zones[z]["name"] == self.zones[oz]["name"] and self.is_hostile(name, other)
                for other, oz in placed.items())]
            cands = ([z for z in quiet if self.sea_land_adj[z] & own]
                     or [z for z in quiet if self.sea_land_adj[z]]
                     or quiet or free or list(self.sea_zones))
            self.sea_zone[name] = min(
                cands,
                key=lambda z: ((self.sea_zones[z]["centroid"][0] - ax) ** 2 +
                                (self.sea_zones[z]["centroid"][1] - ay) ** 2),
            )
            if navy_size.get(name, 0) > 0:
                placed[name] = self.sea_zone[name]
        self.zone_occupier = {}       # zone id -> nation occupying it (None = its own country)
        # garrisons[zone][owner] = {"army": n, "navy": n, "air": n}
        self.garrisons = {}
        self.force_positions = {}       # (zone, owner, kind) -> map x/y drop position
        # units that recently moved: locks[(zone, owner)] = [{"units", "ready"}]
        self.locks = {}
        self.ticks = 0                 # turns elapsed; each turn = 2 months
        for n in self.nations.values():
            _, navy, air = (v * UNIT_SCALE for v in n.start_forces)
            navy *= NAVY_SIZE_MULT                               # navies are x3
            if n.name in MINOR_COUNTRIES:
                continue                                         # unplayable: no troops
            army = self.historical_troops(n.name, START_YEAR)    # real 1939 army size
            cap = self.capital_zone[n.name]
            self.add_force(cap, n.name, new_units(army, 0, air))       # land forces at home
            if n.name in self.sea_zone:
                self.add_force(self.sea_zone[n.name], n.name, new_units(0, navy, 0))
        self.events_fired = set()
        # single-player variation (empty = hotseat / no variation); see roll_variation()
        self.event_shifts = {}
        self.bot_style = {}
        self.bot_mood = {}
        # forces en route:
        # [{owner, origin, dest, units, remaining, total}]  (origin/dest are zone ids)
        self.pending_offensives = []

    # ---------------- alliance / trade rules ----------------

    @staticmethod
    def are_allies(a, b):
        """Same-side countries are automatic allies. Neutrals are free agents
        and are never allied with anyone (not even each other)."""
        return a.side == b.side and a.side != "Neutral"

    def is_hostile(self, a_name, b_name):
        """True if forces of country a would fight forces/territory of country b."""
        if a_name == b_name:
            return False
        return not self.are_allies(self.nations[a_name], self.nations[b_name])

    def can_trade(self, a, b):
        """Allies can trade with each other; Neutrals can trade with anyone
        they aren't at war with. Defeated countries can't receive anything."""
        if b.name == a.name or not b.alive:
            return False
        if b.name in a.at_war_with:
            return False
        return self.are_allies(a, b) or a.side == "Neutral" or b.side == "Neutral"

    def declare_war(self, a_name, b_name):
        if a_name != b_name:
            self.nations[a_name].at_war_with.add(b_name)
            self.nations[b_name].at_war_with.add(a_name)

    # ---------------- calendar ----------------

    @property
    def year(self):
        """Fractional year used for comparisons (each turn = 2 months)."""
        return START_YEAR + self.ticks / TURNS_PER_YEAR

    def date_label(self):
        """e.g. '1939 February'."""
        months = self.ticks * MONTHS_PER_TURN
        return f"{START_YEAR + months // 12} {MONTH_NAMES[months % 12]}"

    # ---------------- terrain and winter ----------------

    def terrain_of(self, z):
        """Terrain key of a land zone ('plains' for sea zones and unlisted countries)."""
        if self.is_sea_zone(z) or ":" not in z:
            return "plains"
        nation, idx = self.zone_nation(z), int(z.rsplit(":", 1)[1])
        t = ZONE_TERRAIN.get(nation, "plains")
        if isinstance(t, tuple):
            t = t[idx] if idx < len(t) else t[-1]
        return t if t in TERRAIN_EFFECTS else "plains"

    def winter_info(self, z):
        """(penalty, name) of the winter weighing on land zone z this turn, or None."""
        if self.is_sea_zone(z) or z not in self.zones:
            return None
        lat = self.zone_latlon(z)[0]
        turn = self.ticks % TURNS_PER_YEAR
        if turn not in (WINTER_TURNS_NORTH if lat >= 0 else WINTER_TURNS_SOUTH):
            return None
        for min_lat, penalty, name in WINTER_SEVERITY:
            if abs(lat) >= min_lat:
                return penalty, name
        return None

    def is_winter_now(self):
        return self.ticks % TURNS_PER_YEAR in WINTER_TURNS_NORTH

    def battle_modifiers(self, z, a_names, d_names):
        """Per-country power multipliers for a land battle in z from terrain and winter:
        (attacker mults, defender mults, [description lines]). Sea zones: no modifiers."""
        a_mult = {o: 1.0 for o in a_names}
        d_mult = {o: 1.0 for o in d_names}
        lines = []
        if self.is_sea_zone(z) or z not in self.zones:
            return a_mult, d_mult, lines
        label, t_att, t_def = TERRAIN_EFFECTS[self.terrain_of(z)]
        if (t_att, t_def) != (1.0, 1.0):
            for o in a_mult:
                a_mult[o] *= t_att
            for o in d_mult:
                d_mult[o] *= t_def
            bits = []
            if t_def != 1.0:
                bits.append(f"defenders +{round((t_def - 1) * 100)}%")
            if t_att != 1.0:
                bits.append(f"attackers -{round((1 - t_att) * 100)}%")
            lines.append(f"TERRAIN: {label} - " + ", ".join(bits) + ".")
        w = self.winter_info(z)
        if w:
            penalty, wname = w
            hit_a, hit_d = [], []
            for o in a_mult:
                p = penalty * WINTER_HARDENED.get(o, 1.0)
                a_mult[o] *= 1 - p
                hit_a.append(f"{o} -{round(p * 100)}%")
            for o in d_mult:
                p = penalty * WINTER_DEFENDER_SHARE * WINTER_HARDENED.get(o, 1.0)
                d_mult[o] *= 1 - p
                hit_d.append(f"{o} -{round(p * 100)}%")
            lines.append(f"WINTER: {wname}. Attackers: " + ", ".join(hit_a)
                         + ". Defenders: " + ", ".join(hit_d) + ".")
        return a_mult, d_mult, lines

    def bot_terrain_ratio(self, bot, z):
        """How much terrain and winter change the bot's odds of taking zone z (attacker power
        multiplier / defender power multiplier), judged against the hostile troops there."""
        defenders = [o for o, u in self.garrisons.get(z, {}).items()
                     if o in self.nations and self.is_hostile(bot.name, o)
                     and units_total(self.battle_units(z, u)) > 0]
        if not defenders:
            return 1.0
        a_mult, d_mult, _ = self.battle_modifiers(z, [bot.name], defenders)
        return (a_mult[bot.name] / (sum(d_mult.values()) / len(d_mult))
                * self.bot_defender_air_factor(bot, z))

    # ---------------- movement cooldown ("resting") ----------------

    def locked_units(self, loc, owner):
        """Units at loc that recently moved and can't act yet."""
        total = new_units()
        lst = self.locks.get((loc, owner))
        if not lst:
            return total
        lst[:] = [e for e in lst if e["ready"] > self.ticks]
        for e in lst:
            for k in UNIT_KEYS:
                total[k] += e["units"][k]
        return total

    def available_units(self, loc, owner):
        """Units at loc that are rested and can be ordered to move or attack."""
        f = self.get_force(loc, owner)
        if not f:
            return new_units()
        lk = self.locked_units(loc, owner)
        return {k: max(0, f[k] - lk[k]) for k in UNIT_KEYS}

    def rest_turns_left(self, loc, owner):
        ready = [e["ready"] for e in self.locks.get((loc, owner), [])
                 if e["ready"] > self.ticks]
        return (min(ready) - self.ticks) if ready else 0

    def add_lock(self, loc, owner, units, fight_ok=False):
        """Rest `units` at loc for MOVE_COOLDOWN_TURNS. With fight_ok they only can't move:
        they marched in to attack, so they still fight when the battle there starts."""
        if units_total(units) > 0:
            self.locks.setdefault((loc, owner), []).append(
                {"units": dict(units), "ready": self.ticks + MOVE_COOLDOWN_TURNS,
                 "fight_ok": fight_ok})

    def station(self, loc, owner, units, position=None, can_fight=False):
        """Units arrive and stand in loc; they must rest before acting again. With
        can_fight (they arrived to attack enemy forces standing here) the rest only
        stops them moving - they still fight when the battle starts."""
        # Reinforcing a beachhead: if the owner (or an ally) already has rested (ready)
        # troops standing on enemy-held land here, troops arriving to join them are ready at once instead
        # of having to rest. (Air and navy still rest.)
        existing = self.get_force(loc, owner) or new_units()
        # Air force must never trigger the "merged stack" rule.  On land, only
        # army troops count as the troops being merged; at sea, only navy counts.
        # This prevents moving planes into an army stack from resetting the
        # army's movement/combat state.
        merge_kind = "navy" if self.is_sea_zone(loc) else "army"
        merging_with_existing = (existing[merge_kind] > 0 and units[merge_kind] > 0)
        stack_ready = merging_with_existing and self.available_units(loc, owner)[merge_kind] > 0
        self.add_force(loc, owner, units)
        if stack_ready:
            # Resting troops joining an unrested (ready) stack make the whole
            # stack unrested, so reinforcements can join a powerful attack at once.
            # (Only the merged kind is freed; e.g. air keeps resting.)
            lst = self.locks.get((loc, owner), [])
            for e in lst:
                e["units"][merge_kind] = 0
            self.locks[(loc, owner)] = [e for e in lst if units_total(e["units"]) > 0]
            if not self.locks[(loc, owner)]:
                self.locks.pop((loc, owner), None)
            for k in UNIT_KEYS:
                if k != merge_kind and units[k] > 0:
                    self.add_lock(loc, owner, {kk: (units[kk] if kk == k else 0) for kk in UNIT_KEYS})
        elif merging_with_existing:
            # Whole stack was already resting: it keeps resting.
            self.add_lock(loc, owner, dict(units))
        else:
            self.add_lock(loc, owner, dict(units), fight_ok=can_fight)
        if position is not None:
            for kind in UNIT_KEYS:
                if self.garrisons.get(loc, {}).get(owner, {}).get(kind, 0) > 0:
                    self.force_positions[(loc, owner, kind)] = position

    def clamp_locks(self, loc, owner):
        """After losses, make sure resting units never exceed the units present."""
        lst = self.locks.get((loc, owner))
        if not lst:
            return
        f = self.garrisons.get(loc, {}).get(owner) or new_units()
        for k in UNIT_KEYS:
            over = sum(e["units"][k] for e in lst) - f[k]
            for e in reversed(lst):
                if over <= 0:
                    break
                cut = min(over, e["units"][k])
                e["units"][k] -= cut
                over -= cut
        lst[:] = [e for e in lst if units_total(e["units"]) > 0]

    # ---------------- zones / territory ----------------

    def zone_nation(self, z):
        return self.zones[z]["nation"]

    def is_sea_zone(self, z):
        return self.zones.get(z, {}).get("sea", False)

    def zone_label(self, z):
        return self.zones[z]["name"]

    def zone_latlon(self, z):
        x, y = self.zones[z]["centroid"]
        return (90 - y / MAP_H * 180, x / MAP_W * 360 - 180)

    def controller(self, z):
        """The country currently controlling zone z (None if nobody does)."""
        if self.is_sea_zone(z):
            return None
        occ = self.zone_occupier.get(z)
        if occ is not None:
            return occ
        home = self.zone_nation(z)
        return home if self.nations[home].alive else None

    def zone_fill(self, z):
        """Political color (red=Axis, blue=Allies, yellow=Neutral, grey=unclaimed minor).
        The color follows who actually CONTROLS the zone, so troops that merely arrive in
        unclaimed land do not repaint it - the zone only flips once they attack and claim
        it (see claim_zone / take_zone). Zones where opposing armies stand face to face
        are shown in the mixed color."""
        if self.is_sea_zone(z):
            return SEA_ZONE_FILL
        if self.is_contested(z):
            return ZONE_MIXED
        occ = self.zone_occupier.get(z)
        if occ is not None and self.nations[occ].alive:     # claimed by another country
            return SIDE_COLOR[self.nations[occ].side]
        home = self.zone_nation(z)
        if home in MINOR_COUNTRIES:                         # greyed out until someone takes it
            return MINOR_GREY
        return SIDE_COLOR[self.nations[home].side]

    def zone_at_map(self, mx, my):
        for z, info in self.zones.items():
            if self.is_sea_zone(z):
                continue
            if point_in_polygon(mx, my, info["poly"]):
                return z
        if 0 <= mx < MAP_W and 0 <= my < MAP_H:
            return self.sea_index.at(mx, my)         # open water (free-form sea zones)
        return None

    def zone_at_screen(self, sx, sy):
        for z, x0, y0, x1, y1 in getattr(self, "panel_cols", []):
            if x0 <= sx <= x1 and y0 <= sy <= y1:
                return z                  # the box of a small country
        return self.zone_at_map((sx - self.pan_x) / self.zoom, (sy - self.pan_y) / self.zoom)

    def recount_zones(self, home_name):
        n = self.nations[home_name]
        n.zones_held = sum(1 for z in self.nation_zones[home_name]
                           if self.zone_occupier.get(z) is None)
        if n.zones_held == 0 and n.alive:
            self.defeat_nation(n)

    def update_occupation_counts(self):
        """Refresh how many foreign zones each country is occupying (for objectives)."""
        counts = {}
        for occ in self.zone_occupier.values():
            if occ is not None:
                counts[occ] = counts.get(occ, 0) + 1
        for n in self.nations.values():
            n.zones_occupied = counts.get(n.name, 0)

    def take_zone(self, owner_name, z):
        """owner_name won control of zone z. Returns 'conquered', 'liberated' or 'held'.

        Air force alone can never capture a land zone. A country must have at least
        one ground troop present to establish control; aircraft can support the fight
        but cannot occupy territory by themselves.
        """
        if self.is_sea_zone(z):          # sea zones have no owner country to conquer
            return "held"
        force = self.get_force(z, owner_name)
        if not force or force["army"] <= 0:
            return "held"
        owner = self.nations[owner_name]
        home_name = self.zone_nation(z)
        home = self.nations[home_name]
        prev = self.zone_occupier.get(z)
        if owner_name == home_name or self.are_allies(owner, home):
            new_occ, mode = None, "liberated"
        else:
            new_occ, mode = owner_name, "conquered"
        if new_occ == prev:
            return "held"
        self.zone_occupier[z] = new_occ
        self.update_occupation_counts()
        label = self.zone_label(z)
        if mode == "conquered":
            owner.victories_over.add(home_name)
            owner.stability = min(100, owner.stability + 3)
            home.stability = max(0, home.stability - 5)
            msg = f"{owner_name} conquers {label}!"
            if prev is None:           # 20% of the country's oil and iron falls into enemy hands
                oil_loot = int(home.oil * ZONE_CAPTURE_RESOURCE_SHARE)
                iron_loot = int(home.iron * ZONE_CAPTURE_RESOURCE_SHARE)
                home.oil -= oil_loot
                home.iron -= iron_loot
                # the attackers (the owner plus allied countries with troops in the zone) split it
                takers = [owner_name]
                for o, u in self.garrisons.get(z, {}).items():
                    if (o != owner_name and u.get("army", 0) > 0
                            and self.are_allies(owner, self.nations[o])):
                        takers.append(o)
                for i, t in enumerate(takers):
                    # remainders go to the first countries so nothing is lost
                    self.nations[t].oil += oil_loot // len(takers) + (1 if i < oil_loot % len(takers) else 0)
                    self.nations[t].iron += iron_loot // len(takers) + (1 if i < iron_loot % len(takers) else 0)
                msg += f" {oil_loot} oil and {iron_loot} iron captured"
                if len(takers) > 1:
                    msg += f" and split between {', '.join(takers)}"
                msg += "."
            self.log_msg(msg)
        else:
            self.log_msg(f"{label} is liberated!")
        self.recount_zones(home_name)
        return mode

    # ---------------- force bookkeeping ----------------

    def get_force(self, loc, owner):
        u = self.garrisons.get(loc, {}).get(owner)
        return u if u and units_total(u) > 0 else None

    def add_force(self, loc, owner, units):
        if units_total(units) <= 0:
            return
        slot = self.garrisons.setdefault(loc, {})
        cur = slot.setdefault(owner, new_units())
        for k in UNIT_KEYS:
            cur[k] += units[k]

    def set_force(self, loc, owner, units):
        slot = self.garrisons.setdefault(loc, {})
        if units_total(units) <= 0:
            slot.pop(owner, None)
        else:
            slot[owner] = dict(units)
        self.clamp_locks(loc, owner)

    def owned_force_locations(self, owner):
        return [loc for loc, owners in self.garrisons.items()
                if owner in owners and units_total(owners[owner]) > 0]

    def hostile_forces_at(self, loc, owner):
        """Owners of stationed forces at loc that would fight `owner`."""
        return [o for o, u in self.garrisons.get(loc, {}).items()
                if units_total(u) > 0 and self.is_hostile(owner, o)]

    def nation_units(self, owner):
        """Total units owned by a nation, including forces en route."""
        total = new_units()
        for owners in self.garrisons.values():
            u = owners.get(owner)
            if u:
                for k in UNIT_KEYS:
                    total[k] += u[k]
        for off in self.pending_offensives:
            if off["owner"] == owner:
                for k in UNIT_KEYS:
                    total[k] += off["units"][k]
        return total

    def defeat_nation(self, n):
        n.alive = False
        n.zones_held = 0
        for owners in self.garrisons.values():
            owners.pop(n.name, None)
        for key in [k for k in self.locks if k[1] == n.name]:
            del self.locks[key]
        self.pending_offensives = [o for o in self.pending_offensives if o["owner"] != n.name]
        self.log_msg(f"{n.name} has been completely defeated!")
        # zones it was occupying go back to their own countries
        for z, occ in list(self.zone_occupier.items()):
            if occ == n.name:
                self.zone_occupier[z] = None
                self.recount_zones(self.zone_nation(z))
        self.update_occupation_counts()

    # ---------------- UI construction ----------------

    def build_ui(self):
        # ---- header bar: title on the left, date + phase on the right ----
        header = tk.Frame(self, bg=HEADER_BG)
        header.pack(fill="x")
        tk.Label(header, text="WORLD WAR II", font=("Georgia", 18, "bold"),
                 fg=HEADER_FG, bg=HEADER_BG).pack(side="left", padx=(16, 8), pady=10)
        tk.Label(header, text="Grand Strategy Simulation", font=(UI_FONT, 11),
                 fg="#9fb3c8", bg=HEADER_BG).pack(side="left", pady=(6, 0))
        self.result_var = tk.StringVar()      # battle-win text (shown above the map)
        self.bot_var = tk.StringVar()         # what the bots are doing (shown above the map)
        self.result_color = "#ffffff"         # side color of the battle-result text
        self.result_fill = "#ffffff"          # color it is drawn in right now (it flashes)
        self.bot_color = "#ffffff"            # side color of the bot-move text
        self._confetti = []                   # live confetti particles
        self._confetti_job = None
        status = tk.Frame(header, bg=HEADER_BG)
        status.pack(side="right", padx=16)
        self.date_var = tk.StringVar()
        self.phase_var = tk.StringVar()
        tk.Label(status, textvariable=self.date_var, font=("Georgia", 15, "bold"),
                 fg=HEADER_FG, bg=HEADER_BG).pack(side="left", padx=(0, 14))
        self.phase_badge = tk.Label(status, textvariable=self.phase_var,
                                    font=(UI_FONT, 10, "bold"), fg="#ffffff",
                                    bg=SIDE_COLOR["Axis"], padx=12, pady=4)
        self.phase_badge.pack(side="left")
        self.panel_hidden = False
        self.panel_toggle = make_button(status, "Hide Panel", self.toggle_control_panel,
                                        "quiet", 11, padx=12, pady=5)
        self.panel_toggle.pack(side="left", padx=(12, 0))
        self.btn_end = make_button(status, "End Phase  \u25b6", self.end_phase,
                       "primary", 11, padx=12, pady=5)
        self.btn_end.pack(side="left", padx=(8, 0))
        self.btn_skip = make_button(status, "Skip \u25b6\u25b6", self.skip_bot_wait,
                                    "quiet", 11, padx=12, pady=5)   # shown only while bots move

        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(fill="both", expand=True, padx=10, pady=(8, 4))

        # ---- Left: map ----
        left = tk.Frame(main, bg=BG_MAIN, width=MAP_W)
        left.pack(side="left", fill="y", expand=False)
        left.pack_propagate(False)
        self.left_panel = left

        map_toolbar = tk.Frame(left, bg=BG_MAIN)
        map_toolbar.pack(fill="x", pady=(0, 4))

        def toolbar_btn(text, cmd):
            make_button(map_toolbar, text, cmd, "quiet", 9, padx=9, pady=3).pack(
                side="left", padx=(0, 4))

        toolbar_btn("Zoom In (+)", lambda: self.zoom_at(MAP_W / 2, MAP_H / 2, 1.25, True))
        toolbar_btn("Zoom Out (-)", lambda: self.zoom_at(MAP_W / 2, MAP_H / 2, 1 / 1.25, True))
        toolbar_btn("World", self.reset_view)
        toolbar_btn("Europe", lambda: self.focus_on(12, 51.5, 8.0))
        toolbar_btn("Asia-Pacific", lambda: self.focus_on(115, 25, 2.5))
        tk.Label(map_toolbar, text="Scroll = zoom   \u00b7   Right-drag = pan",
                 bg=BG_MAIN, fg=DIM, font=(UI_FONT, 9)).pack(side="left", padx=10)

        self.canvas = tk.Canvas(left, width=MAP_W, height=MAP_H, bg=OCEAN_COLOR,
                                highlightthickness=1, highlightbackground=BORDER)
        self.canvas.pack()

        self.draw_map()

        # zoom (mouse wheel) and pan (right-click drag) bindings
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())   # wheel events go to the focused widget
        self.canvas.bind("<MouseWheel>", self.on_zoom_wheel)          # Windows/Mac
        self.canvas.bind("<Button-4>", lambda e: self.zoom_at(e.x, e.y, 1.1))   # Linux up
        self.canvas.bind("<Button-5>", lambda e: self.zoom_at(e.x, e.y, 1 / 1.1))  # Linux down
        for key in ("<plus>", "<equal>", "<KP_Add>"):
            self.canvas.bind(key, lambda e: self.zoom_at(MAP_W / 2, MAP_H / 2, 1.25, True))
        for key in ("<minus>", "<underscore>", "<KP_Subtract>"):
            self.canvas.bind(key, lambda e: self.zoom_at(MAP_W / 2, MAP_H / 2, 1 / 1.25, True))
        self.canvas.bind("<ButtonPress-3>", self.on_pan_start)
        self.canvas.bind("<B3-Motion>", self.on_pan_move)
        self.canvas.bind("<ButtonRelease-3>", self.on_pan_end)
        self.canvas.bind("<ButtonRelease-2>", self.on_pan_end)
        self.canvas.bind("<ButtonPress-2>", self.on_pan_start)
        self.canvas.bind("<B2-Motion>", self.on_pan_move)
        # drag and drop forces: press on a force box, drag, release on a zone
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_release)

        # ---- legend: colour chips + a short how-to ----
        legend = tk.Frame(left, bg=BG_MAIN)
        legend.pack(fill="x", pady=(6, 0))

        def chip(color, text):
            box = tk.Frame(legend, bg=BG_MAIN)
            box.pack(side="left", padx=(0, 16))
            tk.Frame(box, bg=color, width=14, height=14, highlightthickness=1,
                     highlightbackground="#2c3e50").pack(side="left", padx=(0, 5))
            tk.Label(box, text=text, bg=BG_MAIN, fg=FG_TEXT,
                     font=(UI_FONT, 9, "bold")).pack(side="left")

        chip(SIDE_COLOR["Axis"], "Axis")
        chip(SIDE_COLOR["Allies"], "Allied")
        chip(SIDE_COLOR["Neutral"], "Neutral")
        tk.Label(legend, text="T = Troops   \u2693 = Navy   wing = Air Force   * = capital zone",
                 bg=BG_MAIN, fg=DIM, font=(UI_FONT, 9)).pack(side="left", padx=8)
        self.map_hint = tk.Label(left, bg=BG_MAIN, fg=DIM, font=(UI_FONT, 9), justify="left",
                 wraplength=MAP_W,
                 text="Drag a force box onto a zone to send it, then pick 10% / 25% / 50% / All. "
                      "Click any country's troops to act as that country. "
                      "Red dashed outline = opposing armies: click the zone to fight. "
                      "Dashed line = forces en route."
                 )
        self.map_hint.pack(anchor="w", pady=(4, 0))

        # ---- Right: control panel ----
        right = tk.Frame(main, bg=BG_MAIN)
        right.pack(side="right", fill="y", padx=(10, 0), before=left)
        self.right_panel = right

        # single-player tag, shown above "Acting as" only in that mode (see begin_game)
        self.mode_label = tk.Label(right, textvariable=self.mode_var, anchor="w",
                                   bg=ACCENT, fg="#ffffff", font=(UI_FONT, 10, "bold"),
                                   padx=10, pady=5)
        acting = make_card(right, "Acting as")
        self.acting_card = acting
        acting.pack(fill="x", pady=(0, 8))
        self.acting_var = tk.StringVar()
        self.acting_combo = ttk.Combobox(acting, textvariable=self.acting_var,
                                         state="readonly", font=(UI_FONT, 11))
        self.acting_combo.pack(fill="x", padx=10, pady=(2, 10))
        self.acting_combo.bind("<<ComboboxSelected>>", self.on_acting_change)

        info = make_card(right, "Briefing")
        info.pack(fill="x", pady=(0, 8))
        inner = tk.Frame(info, bg=BG_CARD)
        inner.pack(fill="x", padx=2, pady=(0, 6))
        self.info_box = tk.Text(inner, width=44, height=15, bg=BG_CARD, fg=FG_TEXT,
                                font=(UI_FONT, 10), relief="flat", bd=0, wrap="word",
                                padx=10, pady=2, highlightthickness=0, state="disabled",
                                cursor="arrow")
        info_scroll = ttk.Scrollbar(inner, orient="vertical", command=self.info_box.yview)
        self.info_box.configure(yscrollcommand=info_scroll.set)
        info_scroll.pack(side="right", fill="y")
        self.info_box.pack(side="left", fill="x", expand=True)
        ib = self.info_box
        ib.tag_configure("title", font=(UI_FONT, 14, "bold"), foreground=FG_TEXT)
        ib.tag_configure("h", font=(UI_FONT, 10, "bold"), foreground=ACCENT,
                         spacing1=8, spacing3=2)
        ib.tag_configure("key", font=(UI_FONT, 10, "bold"))
        ib.tag_configure("good", foreground=GOOD, font=(UI_FONT, 10, "bold"))
        ib.tag_configure("bad", foreground=BAD, font=(UI_FONT, 10, "bold"))
        ib.tag_configure("dim", foreground=DIM)
        for side, color in SIDE_DARK.items():
            ib.tag_configure("side_" + side, foreground=color, font=(UI_FONT, 10, "bold"))

        forces = make_card(right, "Your forces")
        forces.pack(fill="x", pady=(0, 8))
        self.force_list = tk.Listbox(forces, height=4, exportselection=False,
                                     bg=BG_CARD, fg=FG_TEXT, font=(MONO_FONT, 10),
                                     relief="flat", highlightthickness=0,
                                     selectbackground=ACCENT, selectforeground="#ffffff",
                                     activestyle="none")
        self.force_list.pack(fill="x", padx=10, pady=(2, 4))
        self.force_list.bind("<<ListboxSelect>>", self.on_force_list_select)
        tk.Label(forces, text="Drag a force box on the map onto a zone to send it.",
                 bg=BG_CARD, fg=GOOD, font=(UI_FONT, 9, "bold"),
                 wraplength=330, justify="left").pack(anchor="w", padx=10)
        tk.Label(forces, text="SELECTED TARGET", bg=BG_CARD, fg=DIM,
                 font=(UI_FONT, 8, "bold")).pack(anchor="w", padx=10, pady=(6, 0))
        self.target_var = tk.StringVar(value="(click a zone on the map)")
        tk.Label(forces, textvariable=self.target_var, bg=BG_CARD, fg=BAD,
                 font=(UI_FONT, 10, "bold")).pack(anchor="w", padx=10, pady=(0, 8))

        # the send / battle panel lives INSIDE the main window (placed over it when opened)
        self.send_panel_window = tk.Frame(self, bg=BG_CARD)
        self.send_panel = tk.Frame(self.send_panel_window, bg=BG_CARD,
                       highlightthickness=1, highlightbackground=BORDER)
        self.send_panel.pack(fill="both", expand=True)
        self.send_panel_header = tk.Frame(self.send_panel, bg=HEADER_BG)
        self.send_panel_header.pack(fill="x")
        self.send_panel_title = tk.Label(self.send_panel_header, bg=HEADER_BG,
                         fg="#ffffff", font=("Georgia", 14, "bold"))
        self.send_panel_title.pack(anchor="w", padx=16, pady=(12, 2))
        self.send_panel_close = tk.Button(self.send_panel_header, text="X",
                                          command=lambda: self.after_idle(
                                              self.close_send_panel),
                                          bg=BAD, fg="#ffffff",
                                          activebackground="#a5281b",
                          activeforeground="#ffffff", relief="flat",
                          bd=0, font=(UI_FONT, 12, "bold"),
                          cursor="hand2", padx=10)
        self.send_panel_close.pack(side="right", padx=6, pady=6)
        self.send_panel_prompt = tk.Label(self.send_panel_header, bg=HEADER_BG,
                          fg="#c9d6e3", font=(UI_FONT, 9),
                          wraplength=480, justify="left")
        self.send_panel_prompt.pack(anchor="w", padx=16, pady=(0, 12))
        self.send_panel_body = tk.Frame(self.send_panel, bg=BG_CARD)
        self.send_panel_body.pack(fill="both", expand=True, padx=16, pady=(12, 14))
        self.pending_send = None

        btn_frame = tk.Frame(right, bg=BG_MAIN)
        btn_frame.pack(fill="x")
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        self.btn_trade = self.make_btn(btn_frame, "Trade", self.action_trade, 0, 0)
        self.btn_objectives = self.make_btn(btn_frame, "Claim Reward",
                                            self.action_objective, 0, 1, kind="accent")
        self.btn_all = self.make_btn(btn_frame, "All Nations", self.action_view_all, 1, 0,
                                     span=2)

        # ---- Bottom: campaign log ----
        log_card = make_card(self, "Campaign log")
        log_card.pack(fill="both", expand=False, padx=10, pady=(4, 10))
        self.log = scrolledtext.ScrolledText(log_card, height=6, bg=BG_CARD, fg=FG_TEXT,
                                             font=(UI_FONT, 10), wrap="word", relief="flat",
                                             bd=0, padx=8, pady=4, highlightthickness=0)
        self.log.pack(fill="both", expand=True, padx=2, pady=(0, 4))
        self.log.tag_configure("date", foreground=DIM)
        self.log.tag_configure("battle", foreground=BAD, font=(UI_FONT, 10, "bold"))
        self.log.tag_configure("event", foreground=ACCENT, font=(UI_FONT, 10, "bold"))
        self.log.tag_configure("food_shortage", foreground="#d4ac0d",
                       font=(UI_FONT, 10, "bold"))
        self.log.tag_configure("extra_supply", foreground=GOOD,
                       font=(UI_FONT, 10, "bold"))
        self.log.tag_configure("good", foreground=GOOD)

    def make_btn(self, parent, text, cmd, row, col, kind="normal", span=1, font_size=10):
        b = make_button(parent, text, cmd, kind, font_size,
                        pady=8 if font_size > 10 else 6)
        b.grid(row=row, column=col, columnspan=span, sticky="ew", padx=2, pady=3)
        return b

    def toggle_control_panel(self):
        if self.panel_hidden:
            self.right_panel.pack(side="right", fill="y", padx=(10, 0), before=self.left_panel)
            self.left_panel.pack_configure(expand=False)
            self.panel_toggle.config(text="Hide Panel")
        else:
            self.right_panel.pack_forget()
            self.left_panel.pack_configure(expand=True)    # center the map in the window
            self.panel_toggle.config(text="Show Panel")
        self.panel_hidden = not self.panel_hidden

    def refresh_map_messages(self):
        self.draw_map_messages()

    def draw_map_messages(self):
        """Battle-result and bot-move text, drawn straight on the map (no background),
        centred along its top edge in the color of the side it belongs to. The canvas is
        cleared on every redraw, so draw_map calls this again at the end."""
        c = self.canvas
        c.delete("mapmsg")
        cw = c.winfo_width()
        cx = (cw if cw > 1 else MAP_W) / 2
        y = 24
        for key, text, fill, size in (
                ("result", self.result_var.get(), self.result_fill, 17),
                ("bot", self.bot_var.get(), self.bot_color, 13)):
            if not text:
                continue
            font = (UI_FONT, size, "bold")
            tags = ("mapmsg", "mapmsg_" + key)
            # a thin dark outline keeps the colored letters readable on sea and land
            for dx in (-2, -1, 0, 1, 2):
                for dy in (-2, -1, 0, 1, 2):
                    if (dx or dy) and abs(dx) + abs(dy) <= 3:
                        c.create_text(cx + dx, y + dy, text=text, fill="#101820",
                                      font=font, tags=tags)
            c.create_text(cx, y, text=text, fill=fill, font=font, tags=tags)
            y += size * 2 + 4
        c.tag_raise("mapmsg")

    # ---- confetti burst around the battle-result text ----

    def spawn_confetti(self, color):
        bbox = self.canvas.bbox("mapmsg_result")
        if not bbox:
            return
        x0, y0, x1, y1 = bbox
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        palette = [color, lighten(color, 0.3), shade(color, 0.2), lighten(color, 0.6)]
        for _ in range(90):
            # start somewhere along the edge of the text and fly outward
            px = random.uniform(x0 - 12, x1 + 12)
            py = random.choice((y0 - 6, y1 + 6, random.uniform(y0 - 6, y1 + 6)))
            dx, dy = px - cx, py - cy
            dist = max(1.0, (dx * dx + dy * dy) ** 0.5)
            speed = random.uniform(1.5, 5.5)
            self._confetti.append({
                "x": px, "y": py,
                "vx": dx / dist * speed + random.uniform(-0.8, 0.8),
                "vy": dy / dist * speed - random.uniform(1.0, 3.0),
                "ang": random.uniform(0, 6.283), "spin": random.uniform(-0.45, 0.45),
                "w": random.uniform(3, 7), "h": random.uniform(2, 4),
                "color": random.choice(palette), "life": random.randint(40, 70),
                "max": 70})
        if self._confetti_job is None:
            self._confetti_job = self.after(30, self.animate_confetti)

    def animate_confetti(self):
        self._confetti_job = None
        c = self.canvas
        c.delete("confetti")
        alive = []
        for p in self._confetti:
            p["life"] -= 1
            if p["life"] <= 0:
                continue
            p["vy"] += 0.22                      # gravity
            p["vx"] *= 0.97                      # air drag
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["ang"] += p["spin"]
            k = min(1.0, p["life"] / 15)         # shrink away at the end
            ca, sa = math.cos(p["ang"]), math.sin(p["ang"])
            pts = []
            for ux, uy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                lx, ly = ux * p["w"] * k, uy * p["h"] * k
                pts += [p["x"] + lx * ca - ly * sa, p["y"] + lx * sa + ly * ca]
            c.create_polygon(pts, fill=p["color"], outline="", tags="confetti")
            alive.append(p)
        self._confetti = alive
        c.tag_raise("mapmsg")
        if alive:
            self._confetti_job = self.after(30, self.animate_confetti)

    def announce_battle_result(self, text, side):
        self._result_sequence = getattr(self, "_result_sequence", 0) + 1
        sequence = self._result_sequence
        color = SIDE_COLOR[side]
        self.result_color = color
        self.result_fill = "#ffffff"
        self.result_var.set(text)
        self.draw_map_messages()
        self.spawn_confetti(color)               # confetti in the winning side's colors
        flash = ["#ffffff", color, "#ffffff", color, "#ffffff", color]

        def pulse(index=0):
            if sequence != self._result_sequence:
                return
            self.result_fill = flash[index] if index < len(flash) else color
            self.draw_map_messages()
            if index < len(flash):
                self.after(140, pulse, index + 1)

        pulse()
        self.after(4500, lambda: self.clear_battle_result(sequence))

    def clear_battle_result(self, sequence):
        if sequence == getattr(self, "_result_sequence", 0):
            self.result_var.set("")
            self.draw_map_messages()

    # ---------------- map drawing (real projected coastlines) ----------------

    def to_screen(self, x, y):
        return x * self.zoom + self.pan_x, y * self.zoom + self.pan_y

    def marker_radius(self):
        return 8 * min(1.8, max(0.6, self.zoom))

    def token_scale(self):
        return min(1.1, max(0.75, self.zoom))

    # ---------------- unit boxes: flag + icon + count ----------------

    def box_height(self):
        return max(7, int(8 * self.token_scale())) * 2.3 * UNIT_BOX_SCALE

    def new_tag(self):
        self._tag_n = getattr(self, "_tag_n", 0) + 1
        return f"unit{self._tag_n}"

    def draw_flag(self, x0, y0, x1, y1, nation, tag):
        c = self.canvas
        w, h = x1 - x0, y1 - y0
        for op in FLAGS.get(nation, [("rect", 0, 0, 1, 1, "#888888")]):
            kind = op[0]
            if kind == "rect":
                _, a, b, e, d, color = op
                c.create_rectangle(x0 + a * w, y0 + b * h, x0 + e * w, y0 + d * h,
                                    fill=color, outline="", tags=tag)
            elif kind == "circle":
                _, cx, cy, r, color = op
                px, py = x0 + cx * w, y0 + cy * h
                c.create_oval(px - r * h, py - r * h, px + r * h, py + r * h,
                               fill=color, outline="", tags=tag)
            elif kind == "star":
                _, cx, cy, r, color = op
                c.create_polygon(star_points(x0 + cx * w, y0 + cy * h, r * h),
                                  fill=color, outline="", tags=tag)
            elif kind == "jack":
                _, a, b, e, d = op
                self.draw_jack(x0 + a * w, y0 + b * h, x0 + e * w, y0 + d * h, tag)

    def draw_jack(self, x0, y0, x1, y1, tag):
        """Simplified Union Jack."""
        c = self.canvas
        w, h = x1 - x0, y1 - y0
        red, blue = "#c8102e", "#1f3a93"
        c.create_rectangle(x0, y0, x1, y1, fill=blue, outline="", tags=tag)
        for (ax, ay, bx, by) in ((x0, y0, x1, y1), (x0, y1, x1, y0)):
            c.create_line(ax, ay, bx, by, fill="#ffffff", width=max(1.5, h * 0.22), tags=tag)
            c.create_line(ax, ay, bx, by, fill=red, width=max(1, h * 0.08), tags=tag)
        c.create_rectangle(x0 + w * 0.40, y0, x0 + w * 0.60, y1, fill="#ffffff", outline="", tags=tag)
        c.create_rectangle(x0, y0 + h * 0.36, x1, y0 + h * 0.64, fill="#ffffff", outline="", tags=tag)
        c.create_rectangle(x0 + w * 0.45, y0, x0 + w * 0.55, y1, fill=red, outline="", tags=tag)
        c.create_rectangle(x0, y0 + h * 0.43, x1, y0 + h * 0.57, fill=red, outline="", tags=tag)

    def draw_anchor(self, cx, cy, s, tag):
        """Anchor icon (white with black outline) for the navy."""
        c = self.canvas
        for color, wd in (("#000000", 3), ("#ffffff", 1.5)):
            c.create_oval(cx - 0.25 * s, cy - 0.95 * s, cx + 0.25 * s, cy - 0.45 * s,
                           outline=color, width=wd, tags=tag)
            c.create_line(cx, cy - 0.45 * s, cx, cy + 0.8 * s, fill=color, width=wd, tags=tag)
            c.create_line(cx - 0.4 * s, cy - 0.2 * s, cx + 0.4 * s, cy - 0.2 * s,
                           fill=color, width=wd, tags=tag)
            c.create_arc(cx - 0.75 * s, cy - 0.35 * s, cx + 0.75 * s, cy + 0.95 * s,
                          start=200, extent=140, style="arc", outline=color, width=wd,
                          tags=tag)

    def draw_wing(self, cx, cy, s, tag):
        """Wing icon (white with black outline) for the air force."""
        pts = [(-1.0, 0.35), (-0.55, -0.15), (0.1, -0.55), (0.95, -0.7), (0.65, -0.35),
               (1.0, -0.2), (0.6, 0.0), (0.85, 0.2), (0.4, 0.3), (0.55, 0.5), (-0.1, 0.5)]
        flat = []
        for px, py in pts:
            flat += [cx + px * s, cy + (py + 0.1) * s]
        self.canvas.create_polygon(flat, fill="#ffffff", outline="#000000", width=1,
                                    tags=tag)

    def draw_plane_bg(self, cx, cy, span, length, tag, shadow=None, nation=None,
                      shadow_color="#000000", selected=False, facing=1):
        """Small side-view WW2 fighter (nose pointing right) drawn behind an air-force
        box, painted in the owner's colors, with a black oval shadow below it.
        `shadow` = (width, height) of the oval. When `selected`, the plane's own outline
        turns purple (the air box has no rectangle of its own)."""
        c = self.canvas
        sx, sy = span / 2, length / 2
        sxf = sx * facing                            # facing=-1 mirrors the plane (nose left)

        def pts(frac):
            flat = []
            for fx, fy in frac:
                flat += [cx + fx * sxf, cy + fy * sy]
            return flat

        if shadow:                                   # black oval shadow just below the plane
            ow, oh = shadow
            oy = cy + sy - oh * 0.2
            c.create_oval(cx - ow / 2, oy, cx + ow / 2, oy + oh, fill=shadow_color,
                          outline="", tags=tag)

        outline = "#8e44ad" if selected else "#1c1c1c"
        ow_ = 1.6 if selected else 1                 # outline width (purple: 20% thinner)
        body, wing, accent = PLANE_COLORS.get(nation, ("#dfe5ea", "#b9c4cd", "#2f3b45"))
        # tail fin (vertical stabilizer)
        c.create_polygon(pts([(-0.97, -0.12), (-0.90, -0.88), (-0.72, -0.88),
                              (-0.52, -0.22)]),
                         fill=wing, outline=outline, width=ow_, tags=tag)
        # tailplane (horizontal stabilizer, seen edge-on)
        c.create_polygon(pts([(-0.95, -0.04), (-0.62, -0.10), (-0.58, 0.04),
                              (-0.93, 0.08)]),
                         fill=wing, outline=outline, width=ow_, tags=tag)
        # fuselage: slim tail, deep cowling at the nose
        c.create_polygon(pts([(-0.98, -0.08), (-0.60, -0.22), (-0.10, -0.38), (0.40, -0.36),
                              (0.72, -0.28), (0.88, -0.10), (0.88, 0.14), (0.62, 0.30),
                              (0.15, 0.32), (-0.40, 0.14), (-0.98, 0.04)]),
                         fill=body, outline=outline, width=ow_, smooth=True, tags=tag)
        # accent band across the rear fuselage
        c.create_polygon(pts([(-0.80, -0.14), (-0.62, -0.20), (-0.62, 0.10), (-0.80, 0.06)]),
                         fill=accent, outline="", tags=tag)
        # wing (seen from the side, below the canopy)
        c.create_polygon(pts([(-0.12, 0.00), (0.38, -0.02), (0.30, 0.42), (-0.06, 0.40)]),
                         fill=wing, outline=outline, width=ow_, tags=tag)
        # cockpit canopy
        c.create_oval(cx - 0.10 * sxf, cy - 0.66 * sy, cx + 0.30 * sxf, cy - 0.24 * sy,
                      fill="#2c4a63", outline=outline, width=ow_, tags=tag)
        # propeller blur + spinner at the nose
        c.create_line(cx + 0.95 * sxf, cy - 0.70 * sy, cx + 0.95 * sxf, cy + 0.55 * sy,
                      fill="#3a3a3a", width=2, tags=tag)
        c.create_oval(cx + 0.82 * sxf, cy - 0.12 * sy, cx + 1.00 * sxf, cy + 0.14 * sy,
                      fill=accent, outline=outline, width=ow_, tags=tag)

    def draw_outlined_text(self, x, y, text, font, tag):
        c = self.canvas
        for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            c.create_text(x + dx, y + dy, text=text, fill="#000000", font=font, tags=tag)
        c.create_text(x, y, text=text, fill="#ffffff", font=font, tags=tag)

    def unit_box_metrics(self, kind, count):
        """Size of a force box and its footprint (box + plane/shadow/waves) so the
        layout code can keep boxes from overlapping. foot = extents from the box
        center: (left, top, right, bottom)."""
        k = UNIT_BOX_SCALE
        fs_full = max(7, int(8 * self.token_scale()))
        fs = max(5, int(fs_full * k))              # font (kept legible)
        h = fs_full * 2.3 * k
        text = fmt_count(count, True)
        if kind == "army":
            text = "T" + text
        icon_w = h * 0.9 if kind in ("navy", "air") else 0
        w = (0.78 * fs_full * len(text) + 10) * k + icon_w
        m = {"fs": fs, "h": h, "w": w, "text": text, "icon_w": icon_w}
        if kind == "air":
            span = max(w * 1.45, h * 2.5) * 1.1   # small side-view plane behind the box
            length = h * 1.1 * 1.1
            ow, oh = span * 0.6, h * 0.3          # black oval shadow below the plane
            m.update(span=span, length=length, shadow=(ow, oh))
            half_w = max(span / 2, w / 2)
            foot = (half_w, length / 2, half_w, length / 2 + oh * 0.8)
        elif kind == "navy":
            foot = (w / 2 + 5, h / 2, w / 2 + 5, h / 2 + 8)     # waves under the box
        else:
            foot = (w / 2, h / 2, w / 2, h / 2)
        m["foot"] = tuple(v + 2 for v in foot)
        return m

    def draw_unit_box(self, x, y, owner_name, kind, count, selected=False, drag=None,
                      tag=None, bg=None):
        """One box (centered at x, y) for a single unit type. Army and navy have the
        owner's flag behind them; Air has a small side-view plane painted in the
        owner's colors instead. Army = 'T' count, Navy = anchor icon, Air = wing icon. `drag` = (zone, owner,
        kind) makes it draggable. Overall size is controlled by UNIT_BOX_SCALE."""
        c = self.canvas
        tag = tag or self.new_tag()
        m = self.unit_box_metrics(kind, count)
        fs, h, w, text, icon_w = m["fs"], m["h"], m["w"], m["text"], m["icon_w"]
        x0, x1, y0, y1 = x - w / 2, x + w / 2, y - h / 2, y + h / 2

        if kind == "air":     # plane silhouette with a shadow below, behind the box
            if bg is None:                       # what the shadow falls on: the zone color
                bg = "#b7d8a1"
                if drag and drag[0] in self.zones and not self.is_sea_zone(drag[0]):
                    bg = self.zone_fill(drag[0])
            self.draw_plane_bg(x, y, m["span"], m["length"], tag, m["shadow"], owner_name,
                               shade(bg, 0.5), selected)    # 50% black shadow
        if kind == "navy":    # waves under the box: the water
            n = 8
            pts = []
            for i in range(n + 1):
                pts += [x0 - 5 + i * (w + 10) / n, y1 + 4 + (2 if i % 2 else -1)]
            c.create_line(*pts, smooth=True, fill="#3d7ea6", width=2, tags=tag)

        if kind != "air":           # air force: the plane carries the country colors
            self.draw_flag(x0, y0, x1, y1, owner_name, tag)
        if kind != "air":               # air box: no rectangle at all; the plane is its outline
            c.create_rectangle(x0, y0, x1, y1, fill="",
                                outline="#8e44ad" if selected else "#000000",
                                width=1.6 if selected else 1, tags=tag)
        if kind == "navy":
            self.draw_anchor(x0 + icon_w / 2 + 3, y, h * 0.42, tag)
        elif kind == "air":
            self.draw_wing(x0 + icon_w / 2 + 3, y, h * 0.46, tag)
        self.draw_outlined_text(x0 + icon_w + (w - icon_w) / 2, y, text,
                                 ("Consolas", fs, "bold"), tag)
        if drag:
            c.tag_bind(tag, "<ButtonPress-1>",
                       lambda e, d=drag: self.on_box_press(e, d))
        return w, h

    # ---------------- overlap-free layout for boxes and labels ----------------

    def queue_box(self, x, y, owner, kind, count, sel=False, drag=None):
        """Remember a force box to draw later; positions are fixed up so no two
        boxes overlap (see layout_items)."""
        zone = None                       # land boxes must stay inside their own zone
        if drag and kind in ("army", "air") and not self.is_sea_zone(drag[0]):
            zone = drag[0]
        item = {"x": x, "y": y, "owner": owner, "kind": kind, "count": count,
                "sel": sel, "drag": drag, "zone": zone,
                "foot": self.unit_box_metrics(kind, count)["foot"]}
        self._box_items.append(item)
        return item

    @staticmethod
    def item_rect(it):
        l, t, r, b = it["foot"]
        return (it["x"] - l, it["y"] - t, it["x"] + r, it["y"] + b)

    @staticmethod
    def _overlap(ra, rb):
        ox = min(ra[2], rb[2]) - max(ra[0], rb[0])
        oy = min(ra[3], rb[3]) - max(ra[1], rb[1])
        return ox, oy

    def layout_items(self, items, obstacles):
        """Give every force box a spot where it overlaps no other box and none of the
        fixed `obstacles` rectangles. Each box keeps its preferred spot if that is free;
        otherwise it takes the nearest free spot found by searching outward in rings.
        Army and air boxes are kept INSIDE their own zone whenever the zone has room:
        first the whole box must fit in the zone, then at least its center; only if the
        zone is completely full does a box fall back to the nearest free spot anywhere."""
        # The result only depends on the zoom and on where things sit relative to the map
        # origin, so remember it: panning, selecting a zone or re-drawing at the same zoom
        # then costs nothing here.
        px, py = self.pan_x, self.pan_y
        key = (round(self.zoom, 5),
               tuple((it["kind"], it["count"], it.get("zone"),
                      tuple(round(v, 1) for v in it["foot"]),
                      round(it["x"] - px, 1), round(it["y"] - py, 1)) for it in items),
               tuple((round(r[0] - px, 1), round(r[1] - py, 1),
                      round(r[2] - px, 1), round(r[3] - py, 1)) for r in obstacles))
        cache = self.__dict__.setdefault("_layout_cache", {})
        hit = cache.get(key)
        if hit is not None:
            for it, (hx, hy) in zip(items, hit):
                it["x"], it["y"] = hx + px, hy + py
            return

        # placed rectangles are kept in a coarse grid so a candidate spot is only compared
        # with the few rectangles near it (the ring search below tries thousands of spots)
        CELL = 64.0
        grid = {}

        def cells_of(r):
            for gx in range(int(r[0] // CELL), int(r[2] // CELL) + 1):
                for gy in range(int(r[1] // CELL), int(r[3] // CELL) + 1):
                    yield (gx, gy)

        def add_placed(r):
            for key in cells_of(r):
                grid.setdefault(key, []).append(r)

        for r in obstacles:
            add_placed(r)

        def free(it):
            r = self.item_rect(it)
            for key in cells_of(r):
                for q in grid.get(key, ()):
                    if min(r[2], q[2]) - max(r[0], q[0]) > 0 and \
                            min(r[3], q[3]) - max(r[1], q[1]) > 0:
                        return False
            return True

        def inside_ok(it, poly, mode, bbox=None):
            if poly is None or mode == 0:
                return True
            if bbox is not None:                           # cheap reject before point tests
                if mode == 2:
                    if not (bbox[0] <= it["x"] <= bbox[2] and bbox[1] <= it["y"] <= bbox[3]):
                        return False
                else:
                    l, t, r, b = self.item_rect(it)
                    if l < bbox[0] or t < bbox[1] or r > bbox[2] or b > bbox[3]:
                        return False
            if mode == 2:                                  # center point only
                return point_in_polygon(it["x"], it["y"], poly)
            l, t, r, b = self.item_rect(it)                # whole box inside the zone
            return all(point_in_polygon(px, py, poly)
                       for px, py in ((l, t), (r, t), (l, b), (r, b),
                                      ((l + r) / 2, t), ((l + r) / 2, b)))

        for it in items:
            bx, by = it["x"], it["y"]
            poly = bbox = None
            if it.get("zone") in self.zones:
                poly = [self.to_screen(px, py) for px, py in self.zones[it["zone"]]["poly"]]
                bbox = (min(p[0] for p in poly), min(p[1] for p in poly),
                        max(p[0] for p in poly), max(p[1] for p in poly))
            # a box already in a good free spot stays put
            if free(it) and (poly is None or inside_ok(it, poly, 1, bbox)):
                add_placed(self.item_rect(it))
                continue
            found = False
            for mode in ((1, 2, 0) if poly else (0,)):
                radius = 3.0
                while radius < 8000 and not found:
                    n = 24
                    for k in range(n):
                        ang = 2 * math.pi * k / n
                        it["x"] = bx + radius * math.cos(ang)
                        it["y"] = by + radius * math.sin(ang)
                        if inside_ok(it, poly, mode, bbox) and free(it):
                            found = True
                            break
                    radius = radius * 1.08 + 1.5
                    if mode != 0 and radius > 400:         # zone is full: relax the rule
                        break
                if found:
                    break
            if not found:
                it["x"], it["y"] = bx, by
            add_placed(self.item_rect(it))
        if len(cache) > 60:
            cache.clear()
        cache[key] = [(it["x"] - px, it["y"] - py) for it in items]

    def label_font(self, spec):
        key = tuple(spec)
        cache = self.__dict__.setdefault("_font_cache", {})
        if key not in cache:
            family, size, style = spec
            cache[key] = tkfont.Font(family=family, size=size,
                                     weight="bold" if "bold" in style else "normal",
                                     slant="italic" if "italic" in style else "roman")
        return cache[key]

    def label_size(self, spec, text):
        """(width, line height) of text in the given font spec, measured once."""
        cache = self.__dict__.setdefault("_size_cache", {})
        key = (tuple(spec), text)
        if key not in cache:
            f = self.label_font(spec)
            cache[key] = (f.measure(text), f.metrics("linespace"))
        return cache[key]

    def place_label(self, x, y, text, spec, fill, avoid, nudges=((0, 0),), inside=None):
        """Draw a map text at (x, y) - or at the first of the small `nudges` offsets where
        it overlaps no other text, force box or panel. If no spot is free the text is left
        out. `inside` (a list of screen (x, y) points) keeps the text over its own country.
        Returns whether it was drawn."""
        w, h = self.label_size(spec, text)
        for ndx, ndy in nudges:
            tx, ty = x + ndx, y + ndy
            if inside is not None and not point_in_polygon(tx, ty, inside):
                continue
            rect = (tx - w / 2 - 2, ty - h / 2 - 1, tx + w / 2 + 2, ty + h / 2 + 1)
            if any(self._overlap(rect, r)[0] > 0 and self._overlap(rect, r)[1] > 0
                   for r in avoid):
                continue
            avoid.append(rect)
            self.canvas.create_text(tx, ty, text=text, fill=fill, font=spec)
            return True
        return False

    def small_panel_layouts(self):
        """Geometry of the box above each small country (Belgium, Netherlands) that holds
        the forces in its center zone. Rows are spaced so nothing in it overlaps."""
        s = self.token_scale()
        layouts = {}
        for name, (dx, rise) in SMALL_COUNTRY_BOX.items():
            z = self.capital_zone[name]
            owners = [o for o in sorted(self.garrisons.get(z, {}),
                                        key=lambda o: (o != name, o))
                      if units_total(self.garrisons[z][o]) > 0]
            rows = [(o, k) for o in owners for k in ("army", "air")
                    if self.garrisons[z][o][k] > 0]
            mets = [self.unit_box_metrics(k, self.garrisons[z][o][k]) for o, k in rows]
            pad = 4
            pw = max([72 * s] + [m["foot"][0] + m["foot"][2] + 8 for m in mets])
            ph = (sum(m["foot"][1] + m["foot"][3] for m in mets) + 2 * pad
                  if mets else 27 * s + 9)
            ccx, ccy = self.nation_center_screen(name)
            px0, py1 = ccx + dx * s - pw / 2, ccy - rise * s
            layouts[name] = {"z": z, "rows": rows, "mets": mets, "pad": pad,
                             "rect": [px0, py1 - ph, px0 + pw, py1],
                             "center": (ccx, ccy)}
        names = list(layouts)
        for _ in range(50):                      # keep the panels off each other
            moved = False
            for i, n1 in enumerate(names):
                for n2 in names[i + 1:]:
                    r1, r2 = layouts[n1]["rect"], layouts[n2]["rect"]
                    ox, oy = self._overlap(r1, r2)
                    if ox <= 0 or oy <= 0:
                        continue
                    moved = True
                    axis = (0, 2) if ox < oy else (1, 3)
                    amt = (ox if ox < oy else oy) / 2 + 0.5
                    sign = 1 if (r2[axis[0]] + r2[axis[1]]) >= (r1[axis[0]] + r1[axis[1]]) else -1
                    for idx in axis:
                        r1[idx] -= sign * amt
                        r2[idx] += sign * amt
            if not moved:
                break
        return layouts

    def sea_region_data(self):
        """(border lines, label spots) of the named sea regions ("North Sea Zone"...).
        Borders are the wavy edges between neighbouring sea zones that carry different
        names, joined into long lines so they can be drawn as smooth curves. A label goes
        on each connected stretch of a name. Computed once (map coordinates)."""
        if getattr(self, "_sea_regions", None) is not None:
            return self._sea_regions
        zones = self.sea_zones
        pieces = [info["edges"][nb] for z, info in zones.items() for nb in info["edges"]
                  if nb > z and zones[nb]["name"] != info["name"]]
        lines = chain_polylines(pieces)
        # labels: connected stretches of the same name; label the zone nearest the middle
        unit = (MAP_W / 36) * (MAP_H / 18)               # area of one 10 x 10 degree square
        seen, comps = set(), []
        for z0 in zones:
            if z0 in seen:
                continue
            comp, stack = [], [z0]
            seen.add(z0)
            while stack:
                cur = stack.pop()
                comp.append(cur)
                for nb in zones[cur]["edges"]:
                    if nb not in seen and zones[nb]["name"] == zones[z0]["name"]:
                        seen.add(nb)
                        stack.append(nb)
            area = sum(abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in
                               zip(zones[z]["poly"], zones[z]["poly"][1:] + zones[z]["poly"][:1])))
                       / 2 for z in comp) / unit
            comps.append((zones[z0]["name"], comp, area))
        biggest = {}
        for n, comp, area in comps:
            biggest[n] = max(biggest.get(n, 0), area)
        spots = []
        for n, comp, area in sorted(comps, key=lambda t: -t[2]):
            if area < max(2, 0.25 * biggest[n]) and area < biggest[n]:
                continue                              # skip tiny leftover pieces
            mx = sum(zones[z]["centroid"][0] for z in comp) / len(comp)
            my = sum(zones[z]["centroid"][1] for z in comp) / len(comp)
            best = min(comp, key=lambda z: (zones[z]["centroid"][0] - mx) ** 2
                       + (zones[z]["centroid"][1] - my) ** 2)
            spots.append((n, zones[best]["centroid"], area))
        self._sea_regions = (lines, spots)
        return self._sea_regions

    def zone_screen_poly(self, z):
        pts = []
        for x, y in self.zones[z]["poly"]:
            sx, sy = self.to_screen(x, y)
            pts += [sx, sy]
        return pts

    def nation_center_screen(self, name):
        cx, cy = polygon_centroid(self.cells[name])
        return self.to_screen(cx, cy)

    def draw_map(self):
        job = getattr(self, "_zoom_job", None)
        if job is not None:
            self.after_cancel(job)
            self._zoom_job = None
        self.canvas.delete("all")
        c = self.canvas

        # (The sea is the canvas background. Each sea cell used to be drawn as its own
        # invisible-to-the-eye polygon with a click binding - ~330 canvas items rebuilt on
        # every redraw. Clicks on open water are handled by the canvas-level release
        # handler via zone_at_screen, so those items, and the gridlines they hid, are gone.)

        # faint outline around every sea box (coastal and open-ocean); the darker region
        # borders and the land are drawn on top of it
        for z in self.sea_zones:
            c.create_polygon(self.zone_screen_poly(z), fill="", outline=SEA_MINOR_OUTLINE,
                             width=1, smooth=True)

        for line in self.sea_region_data()[0]:                 # thin, wavy zone borders
            pts = []
            for x, y in line:
                pts += self.to_screen(x, y)
            c.create_line(pts, fill=SEA_BORDER, width=1, smooth=True)

        # Sea-zone highlights are drawn BEFORE the land, so the land covers the part of a
        # free-form zone that reaches under it and only the real stretch of water shows.
        for z, info in self.sea_zones.items():
            if self.is_contested(z):
                c.create_polygon(self.zone_screen_poly(z), fill="", outline="#c0392b",
                                  width=3, dash=(6, 3), smooth=True)
        if self.selected_target in self.sea_zones:
            c.create_polygon(self.zone_screen_poly(self.selected_target), fill="",
                              outline="#000000", width=4, smooth=True)

        scale = self.token_scale()
        r = self.marker_radius()

        # territories: every country is split into 3 zones, colored by political
        # allegiance (red=Axis, blue=Allies, yellow=Neutral), flipping to the
        # color of whichever side actually claims them (see zone_fill)
        for z in self.zones:
            if self.is_sea_zone(z):
                continue
            tag = "zone_" + z.replace(":", "_")
            c.create_polygon(self.zone_screen_poly(z), fill=self.zone_fill(z),
                              outline="#5d6d7e", width=1, tags=(tag, "land"))
        for poly in self.cells.values():          # heavier line around each country
            pts = []
            for x, y in poly:
                sx, sy = self.to_screen(x, y)
                pts += [sx, sy]
            c.create_polygon(pts, fill="", outline="#2c3e50", width=2)
        if self.current and self.current.name in self.cells:   # highlight acting country
            pts = []
            for x, y in self.cells[self.current.name]:
                sx, sy = self.to_screen(x, y)
                pts += [sx, sy]
            c.create_polygon(pts, fill="", outline="#8e44ad", width=3.2)
        for z in self.zones:                      # opposing forces: red dashed outline
            if self.is_sea_zone(z):
                continue                          # (sea zones were outlined under the land)
            if self.is_contested(z):
                c.create_polygon(self.zone_screen_poly(z), fill="", outline="#c0392b",
                                  width=3, dash=(6, 3))
            elif self.is_unclaimed(z):        # troops inside, zone not claimed yet
                c.create_polygon(self.zone_screen_poly(z), fill="", outline="#e67e22",
                                  width=3, dash=(2, 4))
        if self.selected_target in self.zones and not self.is_sea_zone(self.selected_target):
            c.create_polygon(self.zone_screen_poly(self.selected_target), fill="",
                              outline="#000000", width=4)

        # ---- 1. queue every force box (positions are fixed up so none overlap) ----
        self._box_items = []
        step = 10 * scale

        # forces en route: dashed line from origin to destination, with boxes that
        # advance along the line each turn
        transit = []
        for off in self.pending_offensives:
            if off["origin"] not in self.zones or off["dest"] not in self.zones:
                continue
            owner = self.nations.get(off["owner"])
            ox, oy = self.to_screen(*self.zones[off["origin"]]["centroid"])
            dx, dy = self.to_screen(*self.zones[off["dest"]]["centroid"])
            c.create_line(ox, oy, dx, dy, fill=SIDE_COLOR[owner.side], width=2, dash=(6, 4))
            frac = (off["total"] - off["remaining"]) / max(1, off["total"])
            mx, my = ox + (dx - ox) * frac, oy + (dy - oy) * frac
            kinds = [k for k in ("air", "army", "navy") if off["units"][k] > 0]
            gstep = self.box_height() + 2
            top = my - (len(kinds) - 1) * gstep / 2
            group = [self.queue_box(mx, top + i * gstep, off["owner"], k, off["units"][k])
                     for i, k in enumerate(kinds)]
            transit.append((off, group))

        # stationed forces: Army and Air Force stand over land zones; Navy occupies
        # the sea zone where it is currently stationed.
        navy_at = {}
        for z, owners in self.garrisons.items():
            nation_name = self.zones[z]["nation"]
            for owner in owners:
                if not self.is_sea_zone(z) and owners[owner]["navy"] > 0:
                    navy_at.setdefault(nation_name, []).append((z, owner))
        for nation_name in navy_at:               # dotted line: country -> its naval base
            lat, lon = self.nations[nation_name].latlon
            x, y = self.to_screen(*project(lon, lat))
            alon, alat = NAVY_ANCHOR.get(nation_name, (lon, lat - 5))
            ax, ay = self.to_screen(*project(alon, alat))
            c.create_line(x, y, ax, ay, fill="#5896b5", dash=(2, 4), width=2)

        for z, owners in self.garrisons.items():
            if self.is_sea_zone(z):
                for i, owner in enumerate(sorted(owners)):
                    navy = owners[owner]["navy"]
                    if navy <= 0:
                        continue
                    position = self.force_positions.get(
                        (z, owner, "navy"), self.zones[z]["centroid"])
                    x, y = self.to_screen(*position)
                    sel = (self.current is not None and owner == self.current.name
                           and z == self.selected_force_loc)
                    self.queue_box(x, y + i * step, owner, "navy", navy, sel,
                                   (z, owner, "navy"))
                continue
            nation_name = self.zones[z]["nation"]
            if nation_name in SMALL_COUNTRY_BOX and z == self.capital_zone[nation_name]:
                continue                          # drawn in the country's box
            present = [o for o in sorted(owners, key=lambda o: (o != nation_name, o))
                       if units_total(owners[o]) > 0]
            for i, owner in enumerate(present):
                u = owners[owner]
                position = self.force_positions.get(
                    (z, owner, "army"),
                    self.force_positions.get((z, owner, "air"),
                                             self.zones[z]["centroid"]))
                x, y = self.to_screen(*position)
                sel = (self.current is not None and owner == self.current.name
                       and z == self.selected_force_loc)
                if u["army"] > 0:
                    self.queue_box(x, y + 3 * scale - i * step, owner, "army",
                                   u["army"], sel, (z, owner, "army"))
                if u["air"] > 0:
                    self.queue_box(x + 18 * scale, y - 11 * scale - i * step, owner,
                                   "air", u["air"], sel, (z, owner, "air"))
        for nation_name, fleets in navy_at.items():
            alon, alat = NAVY_ANCHOR.get(nation_name, self.nations[nation_name].latlon[::-1])
            ax, ay = self.to_screen(*project(alon, alat))
            for j, (z, owner) in enumerate(fleets):
                sel = (self.current is not None and owner == self.current.name
                       and z == self.selected_force_loc)
                self.queue_box(ax, ay + j * step, owner, "navy",
                               self.garrisons[z][owner]["navy"], sel, (z, owner, "navy"))

        # ---- 2. lay everything out so no two force boxes can overlap ----
        # Country names and their "Center" tag are FIXED at the middle of each country.
        # They never move; force boxes treat them as obstacles and shift instead.
        fsize = max(8, min(15, int(11 * scale)))
        name_spec = ("Georgia", fsize, "bold")
        center_spec = ("Consolas", max(7, int(7 * scale)), "italic bold")
        fixed_labels = []                        # (x, y, text, spec, fill, tag)
        fixed_rects = []
        # Country names are placed biggest country first (major powers before the greyed-out
        # minors). A name that would overlap one already placed is left out, and so is its
        # "* CENTER *" tag when that alone would overlap - so a zoomed-out map shows only the
        # names that have room, and the rest come back as you zoom in.
        def label_priority(nm):
            return (nm in MINOR_COUNTRIES, -abs(polygon_area(self.cells[nm])))

        placed_rects = []

        def clumped(rect):
            padded = (rect[0] - 3, rect[1] - 2, rect[2] + 3, rect[3] + 2)
            return any(self._overlap(padded, r)[0] > 0 and self._overlap(padded, r)[1] > 0
                       for r in placed_rects)

        for name in sorted(self.nations, key=label_priority):
            cx, cy = self.nation_center_screen(name)
            ctag = "zone_" + self.capital_zone[name].replace(":", "_")
            nf, cf = self.label_font(name_spec), self.label_font(center_spec)
            ny = cy - 6 * scale                  # country name, centered on the country
            gy = ny + self.label_size(name_spec, name)[1] / 2 + self.label_size(center_spec, "X")[1] / 2 - 1
            ctext = "* CENTER *"                 # identifies the country's center zone
            label_rows = ((cx, ny, name, name_spec, MINOR_TEXT if name in MINOR_COUNTRIES else "#000000"),)
            if name not in MINOR_COUNTRIES:
                label_rows += ((cx, gy, ctext, center_spec, "#2c3e50"),)
            for row_no, (tx, ty, text, spec, fill) in enumerate(label_rows):
                w, h = self.label_size(spec, text)
                rect = (tx - w / 2 - 2, ty - h / 2 - 1, tx + w / 2 + 2, ty + h / 2 + 1)
                if clumped(rect):
                    if row_no == 0:
                        break                    # no room for the name: drop the whole label
                    continue                     # no room for just the CENTER tag
                placed_rects.append(rect)
                fixed_rects.append(rect)
                fixed_labels.append((tx, ty, text, spec, fill, ctag))

        self._panel_layouts = self.small_panel_layouts()
        panel_rects = [tuple(L["rect"]) for L in self._panel_layouts.values()]
        self.layout_items(self._box_items, panel_rects + fixed_rects)

        # ---- 3. map texts: drawn only where they overlap no other text or box ----
        avoid = (list(panel_rects) + list(fixed_rects)
                 + [self.item_rect(it) for it in self._box_items])

        def chip_rect(cx, cy):
            w, h = 22 * scale, 14 * scale
            return (cx - w - 14 * scale, cy - h - 20 * scale, cx - 14 * scale, cy - 20 * scale)

        for z, info in self.zones.items():            # occupation flags also keep clear
            if not self.is_sea_zone(z):
                occ = self.zone_occupier.get(z)
                if occ is not None and self.nations[occ].alive:
                    avoid.append(chip_rect(*self.to_screen(*info["centroid"])))

        for off, group in transit:                    # "N turn(s)" under each moving stack
            if group:
                lx = sum(it["x"] for it in group) / len(group)
                ly = max(it["y"] + it["foot"][3] for it in group) + 8
                self.place_label(lx, ly, f"{off['remaining']} turn(s)",
                                 ("Consolas", 8, "bold"), "#000000", avoid)

        # country names + center text: always drawn, always at the country's center.
        # The tag lets a click on the text still select the country's center zone.
        for tx, ty, text, spec, fill, ctag in fixed_labels:
            c.create_text(tx, ty, text=text, fill=fill, font=spec, tags=ctag)
        # sea zone names, like a political wall map: "North Sea Zone", "Black Sea Zone"...
        sea_spec = (UI_FONT, max(7, int(8 * scale)), "bold")
        for name, (mx, my), size in self.sea_region_data()[1]:
            cx, cy = self.to_screen(mx, my)
            self.place_label(cx, cy, name + " Zone", sea_spec, "#06303a", avoid,
                             [(0, 0)] + [(dx * scale, dy * scale)
                                         for dy in (0, -12, 12) for dx in (-30, 30, -60, 60)])
        # zone (West/Center/East) sub-labels only appear when zoomed in
        for z, info in self.zones.items():
            if self.is_sea_zone(z):
                continue
            cx, cy = self.to_screen(*info["centroid"])
            if self.zoom >= 2.2 and z != self.capital_zone[info["nation"]]:
                short = info["name"].split("(")[1].rstrip(")")
                self.place_label(cx, cy - 16 * scale, short,
                                 ("Consolas", max(7, int(7 * scale)), "italic bold"),
                                 "#2c3e50", avoid)
            occ = self.zone_occupier.get(z)
            if occ is not None and self.nations[occ].alive:
                x0, y0, x1, y1 = chip_rect(cx, cy)
                tag = self.new_tag()
                self.draw_flag(x0, y0, x1, y1, occ, tag)
                c.create_rectangle(x0, y0, x1, y1, fill="", outline="#000000", width=1,
                                    tags=tag)

        # ---- 4. draw the force boxes on top ----
        for it in self._box_items:
            self.draw_unit_box(it["x"], it["y"], it["owner"], it["kind"], it["count"],
                               it["sel"], it["drag"])
        self.draw_small_country_boxes()
        self.draw_bot_arrow()
        self.draw_map_messages()

    def draw_bot_arrow(self):
        """Temporary arrow showing where a bot's troops just moved (single player)."""
        if not self._bot_arrow:
            return
        a, b = self._bot_arrow
        x0, y0 = self.to_screen(*self.zones[a]["centroid"])
        x1, y1 = self.to_screen(*self.zones[b]["centroid"])
        if abs(x1 - x0) + abs(y1 - y0) < 4:
            return
        w = max(4, int(5 * self.token_scale()))
        self.canvas.create_line(x0, y0, x1, y1, fill="#000000", width=w + 4,
                                arrow="last", arrowshape=(w * 3 + 4, w * 3 + 4, w * 1.5 + 2),
                                tags="botarrow")
        self.canvas.create_line(x0, y0, x1, y1, fill="#f1c40f", width=w,
                                arrow="last", arrowshape=(w * 3, w * 3, w * 1.5),
                                tags="botarrow")

    def draw_small_country_boxes(self):
        """A box above each small country holding the forces in its center zone,
        joined to the country by a plain line."""
        c = self.canvas
        self.panel_cols = []
        for name, L in self._panel_layouts.items():
            z, rows, mets, pad = L["z"], L["rows"], L["mets"], L["pad"]
            px0, py0, px1, py1 = L["rect"]
            ccx, ccy = L["center"]
            mid = (px0 + px1) / 2

            c.create_line(mid, py1, ccx, ccy, width=2, fill="#2c3e50")   # plain line
            tag = "pcol_" + z.replace(":", "_")
            c.create_rectangle(px0, py0, px1, py1,
                               fill=lighten(self.zone_fill(z), 0.6),
                               outline="#2c3e50", width=2, tags=tag)
            cursor = py0 + pad
            for (owner, kind), m in zip(rows, mets):
                l, t, r, b = m["foot"]
                sel = (self.current is not None and owner == self.current.name
                       and z == self.selected_force_loc)
                self.draw_unit_box(mid - (r - l) / 2, cursor + t, owner, kind,
                                   self.garrisons[z][owner][kind], sel,
                                   (z, owner, kind),
                                   bg=lighten(self.zone_fill(z), 0.6))
                cursor += t + b
            if self.is_contested(z):
                c.create_rectangle(px0, py0, px1, py1, fill="", outline="#c0392b",
                                   width=3, dash=(6, 3))
            elif self.is_unclaimed(z):
                c.create_rectangle(px0, py0, px1, py1, fill="", outline="#e67e22",
                                   width=3, dash=(2, 4))
            if z == self.selected_target:
                c.create_rectangle(px0, py0, px1, py1, fill="", outline="#000000", width=3)
            self.panel_cols.append((z, px0, py0, px1, py1))

    # ---------------- drag and drop ----------------

    def on_box_press(self, event, drag):
        """Mouse pressed on a force box: remember it; motion turns it into a drag."""
        if self.bot_running or self.battle_busy:
            return                         # no orders while bots move or a battle plays out
        z, owner, kind = drag
        if (not self.single_player and owner in self.nations and
                owner not in MINOR_COUNTRIES and
                (not self.current or owner != self.current.name)):
            # clicking another country's troops makes you act as that country
            self.current = self.nations[owner]
            self.acting_var.set(owner)
            self.selected_force_loc = z
        self.drag = {"loc": z, "owner": owner, "kind": kind, "sx": event.x, "sy": event.y,
                     "lx": event.x, "ly": event.y, "active": False, "hover": None}

    def on_drag_motion(self, event):
        d = self.drag
        if not d:
            return
        if not d["active"]:
            if abs(event.x - d["sx"]) + abs(event.y - d["sy"]) < 6:
                return
            if not self.current or d["owner"] != self.current.name:
                return                     # you can only drag your own forces
            force = self.get_force(d["loc"], d["owner"])
            if not force:
                return
            d["active"] = True
            self.canvas.config(cursor="fleur")
            # a ghost copy of the box follows the mouse
            self.draw_unit_box(event.x, event.y, d["owner"], d["kind"], force[d["kind"]],
                               True, tag="ghost")
        else:
            self.canvas.move("ghost", event.x - d["lx"], event.y - d["ly"])
        d["lx"], d["ly"] = event.x, event.y
        z = self.zone_at_screen(event.x, event.y)     # highlight the zone under the mouse
        if z != d["hover"]:
            self.canvas.delete("hl")
            d["hover"] = z
            if z and z != d["loc"]:
                self.canvas.create_polygon(self.zone_screen_poly(z), fill="",
                                            outline="#f1c40f", width=4, tags="hl",
                                            smooth=self.is_sea_zone(z))
                if self.is_sea_zone(z):               # slide it under the land: water only
                    self.canvas.tag_lower("hl", "land")
        self.canvas.tag_raise("ghost")

    def on_drag_release(self, event):
        d = self.drag
        self.drag = None
        if self.bot_running or self.battle_busy:
            return
        if not d:
            z = self.zone_at_screen(event.x, event.y)
            if z:
                self.select_target(z)
            return
        self.canvas.delete("ghost")
        self.canvas.delete("hl")
        self.canvas.config(cursor="")
        if not d["active"]:                # a plain click on a box
            if self.current and d["owner"] == self.current.name:
                self.selected_force_loc = d["loc"]
                self.refresh_view()
            else:
                self.select_target(d["loc"])
            return
        dest = self.zone_at_screen(event.x, event.y)
        if dest and dest != d["loc"]:
            drop_point = ((event.x - self.pan_x) / self.zoom,
                          (event.y - self.pan_y) / self.zoom)
            self.after_idle(self.send_forces, d["loc"], dest, d["kind"], drop_point)

    def select_target(self, z):
        self.selected_target = z
        terrain = TERRAIN_EFFECTS[self.terrain_of(z)][0]
        self.target_var.set(self.zone_label(z) if self.is_sea_zone(z)
                            else f"{self.zone_label(z)} ({terrain})")
        sides = self.battle_sides(z, self.current)
        if sides:                          # opposing armies here: offer to fight
            att, dfn = sides
            # every friendly country with air force in this zone can bomb (even if it has
            # no troops here): 1 bombing per country per battle, BOMBINGS_PER_COUNTRY in total per country
            bombers = {o: self.nations[o].bombing_uses
                       for o, u in self.garrisons[z].items()
                       if u.get("air", 0) > 0 and self.nations[o].alive
                       and self.nations[o].bombing_uses > 0
                       and (o == self.current.name
                            or self.are_allies(self.current, self.nations[o]))}
            self.show_battle_panel(z, att, dfn, bombers)
            return
        claim = self.claim_sides(z, self.current)
        if claim:                          # undefended enemy zone with rested troops in it
            self.draw_map()
            self.refresh_info()
            self.show_claim_panel(z, claim)
            return
        self.draw_map()
        self.refresh_info()

    # ---------------- zoom / pan ----------------

    def zoom_at(self, mx, my, factor, immediate=False):
        """Zoom about screen point (mx, my). The mouse wheel fires many events, so it only
        rescales what is on the canvas and does the exact redraw once it settles. The
        zoom buttons and +/- keys are single clicks: they redraw right away
        (immediate=True) so the map updates at once instead of waiting for a later event."""
        new_zoom = max(0.4, min(10.0, self.zoom * factor))
        factor = new_zoom / self.zoom
        if abs(factor - 1) < 1e-9:
            return
        self.pan_x = mx - (mx - self.pan_x) * factor
        self.pan_y = my - (my - self.pan_y) * factor
        self.zoom = new_zoom
        self._user_zoomed = True                          # bots must not override a manual zoom
        job = getattr(self, "_zoom_job", None)
        if job is not None:
            self.after_cancel(job)
            self._zoom_job = None
        if immediate:
            self.draw_map()
            self.canvas.update_idletasks()                # paint now, don't wait for a mouse move
            return
        self.canvas.scale("all", mx, my, factor)         # instant, approximate feedback
        self.draw_map_messages()                          # the text stays put at the top
        self._zoom_job = self.after(140, self._finish_zoom)   # exact redraw when it settles

    def _finish_zoom(self):
        self._zoom_job = None
        self.draw_map()
        self.canvas.update_idletasks()

    def on_zoom_wheel(self, event):
        if getattr(event, "num", None) == 4:
            up = True
        elif getattr(event, "num", None) == 5:
            up = False
        else:
            up = event.delta > 0
        self.zoom_at(event.x, event.y, 1.1 if up else 1 / 1.1)

    def on_pan_start(self, event):
        self._pan_start = (event.x, event.y, self.pan_x, self.pan_y)
        self._pan_last = (event.x, event.y)

    def on_pan_move(self, event):
        if not self._pan_start:
            return
        sx, sy, ox, oy = self._pan_start
        lx, ly = getattr(self, "_pan_last", (sx, sy))
        self.pan_x = ox + (event.x - sx)
        self.pan_y = oy + (event.y - sy)
        # slide what is already on the canvas instead of redrawing ~500 zones per mouse
        # event; the exact redraw happens once, when the button is released
        self.canvas.move("all", event.x - lx, event.y - ly)
        self.draw_map_messages()                          # the text stays put at the top
        self._pan_last = (event.x, event.y)
        self._pan_moved = True

    def on_pan_end(self, event):
        self._pan_start = None
        if getattr(self, "_pan_moved", False):
            self._pan_moved = False
            self.draw_map()

    def reset_view(self):
        self.zoom = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.draw_map()

    def focus_on(self, lon, lat, zoom):
        """Center the map on a lon/lat point at the given zoom level."""
        x, y = project(lon, lat)
        self.zoom = zoom
        self.pan_x = MAP_W / 2 - x * zoom
        self.pan_y = MAP_H / 2 - y * zoom
        self.draw_map()

    def pan_to_zone(self, z, min_zoom=3.0):
        """Move the camera to zone z (zooming in to at least min_zoom) and redraw."""
        if z not in self.zones or not hasattr(self, "canvas"):
            return
        x, y = self.zones[z]["centroid"]
        self.zoom = max(self.zoom, min_zoom)
        self.pan_x = MAP_W / 2 - x * self.zoom
        self.pan_y = MAP_H / 2 - y * self.zoom
        self.draw_map()
        self.update_idletasks()

    # ---------------- setup ----------------

    def welcome_dialog(self):
        outer = tk.Frame(self, bg=BG_MAIN)          # covers the main window (no new window)
        outer.place(x=0, y=0, relwidth=1, relheight=1)
        outer.lift()
        win = tk.Frame(outer, bg=BG_MAIN)
        win.place(relx=0.5, rely=0, anchor="n", relheight=1, width=640)

        head = tk.Frame(win, bg=HEADER_BG)
        head.pack(fill="x")
        tk.Label(head, text="WORLD WAR II", font=("Georgia", 24, "bold"),
                 fg=HEADER_FG, bg=HEADER_BG).pack(pady=(18, 0))
        tk.Label(head, text="Grand Strategy Simulation  \u00b7  1939 \u2013 1946",
                 font=(UI_FONT, 11), fg="#9fb3c8", bg=HEADER_BG).pack(pady=(0, 16))

        footer = tk.Frame(win, bg=BG_MAIN)
        footer.pack(side="bottom", fill="x", pady=14)

        # ---- game mode: hotseat (everyone) or single player (one country vs bots) ----
        mode_card = make_card(footer, "Game mode")
        mode_card.pack(fill="x", padx=16, pady=(0, 12))
        mode_var = tk.StringVar(value="hotseat")
        majors = self.controlled_nations()
        country_choices = [f"{n.name}  ({n.side})" for n in majors]
        country_var = tk.StringVar(value=country_choices[0])

        def sync_mode(*_):
            combo.config(state="readonly" if mode_var.get() == "single" else "disabled")

        for value, text in (("hotseat", "Hotseat - a group plays every country on one device"),
                            ("single", "Single player - you play one country, bots play the rest")):
            tk.Radiobutton(mode_card, text=text, variable=mode_var, value=value,
                           command=sync_mode, bg=BG_CARD, activebackground=BG_CARD,
                           fg=FG_TEXT, selectcolor=BG_CARD, anchor="w",
                           font=(UI_FONT, 10)).pack(fill="x", padx=10, pady=1)
        pick = tk.Frame(mode_card, bg=BG_CARD)
        pick.pack(fill="x", padx=10, pady=(2, 10))
        tk.Label(pick, text="Your country:", bg=BG_CARD, fg=FG_TEXT,
                 font=(UI_FONT, 10)).pack(side="left", padx=(22, 8))
        combo = ttk.Combobox(pick, textvariable=country_var, values=country_choices,
                             state="disabled", font=(UI_FONT, 10), width=26)
        combo.pack(side="left")

        body = make_card(win)
        body.pack(fill="both", expand=True, padx=16, pady=(14, 0))
        txt = tk.Text(body, wrap="word", bg=BG_CARD, fg=FG_TEXT, relief="flat",
                      font=(UI_FONT, 10), padx=16, pady=10, highlightthickness=0,
                      cursor="arrow", spacing2=2)
        sb = ttk.Scrollbar(body, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        txt.pack(fill="both", expand=True)
        txt.tag_configure("h", font=(UI_FONT, 11, "bold"), foreground=ACCENT,
                          spacing1=10, spacing3=3)
        txt.tag_configure("b", spacing3=2)
        for side, color in SIDE_DARK.items():
            txt.tag_configure("side_" + side, foreground=color, font=(UI_FONT, 10, "bold"))

        penalty = int(round((1 - ATTACKER_PENALTY) * 100))
        sections = [
            ("The table",
             "A group shares one device. Each of the 16 major powers is playable: pick "
             "one in the \"Acting as\" box, or just click any country's troops on the map "
             "to act as that country. Everyone on the same side is automatically an ally; "
             "Neutral countries are free agents. In SINGLE PLAYER mode you choose one "
             "country and can only move that country; every other power is run by a bot "
             "that plays its own War Phase automatically when you press End Phase."),
            ("Zones and armies",
             "Each country is split into 3 zones (Belgium and Netherlands have a single "
             "center zone, shown in a box above the country). Zones are red for Axis, blue "
             "for Allied and yellow for Neutral, and flip color once the opposing side's "
             "troops claim them (arriving is not enough - they must attack). Armies are boxes carrying the owner's flag: T = Troops, "
             "anchor = Navy, wing = Air Force. Every January each country whose center zone "
             "is still free is topped up with troops there to match its real historical army "
             "size for that year (1 troop = 250 soldiers)."),
            ("Moving and attacking",
             "There is no movement phase: on your side's War Phase you can both move and "
             "battle. Drag one of your force boxes onto a zone, then choose how much to "
             "send: 10%, 25%, 50% or All. Troops crossing the sea need Navy (1 per troop), and "
             "a fleet can only land them on zones that border its own sea zone - sail it "
             "next to the coast first. "
             "Distant targets take a few turns. There is no limit on attacks per turn, "
             "but units that move or fight must rest until your side's next turn."),
            ("Battles",
             "Moving into an enemy-held zone does not start a fight by itself. Click the "
             "red-outlined zone during a war phase to start the battle. Only troops (on land) "
             f"and navy (at sea) fight; air force only bombs ({BOMBINGS_PER_COUNTRY} per country, 1 per battle, "
             "-10% enemy power each; bombings from different countries stack, and defenders "
             "with air force can bomb the attackers too). The side whose turn "
             f"it is fights at -{penalty}%, so defenders have the edge. Winning takes "
             "territory and a share of the loser's oil."),
            ("Oil and objectives",
             "Oil is your only resource: it is produced each year (but 10% of your stockpile is "
             "lost every new year), can be traded, and is "
             "captured in victory. Your country has a chain of objectives that follows its "
             "part in the real war: achieve the current one, claim its oil reward during "
             "your War Phase, and the next objective appears."),
            ("The calendar",
             "Each End Phase advances 2 months (6 turns = 1 year). Phases alternate: Axis "
             "War Phase, then Allied War Phase. The war ends at the start of 1946. Tip: use "
             "the Europe button to zoom in on the crowded European armies."),
        ]
        for heading, text in sections:
            txt.insert("end", heading + "\n", "h")
            txt.insert("end", text + "\n", "b")
        txt.insert("end", "Sides\n", "h")
        for side, label in (("Axis", "Axis"), ("Allies", "Allies"), ("Neutral", "Neutral")):
            names = [row[0] for row in NATION_DATA
                     if row[1] == side and row[0] not in MINOR_COUNTRIES]
            txt.insert("end", label + ": ", "side_" + side)
            txt.insert("end", ", ".join(names) + "\n", "b")
        txt.config(state="disabled")

        def begin():
            chosen = None
            if mode_var.get() == "single":
                chosen = country_var.get().split("  (")[0]
            outer.destroy()
            self.begin_game(chosen)

        make_button(footer, "Begin Simulation", begin, "primary", 12, padx=26,
                    pady=8).pack()
        self.wait_window(outer)

    def begin_game(self, player_name=None):
        """Start the game. player_name=None -> hotseat; otherwise single player as that
        country, with bots running every other major power."""
        self.player_name = player_name
        if player_name:
            self.roll_variation()
            p = self.nations[player_name]
            self.current = p
            self.selected_force_loc = self.capital_zone[player_name]
            self.mode_var.set(f"SINGLE PLAYER  \u00b7  you command {player_name}")
            self.mode_label.pack(fill="x", pady=(0, 6), before=self.acting_card)
            self.log_msg("Historical events keep their dates, but the bots play a little "
                         "differently every game.")
            self.log_msg(f"Single player: you command {player_name} ({p.side}). Every other "
                         f"country is played by a bot, which moves when its side's War Phase "
                         f"comes round. Press End Phase when you are done with your orders.")
            self.map_hint.config(
                text="Drag one of your force boxes onto a zone to send it, then pick 10% / 25% / "
                     "50% / All. Red dashed outline = opposing armies: click the zone to fight. "
                     "Dashed line = forces en route. Press End Phase when you are done; the bots "
                     "then play their phases.")
            lat, lon = p.latlon
            self.focus_on(lon, lat, 2.0 if p.name not in SMALL_COUNTRY_BOX else 6.0)
        else:
            self.mode_var.set("")
            self.log_msg("The simulation begins in 1939. Position your forces, then pass the "
                         "device around the table as each country takes its turn.")
        self.refresh_all()
        if self.single_player:
            # let the window finish drawing, then let any bots that act before you move
            self.after(100, self.start_bots)

    # ---------------- info / status refresh ----------------

    @property
    def single_player(self):
        return self.player_name is not None

    @property
    def player(self):
        return self.nations[self.player_name] if self.player_name else None

    def is_bot(self, n):
        """In single player, every major power except the player's is run by a bot."""
        return (self.single_player and n.name != self.player_name
                and n.name not in MINOR_COUNTRIES)

    def controlled_nations(self):
        if self.single_player:
            return [self.player]          # you can only ever act as your own country
        # the 16 major powers are playable (minor countries are just places on the map);
        # list Axis first since the turn starts as Axis
        return sorted((n for n in self.nations.values() if n.name not in MINOR_COUNTRIES),
                       key=lambda n: (self.SIDE_ORDER.get(n.side, 9), n.name))

    def refresh_all(self):
        self.date_var.set(self.date_label() + ("  (Winter)" if self.is_winter_now() else ""))
        self.phase_var.set(self.phase.upper())
        axis = self.phase.startswith("Axis")
        self.phase_badge.config(bg=SIDE_COLOR["Axis" if axis else "Allies"])
        names = [n.name for n in self.controlled_nations()]
        self.acting_combo.config(state="disabled" if self.single_player else "readonly")
        self.acting_combo["values"] = names
        if self.current and self.current.name in names:
            self.acting_var.set(self.current.name)
        elif names:
            self.acting_var.set(names[0])
            self.current = self.nations[names[0]]
        self.refresh_view()

    def refresh_view(self):
        self.refresh_forces_list()
        self.draw_map()
        self.refresh_info()
        self.update_button_states()

    def on_acting_change(self, event=None):
        name = self.acting_var.get()
        if self.single_player or self.battle_busy:
            return
        if name in self.nations:
            self.current = self.nations[name]
            self.refresh_view()

    def refresh_forces_list(self):
        p = self.current
        self.force_list.delete(0, "end")
        self.force_locs = []
        if not p:
            self.selected_force_loc = None
            return
        cap = self.capital_zone[p.name]
        locs = sorted(self.owned_force_locations(p.name), key=lambda z: (z != cap, z))
        for z in locs:
            u = self.garrisons[z][p.name]
            resting = self.locked_units(z, p.name)
            note = f"  (resting: {units_text(resting, True)})" if units_total(resting) else ""
            where = self.zone_label(z) + ("*" if z == cap else "")
            self.force_list.insert("end", f"{where}: {units_text(u, True)}{note}")
            self.force_locs.append(z)
        if self.selected_force_loc not in self.force_locs:
            self.selected_force_loc = self.force_locs[0] if self.force_locs else None
        if self.selected_force_loc in self.force_locs:
            self.force_list.selection_set(self.force_locs.index(self.selected_force_loc))

    def on_force_list_select(self, event=None):
        sel = self.force_list.curselection()
        if sel and sel[0] < len(self.force_locs):
            self.selected_force_loc = self.force_locs[sel[0]]
            self.draw_map()
            self.refresh_info()

    def refresh_info(self):
        ib = self.info_box
        ib.config(state="normal")
        ib.delete("1.0", "end")
        p = self.current
        if not p:
            ib.config(state="disabled")
            return

        def put(text, *tags):
            ib.insert("end", text, tags)

        def kv(key, value, *tags):
            put(f"{key}: ", "key")
            put(f"{value}\n", *tags)

        put(p.name, "title")
        put(f"   {p.side}", "side_" + p.side)
        if not p.alive:
            put("   DEFEATED", "bad")
        put("\n")
        kv("Zones held", f"{p.zones_held}/{p.zone_count}  ({p.territory}%)")
        kv("Stability", p.stability)
        kv("Oil", f"{p.oil}  (+{p.oil_income()}/yr)")
        kv("Iron", f"{p.iron}  (+{p.iron_income()}/yr)")
        kv("Ratings", f"Army {p.army_rating}/10   Navy {p.navy_rating}/10   "
                  f"Air {p.air_rating}/10")
        kv("Bombing uses", f"{p.bombing_uses}/{BOMBINGS_PER_COUNTRY}")
        kv(f"Troops in {int(self.year)}", f"+{self.yearly_troops(p)} yearly reinforcement")
        total = self.nation_units(p.name)
        kv("Forces", f"Troops {total['army']}   Navy {total['navy']}   Air {total['air']}")
        kv("At war with", ", ".join(sorted(p.at_war_with)) if p.at_war_with else "none")
        if self.can_attack_now(p):
            kv("Attack this turn", "unlimited", "good")

        total_obj = len(p.objectives)
        if p.objective_claimed:
            put("Objectives\n", "h")
            put(f"All {total_obj} objectives complete\n", "good")
        else:
            put(f"Objective {p.objective_index + 1} of {total_obj}\n", "h")
            put(p.objective + "\n")
            put(f"Reward: +{self.reward_oil(p)} oil, +{self.reward_iron(p)} iron (unclaimed)\n", "dim")
            for text, met in p.objective_progress(self.year):
                put(("  \u2713 " if met else "  \u25cb ") + text + "\n",
                    "good" if met else "dim")

        z = self.selected_target
        if z in self.zones:
            if self.is_sea_zone(z):
                put(self.zone_label(z) + "\n", "h")
                present = [f"{o}: {units_text(u)}" for o, u in self.garrisons.get(z, {}).items()
                           if units_total(u) > 0]
                kv("Forces there", ", ".join(present) if present else "none")
                put("Navy-only zone\n", "good")
                if self.is_contested(z):
                    put("CONTESTED: click this zone to start the battle\n", "bad")
                if self.selected_force_loc and self.selected_force_loc != z:
                    turns = self.travel_turns(self.selected_force_loc, z)
                    put(f"Travel time: {turns} turn(s) from selected force\n", "dim")
                ib.config(state="disabled")
                return
            home = self.nations[self.zone_nation(z)]
            ctrl = self.controller(z)
            put(self.zone_label(z) + "\n", "h")
            kv("Country", f"{home.name} ({home.side})")
            kv("Held by", ctrl or "nobody")
            present = [f"{o}: {units_text(u)}" for o, u in self.garrisons.get(z, {}).items()
                       if units_total(u) > 0]
            kv("Forces there", ", ".join(present) if present else "none")
            if self.is_contested(z):
                if self.battle_sides(z, p):
                    put("CONTESTED: click this zone to start the battle\n", "bad")
                else:
                    put("CONTESTED: opposing armies here. A battle needs your side's War "
                        "Phase and rested (not resting) forces of your side in the zone.\n",
                        "bad")
            if self.claim_sides(z, p):
                put("UNCLAIMED: click this zone to attack and claim it\n", "bad")
            elif self.is_unclaimed(z):
                put("NOT CLAIMED YET: troops are in the zone, but they must attack it "
                    "(War Phase, at least one rested troop) to take it.\n", "bad")
            if self.is_attack(p, z):
                put("Enemy zone: drop forces here, then attack to claim it\n", "bad")
            else:
                put("Friendly zone\n", "good")
            if self.selected_force_loc and self.selected_force_loc != z:
                turns = self.travel_turns(self.selected_force_loc, z)
                if turns <= 0:
                    put("Adjacent: forces arrive immediately\n", "dim")
                else:
                    put(f"Travel time: {turns} turn(s) from selected force\n", "dim")
        ib.config(state="disabled")

    def update_button_states(self):
        p = self.current
        alive = p.alive if p else False
        can_move = alive and self.can_attack_now(p)
        can_claim = can_move and not p.objective_claimed
        self.btn_trade.config(state="normal" if can_move else "disabled")
        self.btn_objectives.config(state="normal" if can_claim else "disabled")
        if self.game_over or self.bot_running or self.battle_busy:
            self.btn_end.config(state="disabled")
        else:
            self.btn_end.config(state="normal")

    def log_msg(self, text):
        tag = None
        if text.startswith("BATTLE") or "defeated" in text or "conquers" in text:
            tag = "battle"
        if "Food shortage" in text:
            tag = "food_shortage"
        elif "Extra supply" in text:
            tag = "extra_supply"
        elif text.startswith("HISTORICAL"):
            tag = "event"
        elif "liberated" in text or "achieves" in text:
            tag = "good"
        self.log.insert("end", f"[{self.date_label()}] ", "date")
        self.log.insert("end", f"{text}\n", (tag,) if tag else ())
        self.log.see("end")

    # ---------------- phase rules ----------------

    def can_attack_now(self, p):
        # In single-player mode the human's control is gated separately from the
        # temporary phase used while bots animate. Bots still need to be able to
        # resolve battles and claim zones during their own automatic phase.
        if self.single_player:
            if self.bot_running and p is not None and self.is_bot(p):
                if not p.alive:
                    return False
                if self.phase == "Axis War Phase":
                    return p.side == "Axis"
                if self.phase == "Allied War Phase":
                    return p.side in ("Allies", "Neutral")
                return False
            return bool(self.player_turn_active and p is self.player and p.alive)
        if self.phase == "Axis War Phase":
            return p.side == "Axis"
        if self.phase == "Allied War Phase":
            return p.side in ("Allies", "Neutral")
        return False

    def is_attack(self, p, z):
        """Sending forces to zone z is an attack if its controller is hostile or
        hostile forces are standing there (e.g. liberating an occupied ally)."""
        ctrl = self.controller(z)
        return (ctrl is not None and self.is_hostile(p.name, ctrl)) or bool(
            self.hostile_forces_at(z, p.name))

    # ---------------- travel time between nations ----------------

    def can_move_one_space(self, from_zone, to_zone):
        """Return whether an army can walk to this land zone in one move: it must share a
        border with the zone it starts in, and it can't step straight into the center of
        another country (it has to fight through that country's border zones first)."""
        if from_zone == to_zone or self.is_sea_zone(from_zone) or self.is_sea_zone(to_zone):
            return False
        if to_zone not in self.land_adj.get(from_zone, ()):
            return False
        if self.region(from_zone) != self.region(to_zone):
            return False                      # separate landmasses (e.g. Britain): needs a navy
        if (self.zone_nation(from_zone) != self.zone_nation(to_zone)
                and self.is_inner_zone(to_zone)):
            return False
        return True

    def is_inner_zone(self, z):
        """True for a country's Center zone when it has outer zones protecting it
        (Belgium and the Netherlands only have a Center zone, so it counts as a border)."""
        nation = self.zone_nation(z)
        return nation not in SINGLE_ZONE_COUNTRIES and z == self.capital_zone.get(nation)

    def air_steps(self, a, b):
        """Number of zones (borders crossed) between a and b for the air force, or None
        if b is further than AIR_MOVE_SPACES away."""
        seen, frontier = {a}, {a}
        for steps in range(1, AIR_MOVE_SPACES + 1):
            frontier = {n for z in frontier for n in self.air_adj.get(z, ())} - seen
            if b in frontier:
                return steps
            seen |= frontier
        return None

    def sea_path(self, a, b):
        """Shortest chain of neighbouring sea zones from sea zone a to sea zone b
        (list of zone ids, a first), or None if they aren't connected."""
        if a == b:
            return [a]
        prev, queue = {a: None}, [a]
        for cur in queue:
            for nb in self.zones[cur].get("edges", ()):
                if nb in prev or not self.is_sea_zone(nb):
                    continue
                prev[nb] = cur
                if nb == b:
                    path = [b]
                    while prev[path[-1]] is not None:
                        path.append(prev[path[-1]])
                    return path[::-1]
                queue.append(nb)
        return None

    def navy_steps(self, a, b):
        """Number of sea zones a fleet moves through to get from sea zone a to b
        (None if it is further than NAVY_MOVE_ZONES away or there is no sea route)."""
        path = self.sea_path(a, b)
        if path is None or len(path) - 1 > NAVY_MOVE_ZONES:
            return None
        return len(path) - 1

    def navy_range_message(self, dest):
        return ("Out of range",
                f"A fleet can only sail through {NAVY_MOVE_ZONES} sea zones in one move, "
                f"and {self.zone_label(dest)} is further than that (or has no sea route). "
                f"Move it part of the way first.")

    def can_enter_center(self, p, z):
        """Troops arriving by sea or air can't land straight in a foreign country's center."""
        return not (self.is_inner_zone(z) and self.zone_nation(z) != p.name)

    def can_land_on(self, fleet_zone, dest):
        """A fleet in sea zone `fleet_zone` can only put troops ashore on a land zone
        that borders that sea zone."""
        return dest in self.sea_land_adj.get(fleet_zone, ())

    def coast_message(self, fleet_zone, dest):
        """(title, text) explaining why a fleet can't land troops on `dest`."""
        names = sorted(self.zone_label(z) for z in self.sea_land_adj.get(fleet_zone, ()))
        if names:
            shown = ", ".join(names[:6]) + (" and more" if len(names) > 6 else "")
            where = f"This fleet's sea zone only borders: {shown}."
        else:
            where = "This fleet's sea zone doesn't touch any coast."
        return ("Not on this coast",
                f"A fleet can only land troops on a zone that borders its own sea zone, and "
                f"{self.zone_label(dest)} doesn't. {where} Sail the fleet to a sea zone next "
                f"to {self.zone_label(dest)} first, then land the troops.")

    def landing_source(self, p, dest):
        """(zone, rested troops) of the biggest stack a fleet can ferry troops from, or
        (None, 0). The landing zone itself never counts - otherwise the troops already
        there would be 'shipped' back onto it and reset, instead of reinforcing it -
        and neither does a beachhead the country is still fighting for."""
        best = (None, 0)
        for loc in self.owned_force_locations(p.name):
            if self.is_sea_zone(loc) or loc == dest:
                continue
            ctrl = self.controller(loc)
            if (ctrl is not None and self.is_hostile(p.name, ctrl)) or self.is_contested(loc):
                continue
            n = self.available_units(loc, p.name)["army"]
            if n > best[1]:
                best = (loc, n)
        return best

    def travel_turns(self, from_zone, to_zone):
        if from_zone == to_zone:
            return 0
        if self.zone_nation(to_zone) in SMALL_COUNTRY_BOX:
            return 0                      # small countries: forces arrive instantly
        dist = haversine_km(self.zone_latlon(from_zone), self.zone_latlon(to_zone))
        return min(MAX_TRAVEL_TURNS, int(dist // KM_PER_TRAVEL_TURN))

    def region(self, zone):
        name = self.zone_nation(zone) if ":" in zone else zone
        return REGION.get(name, name)

    # ---------------- player actions (operate on self.current) ----------------

    def send_forces(self, src, dest, default_kind=None, drop_point=None):
        """A force box was dragged from zone `src` and dropped on zone `dest`."""
        p = self.current
        cur = self.get_force(src, p.name) if p else None
        if not cur:
            self.show_message("No force", "There is no force of yours there to send.")
            return
        if not p.alive:
            return
        dest_label = self.zone_label(dest)

        attack = self.is_attack(p, dest)
        if not self.can_attack_now(p):
            self.show_message(
                "Not your turn",
                f"It's the {self.phase}. Axis countries act in the Axis War Phase; "
                f"Allied and Neutral countries act in the Allied War Phase.")
            return

        avail = self.available_units(src, p.name)
        transport_source = None
        transport_avail = 0
        # Airlift: the air force in this zone can fly rested troops from the same zone to
        # another land zone within range (the planes stay behind and rest for a turn).
        airlift_avail = 0
        if default_kind == "air" and not self.is_sea_zone(src) and not self.is_sea_zone(dest):
            if self.air_steps(src, dest) is None:
                self.show_message(
                    "Out of range",
                    f"Air force can only fly {AIR_MOVE_SPACES} zones in one move.")
                return
            if avail["army"] > 0 and avail["air"] > 0 and self.can_enter_center(p, dest):
                airlift_avail = min(avail["army"], avail["air"] * TROOPS_PER_PLANE)
        if self.is_sea_zone(src) or self.is_sea_zone(dest):
            if (default_kind == "navy" and self.is_sea_zone(src) and self.is_sea_zone(dest)
                    and self.navy_steps(src, dest) is None):
                self.show_message(*self.navy_range_message(dest))
                return
            avail = new_units(navy=avail["navy"])
            if default_kind == "navy" and self.is_sea_zone(src) and not self.is_sea_zone(dest):
                if not self.can_land_on(src, dest):
                    self.show_message(*self.coast_message(src, dest))
                    return
                transport_source, largest_stack = self.landing_source(p, dest)
                if transport_source is not None:
                    transport_avail = min(largest_stack, avail["navy"] * TROOPS_PER_SHIP)
                elif avail["navy"] > 0:
                    # Ships can only ferry troops ashore - they never sail onto land (that
                    # used to strand the fleet and made a second landing impossible).
                    self.show_message(
                        "No troops to land",
                        f"{p.name} has no rested troops that the fleet can ferry to "
                        f"{dest_label}. The troops must be standing on land elsewhere "
                        f"(not in the zone being landed on, and not in a contested or "
                        f"enemy-held zone) and must not be resting. The fleet stays at sea.")
                    return
        elif default_kind in UNIT_KEYS:
            avail = new_units(**{default_kind: avail[default_kind]})
        if units_total(avail) <= 0:
            wait = self.rest_turns_left(src, p.name)
            self.show_message("Forces resting",
                                 f"These forces moved recently and are resting. They can "
                                 f"move or attack again in {wait} turn(s).")
            return

        verb = "attack" if attack else "move to"
        kind_label = UNIT_TYPES[default_kind]["label"].lower()
        if transport_avail > 0 and default_kind == "navy":
            kind_label = "troops"      # landing from the sea: troops are the only choice
        self.show_send_panel(
            "Send Forces",
            f"{p.name}: how many {kind_label} to {verb} "
            f"{dest_label}?",
            avail,
            default_kind,
            lambda sent, airlift=False: self.commit_send_forces(
                src, dest, p, attack, sent, drop_point, transport_source, airlift),
            transport_avail,
            airlift_avail,
        )

    def commit_send_forces(self, src, dest, p, attack, sent, drop_point=None,
                           transport_source=None, airlift=False):
        """Commit a movement after the inline send panel is confirmed."""
        err = self.execute_send(src, dest, p, attack, sent, drop_point,
                                transport_source, airlift)
        if err:
            if err[1]:
                self.show_message(err[0], err[1])
            return
        self.refresh_all()

    def execute_send(self, src, dest, p, attack, sent, drop_point=None,
                     transport_source=None, airlift=False):
        """Validate and carry out a movement/attack order (no dialogs, no redraw).
        Returns None on success, or (title, message) describing why it was refused.
        Used by both the send panel and the single-player bots."""
        cur = self.get_force(src, p.name)
        if not cur:
            return (None, None)

        # A movement order may only use troops that are actually rested at its
        # originating zone.  The bot planner uses available_units(), but this
        # validator is the final authority; without this check a bot could reuse
        # the full garrison from a zone even when part of it was still resting.
        # This also protects human orders and any future bot movement code that
        # calls execute_send() directly.
        available = self.available_units(src, p.name)
        # During an amphibious landing, the navy comes from `src`, while the army
        # comes from `transport_source`. Do not require the fleet's sea zone to
        # contain the army being carried.
        if transport_source is not None and sent["army"] > 0:
            for k in UNIT_KEYS:
                if k != "army" and sent[k] > available[k]:
                    return (None, None)
            transport_available = self.available_units(transport_source, p.name)
            if sent["army"] > transport_available["army"]:
                return (None, None)
        else:
            for k in UNIT_KEYS:
                if sent[k] > available[k]:
                    return (None, None)

        dest_label = self.zone_label(dest)

        if (sent["navy"] > 0 and sent["army"] == 0 and self.is_sea_zone(src)
                and self.is_sea_zone(dest) and self.navy_steps(src, dest) is None):
            return self.navy_range_message(dest)

        # A fleet can never end up standing on a land zone: it only ferries troops ashore
        # and stays at sea, so it can keep landing troops every turn.
        if (sent["navy"] > 0 and sent["army"] == 0 and self.is_sea_zone(src)
                and not self.is_sea_zone(dest)):
            return ("Fleets stay at sea",
                    "A fleet can't sail onto land. Drag it onto a coastal zone to land "
                    "troops from it, or onto another sea zone to move it.")

        if airlift:
            if cur["army"] < sent["army"] or cur["air"] < sent["air"]:
                return (None, None)
            if self.air_steps(src, dest) is None or not self.can_enter_center(p, dest):
                return ("Can't airlift there",
                        "That zone is out of range, or is another country's "
                        "center, which troops can't reach directly.")

        if transport_source is not None and sent["army"] > 0:
            transport_force = self.get_force(transport_source, p.name)
            if not transport_force or transport_force["army"] < sent["army"]:
                return (None, None)
            if transport_source == dest:
                return ("Can't land there",
                        "Troops can't be ferried from the zone they are landing in.")
            if not self.can_land_on(src, dest):
                return self.coast_message(src, dest)

        if sent["army"] > 0 and not airlift and self.region(src) != self.region(dest):
            ships_needed = -(-sent["army"] // TROOPS_PER_SHIP)
            if sent["navy"] < ships_needed:
                return ("Naval transport needed",
                        f"Troops crossing the sea need Navy to carry them: "
                        f"1 Navy per {TROOPS_PER_SHIP} troops. Sending {sent['army']} troops "
                        f"needs at least {ships_needed} Navy in the group.")
        if (sent["army"] > 0 and transport_source is None and not airlift
                and not self.can_move_one_space(src, dest)):
            return ("Move one space at a time",
                    "Troops can only move to a zone that shares a border with where they "
                    "stand, and can't go straight into another country's center. Fight "
                    "through its border zones first.")

        if transport_source is not None and sent["army"] > 0 and not self.can_enter_center(p, dest):
            return ("Can't land there",
                    "Troops can't land straight in another country's center. "
                    "Land in a border zone first.")

        # commit the order (troops are only removed once every check has passed)
        if transport_source is not None and sent["army"] > 0:
            transport_force = self.get_force(transport_source, p.name)
            self.set_force(transport_source, p.name,
                           {k: transport_force[k] - (sent["army"] if k == "army" else 0)
                            for k in UNIT_KEYS})
            cur = self.get_force(src, p.name) or new_units()
        if airlift and sent["army"] > 0:
            # Airlift: the troops and the planes carrying them fly to the destination
            # together and rest there for a turn.
            sent = new_units(army=sent["army"], air=min(sent["air"], cur["air"]))
            self.set_force(src, p.name, {k: cur[k] - sent[k] for k in UNIT_KEYS})
        elif transport_source is not None and sent["army"] > 0:
            # Amphibious landing: the fleet only ferries the troops. It stays at sea
            # (resting for a turn) so it can pick up and carry more troops later,
            # instead of sailing onto the land zone and getting stuck there.
            ships_used = min(sent["navy"], cur["navy"])
            self.add_lock(src, p.name, new_units(navy=ships_used))
            sent = new_units(army=sent["army"])
        else:
            source_sent = dict(sent)
            self.set_force(src, p.name, {k: cur[k] - source_sent[k] for k in UNIT_KEYS})
        if attack:
            p.last_attack_tick = self.ticks
        ctrl = self.controller(dest)
        if ctrl is not None and self.is_hostile(p.name, ctrl):
            self.declare_war(p.name, ctrl)
        turns = self.travel_turns(src, dest)
        if turns <= 0:
            self.arrive(p.name, dest, sent, src, drop_point)
        else:
            self.pending_offensives.append({"owner": p.name, "origin": src, "dest": dest,
                                             "units": sent, "remaining": turns,
                                             "total": turns, "position": drop_point})
            self.log_msg(f"{p.name} sends {units_text(sent)} from {self.zone_label(src)} "
                         f"toward {dest_label} - they will arrive in {turns} turn(s).")
        if self.is_bot(p):                     # single player: let the person watch this move
            if turns <= 0:
                self.bot_show(dest, "move", f"{p.name} moves to {dest_label}", src)
            else:
                self.bot_show(dest, "depart", f"{p.name} sets out for {dest_label}", src)
        return None

    def process_pending_offensives(self):
        still_pending = []
        for off in self.pending_offensives:
            owner = self.nations.get(off["owner"])
            if not owner or not owner.alive:
                self.log_msg(f"The forces of {off['owner']} en route to "
                             f"{self.zone_label(off['dest'])} are lost.")
                continue
            off["remaining"] -= 1
            if off["remaining"] <= 0:
                self.arrive(off["owner"], off["dest"], off["units"], off["origin"],
                            off.get("position"))
            else:
                still_pending.append(off)
        self.pending_offensives = still_pending

    def action_trade(self):
        p = self.current
        partners = sorted(n.name for n in self.nations.values()
                          if n.name not in MINOR_COUNTRIES and self.can_trade(p, n))
        if not partners:
            self.show_message("No partners", "No countries available to trade oil with.")
            return
        idx = self._choose_from_list("Trade", f"{p.name}: send a resource to whom?", partners)
        if idx is None:
            return
        ally = self.nations[partners[idx]]
        resource_idx = self._choose_from_list("Trade Resource", "What resource do you want to send?",
                                              ["Oil", "Iron"])
        if resource_idx is None:
            return
        resource = "oil" if resource_idx == 0 else "iron"
        available = getattr(p, resource)
        if available <= 0:
            self.show_message("None available", f"{p.name} has no {resource} to send.")
            return
        amt = self.ask_integer(
            f"Trade {resource.title()}",
            f"How much {resource} to send? (0-{available})",
            0, available)
        if not amt:
            return
        setattr(p, resource, available - amt)
        setattr(ally, resource, getattr(ally, resource) + amt)
        self.log_msg(f"{p.name} sends {amt} {resource} to {ally.name}.")
        self.refresh_all()

    def action_view_all(self):
        win = self._modal_open("All Nations")
        done = self._modal_done
        card = make_card(win)
        card.pack(fill="both", expand=True)
        cols = ("Nation", "Side", "Zones", "Troops", "Navy", "Air", "Oil", "Iron",
            "Army R", "Navy R", "Air R", "Stab", "Status")
        tree = ttk.Treeview(card, columns=cols, show="headings", height=16,
                    style="Compact.Treeview")
        widths = {"Nation": 105, "Side": 62, "Zones": 54, "Troops": 62,
              "Navy": 52, "Air": 48, "Oil": 48, "Iron": 48,
              "Army R": 54, "Navy R": 54, "Air R": 48, "Stab": 48,
              "Status": 62}
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=widths.get(c, 80), anchor="w" if c == "Nation" else "center")
        for side, color in SIDE_DARK.items():
            tree.tag_configure(side, foreground=color)
        tree.tag_configure("Defeated", foreground="#9aa5b1")
        ordered = sorted((n for n in self.nations.values() if n.name not in MINOR_COUNTRIES),
                         key=lambda n: (self.SIDE_ORDER.get(n.side, 9), n.name))
        for n in ordered:
            status = "Active" if n.alive else "Defeated"
            u = self.nation_units(n.name)
            tree.insert("", "end", values=(n.name, n.side, f"{n.zones_held}/{n.zone_count}",
                                            u["army"], u["navy"], u["air"], n.oil,
                                            n.iron, n.army_rating, n.navy_rating,
                                            n.air_rating, n.stability, status),
                        tags=(n.side if n.alive else "Defeated",))
        tree.pack(fill="both", expand=True, padx=4, pady=4)
        make_button(win, "Close", lambda: done.set(True), "primary", 11, padx=26,
                    pady=6).pack(pady=(12, 0))
        self._modal_box.bind("<Escape>", lambda e: done.set(True))
        self._modal_show(width=900)

    def reward_oil(self, n):
        """Oil paid out for a completed objective (the data's reward number / 10)."""
        return max(1, n.objective_reward // OIL_REWARD_DIVISOR)

    def reward_iron(self, n):
        """Iron paid out alongside the oil reward for a completed objective."""
        return max(1, n.objective_reward // OIL_REWARD_DIVISOR)

    def action_objective(self):
        p = self.current
        if not p.alive:
            self.show_message(f"{p.name}'s Objective",
                                 f"{p.name} has been defeated and can't claim rewards.")
            return
        if p.objective_claimed:
            self.show_message(f"{p.name}'s Objectives",
                                 f"All {len(p.objectives)} of {p.name}'s objectives are "
                                 f"complete.")
            return
        progress = p.objective_progress(self.year)
        if not all(met for _, met in progress):
            checklist = "\n".join(f"[{'x' if met else ' '}] {text}"
                                   for text, met in progress)
            self.show_message(f"{p.name}'s Objective",
                                 f"{p.objective}\n\nObjective not yet achieved:\n{checklist}")
            return
        done_text = p.objective
        number = p.objective_index + 1
        oil = self.reward_oil(p)
        iron = self.reward_iron(p)
        p.oil += oil
        p.iron += iron
        p.claim_objective()                   # the next objective in the chain appears
        msg = (f"{done_text}\n\nObjective achieved! Reward claimed: +{oil} oil and +{iron} iron!")
        if p.objective_claimed:
            msg += f"\n\nThat was the last one - all {len(p.objectives)} objectives complete."
        else:
            msg += f"\n\nNEXT OBJECTIVE ({number + 1} of {len(p.objectives)}):\n{p.objective}"
        self.show_message(f"{p.name}'s Objective", msg)
        self.log_msg(f"{p.name} achieves objective {number} and claims +{oil} oil.")
        self.refresh_all()

    # ---------------- helpers ----------------

    # ---------------- in-window dialogs (no extra OS windows) ----------------

    # Tk widgets can't be see-through, so the "50% dark" backdrop is made by halving the
    # brightness of every colour in the window while a dialog is open (and restoring them
    # afterwards). Pure Tk - nothing to install. ttk widgets (scrollbars, drop-downs) keep
    # their colour. A grab on the dialog stops clicks reaching the dimmed window.

    _DIM_WIDGET_OPTS = ("bg", "fg", "activebackground", "activeforeground",
                        "highlightbackground", "highlightcolor", "selectbackground",
                        "selectforeground", "insertbackground", "disabledforeground",
                        "selectcolor", "troughcolor")

    def _half(self, color, cache):
        """`color` at 50% brightness as #rrggbb (None if it isn't a real colour)."""
        if not color:
            return None
        if color not in cache:
            try:
                r, g, b = self.winfo_rgb(color)
                cache[color] = "#%02x%02x%02x" % (r // 512, g // 512, b // 512)
            except tk.TclError:
                cache[color] = None
        return cache[color]

    def dim_window(self, keep=()):
        """Halve the brightness of the whole window (except the `keep` widgets and
        everything inside them). Returns an undo list for undim_window."""
        undo, cache = [], {}
        keep = tuple(k for k in keep if k is not None)

        def kept(w):
            while w is not None:
                if w in keep:
                    return True
                w = w.master
            return False

        stack = [self]
        while stack:
            w = stack.pop()
            stack.extend(w.winfo_children())
            if kept(w):
                continue
            cls = w.winfo_class()
            if cls in ("TCombobox", "TScrollbar"):
                self._dim_ttk(w, cls, undo, cache)        # themed widgets need a style
                continue
            if cls.startswith("T") and cls not in ("Tk", "Text", "Toplevel"):
                continue                                  # other ttk widgets
            if cls == "Button":                           # hovering must not relight it
                w._dimmed = getattr(w, "_dimmed", 0) + 1
                undo.append((("dim", w, None), None, None))
            for opt in self._DIM_WIDGET_OPTS:
                try:
                    cur = w.cget(opt)
                except tk.TclError:
                    continue
                new = self._half(str(cur), cache)
                if new and new != str(cur):
                    try:
                        w.configure(**{opt: new})
                        undo.append((w, opt, str(cur)))
                    except tk.TclError:
                        pass
            if cls == "Text":                             # coloured tags (log, info box)
                for tag in w.tag_names():
                    for opt in ("foreground", "background"):
                        try:
                            cur = w.tag_cget(tag, opt)
                        except tk.TclError:
                            continue
                        new = self._half(str(cur), cache)
                        if new:
                            w.tag_configure(tag, **{opt: new})
                            undo.append((("tag", w, tag), opt, str(cur)))
            if cls == "Canvas":                           # every drawn shape and label
                for item in w.find_all():
                    try:
                        cfg = w.itemconfigure(item)
                    except tk.TclError:
                        continue
                    changes = {}
                    for opt in ("fill", "outline"):
                        if opt in cfg:
                            cur = str(cfg[opt][-1])
                            new = self._half(cur, cache)
                            if new:
                                changes[opt] = new
                                undo.append((("item", w, item), opt, cur))
                    if changes:
                        w.itemconfigure(item, **changes)
        return undo

    def _dim_ttk(self, w, cls, undo, cache):
        """Give a ttk combobox / scrollbar a half-brightness style (ttk colors come from
        styles, not widget options). The old style name goes in the undo list."""
        h = lambda c: self._half(c, cache) or c
        st = ttk.Style(self)
        if cls == "TCombobox":
            name = "Dim.TCombobox"
            st.configure(name, padding=4, fieldbackground=h(BG_CARD),
                         background=h(BG_CARD), foreground=h(FG_TEXT),
                         arrowcolor=h(FG_TEXT), bordercolor=h("#aab4c0"))
            st.map(name, fieldbackground=[("readonly", h(BG_CARD)), ("disabled", h(BG_CARD))],
                   foreground=[("readonly", h(FG_TEXT)), ("disabled", h(FG_TEXT))],
                   background=[("active", h(BG_CARD)), ("readonly", h(BG_CARD))])
        else:
            name = ("Dim.Vertical.TScrollbar" if str(w.cget("orient")) == "vertical"
                    else "Dim.Horizontal.TScrollbar")
            st.configure(name, background=h("#c4ccd6"), troughcolor=h(BG_PANEL),
                         bordercolor=h(BG_PANEL), arrowcolor=h(FG_TEXT))
            st.map(name, background=[("active", h("#c4ccd6"))])
        try:
            undo.append((("ttk", w, None), "style", str(w.cget("style"))))
            w.configure(style=name)
        except tk.TclError:
            pass

    def undim_window(self, undo):
        for target, opt, value in reversed(undo):
            try:
                if isinstance(target, tuple):
                    kind, w, ident = target
                    if kind == "tag":
                        w.tag_configure(ident, **{opt: value})
                    elif kind == "ttk":
                        w.configure(style=value)
                    elif kind == "dim":
                        w._dimmed = max(0, getattr(w, "_dimmed", 1) - 1)
                        if not w._dimmed:             # back to normal: drop a stale hover color
                            under = w.winfo_containing(*w.winfo_pointerxy())
                            if under is not w and getattr(w, "_rest_bg", None):
                                w.configure(bg=w._rest_bg)
                    else:
                        w.itemconfigure(ident, **{opt: value})
                else:
                    target.configure(**{opt: value})
            except tk.TclError:
                pass                                      # widget/item no longer exists

    def _grab(self, widget):
        """Send all mouse/keyboard input to `widget` (so the dimmed window is inert)."""
        try:
            widget.wait_visibility()
            widget.grab_set()
        except tk.TclError:
            pass

    def _modal_open(self, title, prompt=""):
        """Start a dialog drawn over the main window. Returns its body frame."""
        self._modal_close()
        self._modal_done = tk.BooleanVar(value=False)
        self._modal_undo = self.dim_window(keep=(self.send_panel_window,))
        box = tk.Frame(self, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
        head = tk.Frame(box, bg=HEADER_BG)
        head.pack(fill="x")
        tk.Label(head, text=title, bg=HEADER_BG, fg="#ffffff",
                 font=("Georgia", 14, "bold")).pack(anchor="w", padx=16,
                                                    pady=(12, 2 if prompt else 12))
        if prompt:
            tk.Label(head, text=prompt, bg=HEADER_BG, fg="#c9d6e3", font=(UI_FONT, 9),
                     wraplength=440, justify="left").pack(anchor="w", padx=16, pady=(0, 12))
        body = tk.Frame(box, bg=BG_CARD)
        body.pack(fill="both", expand=True, padx=16, pady=(12, 14))
        self._modal_box = box
        return body

    def _modal_show(self, width=480, focus=None):
        """Show the dialog centered in the window and wait until it is dismissed."""
        self.update_idletasks()
        box = self._modal_box
        w = min(width, max(300, self.winfo_width() - 40))
        h = min(box.winfo_reqheight(), max(200, self.winfo_height() - 40))
        box.place(relx=0.5, rely=0.5, anchor="center", width=w, height=h)
        box.lift()
        self._grab(box)
        (focus or box).focus_set()
        self.wait_variable(self._modal_done)
        self._modal_close()

    def _modal_close(self):
        box = getattr(self, "_modal_box", None)
        if box is not None:
            self._modal_box = None
            try:
                box.destroy()                             # also releases its grab
            except tk.TclError:
                pass
            self.undim_window(self._modal_undo)
            self._modal_undo = []
            self._modal_done.set(True)
            if self.send_panel_window.winfo_ismapped():   # a panel is still open under it
                self._grab(self.send_panel_window)

    def show_message(self, title, text, mono=False):
        """A message shown inside the main window (no pop-up box)."""
        body = self._modal_open(title)
        done = self._modal_done
        font = (MONO_FONT, 10) if mono else (UI_FONT, 10)
        if text.count("\n") + 1 + len(text) // 60 > 18:
            holder = tk.Frame(body, bg=BG_CARD)
            holder.pack(fill="both", expand=True)
            sb = ttk.Scrollbar(holder, orient="vertical")
            txt = tk.Text(holder, wrap="word", height=18, width=60, font=font, bg=BG_CARD,
                          fg=FG_TEXT, relief="flat", highlightthickness=0,
                          yscrollcommand=sb.set)
            sb.config(command=txt.yview)
            sb.pack(side="right", fill="y")
            txt.pack(side="left", fill="both", expand=True)
            txt.insert("1.0", text)
            txt.config(state="disabled")
        else:
            tk.Label(body, text=text, bg=BG_CARD, fg=FG_TEXT, font=font, wraplength=520,
                     justify="left").pack(anchor="w")
        make_button(body, "OK", lambda: done.set(True), "primary", 11, padx=26,
                    pady=6).pack(pady=(14, 0))
        for key in ("<Return>", "<Escape>"):
            self._modal_box.bind(key, lambda e: done.set(True))
        self._modal_show(width=700 if mono else 560)

    def ask_integer(self, title, prompt, minvalue, maxvalue):
        """Ask for a whole number inside the main window. Returns an int or None."""
        body = self._modal_open(title, prompt)
        done = self._modal_done
        result = {"v": None}
        var = tk.StringVar()
        entry = tk.Entry(body, textvariable=var, font=(UI_FONT, 14), justify="center",
                         relief="solid", bd=1)
        entry.pack(fill="x", pady=(4, 4))
        err = tk.Label(body, text="", bg=BG_CARD, fg=BAD, font=(UI_FONT, 9))
        err.pack(anchor="w")

        def ok(event=None):
            try:
                v = int(var.get().strip())
                if not minvalue <= v <= maxvalue:
                    raise ValueError
            except ValueError:
                err.config(text=f"Enter a whole number from {minvalue} to {maxvalue}.")
                return
            result["v"] = v
            done.set(True)

        row = tk.Frame(body, bg=BG_CARD)
        row.pack(fill="x", pady=(14, 0))
        make_button(row, "Cancel", lambda: done.set(True), "quiet").pack(side="left")
        make_button(row, "OK", ok, "primary").pack(side="right")
        entry.bind("<Return>", ok)
        entry.bind("<Escape>", lambda e: done.set(True))
        self._modal_show(width=420, focus=entry)
        return result["v"]

    def _choose_from_list(self, title, prompt, options):
        body = self._modal_open(title, prompt)
        done = self._modal_done
        card = make_card(body)
        card.pack(fill="both", expand=True)
        lb = tk.Listbox(card, height=min(12, max(4, len(options))), font=(UI_FONT, 11),
                        bg=BG_CARD, fg=FG_TEXT, relief="flat", highlightthickness=0,
                        selectbackground=ACCENT, selectforeground="#ffffff",
                        activestyle="none", exportselection=False)
        for o in options:
            lb.insert("end", "  " + o)
        lb.pack(fill="both", expand=True, padx=6, pady=6)
        if options:
            lb.selection_set(0)
        result = {"idx": None}

        def confirm(event=None):
            sel = lb.curselection()
            if sel:
                result["idx"] = sel[0]
            done.set(True)

        lb.bind("<Double-Button-1>", confirm)
        lb.bind("<Return>", confirm)
        lb.bind("<Escape>", lambda e: done.set(True))
        row = tk.Frame(body, bg=BG_CARD)
        row.pack(fill="x", pady=(14, 0))
        make_button(row, "Cancel", lambda: done.set(True), "quiet").pack(side="left")
        make_button(row, "Select", confirm, "primary").pack(side="right")
        self._modal_show(width=400, focus=lb)
        return result["idx"]

    def close_send_panel(self):
        self.pending_send = None
        try:
            self.send_panel_window.grab_release()
        except tk.TclError:
            pass
        self.send_panel_window.place_forget()
        undo, self._panel_undo = getattr(self, "_panel_undo", None), None
        if undo is not None:
            self.undim_window(undo)

    def open_center_panel(self, title, prompt, height=440):
        for child in self.send_panel_body.winfo_children():
            child.destroy()
        if getattr(self, "_panel_undo", None) is None:    # dim the window once
            self._panel_undo = self.dim_window(keep=(self.send_panel_window,))
        self.send_panel_window.place(relx=0.5, rely=0.5, anchor="center",
                                     width=520, height=height)
        self.send_panel_window.lift()
        self._grab(self.send_panel_window)
        self.send_panel_title.config(text=title)
        self.send_panel_prompt.config(text=prompt)

    def fit_center_panel(self, minimum_height=0):
        self.update_idletasks()
        root_w, root_h = self.winfo_width(), self.winfo_height()
        width = max(520, min(760, int(root_w * 0.52)))
        height = max(minimum_height, self.send_panel.winfo_reqheight())
        height = min(height, max(minimum_height, root_h - 80))
        self.send_panel_prompt.config(wraplength=width - 40)
        self.send_panel_window.place(relx=0.5, rely=0.5, anchor="center",
                                     width=width, height=height)

    def show_send_panel(self, title, prompt, avail, default_kind, on_send,
                        transport_avail=0, airlift_avail=0):
        """Show an inline single-unit-type movement control."""
        self.open_center_panel(title, prompt)

        details = tk.Frame(self.send_panel_body, bg="#eef1f5", highlightthickness=1,
                   highlightbackground=BORDER)
        details.pack(fill="x", pady=(0, 14))
        tk.Label(details, text="SELECTED FORCE", bg="#eef1f5", fg=ACCENT,
             font=(UI_FONT, 8, "bold")).pack(anchor="w", padx=10, pady=(8, 1))
        # Amphibious landing: the fleet only carries troops, so troops are the one option.
        landing = transport_avail > 0 and default_kind == "navy"
        if landing:
            tk.Label(details, text="Troops only", bg="#eef1f5",
                     fg=FG_TEXT, font=(UI_FONT, 12, "bold")).pack(anchor="w", padx=10)
            tk.Label(details, text=f"Available: {transport_avail}    Ships are assigned automatically "
                                   f"(1 Navy per {TROOPS_PER_SHIP} troops)",
                     bg="#eef1f5", fg=DIM, font=(UI_FONT, 9)).pack(anchor="w", padx=10,
                                                                    pady=(1, 8))
        else:
            tk.Label(details, text=f"{UNIT_TYPES[default_kind]['label']} only", bg="#eef1f5",
                     fg=FG_TEXT, font=(UI_FONT, 12, "bold")).pack(anchor="w", padx=10)
            tk.Label(details, text=f"Available: {avail[default_kind]}    Other unit types are not selectable",
                     bg="#eef1f5", fg=DIM, font=(UI_FONT, 9)).pack(anchor="w", padx=10,
                                                                    pady=(1, 8))

        # Air force can also airlift troops: choose between flying the planes alone
        # and flying troops (the carrying planes go to the destination with them).
        airlift_ok = airlift_avail > 0 and default_kind == "air"
        mode = tk.StringVar(value="fly")
        modes = tk.Frame(self.send_panel_body, bg=BG_CARD)
        if airlift_ok:
            modes.pack(fill="x", pady=(0, 4))
            for val, txt in (("fly", f"Fly the air force ({avail['air']})"),
                             ("airlift", f"Airlift troops (up to {airlift_avail}, "
                                         f"1 Air per {TROOPS_PER_PLANE} troops)")):
                tk.Radiobutton(modes, text=txt, value=val, variable=mode, bg=BG_CARD,
                               fg=FG_TEXT, activebackground=BG_CARD, selectcolor=BG_CARD,
                               font=(UI_FONT, 10, "bold"),
                               command=lambda: refresh_mode()).pack(anchor="w")

        def is_airlift():
            return airlift_ok and mode.get() == "airlift"

        def current_have():
            if landing:
                return transport_avail
            if is_airlift():
                return airlift_avail
            return avail[default_kind]

        def current_label():
            if landing or is_airlift():
                return "Troops"
            return UNIT_TYPES[default_kind]["label"]

        row = tk.Frame(self.send_panel_body, bg=BG_CARD)
        row.pack(fill="x", pady=(8, 4))
        # `state["have"]` = the quantity the person actually chooses (troops when carried)
        state = {"have": current_have()}
        row_label = tk.StringVar(value=current_label())
        tk.Label(row, textvariable=row_label, width=10, anchor="w",
                 bg=BG_CARD, fg=FG_TEXT, font=(UI_FONT, 10, "bold")).pack(side="left")
        amount = tk.StringVar(value=str(state["have"]))
        spin = tk.Spinbox(row, from_=0, to=state["have"], textvariable=amount,
                          width=7, font=(UI_FONT, 10), justify="center")
        spin.pack(side="left")
        carry_text = tk.StringVar()
        tk.Label(row, textvariable=carry_text, bg=BG_CARD, fg=DIM,
                 font=(UI_FONT, 9)).pack(side="left", padx=8)

        def carriers_for(troops):
            per = TROOPS_PER_PLANE if is_airlift() else TROOPS_PER_SHIP
            return -(-troops // per)

        def update_carriers(*_):
            if not (landing or is_airlift()):
                carry_text.set("")
                return
            try:
                t = max(0, min(state["have"], int(amount.get())))
            except ValueError:
                t = 0
            carry_text.set(f"carried by {carriers_for(t)} " +
                           ("Air" if is_airlift() else "Navy"))

        def refresh_mode():
            state["have"] = current_have()
            spin.config(to=state["have"])
            amount.set(str(state["have"]))
            row_label.set(current_label())
            update_carriers()

        amount.trace_add("write", update_carriers)
        update_carriers()

        quick = tk.Frame(self.send_panel_body, bg=BG_CARD)
        quick.pack(fill="x", pady=(2, 6))
        tk.Label(quick, text="QUICK AMOUNT", bg=BG_CARD, fg=ACCENT,
             font=(UI_FONT, 8, "bold")).pack(anchor="w", pady=(0, 4))
        quick_buttons = tk.Frame(quick, bg=BG_CARD, height=68)
        quick_buttons.pack(fill="x")
        quick_buttons.pack_propagate(False)

        def set_amount(fraction):
            have = state["have"]
            amount.set(str(have if fraction >= 1 else max(1, int(round(have * fraction)))))

        for label, fraction in PRESETS:
            make_button(quick_buttons, label, lambda f=fraction: set_amount(f),
                        "accent", 12, padx=8, pady=12).pack(side="left", expand=True,
                                                           fill="both", padx=2)

        tk.Label(self.send_panel_body,
                 text="Select an amount, then press Send. Ground troops move one zone at a time.",
                 bg=BG_CARD, fg=DIM, font=(UI_FONT, 9), wraplength=470,
                 justify="left").pack(anchor="w", pady=(14, 0))

        actions = tk.Frame(self.send_panel_body, bg=BG_CARD)
        actions.pack(fill="x", pady=(16, 0))

        def close_panel():
            self.close_send_panel()

        def confirm():
            try:
                count = max(0, min(state["have"], int(amount.get())))
            except ValueError:
                count = 0
            if count <= 0:
                return
            sent = new_units()
            airlifting = is_airlift()
            if landing:
                sent["army"] = count
                sent["navy"] = min(avail["navy"], carriers_for(count))
            elif airlifting:
                sent["army"] = count
                sent["air"] = min(avail["air"], carriers_for(count))
            else:
                sent[default_kind] = count
            close_panel()
            if airlifting:
                on_send(sent, True)
            else:
                on_send(sent)

        make_button(actions, "Cancel", close_panel, "quiet", 9).pack(side="left")
        make_button(actions, "SEND", confirm, "primary", 12, padx=30, pady=8).pack(
            side="right")
        self.fit_center_panel(440)

    def show_battle_panel(self, zone, attackers, defenders, bombers=None):
        bombers = bombers or {}
        cut = int(round((1 - ATTACKER_PENALTY) * 100))
        self.open_center_panel("Battle", f"Start the battle in {self.zone_label(zone)}?")

        details = tk.Frame(self.send_panel_body, bg="#eef1f5", highlightthickness=1,
                           highlightbackground=BORDER)
        details.pack(fill="x", pady=(0, 14))
        tk.Label(details, text=f"ATTACKERS  (-{cut}% attack penalty)", bg="#eef1f5",
                 fg=BAD, font=(UI_FONT, 9, "bold")).pack(anchor="w", padx=10, pady=(8, 2))
        p = self.current

        def side_lines(fighters, friendly):
            """Fighting units plus air force (which only bombs) for each country here."""
            owners = list(fighters)
            for o, u in self.garrisons.get(zone, {}).items():
                if o in owners or u.get("air", 0) <= 0:
                    continue
                is_friend = o == p.name or self.are_allies(p, self.nations[o])
                if is_friend == friendly and (friendly or self.is_hostile(p.name, o)):
                    owners.append(o)
            lines = []
            for o in owners:
                text = units_text(fighters[o]) if o in fighters else "-"
                air = self.garrisons.get(zone, {}).get(o, {}).get("air", 0)
                if air > 0:
                    text += f"   Air {air} (bombs only)"
                lines.append(f"{o}: {text}")
            return "\n".join(lines)

        tk.Label(details, text=side_lines(attackers, True), bg="#eef1f5",
                 fg=FG_TEXT, font=(MONO_FONT, 10), justify="left").pack(anchor="w",
                                                                         padx=10)
        tk.Label(details, text="DEFENDERS", bg="#eef1f5", fg=ACCENT,
                 font=(UI_FONT, 9, "bold")).pack(anchor="w", padx=10, pady=(10, 2))
        tk.Label(details, text=side_lines(defenders, False), bg="#eef1f5",
                 fg=FG_TEXT, font=(MONO_FONT, 10), justify="left").pack(anchor="w",
                                                                         padx=10, pady=(0, 8))

        _, _, mod_lines = self.battle_modifiers(zone, list(attackers), list(defenders))
        for line in mod_lines:
            tk.Label(self.send_panel_body, text=line, bg=BG_CARD, fg=ACCENT,
                     font=(UI_FONT, 9, "bold"), wraplength=470,
                     justify="left").pack(anchor="w", pady=(6, 0))
        tk.Label(self.send_panel_body,
                 text="Battle events may help or hinder either side by 5–15%.",
                 bg=BG_CARD, fg=DIM, font=(UI_FONT, 9), wraplength=470,
                 justify="left").pack(anchor="w", pady=(8, 0))
        enemy_air = self.defending_air(zone, attackers, self.current.name)
        def_air_humans = [o for o in enemy_air if self.human_decides_air(o)]
        def_air_bots = [o for o in enemy_air if o not in def_air_humans]
        if def_air_bots:                      # bots decide for themselves when the fight starts
            tk.Label(self.send_panel_body,
                     text=("Warning: the defenders' air force may bomb back (-10% attacker "
                           "power each): " + ", ".join(def_air_bots) + "."),
                     bg=BG_CARD, fg=BAD, font=(UI_FONT, 9, "bold"), wraplength=470,
                     justify="left").pack(anchor="w", pady=(6, 0))
        bomb_vars = {}
        if bombers:
            tk.Label(self.send_panel_body,
                     text="AIR FORCE BOMBING  (1 per country per battle, -10% enemy power each)",
                     bg=BG_CARD, fg=ACCENT, font=(UI_FONT, 8, "bold")).pack(anchor="w",
                                                                           pady=(10, 2))
            for o, uses in bombers.items():
                var = tk.BooleanVar(value=False)
                bomb_vars[o] = var
                tk.Checkbutton(self.send_panel_body,
                               text=f"{o} bombs  ({uses}/{BOMBINGS_PER_COUNTRY} bombings left)",
                               variable=var, bg=BG_CARD, fg=FG_TEXT,
                               activebackground=BG_CARD, selectcolor=BG_CARD,
                               font=(UI_FONT, 10, "bold")).pack(anchor="w", pady=1)
        def_vars = {}
        if def_air_humans:                    # the defenders' option, decided as the battle starts
            tk.Label(self.send_panel_body,
                     text="DEFENDERS' AIR FORCE  (they can only bomb back, -10% attacker "
                          "power each - they can't attack on your turn)",
                     bg=BG_CARD, fg=BAD, font=(UI_FONT, 8, "bold"), wraplength=470,
                     justify="left").pack(anchor="w", pady=(10, 2))
            for o in def_air_humans:
                var = tk.BooleanVar(value=False)
                def_vars[o] = var
                tk.Checkbutton(self.send_panel_body,
                               text=f"{o} bombs  ({self.nations[o].bombing_uses}/"
                                    f"{BOMBINGS_PER_COUNTRY} bombings left)",
                               variable=var, bg=BG_CARD, fg=FG_TEXT,
                               activebackground=BG_CARD, selectcolor=BG_CARD,
                               font=(UI_FONT, 10, "bold")).pack(anchor="w", pady=1)
        actions = tk.Frame(self.send_panel_body, bg=BG_CARD)
        actions.pack(fill="x", pady=(30, 0))

        def start():
            # Re-check the battle when the button is actually pressed. This prevents a
            # stale panel from letting the player start an ally's battle or reuse forces
            # that are no longer available.
            fresh = self.battle_sides(zone, self.current)
            if not fresh:
                self.close_send_panel()
                self.refresh_all()
                return
            fresh_att, fresh_def = fresh
            self.close_send_panel()
            counts = {o: 1 for o, var in bomb_vars.items() if var.get()}
            self.fight_battle(zone, fresh_att, fresh_def, self.current.name, counts,
                              {o: int(v.get()) for o, v in def_vars.items()})
            self.refresh_all()

        make_button(actions, "START BATTLE", start, "danger", 14, padx=30, pady=14).pack(
            fill="x", expand=True)
        self.fit_center_panel(440)

    # ---------------- combat ----------------


    def arrive(self, owner_name, dest, units, origin, position=None):
        """Forces of owner_name reach zone `dest`: station peacefully, move into an
        undefended enemy zone, or fight whatever hostile forces stand there."""
        owner = self.nations[owner_name]
        if not owner.alive:
            return
        label = self.zone_label(dest)
        ctrl = self.controller(dest)
        slot = self.garrisons.get(dest, {})
        # only units that fight here (troops on land, navy at sea) defend the zone;
        # air force alone does not hold it
        defenders = {o: u for o, u in slot.items()
                     if units_total(self.battle_units(dest, u)) > 0
                     and self.is_hostile(owner_name, o)}
        dest_hostile = ctrl is not None and self.is_hostile(owner_name, ctrl)

        # friendly, uncontested destination: just station there
        if not defenders and not dest_hostile:
            self.station(dest, owner_name, units, position)
            self.log_msg(f"{owner_name}'s forces ({units_text(units)}) arrive in {label}.")
            return

        for o in defenders:
            self.declare_war(owner_name, o)
        if dest_hostile:
            self.declare_war(owner_name, ctrl)

        # undefended enemy zone: the troops just stand there. The zone is NOT claimed
        # until they attack it (click the zone in a War Phase, with rested troops).
        if not defenders:
            self.station(dest, owner_name, units, position)
            self.log_msg(f"{owner_name}'s forces ({units_text(units)}) arrive in {label}, "
                         f"but it is not claimed yet - attack it with rested troops "
                         f"during a War Phase to take it.")
            return

        # enemy forces are standing here: no automatic fight. The armies simply
        # face each other until someone clicks the zone to start the battle. The
        # arriving troops came to attack, so they can fight in that battle even though
        # they can't move again until they have rested.
        self.station(dest, owner_name, units, position, can_fight=True)
        self.log_msg(f"{owner_name}'s forces ({units_text(units)}) arrive in {label}, "
                     f"facing {', '.join(defenders)}. Click the zone during a war phase "
                     f"to start the battle.")

    def is_contested(self, z):
        """True if forces from hostile countries are standing in zone z."""
        owners = [o for o, u in self.garrisons.get(z, {}).items()
                  if units_total(self.battle_units(z, u)) > 0]
        return any(self.is_hostile(a, b) for i, a in enumerate(owners) for b in owners[i + 1:])

    def battle_units(self, z, units):
        """Return only the unit type allowed to fight in this zone."""
        if self.is_sea_zone(z):
            return new_units(navy=units["navy"])
        return new_units(army=units["army"])

    def battle_sides(self, z, p):
        """(attackers, defenders) for a battle in zone z started by acting country p,
        or None. The attackers are p and p's allies present in the zone; it must be
        a war phase in which p's side acts. Units already in the contested zone can
        participate; resting units can't attack."""
        if not p or not p.alive or not self.can_attack_now(p):
            return None
        slot = {o: self.battle_units(z, u) for o, u in self.garrisons.get(z, {}).items()
            if units_total(self.battle_units(z, u)) > 0}
        att = {}
        for o in slot:
            # Every friendly country with troops (or ships) ready in the zone joins the
            # attack, in single player too - previously the player's allies standing in
            # the zone were left out of the battle.
            if o == p.name or self.are_allies(p, self.nations[o]):
                ready = self.attack_units(z, o)       # resting troops can't attack
                if units_total(ready) > 0:
                    att[o] = ready
        # In single player the human can only START a battle their own country fights in
        # (allies join it, but an ally can't be sent into a fight by itself).
        if self.single_player and not self.is_bot(p) and p.name not in att:
            return None
        dfn = {o: u for o, u in slot.items() if self.is_hostile(p.name, o)}
        return (att, dfn) if att and dfn else None

    def attack_units(self, z, o):
        """Return units of country o that may fight in zone z.

        Resting units can NEVER attack, in any game mode. Troops that just moved in,
        or that joined a resting stack, must wait out their rest first (the old
        "fight_ok" exception let them start battles right away - that was the bug).
        """
        return self.battle_units(z, self.available_units(z, o))

    def is_unclaimed(self, z):
        """Troops stand in land zone z, but its controller is hostile to them - it has
        not been claimed yet (moving in is not enough: they have to attack it)."""
        if self.is_sea_zone(z):
            return False
        ctrl = self.controller(z)
        if ctrl is None:
            return False
        return any(units_total(self.battle_units(z, u)) > 0 and self.is_hostile(o, ctrl)
                   for o, u in self.garrisons.get(z, {}).items())

    def claim_sides(self, z, p):
        """{country: rested troops} that can attack undefended enemy zone z to claim it
        for acting country p, or None (needs p's War Phase, a hostile controller, no
        defenders, and at least one rested troop of p or an ally in the zone)."""
        if (not p or not p.alive or self.is_sea_zone(z) or not self.can_attack_now(p)):
            return None
        ctrl = self.controller(z)
        if ctrl is None or not self.is_hostile(p.name, ctrl):
            return None
        slot = self.garrisons.get(z, {})
        if any(units_total(self.battle_units(z, u)) > 0 and self.is_hostile(p.name, o)
               for o, u in slot.items()):
            return None                       # defenders present: that's a battle
        att = {}
        for o in slot:
            if o == p.name or self.are_allies(p, self.nations[o]):
                ready = self.attack_units(z, o)
                if units_total(ready) > 0:
                    att[o] = ready
        return att or None

    def claim_zone(self, z, p, att):
        """Attack an undefended zone with currently rested troops and claim it.
        Re-check readiness at the moment the button is pressed so a stale attack
        panel can never bypass the resting rule."""
        label = self.zone_label(z)
        fresh_att = self.claim_sides(z, p)
        if not fresh_att:
            self.log_msg(f"{p.name} cannot attack {label}: all available troops are still resting.")
            return
        att = fresh_att
        ctrl = self.controller(z)
        if ctrl is not None and self.is_hostile(p.name, ctrl):
            self.declare_war(p.name, ctrl)
        for o in [o for o, u in self.garrisons.get(z, {}).items()
                  if self.is_hostile(p.name, o)]:
            # Ground troops cannot attack aircraft.  Keep an enemy air force in place
            # when taking an undefended ground zone; it is only vulnerable if opposing
            # air power is present.
            existing = self.get_force(z, o)
            self.set_force(z, o, new_units(air=existing["air"]))
        for o, u in att.items():
            self.add_lock(z, o, u)
            self.nations[o].battles_won += 1
        p.last_attack_tick = self.ticks
        self.log_msg(f"{p.name} attacks undefended {label} with "
                     f"{', '.join(f'{o} {units_text(u)}' for o, u in att.items())}.")
        self.take_zone(p.name, z)
        self.announce_battle_result(
            f"{p.side} Powers Advance - {label} Falls", p.side)

    def show_claim_panel(self, z, att):
        self.open_center_panel("Claim zone", f"Attack {self.zone_label(z)}?")
        tk.Label(self.send_panel_body,
                 text=f"{self.zone_label(z)} has no defenders, but it is still held by "
                      f"{self.controller(z)}. Your troops must attack to claim it.\n\n"
                      + "\n".join(f"{o}: {units_text(u)}" for o, u in att.items())
                      + "\n\nTroops that attack must rest for a turn afterwards.",
                 bg=BG_CARD, fg=FG_TEXT, font=(UI_FONT, 10), wraplength=470,
                 justify="left").pack(anchor="w", pady=(4, 0))
        actions = tk.Frame(self.send_panel_body, bg=BG_CARD)
        actions.pack(fill="x", pady=(30, 0))

        def go():
            self.close_send_panel()
            self.claim_zone(z, self.current, att)
            self.refresh_all()

        make_button(actions, "ATTACK & CLAIM", go, "danger", 14, padx=30,
                    pady=14).pack(fill="x", expand=True)
        self.fit_center_panel(440)

    def battle_event(self, attackers, defenders):
        """Return a random battle event and its power/loss modifiers."""
        affected_side = random.choice(("attackers", "defenders"))
        affected_names = attackers if affected_side == "attackers" else defenders
        affected_label = "attacking" if affected_side == "attackers" else "defending"
        names = ", ".join(affected_names)
        percent = random.randint(5, 15) / 100
        event = random.choice(("food shortage", "extra supply", "local reinforcements",
                               "supply breakdown"))
        power_mod = {"attackers": 1.0, "defenders": 1.0}
        loss_mod = {"attackers": 1.0, "defenders": 1.0}
        if event in ("food shortage", "supply breakdown"):
            loss_mod[affected_side] += percent
            text = (f"BATTLE EVENT: {event.title()} affects the {affected_label} side "
                    f"({names}); they suffer {percent:.0%} extra losses.")
        else:
            power_mod[affected_side] += percent
            text = (f"BATTLE EVENT: {event.title()} helps the {affected_label} side "
                    f"({names}); they gain {percent:.0%} combat power.")
        return text, power_mod, loss_mod

    def fight_battle(self, z, attackers, defenders, lead_name, bombings=None,
                     def_bombings=None):
        """Resolve a battle in zone z. `attackers` maps each attacking country to the
        rested units it commits; `defenders` maps each defending country to its units
        (all of which defend). The attacking side (whose turn it is) loses army rating.
        `def_bombings` = {country: 0/1} choices the defending side already made in the battle
        window; any defending air force not decided there is settled when the fight begins
        (see defender_bombings)."""
        label = self.zone_label(z)
        a_names, d_names = list(attackers), list(defenders)
        for a in a_names:
            for d in d_names:
                self.declare_war(a, d)
        a_fight = {o: dict(u) for o, u in attackers.items()}
        d_units = {o: dict(self.battle_units(z, self.garrisons[z][o])) for o in d_names}
        event_text, power_mod, loss_mod = self.battle_event(a_names, d_names)
        self.log_msg(event_text)
        a_mult, d_mult, terrain_lines = self.battle_modifiers(z, a_names, d_names)
        for line in terrain_lines:
            self.log_msg(line)
        a_power = (sum(units_power(u, self.nations[o]) * a_mult[o] for o, u in a_fight.items())
                   * power_mod["attackers"] * ATTACKER_PENALTY)
        d_power = sum(units_power(u, self.nations[o]) * d_mult[o] for o, u in d_units.items()) \
            * power_mod["defenders"]
        # each country may bomb once per battle (BOMBINGS_PER_COUNTRY in total); bombings from different
        # countries stack, each cutting enemy power by 10%.
        total_bombs = 0
        bombers_used = []                 # countries whose planes bomb (drawn in the battle)
        for o, n_b in (bombings or {}).items():
            n_b = max(0, min(n_b, 1, self.nations[o].bombing_uses))   # max 1 per battle
            if n_b > 0:
                self.nations[o].bombing_uses -= n_b
                total_bombs += n_b
                bombers_used.append(o)
                self.log_msg(f"AIR RAID: {o} flies {n_b} bombing(s) "
                             f"({self.nations[o].bombing_uses} bombing uses remain).")
        if total_bombs:
            d_power *= max(0.0, 1 - 0.1 * total_bombs)
            self.log_msg(f"Bombing cuts the defenders' power by {min(100, total_bombs * 10)}%.")
        # the defenders' air forces can bomb back (-10% attacker power each, stacking)
        def_bombings = self.defender_bombings(z, a_fight, lead_name, a_power, d_power,
                                              decided=def_bombings)
        def_bombers_used, def_bombs = [], 0
        for o, n_b in def_bombings.items():
            n_b = max(0, min(n_b, 1, self.nations[o].bombing_uses))
            if n_b > 0:
                self.nations[o].bombing_uses -= n_b
                def_bombs += n_b
                def_bombers_used.append(o)
                self.log_msg(f"AIR RAID (defence): {o} flies {n_b} bombing(s) against the "
                             f"attackers ({self.nations[o].bombing_uses} bombing uses remain).")
        if def_bombs:
            a_power *= max(0.0, 1 - 0.1 * def_bombs)
            self.log_msg(f"Bombing cuts the attackers' power by {min(100, def_bombs * 10)}%.")
        a_roll = a_power * random.uniform(0.85, 1.15)
        d_roll = d_power * random.uniform(0.85, 1.15)
        ratio = min(a_roll, d_roll) / max(a_roll, d_roll, 0.01)
        win_loss = min(0.9, 0.05 + 0.7 * ratio)   # share of the winner's force lost
        a_txt, d_txt = ", ".join(a_names), ", ".join(d_names)

        # units of the attacking side that were resting stay put either way
        resting = {o: {k: self.garrisons[z][o][k] - a_fight[o][k] for k in UNIT_KEYS}
                   for o in a_names}

        # The outcome is decided now, but not applied at once: work out what each country
        # will have left, then let the losses play out tick by tick (animate_battle).
        # A battle always ends with a winning side: by the last tick the loser has no
        # fighting units left in the zone, and the winner has at least one.
        a_wins = a_roll >= d_roll
        kind = "navy" if self.is_sea_zone(z) else "army"      # the unit type that fights here

        def fighters_wiped(units):
            return {k: (0 if k == kind else units[k]) for k in UNIT_KEYS}

        def ensure_survivor(owners, final_units, committed):
            """Winning side keeps at least one fighting unit, even if rounding would
            have left it with none."""
            if any(final_units[o][kind] > 0 for o in owners):
                return None
            o = max(owners, key=lambda n: committed[n][kind])
            final_units[o][kind] += 1
            return o

        start = {o: dict(self.garrisons[z][o]) for o in a_names + d_names}
        final, a_surv = {}, {}
        if a_wins:
            for o in a_names:
                a_surv[o] = scale_units(a_fight[o],
                                        1 - min(0.95, win_loss * loss_mod["attackers"]))
                final[o] = {k: resting[o][k] + a_surv[o][k] for k in UNIT_KEYS}
            for o in d_names:
                # A ground victory does not destroy aircraft.  Air units are only
                # removed when there is opposing air power to engage them.
                final[o] = new_units(air=self.garrisons[z][o]["air"])
            fixed = ensure_survivor(a_names, final, a_fight)
            if fixed:
                a_surv[fixed][kind] += 1
        else:
            for o in a_names:
                final[o] = fighters_wiped(resting[o])   # even resting troops lose the zone
            for o in d_names:
                surv = scale_units(d_units[o], 1 - min(0.95, win_loss * loss_mod["defenders"]))
                other = {k: self.garrisons[z][o][k] - d_units[o][k] for k in UNIT_KEYS}
                final[o] = {k: other[k] + surv[k] for k in UNIT_KEYS}
            ensure_survivor(d_names, final, d_units)
            # attacker-side allies whose troops were all resting are driven out as well
            lead = self.nations[lead_name]
            for o, u in list(self.garrisons[z].items()):
                if (o not in start and units_total(self.battle_units(z, u)) > 0
                        and (o == lead_name or self.are_allies(lead, self.nations[o]))):
                    start[o] = dict(u)
                    final[o] = fighters_wiped(u)

        self.animate_battle(z, label, lead_name, start, final, a_names, d_names,
                            bombers_used, def_bombers_used)

        if a_wins:
            for o in a_names:
                self.set_force(z, o, final[o])
                self.add_lock(z, o, a_surv[o])      # fighters must rest afterwards
                for e in self.locks.get((z, o), ()):
                    e["fight_ok"] = False            # the battle is over: no second fight
                self.nations[o].battles_won += 1
                self.nations[o].victories_over.update(d_names)
            for o in d_names:
                self.set_force(z, o, new_units())
            left = ", ".join(f"{o} {units_text(self.garrisons[z].get(o) or new_units())}"
                             for o in a_names)
            self.log_msg(f"BATTLE in {label}: {a_txt} (power {a_power:.0f} after the "
                         f"attacker penalty) defeat {d_txt} (power {d_power:.0f}). "
                         f"Survivors: {left}.")
            self.announce_battle_result(
                f"{self.nations[lead_name].side} Powers Advance - {label} Falls",
                self.nations[lead_name].side)
            self.take_zone(lead_name, z)
        else:
            for o in final:
                if o not in d_names:
                    self.set_force(z, o, final[o])      # the losing side leaves the zone
            for o in d_names:
                self.set_force(z, o, final[o])
                self.nations[o].battles_won += 1
                self.nations[o].victories_over.update(a_names)
            self.log_msg(f"BATTLE in {label}: the attack by {a_txt} (power {a_power:.0f} "
                         f"after the attacker penalty) is crushed by {d_txt} "
                         f"(power {d_power:.0f}). The attacking units are destroyed.")
            winner_side = self.nations[d_names[0]].side
            attacker_side = self.nations[lead_name].side
            self.announce_battle_result(
                f"{attacker_side} Powers Are Defeated - {label} Holds", winner_side)

    def defending_air(self, z, attackers, lead_name):
        """Countries whose air force in zone z may bomb the attackers: every country hostile
        to the attack's leader with air force there and bombings left."""
        return [o for o, u in self.garrisons.get(z, {}).items()
                if o in self.nations and o not in attackers and u.get("air", 0) > 0
                and self.nations[o].alive and self.nations[o].bombing_uses > 0
                and self.is_hostile(lead_name, o)]

    def human_decides_air(self, o):
        """Does a person (rather than a bot) choose whether country o's air force bombs?
        Hotseat: any major power. Single player: only the player's own country."""
        return o not in MINOR_COUNTRIES and (not self.single_player or o == self.player_name)

    def defender_bombings(self, z, attackers, lead_name, a_power, d_power, decided=None):
        """Which air forces of the defending side bomb the attackers in this battle:
        {country: 1}. Every hostile country with air force in the zone and bombings left
        may bomb once. `decided` holds the choices already made in the battle window.
        Anyone else: a human defender (the player's own country in single player, any major
        power in hotseat) is asked, and bots decide for themselves. Defenders only ever
        choose whether to bomb - they can't attack on the attacker's turn."""
        decided = decided or {}
        eligible = self.defending_air(z, attackers, lead_name)
        chosen = [o for o in eligible if decided.get(o)]
        eligible = [o for o in eligible if o not in decided]
        if not eligible:
            return {o: 1 for o in chosen}
        humans = [o for o in eligible if self.human_decides_air(o)]
        bots = [o for o in eligible if o not in humans]
        if bots:
            chosen += self.bot_defense_bomb_plan(
                a_power, d_power, {o: self.nations[o].bombing_uses for o in bots})
        if humans:
            chosen += self.ask_defender_bombing(z, humans)
        return {o: 1 for o in chosen}

    def ask_defender_bombing(self, zone, countries):
        """Pop-up for battles that start without a battle window (a bot attacks the player,
        or a scripted event): the defending player decides whether their air force bombs
        the attackers. Returns the list of countries that bomb."""
        body = self._modal_open(
            "Defenders' Air Force",
            f"An attack on {self.zone_label(zone)} is about to begin. Defending air force "
            f"can bomb back: -10% attacker power per bombing, 1 per country per battle.")
        done = self._modal_done
        vars_ = {}
        for o in countries:
            var = tk.BooleanVar(value=False)
            vars_[o] = var
            air = self.garrisons[zone][o]["air"]
            tk.Checkbutton(body, text=f"{o} bombs  (air {air}, "
                                      f"{self.nations[o].bombing_uses}/{BOMBINGS_PER_COUNTRY} "
                                      f"bombings left)",
                           variable=var, bg=BG_CARD, fg=FG_TEXT, activebackground=BG_CARD,
                           selectcolor=BG_CARD, font=(UI_FONT, 10, "bold")).pack(anchor="w",
                                                                                 pady=2)
        make_button(body, "DEFEND", lambda: done.set(True), "danger", 11, padx=26,
                    pady=8).pack(pady=(14, 0))
        self._modal_box.bind("<Return>", lambda e: done.set(True))
        self._modal_show(width=520)
        return [o for o, v in vars_.items() if v.get()]

    def bot_defense_bomb_plan(self, a_power, d_power, uses):
        """Which of `uses` ({country: bombings left}) bomb the attackers when a bot defends
        (attacker power a_power against its d_power). Bombings are scarce, so: none if the
        defence is comfortable, the fewest that turn the fight if it isn't, one insurance
        bombing (from a country with more than one left) in a close fight, and everything it
        has when the fight is lost without it but still within reach."""
        pool = sorted((o for o, n in uses.items() if n > 0), key=lambda o: -uses[o])
        for k in range(len(pool) + 1):
            if d_power >= a_power * max(0.0, 1 - 0.1 * k):
                if k > 0:
                    return pool[:k]
                if d_power >= a_power * BOT_BOMB_COMFORT:
                    return []                     # safe: save the bombing
                return [o for o in pool if uses[o] > 1][:1]    # close fight: one insurance
        if pool and d_power >= a_power * max(0.0, 1 - 0.1 * len(pool)) * 0.8:
            return pool                           # a long shot, but bombing makes it costly
        return []

    def bot_defender_air_factor(self, bot, z):
        """How much the enemy's air forces standing in zone z (they bomb the bot's attackers
        back, -10% each) are expected to cut a bot attack's power: a multiplier below 1."""
        n = sum(1 for o, u in self.garrisons.get(z, {}).items()
                if o in self.nations and u.get("air", 0) > 0 and self.nations[o].alive
                and self.nations[o].bombing_uses > 0 and self.is_hostile(bot.name, o))
        return max(0.5, 1 - 0.1 * n)

    def battle_pause(self, ms):
        """Wait `ms` milliseconds while the window stays live (like bot_show does). During a
        bot run the Skip button can cut the wait short."""
        wait = tk.BooleanVar(value=False)
        self.after(ms, lambda: wait.set(True))
        if self.bot_running:
            self._bot_wait = wait
        self.wait_variable(wait)
        if self.bot_running:
            self._bot_wait = None

    def animate_battle(self, z, label, lead_name, start, final, a_names=(), d_names=(),
                       bombers=(), def_bombers=()):
        """Play a battle out over BATTLE_TICKS ticks, BATTLE_TICK_MS apart. During each tick
        swords swing from the fighting countries (and bombs fall from the sky if air force
        bombs); at the end of the tick every force in zone z moves a tenth of the way from
        its `start` numbers to its `final` numbers and the map is redrawn, so the armies
        bleed away gradually. On the last tick every force holds exactly its final numbers.
        Input is locked meanwhile."""
        if self.bot_running and self.bot_skip:
            return                              # Skip pressed: no pauses for bots
        old_phase = self.phase_var.get()
        frame_ms = max(10, BATTLE_TICK_MS // BATTLE_FX_FRAMES)
        self.battle_busy = True
        try:
            if self.bot_running:
                self.bot_show(z, "battle", f"{lead_name} fights for {label}", pause=False)
            else:
                if self.single_player:
                    self.pan_to_zone(z)         # every battle: bring the camera to it
                self.update_button_states()     # greys out End Phase while it plays
            planes = list(bombers) + list(def_bombers)           # the defenders' planes too
            plane_sides = [1] * len(bombers) + [-1] * len(def_bombers)
            bombs = self.fx_new_bombs(len(planes), BATTLE_TICKS * BATTLE_FX_FRAMES,
                                      plane_sides)
            for t in range(1, BATTLE_TICKS + 1):
                for f in range(BATTLE_FX_FRAMES):       # the fighting, frame by frame
                    if self.bot_running and self.bot_skip:
                        break
                    g = (t - 1) * BATTLE_FX_FRAMES + f  # frame number since the battle began
                    self.fx_draw(z, g, a_names, d_names, planes, bombs)
                    self.battle_pause(frame_ms)
                self.canvas.delete("fx")
                for o, begin in start.items():
                    end = final[o]
                    self.set_force(z, o, {k: int(round(begin[k] + (end[k] - begin[k])
                                                       * t / BATTLE_TICKS))
                                          for k in UNIT_KEYS})
                self.phase_var.set(f"BATTLE IN {label.upper()}  {t}/{BATTLE_TICKS}")
                if t < BATTLE_TICKS:            # the caller redraws after the final tick
                    self.refresh_forces_list()
                    self.draw_map()
                    self.refresh_info()
        finally:
            self.canvas.delete("fx")
            self.battle_busy = False
            self.phase_var.set(old_phase)

    # ---------------- battle effects: swords, sparks, bombs ----------------

    # A bomber circles above the zone in a loop of BOMB_LOOP_FRAMES frames: it flies in over
    # the target, drops bombs, banks round at the end, flies back along the top of the loop
    # and comes round again for the next pass. Bombs are released at these frames of each loop.
    BOMB_LOOP_FRAMES = 16
    BOMB_RELEASES = (2, 5)

    def fx_new_bombs(self, n_bombers, total_frames, sides=None):
        """Every bomb of the whole battle: which plane drops it, the frame it is released
        (counted from the start of the battle) and where it lands. Planes are staggered so
        they don't fly on top of each other. `sides` (1 = attacker's plane, -1 = defender's)
        makes a plane bomb the enemy's half of the field: the defenders stand on the right."""
        loop = self.BOMB_LOOP_FRAMES
        bombs = []
        for k in range(min(n_bombers, 5)):
            for n in range(total_frames // loop + 1):
                for r in self.BOMB_RELEASES:
                    g = n * loop + k * 3 + r
                    if g + 7 <= total_frames:            # bomb has time to land and burst
                        side = sides[k] if sides and k < len(sides) else 0
                        tx = (random.uniform(4, 28) * side if side
                              else random.uniform(-26, 26))
                        bombs.append({"k": k, "start": g, "tx": tx,
                                      "ty": random.uniform(-14, 14)})
        return bombs

    def fx_sword(self, px, py, ang, length, facing, color, s, trail_ang=None):
        """One sword gripped at (px, py), blade `ang` degrees above horizontal, pointing
        right (facing=1) or left (facing=-1). `color` is the owner's side color (guard and
        pommel). trail_ang draws a faint streak where the blade just was."""
        c = self.canvas

        def vec(a):
            r = math.radians(a)
            return facing * math.cos(r), -math.sin(r)

        if trail_ang is not None:
            tx, ty = vec(trail_ang)
            c.create_line(px + tx * length * 0.3, py + ty * length * 0.3,
                          px + tx * length, py + ty * length,
                          fill="#dfe6e9", width=max(2, 3 * s), tags="fx")
        vx, vy = vec(ang)
        nx, ny = -vy, vx
        gx, gy = px + vx * length * 0.2, py + vy * length * 0.2        # guard position
        tipx, tipy = px + vx * length, py + vy * length
        w = 3.4 * s
        c.create_line(px, py, gx, gy, fill="#5d4037", width=max(3, 4 * s), tags="fx")  # grip
        c.create_polygon(gx + nx * w, gy + ny * w, tipx, tipy, gx - nx * w, gy - ny * w,
                         fill="#ecf0f1", outline="#2c3e50", width=1, tags="fx")        # blade
        c.create_line(gx + vx * length * 0.1, gy + vy * length * 0.1,
                      tipx - vx * 3 * s, tipy - vy * 3 * s,
                      fill="#bdc3c7", width=1, tags="fx")                              # fuller
        c.create_line(gx + nx * 6 * s, gy + ny * 6 * s, gx - nx * 6 * s, gy - ny * 6 * s,
                      fill=color, width=max(3, 4 * s), capstyle="round", tags="fx")    # guard
        c.create_oval(px - 3 * s, py - 3 * s, px + 3 * s, py + 3 * s,
                      fill=color, outline="#2c3e50", tags="fx")                        # pommel

    def fx_sparks(self, x, y, s):
        """Burst of sparks where two blades meet."""
        c = self.canvas
        c.create_oval(x - 5 * s, y - 5 * s, x + 5 * s, y + 5 * s, fill="#ffffff",
                      outline="#f9e79f", width=2, tags="fx")
        for _ in range(9):
            a = random.uniform(0, 2 * math.pi)
            r0, r1 = 5 * s, random.uniform(10, 21) * s
            c.create_line(x + r0 * math.cos(a), y + r0 * math.sin(a),
                          x + r1 * math.cos(a), y + r1 * math.sin(a),
                          fill=random.choice(("#f1c40f", "#ffffff", "#e67e22")),
                          width=2, tags="fx")

    def fx_blast(self, x, y, r, fill):
        """A spiky, flickering explosion cloud."""
        pts = []
        n = 10
        for i in range(n * 2):
            a = math.pi * i / n + random.uniform(-0.12, 0.12)
            rr = r * (1.0 if i % 2 == 0 else 0.55) * random.uniform(0.85, 1.1)
            pts += [x + rr * math.cos(a), y + rr * math.sin(a)]
        self.canvas.create_polygon(pts, fill=fill, outline="", tags="fx")

    def fx_bomb(self, x, y, dx, dy, s):
        """A falling bomb at (x, y) heading along (dx, dy)."""
        d = math.hypot(dx, dy) or 1.0
        ux, uy = dx / d, dy / d
        nx, ny = -uy, ux

        def at(a, b):
            return (x + ux * a * s + nx * b * s, y + uy * a * s + ny * b * s)

        pts = []
        for a, b in ((7, 0), (4, 3), (-3, 3), (-7, 5.5), (-8, 0), (-7, -5.5), (-3, -3),
                     (4, -3)):
            pts += list(at(a, b))
        self.canvas.create_polygon(pts, fill="#2c3e50", outline="#000000", width=1,
                                   tags="fx")

    def fx_draw(self, z, f, a_names, d_names, bombers, bombs):
        """Draw frame `f` (counted from the start of the battle) of the fighting in zone z on top of the
        map: attackers' swords from the left, defenders' from the right, swinging in turn
        and clashing in sparks; and, if there are bombers, their planes flying over with
        bombs that fall and explode."""
        c = self.canvas
        c.delete("fx")
        if z not in self.zones:
            return
        cx, cy = self.to_screen(*self.zones[z]["centroid"])
        s = self.token_scale()
        length = 34 * s
        raised, strike = 70, -8                  # blade angle: raised overhead -> striking

        def swing(ph):
            return raised + (strike - raised) * (ph / 3) ** 1.4

        for names, facing, offset in ((a_names, 1, 0), (d_names, -1, 2)):
            names = list(names)
            gap = 20 if len(names) <= 3 else max(7, 60 / len(names))   # squeeze big sides in
            for i, o in enumerate(names):
                ph = (f + offset + i) % 4        # a swing every 4 frames; sides alternate
                py = cy + (i - (len(names) - 1) / 2) * gap * s
                px = cx - facing * (3 * s + length * 0.99)
                color = SIDE_COLOR[self.nations[o].side]
                self.fx_sword(px, py, swing(ph), length, facing, color, s,
                              swing(ph - 1) if ph > 0 else None)
                if ph == 3:
                    self.fx_sparks(cx, py, s)    # the blades meet

        if bombers:
            sky = max(18 + 16 * s, cy - 130 * s)         # height of the bombers' loop
            loop = self.BOMB_LOOP_FRAMES

            def plane_at(k, frame):
                """(x, y, facing) of bomber k: an oval loop - rightwards along the bottom
                (over the target), leftwards along the top, turning round at both ends."""
                th = 2 * math.pi * (frame - k * 3) / loop
                x = cx - 90 * s * math.cos(th)
                y = sky + k * 22 * s + 16 * s * math.sin(th)
                return x, y, (1 if math.sin(th) >= 0 else -1)

            for k, o in enumerate(list(bombers)[:5]):
                x, y, face = plane_at(k, f)
                self.draw_plane_bg(x, y, 34 * s, 13 * s, "fx", None, o, facing=face)
            for b in bombs:
                rel = f - b["start"]
                if rel < 0:
                    continue
                ox, oy, _ = plane_at(b["k"], b["start"])    # released from the plane
                gx, gy = cx + b["tx"] * s, cy + b["ty"] * s

                def pos(q):
                    return ox + (gx - ox) * q, oy + (gy - oy) * q ** 1.6

                if rel == 0:                                  # the plane fires: muzzle flash
                    c.create_oval(ox - 5 * s, oy - 3 * s, ox + 5 * s, oy + 7 * s,
                                  fill="#f9e79f", outline="#e67e22", tags="fx")
                if rel < 3:                                   # falling
                    x0, y0 = pos(rel / 3)
                    x1, y1 = pos((rel + 1) / 3)
                    c.create_line(x0, y0, x1, y1, fill="#95a5a6", width=2, tags="fx")
                    self.fx_bomb(x1, y1, x1 - x0, y1 - y0, s)
                elif rel < 7:                                 # exploding
                    e = rel - 3
                    r = (7 + 9 * e) * s
                    if e == 3:
                        c.create_oval(gx - r, gy - r * 0.8, gx + r, gy + r * 0.8,
                                      fill="#7f8c8d", outline="", tags="fx")   # smoke
                        self.fx_blast(gx, gy, r * 0.5, "#e67e22")
                    else:
                        if e >= 1:
                            c.create_oval(gx - r * 1.5, gy - r * 1.1, gx + r * 1.5,
                                          gy + r * 1.1, outline="#f9e79f", width=2,
                                          tags="fx")                           # shockwave
                        self.fx_blast(gx, gy, r, "#c0392b")
                        self.fx_blast(gx, gy, r * 0.7, "#e67e22")
                        c.create_oval(gx - r * 0.35, gy - r * 0.35, gx + r * 0.35,
                                      gy + r * 0.35, fill="#f9e79f", outline="",
                                      tags="fx")                               # fireball
                    for _ in range(5):                        # flying debris
                        a = random.uniform(0, 2 * math.pi)
                        dd = r * random.uniform(1.1, 1.7)
                        c.create_oval(gx + dd * math.cos(a) - 1.5 * s,
                                      gy + dd * math.sin(a) - 1.5 * s,
                                      gx + dd * math.cos(a) + 1.5 * s,
                                      gy + dd * math.sin(a) + 1.5 * s,
                                      fill="#2c3e50", outline="", tags="fx")
        c.tag_raise("fx")

    def historical_troops(self, name, year):
        """Troops a country historically had at the start of `year` (1 troop =
        SOLDIERS_PER_TROOP soldiers)."""
        row = ARMY_STRENGTH_K[name]
        idx = max(0, min(len(row) - 1, int(year) - START_YEAR))
        return max(1, int(round(row[idx] * 1000 / SOLDIERS_PER_TROOP)))

    def yearly_troops(self, n):
        """Troops that appear in a country's center each new year: enough to bring its
        army (including forces en route) up to its historical size for this year."""
        only_years = TROOP_GAIN_ONLY_IN_YEARS.get(n.name)
        if only_years is not None and int(self.year) not in only_years:
            return 0                    # e.g. France: no new troops except in 1941
        fixed = YEARLY_TROOP_GAIN_OVERRIDE.get((n.name, int(self.year)))
        if fixed is not None:
            return max(0, int(fixed))
        # Fixed base number for the year: it does NOT depend on how many troops the
        # country still has, so losing your whole army is not refilled for free.
        base = self.historical_troops(n.name, self.year)
        mult = YEARLY_TROOP_MULT.get(n.name, 1.0) if int(self.year) >= 1941 else 1.0   # 1940 is not nerfed
        return max(0, int(round(base * mult)))

    def spawn_reinforcements(self, n):
        """New year: reinforce the army historically, plus air and navy in proportion to its troops."""
        if n.name in MINOR_COUNTRIES:
            return                      # unplayable countries never raise troops

        home = self.capital_zone[n.name]
        troops = self.yearly_troops(n)
        if self.zone_occupier.get(home) is None and troops > 0:
            self.add_force(home, n.name, new_units(troops, 0, 0))
            self.log_msg(f"{n.name} mobilizes {troops} new troops at its center "
                         f"(historical army of {int(self.year)}).")

        # Every January, add 25% of the country's ORIGINAL starting air force and navy.
        # Starting values are scaled the same way as the initial deployment: x100,
        # with navy receiving the existing x3 navy-size multiplier.
        # The amount scales with the army the country has now: its starting air/navy per
        # starting troop, times its current troops.
        _, starting_navy, starting_air = (v * UNIT_SCALE for v in n.start_forces)
        starting_navy *= NAVY_SIZE_MULT
        start_troops = max(1, self.historical_troops(n.name, START_YEAR))
        troops_now = self.nation_units(n.name)["army"]
        yearly_air = max(0, int(round(starting_air / start_troops
                                      * AIR_NAVY_PER_TROOP_SHARE * troops_now)))
        yearly_navy = max(0, int(round(starting_navy / start_troops
                                       * AIR_NAVY_PER_TROOP_SHARE * troops_now)))

        if yearly_air > 0 and self.zone_occupier.get(home) is None:
            self.add_force(home, n.name, new_units(air=yearly_air))
        if yearly_navy > 0 and n.name in self.sea_zone:
            self.add_force(self.sea_zone[n.name], n.name, new_units(navy=yearly_navy))

        if yearly_air > 0 or yearly_navy > 0:
            self.log_msg(f"{n.name} receives yearly reinforcements: "
                         f"+{yearly_air} Air Force, +{yearly_navy} Navy "
                         f"(in proportion to its troops).")

    def economy_tick(self):
        self.log_msg(f"Oil stockpiles lose {int(OIL_DECAY_RATE * 100)}% to waste and "
                     f"consumption this year.")
        for n in self.nations.values():
            if not n.alive:
                continue
            # the old stockpile shrinks first; this year's production is added after it
            n.oil -= int(n.oil * OIL_DECAY_RATE + 0.5)
            n.oil += n.oil_income()
            n.iron += n.iron_income()
            self.spawn_reinforcements(n)
            if n.at_war_with:
                n.stability = max(0, n.stability - 1)
            else:
                n.stability = min(100, n.stability + 1)

    # ---------------- scripted historical events ----------------

    # (tag, year, text, effect method, its arguments). In hotseat each fires in January of
    # its year. In single player each fires on its own turn, shifted by this game's roll.
    SCRIPTED_EVENTS = (
        ("barbarossa", 1941,
         "Germany launches Operation Barbarossa against the USSR, opening the largest "
         "front of the war. Romania joins the invasion.",
         "_war", (("Germany", "USSR"), ("Romania", "USSR"))),
        ("pearl_harbor", 1941,
         "Japan attacks Pearl Harbor. The United States enters the war against Japan "
         "and, soon after, Germany and Italy.",
         "_war", (("Japan", "USA"), ("Germany", "USA"))),
        ("stalingrad", 1942,
         "Brutal urban warfare rages at Stalingrad as Soviet forces grind down the "
         "German advance.",
         "_attrition", ("Germany", 0.15)),
        ("midway", 1942,
         "The Battle of Midway cripples Japan's carrier fleet, turning the tide in the "
         "Pacific.",
         "_attrition", ("Japan", 0.3, ("navy", "air"))),
        ("italy_falls", 1943,
         "Allied landings in Sicily and Italy topple Mussolini's government; Italy "
         "signs an armistice with the Allies.",
         "_occupy_zone", ("Italy", "UK")),
        ("dday", 1944,
         "Allied forces storm the beaches of Normandy on D-Day, opening a major new "
         "front in Western Europe.",
         "_attrition", ("Germany", 0.15)),
        ("berlin", 1945,
         "Soviet forces encircle Berlin as Germany's collapse becomes inevitable.",
         "_occupy_zone", ("Germany", "USSR")),
        ("japan_surrender", 1945,
         "A devastating new weapon forces Japan toward surrender, bringing the war to "
         "a close.",
         "_occupy_zone", ("Japan", "USA")),
    )

    def event_shift(self, tag):
        """Turns this game's version of a historical event comes early (-) or late (+).
        Historical timing is fixed, so this is always 0 (event_shifts stays empty)."""
        return self.event_shifts.get(tag, 0)

    def roll_variation(self):
        """Single player: roll how this game's bots differ. Historical dates never move;
        each bot gets a fixed attacking 'style' and a fresh mood every turn (bot_margin)."""
        self.event_shifts = {}
        self.bot_style = {n: random.uniform(*BOT_STYLE_RANGE) for n in self.nations
                          if n not in MINOR_COUNTRIES}
        self.bot_mood = {}

    def fire_scripted_events(self):
        for tag, year, text, effect, args in self.SCRIPTED_EVENTS:
            if tag in self.events_fired:
                continue
            due = (year - START_YEAR) * TURNS_PER_YEAR + self.event_shift(tag)
            if self.ticks < due:
                continue
            self.events_fired.add(tag)
            self.log_msg(f"HISTORICAL EVENT: {text}")
            if effect == "_attrition" and self.single_player:
                # how brutal it is varies from game to game
                args = (args[0], min(0.6, args[1] * random.uniform(0.6, 1.4))) + tuple(args[2:])
            getattr(self, effect)(*args)
            self.show_message("Historical Event", text)

    def _invade_poland(self):
        """Historical Poland invasion: always place the 1,000 German troops in Poland West."""
        invader, target = "Germany", "Poland"
        dest = f"{target}:0"  # Poland is split West / Center / East.
        if dest not in self.zones:
            # Safety fallback if the map layout ever changes.
            self._spawn_invaders(invader, target, 1000)
            return

        self._war(("Germany", "UK"), ("Germany", "France"), ("Germany", "Poland"))
        self.add_force(dest, invader, new_units(1000, 0, 0))  # ready immediately; not resting
        self.log_msg(f"{invader} launches the historical invasion into {self.zone_label(dest)} with 1,000 troops.")
        self.pan_to_zone(dest)

    def _invade_france(self):
        """Historical France invasion: Germany attacks France's East zone.

        The East zone is always the scripted target instead of choosing an
        arbitrary free outer zone. If French army troops are already there,
        the historical invasion immediately resolves as a battle.
        """
        invader, target = "Germany", "France"
        dest = f"{target}:2"  # France is split West / Center / East.
        # 4,000 troops spawn (Germany's 1941 reinforcement is a fixed 5,800; no debt).
        if dest not in self.zones:
            self._spawn_invaders(invader, target, 4000)
        else:
            self.declare_war(invader, target)
            self.add_force(dest, invader, new_units(4000, 0, 0))
            self.log_msg(f"{invader} launches the historical invasion into {self.zone_label(dest)} "
                         f"with 4,000 troops.")
            self.pan_to_zone(dest)
        if dest not in self.zones:
            return

        french = self.get_force(dest, target)
        if french and french["army"] > 0:
            # The historical invasion starts the battle immediately when
            # French ground troops are already defending the East zone.
            self.fight_battle(dest, {invader: self.battle_units(dest, self.get_force(dest, invader))},
                              {target: self.battle_units(dest, french)}, invader)
        else:
            # No French ground troops: the German landing takes the East zone.
            self.take_zone(invader, dest)

    def _spawn_invaders(self, invader, target, count):
        """Scripted invasion: `count` army troops of `invader` appear in the
        target's West zone, ready to act at once - they are not resting."""
        inv, tgt = self.nations.get(invader), self.nations.get(target)
        if not inv or not tgt:
            return
        # Historical Polish invasion: Germany enters from the west.
        dest = f"{target}:1"
        if dest not in self.zones:
            return
        self.declare_war(invader, target)
        self.add_force(dest, invader, new_units(count, 0, 0))   # no lock = not resting
        self.log_msg(f"{invader} lands {count} troops in {self.zone_label(dest)}.")
        self.pan_to_zone(dest)

    def fire_dated_events(self):
        """Scripted events that fall on a specific two-month turn rather than in January.
        Checked every turn; each fires once, on its date or the first turn after it."""
        def at(year, month_index, tag=None):   # month_index 0 = January ... 10 = November
            # (single player shifts each event by this game's roll; see roll_variation)
            return (((year - START_YEAR) * 12 + month_index) // MONTHS_PER_TURN
                    + self.event_shift(tag))

        # Germany invades Poland in September 1939.  The scripted 1,000 troops
        # are added regardless of how the Polish border zones currently look.
        if self.ticks >= at(1939, 8, "poland") and "poland" not in self.events_fired:
            self.events_fired.add("poland")
            text = ("Germany invades Poland. Britain and France declare war, "
                    "and World War II formally begins.")
            self.log_msg(f"HISTORICAL EVENT: {text}")
            self._invade_poland()
            self.show_message("Historical Event", text)

        # Germany invades France in May 1940.  The scripted 1,000 troops are
        # likewise guaranteed to spawn even if France's zones have changed.
        if self.ticks >= at(1940, 4, "fall_france") and "fall_france" not in self.events_fired:
            self.events_fired.add("fall_france")
            text = ("Germany's blitzkrieg overwhelms the Low Countries and "
                    "France, which falls after a rapid campaign.")
            self.log_msg(f"HISTORICAL EVENT: {text}")
            self._invade_france()
            self.show_message("Historical Event", text)

        if self.ticks >= at(1940, 10, "romania_axis") and "romania_axis" not in self.events_fired:
            self.events_fired.add("romania_axis")
            text = ("Romania signs the Tripartite Pact and joins the Axis. King Carol's "
                    "government has fallen to the pro-German Iron Guard and General "
                    "Antonescu, and German troops pour in to guard the Ploiesti oil fields.")
            self.log_msg(f"HISTORICAL EVENT: {text}")
            self._join_side("Romania", "Axis")
            self.show_message("Historical Event", text)

    def _join_side(self, name, side):
        """A country switches to `side` and goes to war with the enemies of that side's
        members that it is not already allied with."""
        n = self.nations.get(name)
        if not n or not n.alive or n.side == side:
            return
        n.side = side
        for other in self.nations.values():
            if other.name == name or other.name in MINOR_COUNTRIES or not other.alive:
                continue
            if other.side == side:
                for foe in other.at_war_with:
                    if foe in self.nations and self.nations[foe].side != side:
                        self.declare_war(name, foe)
        self.log_msg(f"{name} is now on the {side} side.")

    def _war(self, *pairs):
        for a, b in pairs:
            if a in self.nations and b in self.nations:
                self.declare_war(a, b)

    def _occupy_zone(self, loser_name, winner_name, count=1):
        """Scripted history: winner takes `count` of the loser's outer zones."""
        loser = self.nations.get(loser_name)
        if not loser or not loser.alive or winner_name not in self.nations:
            return
        cap = self.capital_zone[loser_name]
        targets = [z for z in self.nation_zones[loser_name]
                   if z != cap and self.zone_occupier.get(z) is None][:count]
        for z in targets:
            for o in list(self.garrisons.get(z, {})):
                if self.is_hostile(winner_name, o):
                    self.set_force(z, o, new_units())
            self.declare_war(winner_name, loser_name)
            self.take_zone(winner_name, z)

    def _attrition(self, nation_name, fraction, kinds=UNIT_KEYS):
        """Scripted history: a nation loses part of its forces everywhere."""
        for z in self.owned_force_locations(nation_name):
            u = dict(self.garrisons[z][nation_name])
            for k in kinds:
                u[k] = int(round(u[k] * (1 - fraction)))
            self.set_force(z, nation_name, u)

    # ---------------- single player: bot-controlled countries ----------------

    # ---------------- single player: paced, camera-following bot moves ----------------

    def on_close(self):
        self.destroy()
        raise SystemExit                      # also unwinds a bot pause that is waiting

    def skip_bot_wait(self):
        """Skip button: stop pausing for the rest of this bot run."""
        self.bot_skip = True
        if self._bot_wait is not None:
            self._bot_wait.set(True)

    def bot_show(self, z, kind, text, src=None, pause=True):
        """Pan the map to zone `z` (or to fit the move src -> z), redraw, and hold so the
        person can watch a bot's move (BOT_MOVE_DELAY_MS) or battle (BOT_BATTLE_DELAY_MS).
        A move also gets a temporary arrow from src to z. Does nothing outside a
        single-player bot run."""
        if not (self.bot_running and self.single_player) or self.bot_skip or z not in self.zones:
            return
        if pause:
            if self._bot_last_shown == (kind, src, z):
                return                        # same move repeated: one stop is enough
            self._bot_last_shown = (kind, src, z)
        x, y = self.zones[z]["centroid"]
        zoom = max(self.zoom, 3.0)
        if src in self.zones and src != z:
            sx, sy = self.zones[src]["centroid"]
            x, y = (x + sx) / 2, (y + sy) / 2
            self.update_idletasks()
            cw = max(200, self.canvas.winfo_width())
            ch = max(200, self.canvas.winfo_height())
            # leave room for the force boxes drawn around each end of the arrow
            span_x = abs(self.zones[z]["centroid"][0] - sx) + 40
            span_y = abs(self.zones[z]["centroid"][1] - sy) + 40
            zoom = 0.7 * min(cw / span_x, ch / span_y)     # arrow fills most of the screen
            zoom = max(1.0, min(8.0, zoom))
            self._bot_arrow = (src, z)
        else:
            self._bot_arrow = None
        if getattr(self, "_user_zoomed", False):
            zoom = self.zoom                               # respect the player's own zoom
        self.zoom = zoom
        self.pan_x = MAP_W / 2 - x * self.zoom
        self.pan_y = MAP_H / 2 - y * self.zoom
        self.bot_var.set(text)
        self.bot_color = "#ffffff"
        for nm, nat in self.nations.items():     # text starts with the acting country's name
            if text.startswith(nm + " "):
                self.bot_color = SIDE_COLOR[nat.side]
                break
        self.refresh_map_messages()
        self.draw_map()
        self.refresh_info()
        if not pause:
            return                            # just move the camera; the caller does the waiting
        wait = tk.BooleanVar(value=False)
        self._bot_wait = wait
        delay = BOT_BATTLE_DELAY_MS if kind == "battle" else BOT_MOVE_DELAY_MS
        self.after(delay, lambda: wait.set(True))
        self.wait_variable(wait)              # UI stays live (pan/zoom) while we wait
        self._bot_wait = None
        if self._bot_arrow:                   # the arrow is temporary
            self._bot_arrow = None
            self.canvas.delete("botarrow")

    def start_bots(self):
        """Run the opening Axis bot phase, then hand control to the player.

        Single-player order is always: Axis bots -> player -> Allied bots -> next round.
        The calendar advances when an automatic side's phase begins, so the normal
        two-month tick is applied once for the Allied bot phase and once for the next
        Axis bot phase.  `player_turn_active` is the authoritative gate for human orders.
        """
        if not self.single_player or self.game_over:
            return

        player_side = self.player.side
        self.player_turn_active = False
        self.phase = "Axis War Phase"
        if not self.advance_calendar_tick():
            return
        self.play_bot_phases("Axis")
        if self.game_over:
            return

        self.phase = "Axis War Phase" if player_side == "Axis" else "Allied War Phase"
        self.player_turn_active = True
        self.refresh_all()

    def play_bot_phases(self, side=None):
        """Run bots for exactly one side.

        `side` is explicit so a bot can never be accidentally skipped because the
        current phase happens to disagree with the intended bot side.  If omitted,
        the current phase determines the side for compatibility with older callers.
        """
        if self.bot_running:
            return
        if side is None:
            side = "Axis" if self.phase == "Axis War Phase" else "Allies"

        self.bot_running = True
        self.bot_skip = False
        self._bot_last_shown = None
        self._user_zoomed = False
        saved_view = (self.zoom, self.pan_x, self.pan_y)
        self.btn_skip.pack(side="left", padx=(8, 0))
        for b in (self.btn_trade, self.btn_objectives):
            b.config(state="disabled")
        try:
            if not self.game_over and self.player.alive:
                # Show the active side immediately, including its side color, while bots move.
                self.phase = "Axis War Phase" if side == "Axis" else "Allied War Phase"
                self.phase_var.set(f"{side.upper()} BOTS ARE MOVING...")
                self.phase_badge.config(bg=SIDE_COLOR["Axis" if side == "Axis" else "Allies"])
                self.btn_end.config(state="disabled")
                self.update_idletasks()
                self.run_bot_turns(side)
            elif not self.player.alive and not self.game_over:
                self.log_msg(f"{self.player_name} has been defeated. Your war is over.")
                self.show_message("Defeated",
                                  f"{self.player_name} has been completely defeated.")
                self.end_game(f"{self.player_name.upper()} DEFEATED - "
                              f"{self.date_label().upper()}")
        finally:
            self.bot_running = False
            self._bot_wait = None
            self._bot_arrow = None
            self.btn_skip.pack_forget()
            self.bot_var.set("")
            self.refresh_map_messages()
            self.zoom, self.pan_x, self.pan_y = saved_view
        if not self.game_over:
            self.refresh_all()

    def run_bot_turns(self, side=None):
        """Run every living bot belonging to `side`, exactly once."""
        if side is None:
            side = "Axis" if self.phase == "Axis War Phase" else "Allies"

        bots = [n for n in self.nations.values()
                if self.is_bot(n) and n.alive
                and (n.side == side or (side == "Allies" and n.side == "Neutral"))]
        random.shuffle(bots)
        for bot in bots:
            try:
                self.bot_take_turn(bot)
            except Exception as exc:
                import traceback
                traceback.print_exc()
                self.log_msg(f"({bot.name} bot skipped its turn: {exc})")
            if not self.player.alive:
                return

    def bot_margin(self, bot):
        """How many times the defenders' power the bot wants before it attacks: its country's
        base margin, scaled by its personality (rolled once per game) and its mood this turn."""
        base = BOT_ATTACK_MARGIN.get(bot.name, BOT_DEFAULT_MARGIN)
        scale = self.bot_style.get(bot.name, 1.0) * self.bot_mood.get(bot.name, 1.0)
        return max(BOT_MIN_MARGIN, base * scale)

    def bot_take_turn(self, bot):
        self._bot_last_shown = None
        # a fresh mood every turn: now and then a bot is bold or cautious
        self.bot_mood[bot.name] = random.choices(
            [m for m, _ in BOT_MOOD_CHOICES], [w for _, w in BOT_MOOD_CHOICES])[0]
        self.bot_claim_objective(bot)
        enemies = self.bot_enemies(bot)

        # A bot still gets a real turn even when it has no current enemy.  Previously
        # this early return made peaceful Axis countries (notably Italy before 1940)
        # appear to be completely inactive when the player chose Germany.
        if not enemies:
            self.bot_prepare(bot)
            # Germany masses its army before the war: a few extra opening moves.
            if bot.name == "Germany" and self.year < 1939.6:
                for _ in range(GERMANY_EXTRA_OPENING_MOVES):
                    self.bot_prepare(bot)
            return

        self.bot_resolve_battles(bot, enemies)       # finish fights already under way
        self.bot_claim_zones(bot, enemies)           # claim undefended zones we stand in
        self.bot_garrison(bot, enemies)              # cover border zones facing the enemy
        if random.random() >= BOT_HESITATE_CHANCE:   # now and then a bot hesitates
            self.bot_attack(bot, enemies)            # strike adjacent enemy zones
        self.bot_amphibious(bot, enemies)            # landings across the sea
        self.bot_advance(bot, enemies)               # march toward the nearest enemy
        self.bot_resolve_battles(bot, enemies)

    def bot_prepare(self, bot):
        """Make a useful peacetime move so a bot does not silently skip its phase.

        Move a modest portion of the largest available home army stack into a neighboring
        home zone that has fewer troops.  This is only internal repositioning: it never
        crosses a border, declares war, or moves air force/navy, and therefore cannot
        cause a peaceful country to start an unintended invasion.
        """
        candidates = []
        for src in self.owned_force_locations(bot.name):
            if self.is_sea_zone(src):
                continue
            available = self.available_units(src, bot.name)["army"]
            if available < 4 or self.zone_nation(src) != bot.name:
                continue
            for dst in self.land_adj.get(src, ()):
                if self.is_sea_zone(dst) or self.zone_nation(dst) != bot.name:
                    continue
                if not self.can_move_one_space(src, dst):
                    continue
                dst_force = self.get_force(dst, bot.name)
                dst_army = dst_force["army"] if dst_force else 0
                candidates.append((available - dst_army, -dst_army, src, dst, available))

        if not candidates:
            return

        candidates.sort(reverse=True)
        _, _, src, dst, available = random.choice(candidates[:3])

        # Italy gets a little extra pre-war activity so it does not sit completely
        # still during the opening Axis phases.  Before Italy's historical entry
        # into the war, move a larger share of the army toward the French frontier
        # and reposition part of the fleet westward.  These are only home/sea
        # movements; no war is declared and no enemy zone is entered.
        if bot.name == "Italy" and self.year < 1940.4:
            italy_west = "Italy:0"
            italy_center = "Italy:1"
            if (self.get_force(italy_center, bot.name) and
                    self.get_force(italy_center, bot.name)["army"] > 0 and
                    self.can_move_one_space(italy_center, italy_west)):
                ready = self.available_units(italy_center, bot.name)["army"]
                if ready > 0:
                    amount = max(1, ready // 3)
                    if self.execute_send(italy_center, italy_west, bot, False,
                                         new_units(army=amount)):
                        self.bot_show(italy_west, "move",
                                      f"{bot.name} deploys troops toward {self.zone_label(italy_west)}",
                                      italy_center)

            # Shift a portion of the Italian fleet toward another available
            # Mediterranean sea zone so the navy also visibly takes an opening move.
            fleet_locs = [l for l in self.owned_force_locations(bot.name)
                          if self.is_sea_zone(l) and self.available_units(l, bot.name)["navy"] > 0]
            if fleet_locs:
                fleet = max(fleet_locs,
                             key=lambda l: self.available_units(l, bot.name)["navy"])
                navy = self.available_units(fleet, bot.name)["navy"]
                sea_targets = [z for z in self.sea_zones
                               if z != fleet and self.navy_steps(fleet, z) == 1]
                if navy > 0 and sea_targets:
                    # Prefer a nearby free sea zone rather than one occupied by hostile forces.
                    sea_targets.sort(key=lambda z: 0 if not self.hostile_forces_at(z, bot.name) else 1)
                    sea_dst = sea_targets[0]
                    move_navy = max(1, navy // 4)
                    self.execute_send(fleet, sea_dst, bot, False, new_units(navy=move_navy))

        # Always make the normal peace-time repositioning as well.
        amount = max(1, int(available * random.uniform(0.12, 0.28)))
        if self.execute_send(src, dst, bot, False, new_units(army=amount)):
            self.bot_show(dst, "move",
                          f"{bot.name} repositions troops to {self.zone_label(dst)}", src)

    def bot_claim_objective(self, bot):
        if bot.alive and not bot.objective_claimed and bot.objective_met(self.year):
            number = bot.objective_index + 1
            oil = self.reward_oil(bot)
            iron = self.reward_iron(bot)
            bot.oil += oil
            bot.iron += iron
            bot.claim_objective()             # one per turn; the next one then appears
            self.log_msg(f"{bot.name} achieves objective {number} and claims +{oil} oil and +{iron} iron.")

    def bot_enemies(self, bot):
        """Countries this bot is willing to fight: those it is at war with (scripted
        events, or wars someone started by attacking) plus the historical schedule.
        Bots never pick fights with minor countries or with powers they have no war
        with."""
        names = set(bot.at_war_with)
        for since, group_a, group_b, tag in BOT_WAR_SCHEDULE:
            if self.year + 1e-6 >= since + self.event_shift(tag) / TURNS_PER_YEAR:
                if bot.name in group_a:
                    names |= group_b
                elif bot.name in group_b:
                    names |= group_a
        return {x for x in names
                if x in self.nations and x not in MINOR_COUNTRIES
                and self.nations[x].alive and self.is_hostile(bot.name, x)}

    def bot_zone_state(self, bot, z, enemies):
        """'enemy'  - held by, or holding forces of, a country the bot is at war with
        'blocked' - entering would provoke a country the bot is not at war with
        'safe'    - the bot may move in freely"""
        foes = self.hostile_forces_at(z, bot.name)
        if any(o not in enemies for o in foes):
            return "blocked"
        ctrl = self.controller(z)
        if ctrl is not None and self.is_hostile(bot.name, ctrl) and ctrl not in enemies:
            return "blocked"
        if foes or (ctrl is not None and ctrl in enemies):
            return "enemy"
        return "safe"

    def bot_zone_defense(self, bot, z):
        """Combined power of the hostile fighting units standing in zone z."""
        total = 0.0
        for o, u in self.garrisons.get(z, {}).items():
            if o in self.nations and self.is_hostile(bot.name, o):
                total += units_power(self.battle_units(z, u), self.nations[o])
        return total

    def bot_friendly_power(self, bot, z):
        """Power of the bot's own and its (bot-controlled) allies' fighters already in z."""
        total = 0.0
        for o, u in self.garrisons.get(z, {}).items():
            if o == self.player_name or o not in self.nations:
                continue
            if o == bot.name or self.are_allies(bot, self.nations[o]):
                total += units_power(self.battle_units(z, u), self.nations[o])
        return total

    def bot_reserve(self, bot, loc, enemies):
        """Troops that should stay in `loc` to hold it against enemy armies next door."""
        if self.zone_nation(loc) != bot.name:
            return 0
        threat = 0.0
        for z in self.land_adj.get(loc, ()):
            for o, u in self.garrisons.get(z, {}).items():
                if o in enemies:
                    threat += units_power(new_units(army=u["army"]), self.nations[o])
        return int(math.ceil(threat / max(0.2, bot.army_rating / 5)))

    def bot_free_troops(self, bot, enemies):
        """{land zone: rested troops the bot can spare}."""
        free = {}
        for loc in self.owned_force_locations(bot.name):
            if self.is_sea_zone(loc):
                continue
            n = self.available_units(loc, bot.name)["army"] - self.bot_reserve(bot, loc, enemies)
            if n > 0:
                free[loc] = n
        return free

    def bot_resolve_battles(self, bot, enemies, only=None):
        """Start battles the bot expects to win in contested zones where it has troops.
        The human player's units are never committed to a bot's battle."""
        margin = self.bot_margin(bot)
        zones = [only] if only else [z for z in list(self.garrisons) if self.is_contested(z)]
        for z in zones:
            sides = self.battle_sides(z, bot)
            if not sides:
                continue
            att, dfn = sides
            # Bots may only start battles with troops that have finished resting.
            # battle_sides() allows units marked fight_ok to fight immediately after
            # marching in, which is useful for human attacks, but bots must wait until
            # their next turn before attacking with newly moved troops.
            strict_att = {}
            for o in att:
                ready = self.available_units(z, o)
                ready = self.battle_units(z, ready)
                if units_total(ready) > 0:
                    strict_att[o] = ready
            att = {o: u for o, u in strict_att.items() if o != self.player_name}
            if bot.name not in att or any(o not in enemies for o in dfn):
                continue
            a_mult, d_mult, _ = self.battle_modifiers(z, list(att), list(dfn))
            a_power = (sum(units_power(u, self.nations[o]) * a_mult[o]
                           for o, u in att.items()) * ATTACKER_PENALTY
                       * self.bot_defender_air_factor(bot, z))      # they may bomb back
            d_power = sum(units_power(u, self.nations[o]) * d_mult[o] for o, u in dfn.items())
            if self.bot_bomb_plan(bot, a_power, d_power, {bot.name: bot.bombing_uses}) != []:
                self.bot_send_air(bot, None, z)        # a bomb could matter: fly a plane in
            bombers = [o for o, u in self.garrisons[z].items()
                       if u.get("air", 0) > 0 and o != self.player_name
                       and self.nations[o].alive and self.nations[o].bombing_uses > 0
                       and (o == bot.name or self.are_allies(bot, self.nations[o]))]
            plan = self.bot_bomb_plan(bot, a_power, d_power,
                                      {o: self.nations[o].bombing_uses for o in bombers})
            if plan is None:
                continue                          # odds too poor even with bombing: wait
            self.fight_battle(z, att, dfn, bot.name, {o: 1 for o in plan})
            self.bot_show(z, "battle", f"{bot.name} fights for {self.zone_label(z)}")

    def bot_bomb_plan(self, bot, a_power, d_power, uses):
        """Which of the countries in `uses` ({country: bombings left}) the bot decides to
        bomb with in a battle of attacking power a_power against d_power. Returns the list
        (possibly empty), or None if even bombing with all of them leaves the odds too poor
        to attack. A bombing is a scarce resource, so the bot only spends one when:
          - the fight is not won without it (it uses the fewest that make the odds good), or
          - the win is not comfortable (BOT_BOMB_COMFORT) - then one insurance bombing, but
            only from a country with more than one left, so each keeps its last for a
            fight that really needs it."""
        margin = self.bot_margin(bot)
        pool = sorted((o for o, n in uses.items() if n > 0), key=lambda o: -uses[o])
        for k in range(len(pool) + 1):            # fewest bombings that make it worthwhile
            if a_power >= d_power * max(0.0, 1 - 0.1 * k) * margin:
                if k > 0:
                    return pool[:k]
                if a_power >= d_power * margin * BOT_BOMB_COMFORT:
                    return []                     # safe win: save the bombing
                spare = [o for o in pool if uses[o] > 1]
                return spare[:1]                  # close fight: one insurance bombing
        return None

    def bot_claim_zones(self, bot, enemies):
        """Attack undefended enemy zones where the bot has rested troops (moving in alone
        does not claim a zone). The human player's troops are never committed."""
        for z in list(self.garrisons):
            ctrl = self.controller(z) if not self.is_sea_zone(z) else None
            if ctrl is None or ctrl not in enemies:
                continue
            att = self.claim_sides(z, bot)
            if not att:
                continue
            att = {o: u for o, u in att.items() if o != self.player_name}
            if bot.name not in att:
                continue
            self.claim_zone(z, bot, att)
            self.bot_show(z, "battle", f"{bot.name} claims {self.zone_label(z)}")

    def bot_garrison(self, bot, enemies):
        """Put troops into empty home zones that face the enemy, so a token force can't
        simply walk in. A quarter of the neighbouring home stack goes."""
        for z in self.nation_zones.get(bot.name, ()):
            if self.zone_occupier.get(z) is not None:
                continue                              # lost zone: bot_attack retakes it
            held = self.get_force(z, bot.name)
            if held and held["army"] > 0:
                continue
            if not any(self.bot_zone_state(bot, n, enemies) == "enemy"
                       for n in self.land_adj.get(z, ())):
                continue
            stacks = {l: self.available_units(l, bot.name)["army"]
                      for l in self.owned_force_locations(bot.name)
                      if not self.is_sea_zone(l) and self.can_move_one_space(l, z)
                      and self.zone_nation(l) == bot.name}
            if stacks:
                src = max(stacks, key=stacks.get)
                if stacks[src] >= 4:
                    self.execute_send(src, z, bot, False, new_units(
                        army=max(1, int(stacks[src] * random.uniform(0.2, 0.33)))))

    def bot_attack(self, bot, enemies):
        """Attack adjacent enemy zones, pooling every nearby stack against the weakest
        target first."""
        margin = self.bot_margin(bot)
        per = max(0.2, bot.army_rating / 5)       # power of one troop
        tried = set()
        for _ in range(12):
            stacks = self.bot_free_troops(bot, enemies)
            if not stacks:
                return
            options = []
            for z in {z for loc in stacks for z in self.land_adj.get(loc, ())}:
                if z in tried or self.bot_zone_state(bot, z, enemies) != "enemy":
                    continue
                feeders = [loc for loc in stacks if self.can_move_one_space(loc, z)]
                if not feeders:
                    continue
                d = self.bot_zone_defense(bot, z)
                if d <= 0 and self.bot_friendly_power(bot, z) > 0:
                    continue                      # already standing there: claim it next turn
                ratio = self.bot_terrain_ratio(bot, z)      # terrain / winter odds shift
                have = (self.bot_friendly_power(bot, z)
                        + sum(stacks[l] for l in feeders) * per) * ratio
                # a bombing run (-10% defenders) is counted on if planes can reach the zone
                air_ok = bot.bombing_uses > 0 and any(
                    self.available_units(l, bot.name)["air"] > 0
                    and self.air_steps(l, z) is not None for l in feeders)
                factor = 0.9 if air_ok else 1.0
                if d <= 0 or have * ATTACKER_PENALTY >= d * margin * factor:
                    options.append((d * factor, z, feeders))
            if not options:
                return
            if len(options) > 1 and random.random() < BOT_RANDOM_TARGET_CHANCE:
                d, z, feeders = random.choice(options)      # any workable target, not just the weakest
            else:
                d, z, feeders = min(options, key=lambda o: o[0])
            tried.add(z)
            if d <= 0:                            # undefended: a detachment walks in (claims next turn)
                loc = max(feeders, key=lambda l: stacks[l])
                plan = [(loc, max(1, int(stacks[loc] * random.uniform(0.12, 0.3))))]
            else:                                 # defended: send a comfortable surplus
                ratio = self.bot_terrain_ratio(bot, z)
                need = (d * margin / (ATTACKER_PENALTY * ratio)
                        - self.bot_friendly_power(bot, z)) / per
                goal, got, plan = int(max(1, need) * random.uniform(1.35, 1.9)) + 1, 0, []
                for loc in sorted(feeders, key=lambda l: -stacks[l]):
                    take = min(stacks[loc], goal - got)
                    if take > 0:
                        plan.append((loc, take))
                        got += take
                    if got >= goal:
                        break
            send_air = False
            if d > 0:                             # would the bot bomb this fight?
                power = ((self.bot_friendly_power(bot, z) + sum(n for _, n in plan) * per)
                         * ATTACKER_PENALTY * self.bot_terrain_ratio(bot, z))
                send_air = self.bot_bomb_plan(bot, power, self.bot_zone_defense(bot, z),
                                              {bot.name: bot.bombing_uses}) != []
            for loc, n in plan:
                if self.execute_send(loc, z, bot, True, new_units(army=n)):
                    continue
                if send_air:
                    self.bot_send_air(bot, loc, z)
            self.bot_resolve_battles(bot, enemies, only=z)

    def bot_send_air(self, bot, loc, dest):
        """Bring a plane to a battle zone so it can bomb: one plane is enough (a bombing
        needs air force present, nothing more). It comes from the closest of the bot's
        air stacks within flying range - `loc`, where the attacking troops set out, is
        tried first - unless the bot already has planes in the zone."""
        if bot.bombing_uses <= 0 or self.get_force(dest, bot.name) and \
                self.garrisons[dest][bot.name]["air"] > 0:
            return
        best = None
        for l in self.owned_force_locations(bot.name):
            if l == dest or self.is_sea_zone(l) or self.is_sea_zone(dest):
                continue
            if self.available_units(l, bot.name)["air"] <= 0:
                continue
            steps = self.air_steps(l, dest)
            if steps is None:
                continue
            key = (l != loc, steps)
            if best is None or key < best[0]:
                best = (key, l)
        if best:
            self.execute_send(best[1], dest, bot, True, new_units(air=1))

    def bot_amphibious(self, bot, enemies):
        """Ferry troops by sea to an enemy zone on another landmass. A fleet can only land
        on zones that border its own sea zone, so when no target is in reach it sails
        along the coast toward the best one first."""
        if any(o["owner"] == bot.name and self.is_sea_zone(o["origin"])
               for o in self.pending_offensives):
            return                                # a landing (or a fleet) is already on its way
        if random.random() < BOT_AMPHIBIOUS_SKIP_CHANCE:
            return                                # not this turn
        fleets = {z: self.available_units(z, bot.name)["navy"]
                  for z in self.owned_force_locations(bot.name) if self.is_sea_zone(z)}
        fleets = {z: n for z, n in fleets.items() if n > 0}
        armies = self.bot_free_troops(bot, enemies)
        if not fleets or not armies:
            return
        home = max(armies, key=armies.get)        # troops are drawn from the biggest stack
        per = max(0.2, bot.army_rating / 5)
        best = sail = None
        for z in self.zones:
            if (self.is_sea_zone(z) or self.region(z) == self.region(home)
                    or not self.can_enter_center(bot, z)
                    or self.bot_zone_state(bot, z, enemies) != "enemy"):
                continue
            d = self.bot_zone_defense(bot, z)
            for fleet, ships in fleets.items():
                troops = min(armies[home], ships)
                if d > 0 and troops * per * ATTACKER_PENALTY < d * BOT_AMPHIBIOUS_MARGIN:
                    continue
                if self.can_land_on(fleet, z):
                    key = (self.travel_turns(fleet, z), d)
                    if best is None or key < best[0]:
                        best = (key, fleet, z, troops)
                else:
                    # not on this fleet's coast: remember the nearest sea zone that is
                    for sea, land in self.sea_land_adj.items():
                        if z in land:
                            key = (self.travel_turns(fleet, sea), d)
                            if sail is None or key < sail[0]:
                                sail = (key, fleet, sea, ships)
        if best:
            _, fleet, z, troops = best
            self.execute_send(fleet, z, bot, True, new_units(army=troops, navy=troops),
                              None, home, False)
        elif sail:
            _, fleet, sea, ships = sail
            path = self.sea_path(fleet, sea)
            if path and len(path) > 1:            # one move covers at most NAVY_MOVE_ZONES zones
                sea = path[min(NAVY_MOVE_ZONES, len(path) - 1)]
                self.execute_send(fleet, sea, bot, False, new_units(navy=ships), None, None, False)

    def bot_advance(self, bot, enemies):
        """Stacks with no enemy next door step one zone toward the nearest enemy zone."""
        targets = {z for z in self.zones if not self.is_sea_zone(z)
                   and self.bot_zone_state(bot, z, enemies) == "enemy"}
        if not targets:
            return
        for loc, n in self.bot_free_troops(bot, enemies).items():
            if loc in targets or any(z in targets and self.can_move_one_space(loc, z)
                                     for z in self.land_adj.get(loc, ())):
                continue                          # already at the front: wait to attack
            if random.random() < BOT_HOLD_CHANCE:
                continue                          # this stack waits a turn
            step = self.bot_next_step(bot, loc, targets, enemies)
            if step:
                go = n if n < 4 else max(1, int(n * random.uniform(0.7, 1.0)))
                self.execute_send(loc, step, bot, False, new_units(army=go))

    def bot_next_step(self, bot, start, targets, enemies):
        """First zone on the shortest land route from `start` to any target zone."""
        prev = {start: None}
        queue = [start]
        for a in queue:
            for b in self.land_adj.get(a, ()):
                if b in prev or not self.can_move_one_space(a, b):
                    continue
                state = self.bot_zone_state(bot, b, enemies)
                if state == "blocked":
                    continue
                prev[b] = a
                if b in targets:
                    if a == start:
                        return None               # adjacent: bot_attack's job
                    while prev[a] != start:
                        a = prev[a]
                    return a
                queue.append(b)
        return None

    # ---------------- turn/phase progression ----------------

    def end_phase(self):
        if self.game_over or self.bot_running or self.battle_busy:
            return

        if self.single_player:
            player_side = self.player.side

            # Lock the human out while the automatic sides act.
            self.player_turn_active = False

            # Allied bots begin their automatic phase.  The calendar advances exactly
            # one two-month tick at the start of this bot phase.
            self.phase = "Allied War Phase"
            if not self.advance_calendar_tick():
                return
            self.play_bot_phases("Allies")
            if self.game_over:
                return

            # The next phase is the new Axis automatic turn.  Advance another two
            # months before the Axis bots start, then hand control back to the player.
            self.phase = "Axis War Phase"
            if not self.advance_calendar_tick():
                return
            self.play_bot_phases("Axis")
            if self.game_over:
                return

            # Give control back explicitly to the human player's side.
            self.phase = "Axis War Phase" if player_side == "Axis" else "Allied War Phase"
            self.player_turn_active = True
            self.refresh_all()
            return

        # Hotseat mode: one phase at a time, with no bot processing.
        if not self.advance_phase():
            return
        if not self.game_over:
            self.refresh_all()

    def advance_calendar_tick(self):
        """Advance the calendar by one normal turn (2 months).

        In single-player mode this is called at the start of each automatic bot phase,
        so a complete Axis -> player -> Allied -> Axis cycle advances two ticks, matching
        the normal per-phase calendar speed.
        """
        self.ticks += 1
        new_year = self.ticks % TURNS_PER_YEAR == 0

        self.process_pending_offensives()
        if self.year >= END_YEAR:
            self.end_game()
            return False

        if new_year:
            self.economy_tick()
        if new_year or self.single_player:      # single player: each event has its own turn
            self.fire_scripted_events()
        self.fire_dated_events()
        return True

    def advance_round(self):
        """Compatibility wrapper for callers that advance one single-player round."""
        return self.advance_calendar_tick()

    def advance_phase(self):
        """Move the calendar on one phase (no redraw). Returns False if the war ended."""
        next_phase = {"Axis War Phase": "Allied War Phase",
                      "Allied War Phase": "Axis War Phase"}
        self.phase = next_phase[self.phase]
        return self.advance_calendar_tick()

    def end_game(self, headline=None):
        self.game_over = True

        def power(n):
            u = self.nation_units(n.name)
            return units_power(u, n)

        ranked = sorted((n for n in self.nations.values() if n.name not in MINOR_COUNTRIES),
                         key=lambda n: n.territory + power(n), reverse=True)
        lines = [headline or f"THE WAR ENDS - {self.date_label().upper()}", "",
                 "Final standings:"]
        for n in ranked:
            status = "ACTIVE" if n.alive else "DEFEATED"
            lines.append(f"{n.name:<12} Terr:{n.territory:>3}%  "
                          f"Forces: {units_text(self.nation_units(n.name)):<12} {status}")
        lines.append("")
        side_totals = {}
        for n in self.nations.values():
            if n.name in MINOR_COUNTRIES:
                continue
            side_totals.setdefault(n.side, 0)
            side_totals[n.side] += n.territory + power(n)
        winning_side = max(side_totals, key=side_totals.get)
        lines.append(f"Overall dominant side: {winning_side} Powers")
        lines.append(f"Top individual nation: {ranked[0].name}")
        for l in lines:
            self.log_msg(l)
        self.show_message("Game Over", "\n".join(lines), mono=True)
        self.btn_end.config(state="disabled")
        for b in (self.btn_trade, self.btn_objectives):
            b.config(state="disabled")
        self.phase_var.set("GAME OVER")
        self.refresh_view_after_end()

    def refresh_view_after_end(self):
        self.refresh_forces_list()
        self.draw_map()
        self.refresh_info()


if __name__ == "__main__":
    app = WW2Sim()
    app.mainloop()