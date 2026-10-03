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
  YELLOW = Neutral - and flip color when the opposing side's troops
  occupy them. A country's Territory % is the share of its own 3 zones it
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
  navy and air forces are x100 (UNIT_SCALE).
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
    * Air force can also AIRLIFT troops: drag an air box onto a land zone within
      range, choose "Airlift troops", and 1 Air carries 1 troop (from the same zone).
      The planes fly there with the troops, and both rest for a turn.
    * Distant targets take a few turns to reach; forces en route are drawn
      as a box on a dashed line.
    * A country may launch as many attacks per turn as it has rested forces for.
    * Units that move or attack must REST: they can't be moved again or used
      to attack until a full turn has passed (see MOVE_COOLDOWN_TURNS).
      Newly built units are ready immediately.
- COMBAT: Only troops fight troops (on land) and only navy fights navy (at sea);
  air force never fights, so the winner is decided by troops/navy alone.
  Air force instead BOMBS: each country has 3 bombings in total and may use only
  1 per battle (tick the box in the battle window); bombings from different
  countries stack (each bombing = -10% enemy power in that battle). Moving forces into a
  zone held by enemy troops does NOT start a fight by itself: the armies just
  stand there (the zone is outlined in red). During a war phase, CLICK the
  contested zone to start the battle. Likewise, moving troops into an undefended
  enemy zone does not claim it (orange dotted outline): they must ATTACK it - click
  the zone in your War Phase - to take it. Resting troops can't attack, but a single
  rested troop is enough. The side whose turn it is (the attacker)
  loses some army rating (ATTACKER_PENALTY), so the defense has the advantage.
  The loser's forces in the battle are destroyed; the winner loses a
  share depending on how close the fight was. Winning against a country
  takes territory and a share of its oil. Undefended countries are simply
  occupied.
- OIL is the only resource. It is produced each year, can be traded to
  friends, and is captured when you win battles.
- The game begins in January 1938 (Axis War Phase). Every time you End Phase
  the calendar advances 2 months (MONTHS_PER_TURN), so 6 turns = 1 year.
  Phases alternate Axis War -> Allied War. Oil production, reinforcements and
  historical events happen each January. The war ends at the start of 1946.
- SMALL COUNTRIES (Belgium, Netherlands) have a single CENTER zone (no West or
  East). Its army and air forces are shown in a box above the country, joined to it
  by a line (the navy sits in the water). Forces sent there arrive instantly. Drop forces on the box (or on the
  country itself) to send them there.
- Each country has a one-time historical objective. Achieve it, then claim
  an oil reward during your War Phase.

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
GROUND_BORDER_PX = 2.5    # land zones whose outlines come this close (map px) share a border
AIR_GAP_PX = 5            # air force also counts zones across a narrow strait (e.g. the Channel)
ATTACKER_PENALTY = 0.9    # the side whose turn it is (the attacker) fights at -10%,
                          # so the defending side has the advantage
UNIT_SCALE = 100          # starting forces are multiplied by this
SOLDIERS_PER_TROOP = 250  # 1 "troop" in the game = this many real soldiers (see ARMY_STRENGTH_K)
UNIT_BOX_SCALE = 0.75     # size of force boxes on the map (0.75 = three-quarter size)
OIL_REWARD_DIVISOR = 10   # objective_reward / this = oil paid for completing an objective
# Small countries show the forces in their CENTER zone in a box drawn above the country
# and joined to it by a plain line. Forces sent into the center zone arrive instantly.
# nation: (dx, rise). dx = horizontal offset of the box center from the country center;
# rise = how many pixels above the country center the box's bottom edge sits.
SMALL_COUNTRY_BOX = {
    "Belgium": (50, 55),
    "Netherlands": (-45, 70),
}
MOVE_COOLDOWN_TURNS = 1   # units that moved rest for one turn before acting again
START_YEAR = 1938
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
     {"beat": ["Finland"]}, (15, 2, 6)),
    ("USA",         "Allies",  (39.0, -98.0),  100, 85,
     "Support the Allies and project power once drawn into war.", 400,
     {"beat": ["Japan"]}, (8, 6, 6)),
    ("UK",          "Allies",  (54.0, -2.5),   30, 80,
     "Preserve the Empire and defeat Axis aggression in Europe.", 350,
     {"zones": 3, "year": 1943}, (6, 6, 5)),
    ("France",      "Allies",  (47.0, 2.5),    20, 55,
     "Defend the homeland from German aggression.", 250,
     {"zones": 2, "year": 1941}, (10, 2, 3)),
    ("Poland",      "Allies",  (52.0, 19.0),   5, 60,
     "Preserve independence against German and Soviet pressure.", 150,
     {"zones": 2, "year": 1940}, (7, 0, 2)),
    ("China",       "Allies",  (35.0, 105.0),  10, 45,
     "Resist Japanese invasion and unify the nation.", 150,
     {"zones": 2, "year": 1942}, (10, 0, 1)),
    ("Netherlands", "Allies",  (52.2, 5.5),    35, 65,
     "Protect the homeland and the oil-rich colonies.", 150,
     {"zones": 3, "year": 1941}, (3, 1, 1)),
    ("Belgium",     "Allies",  (50.8, 4.4),    5, 60,
     "Maintain independence and defend the homeland.", 120,
     {"zones": 3, "year": 1941}, (3, 0, 1)),
    ("Romania",     "Neutral", (46.0, 25.0),   75, 50,
     "Protect the Ploiesti oil fields amid Axis pressure.", 150,
     {"oil": 75, "zones": 3, "year": 1943}, (4, 0, 1)),
    ("Finland",     "Neutral", (64.0, 26.0),   5, 55,
     "Defend against Soviet aggression and preserve independence.", 120,
     {"zones": 3, "year": 1941}, (3, 0, 1)),
    ("Canada",      "Allies",  (56.0, -106.0), 20, 80,
     "Support the British Commonwealth war effort.", 150,
     {"wins": 1}, (3, 1, 1)),
    ("Australia",   "Allies",  (-25.0, 133.0), 10, 78,
     "Defend Pacific interests and support the Commonwealth.", 150,
     {"beat": ["Japan"]}, (3, 1, 1)),
    ("India",       "Allies",  (21.0, 78.0),   10, 55,
     "Support the British war effort while pressing for independence.", 150,
     {"zones": 3, "year": 1942}, (5, 0, 1)),
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
    "USSR":        (1500, 2000,  3000,  4200,  6000,  8000,  9500, 10500),
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
COUNTRY_OUTLINES.update(FILLER_OUTLINES)
MINOR_COUNTRIES = set(FILLER_OUTLINES)
SINGLE_ZONE_COUNTRIES = set(SMALL_COUNTRY_BOX)      # one Center zone only (minors have 3)
MINOR_GREY = "#c4c9ce"        # unplayable countries are greyed out until someone occupies them
MINOR_TEXT = "#5f6b76"

# zone colours: blue = only Allied troops, red = only Axis troops
ZONE_COLORS = {"Allies": "#7fb3e0", "Axis": "#e88d8d", "Neutral": "#b5bdc2"}
ZONE_EMPTY = "#e6eedb"      # no troops in the zone
ZONE_MIXED = "#c39bd3"      # troops from different sides (shouldn't normally happen)
SEA_ZONE_FILL = "#bfe3f5"       # light blue sea
SEA_BORDER = "#2b2b2b"          # thin solid line between named sea zones
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


def build_sea_zones():
    """Create small coastal zones and larger open-ocean travel zones."""
    zones = {}

    boxes = []
    for outline in COUNTRY_OUTLINES.values():
        lons_ = [point[0] for point in outline]
        lats_ = [point[1] for point in outline]
        boxes.append((min(lons_), max(lons_), min(lats_), max(lats_)))

    def near_land(lon, lat, margin=10):
        mx, my = margin + 6, margin + 1        # open cells are 30 x 20 degrees
        return any(x0 - mx <= lon <= x1 + mx and y0 - my <= lat <= y1 + my
                   for x0, x1, y0, y1 in boxes)

    def add_zone(prefix, lon, lat, width, height):
        center_lon, center_lat = lon + width / 2, lat + height / 2
        if any(point_in_polygon(center_lon, center_lat, outline)
               for outline in COUNTRY_OUTLINES.values()):
            return None
        zone_id = f"sea:{prefix}:{lon + 180}:{lat + 90}"
        zones[zone_id] = {
            "nation": "Ocean",
            "name": sea_name_at(center_lon, center_lat),
            "poly": [project(lon, lat), project(lon + width, lat),
                     project(lon + width, lat + height), project(lon, lat + height)],
            "centroid": project(center_lon, center_lat),
            "sea": True,
            "bounds": (lon, lat, width, height),     # lon/lat of the cell (for region maps)
        }
        return zone_id

    # Open-ocean cells are larger, but only where their center is well away from land.
    open_cells = []
    for lat in range(-80, 80, SEA_OPEN_GRID_LAT):
        for lon in range(-180, 180, SEA_OPEN_GRID_LON):
            center_lon, center_lat = lon + SEA_OPEN_GRID_LON / 2, lat + SEA_OPEN_GRID_LAT / 2
            if near_land(center_lon, center_lat):
                continue
            zone_id = add_zone("open", lon, lat, SEA_OPEN_GRID_LON, SEA_OPEN_GRID_LAT)
            if zone_id:
                open_cells.append(zones[zone_id]["poly"])

    # Fine cells fill the coastlines and all spaces not claimed by open-ocean cells.
    for lat in range(-90, 90, SEA_GRID_LAT):
        for lon in range(-180, 180, SEA_GRID_LON):
            center_lon, center_lat = lon + SEA_GRID_LON / 2, lat + SEA_GRID_LAT / 2
            center = project(center_lon, center_lat)
            if any(point_in_polygon(center[0], center[1], poly) for poly in open_cells):
                continue
            add_zone("coast", lon, lat, SEA_GRID_LON, SEA_GRID_LAT)
    return zones


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

    def on_enter(e):
        if str(b.cget("state")) != "disabled":
            b.config(bg=hover)

    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", lambda e: b.config(bg=bg))
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
# Who bots may fight, and from when (year as a fraction: 1939.8 = Nov 1939). From the
# given date every country in the first group may fight every country in the second.
# This supplements the game's own scripted war declarations and the wars the human
# player starts. Outside of these, a bot stays home.
_WESTERN_ALLIES = {"UK", "France", "Poland", "Belgium", "Netherlands",
                   "Canada", "Australia", "India"}
BOT_WAR_SCHEDULE = (
    (1938.0, {"Japan"}, {"China"}),                       # Sino-Japanese War
    (1939.0, {"Germany"}, _WESTERN_ALLIES),               # invasion of Poland
    (1939.8, {"USSR"}, {"Finland"}),                      # Winter War
    (1940.4, {"Italy"}, _WESTERN_ALLIES),                 # Italy enters the war
    (1941.0, {"Germany", "Italy"}, {"USSR"}),             # Barbarossa
    (1941.0, {"Japan"}, _WESTERN_ALLIES | {"USA"}),       # Pearl Harbor
    (1941.0, {"Germany", "Italy"}, {"USA"}),
)

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
# NATION MODEL
# ----------------------------------------------------------------------

class Nation:
    def __init__(self, name, side, latlon, oil, stability,
                 objective, objective_reward, goal, start_forces):
        self.name = name
        self.side = side          # "Axis", "Allies", "Neutral"
        self.latlon = latlon      # (lat, lon)
        self.oil = oil
        self.iron = IRON_STOCKPILES.get(name, 10)
        self.oil_rate = max(1, oil // 5)   # oil produced per year at 100% territory
        self.stability = stability
        self.objective = objective
        self.objective_reward = objective_reward
        self.goal = goal
        self.start_forces = start_forces
        self.objective_claimed = False
        self.victories_over = set()   # nations this country has beaten in battle
        self.battles_won = 0
        self.zone_count = 1 if name in SINGLE_ZONE_COUNTRIES else 3   # Belgium/Netherlands: 1
        self.zones_held = self.zone_count   # how many of its own zones it still controls
        self.at_war_with = set()
        self.alive = True
        self.last_attack_tick = None   # turn number of this country's last attack order
        self.bombing_uses = 3

    @staticmethod
    def _rating(value):
        return max(1, min(10, int(round(value))))

    @property
    def army_rating(self):
        return self._rating(1 + self.iron / 20 + self.start_forces[0] / 5)

    @property
    def navy_rating(self):
        return self._rating(1 + self.iron / 35 + self.oil / 30 + self.start_forces[1] / 3)

    @property
    def air_rating(self):
        return self._rating(1 + self.oil / 25 + self.start_forces[2] / 3)

    @property
    def territory(self):
        """Territory % = share of the country's own 3 zones it still controls."""
        return int(round(self.zones_held * 100 / self.zone_count))

    def oil_income(self):
        return int(round(self.oil_rate * self.territory / 100))

    def has_oil_field(self):
        return self.oil >= 30

    def objective_progress(self, year):
        """Return a list of (requirement text, is_met) for this nation's goal."""
        g = self.goal
        checks = []
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
        self.sea_zone = {}
        for name, (lon, lat) in NAVY_ANCHOR.items():
            self.sea_zone[name] = min(
                self.sea_zones,
                key=lambda z: ((self.sea_zones[z]["centroid"][0] - project(lon, lat)[0]) ** 2 +
                                (self.sea_zones[z]["centroid"][1] - project(lon, lat)[1]) ** 2),
            )
        self.zone_occupier = {}       # zone id -> nation occupying it (None = its own country)
        # garrisons[zone][owner] = {"army": n, "navy": n, "air": n}
        self.garrisons = {}
        self.force_positions = {}       # (zone, owner, kind) -> map x/y drop position
        # units that recently moved: locks[(zone, owner)] = [{"units", "ready"}]
        self.locks = {}
        self.ticks = 0                 # turns elapsed; each turn = 2 months
        for n in self.nations.values():
            _, navy, air = (v * UNIT_SCALE for v in n.start_forces)
            if n.name in MINOR_COUNTRIES:
                continue                                         # unplayable: no troops
            army = self.historical_troops(n.name, START_YEAR)    # real 1938 army size
            cap = self.capital_zone[n.name]
            self.add_force(cap, n.name, new_units(army, 0, air))       # land forces at home
            if n.name in self.sea_zone:
                self.add_force(self.sea_zone[n.name], n.name, new_units(0, navy, 0))
        self.events_fired = set()
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

    def add_lock(self, loc, owner, units):
        if units_total(units) > 0:
            self.locks.setdefault((loc, owner), []).append(
                {"units": dict(units), "ready": self.ticks + MOVE_COOLDOWN_TURNS})

    def station(self, loc, owner, units, position=None):
        """Units arrive and stand in loc; they must rest before acting again."""
        self.add_force(loc, owner, units)
        self.add_lock(loc, owner, units)
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
        """Political color by default (red=Axis, blue=Allies, yellow=Neutral);
        a zone recolors to whichever side's troops occupy it if contested."""
        if self.is_sea_zone(z):
            return SEA_ZONE_FILL
        sides = {self.nations[o].side for o, u in self.garrisons.get(z, {}).items()
                 if u["army"] > 0}
        if not sides:
            home = self.zone_nation(z)
            if home in MINOR_COUNTRIES:      # greyed out, unless someone has taken it
                occ = self.zone_occupier.get(z)
                return SIDE_COLOR[self.nations[occ].side] if occ else MINOR_GREY
            return SIDE_COLOR[self.nations[home].side]
        if len(sides) == 1:
            return SIDE_COLOR[next(iter(sides))]
        return ZONE_MIXED

    def zone_at_map(self, mx, my):
        for z, info in self.zones.items():
            if self.is_sea_zone(z):
                continue
            if point_in_polygon(mx, my, info["poly"]):
                return z
        for z, info in self.sea_zones.items():
            if point_in_polygon(mx, my, info["poly"]):
                return z
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

    def take_zone(self, owner_name, z):
        """owner_name won control of zone z. Returns 'conquered', 'liberated' or 'held'."""
        if self.is_sea_zone(z):          # sea zones have no owner country to conquer
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
        label = self.zone_label(z)
        if mode == "conquered":
            owner.victories_over.add(home_name)
            owner.stability = min(100, owner.stability + 3)
            home.stability = max(0, home.stability - 5)
            msg = f"{owner_name} conquers {label}!"
            if prev is None:           # a third of the country's oil falls into enemy hands
                captured = home.oil // 3
                home.oil -= captured
                owner.oil += captured
                msg += f" {captured} oil captured."
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

    # ---------------- UI construction ----------------

    def build_ui(self):
        # ---- header bar: title on the left, date + phase on the right ----
        header = tk.Frame(self, bg=HEADER_BG)
        header.pack(fill="x")
        tk.Label(header, text="WORLD WAR II", font=("Georgia", 18, "bold"),
                 fg=HEADER_FG, bg=HEADER_BG).pack(side="left", padx=(16, 8), pady=10)
        tk.Label(header, text="Grand Strategy Simulation", font=(UI_FONT, 11),
                 fg="#9fb3c8", bg=HEADER_BG).pack(side="left", pady=(6, 0))
        self.result_var = tk.StringVar()
        self.result_banner = tk.Label(header, textvariable=self.result_var,
                          bg=HEADER_BG, fg="#ffffff",
                          font=(UI_FONT, 10, "bold"), padx=12, pady=4)
        self.result_banner.pack(side="left", padx=18)
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

        toolbar_btn("Zoom In (+)", lambda: self.zoom_at(MAP_W / 2, MAP_H / 2, 1.25))
        toolbar_btn("Zoom Out (-)", lambda: self.zoom_at(MAP_W / 2, MAP_H / 2, 1 / 1.25))
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
            self.canvas.bind(key, lambda e: self.zoom_at(MAP_W / 2, MAP_H / 2, 1.25))
        for key in ("<minus>", "<underscore>", "<KP_Subtract>"):
            self.canvas.bind(key, lambda e: self.zoom_at(MAP_W / 2, MAP_H / 2, 1 / 1.25))
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

    def announce_battle_result(self, text, side):
        self.result_var.set(text)
        self._result_sequence = getattr(self, "_result_sequence", 0) + 1
        sequence = self._result_sequence
        color = SIDE_COLOR[side]
        flash = ["#ffffff", color, "#ffffff", color, "#ffffff", color]

        def pulse(index=0):
            if sequence != self._result_sequence:
                return
            if index < len(flash):
                self.result_banner.config(bg=flash[index])
                self.after(140, pulse, index + 1)
            else:
                self.result_banner.config(bg=color)

        pulse()
        self.after(4500, lambda: self.clear_battle_result(sequence))

    def clear_battle_result(self, sequence):
        if sequence == getattr(self, "_result_sequence", 0):
            self.result_var.set("")
            self.result_banner.config(bg=HEADER_BG)

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
                      shadow_color="#000000", selected=False):
        """Small side-view WW2 fighter (nose pointing right) drawn behind an air-force
        box, painted in the owner's colors, with a black oval shadow below it.
        `shadow` = (width, height) of the oval. When `selected`, the plane's own outline
        turns purple (the air box has no rectangle of its own)."""
        c = self.canvas
        sx, sy = span / 2, length / 2

        def pts(frac):
            flat = []
            for fx, fy in frac:
                flat += [cx + fx * sx, cy + fy * sy]
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
        c.create_oval(cx - 0.10 * sx, cy - 0.66 * sy, cx + 0.30 * sx, cy - 0.24 * sy,
                      fill="#2c4a63", outline=outline, width=ow_, tags=tag)
        # propeller blur + spinner at the nose
        c.create_line(cx + 0.95 * sx, cy - 0.70 * sy, cx + 0.95 * sx, cy + 0.55 * sy,
                      fill="#3a3a3a", width=2, tags=tag)
        c.create_oval(cx + 0.82 * sx, cy - 0.12 * sy, cx + 1.00 * sx, cy + 0.14 * sy,
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
        """Border lines between differently named sea zones, and one label spot per
        connected stretch of each named zone. Computed once (map coordinates)."""
        if getattr(self, "_sea_regions", None) is not None:
            return self._sea_regions
        unit = {}                                   # (lon index, lat index) -> (zone id, name)
        for z, info in self.sea_zones.items():
            lon, lat, w, h = info["bounds"]
            if any(point_in_polygon(lon + w / 2, lat + h / 2, coast)
                   for coast in COUNTRY_OUTLINES.values()):
                continue                          # cell lies under land: no border or label
            for lo in range(int(lon), int(lon + w), 10):
                for la in range(int(lat), int(lat + h), 10):
                    unit[(lo // 10, la // 10)] = (z, info["name"])
        # borders: shared unit edges whose two sides have different names
        horiz, vert = {}, {}
        for (i, j), (_, n) in unit.items():
            right = unit.get((i + 1, j))
            if right and right[1] != n:
                vert.setdefault(i + 1, []).append(j)      # vertical line at lon index i+1
            up = unit.get((i, j + 1))
            if up and up[1] != n:
                horiz.setdefault(j + 1, []).append(i)     # horizontal line at lat index j+1
        segs = []

        def runs(vals):
            vals = sorted(vals)
            start = prev = vals[0]
            for v in vals[1:]:
                if v != prev + 1:
                    yield start, prev + 1
                    start = v
                prev = v
            yield start, prev + 1

        for lo, las in vert.items():
            for a, b in runs(las):
                segs.append((project(lo * 10, a * 10), project(lo * 10, b * 10)))
        for la, los in horiz.items():
            for a, b in runs(los):
                segs.append((project(a * 10, la * 10), project(b * 10, la * 10)))
        # labels: connected stretches of the same name; label the unit nearest the middle
        seen, labels = set(), []
        for key, (_, n) in unit.items():
            if key in seen:
                continue
            comp, stack = [], [key]
            seen.add(key)
            while stack:
                cur = stack.pop()
                comp.append(cur)
                for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nb = (cur[0] + d[0], cur[1] + d[1])
                    if nb in unit and nb not in seen and unit[nb][1] == n:
                        seen.add(nb)
                        stack.append(nb)
            labels.append((n, comp))
        biggest = {}
        for n, comp in labels:
            biggest[n] = max(biggest.get(n, 0), len(comp))
        spots = []
        for n, comp in sorted(labels, key=lambda t: -len(t[1])):
            if len(comp) < max(2, 0.25 * biggest[n]) and len(comp) < biggest[n]:
                continue                          # skip tiny leftover pieces
            mi = sum(c[0] for c in comp) / len(comp)
            mj = sum(c[1] for c in comp) / len(comp)
            best = min(comp, key=lambda c: (c[0] - mi) ** 2 + (c[1] - mj) ** 2)
            spots.append((n, project(best[0] * 10 + 5, best[1] * 10 + 5), len(comp)))
        self._sea_regions = (segs, spots)
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

        for (ax, ay), (bx, by) in self.sea_region_data()[0]:   # thin zone borders
            x0, y0 = self.to_screen(ax, ay)
            x1, y1 = self.to_screen(bx, by)
            c.create_line(x0, y0, x1, y1, fill=SEA_BORDER, width=1)

        scale = self.token_scale()
        r = self.marker_radius()

        # territories: every country is split into 3 zones, colored by political
        # allegiance (red=Axis, blue=Allies, yellow=Neutral), flipping to the
        # color of whichever side's troops occupy them
        for z in self.zones:
            if self.is_sea_zone(z):
                continue
            tag = "zone_" + z.replace(":", "_")
            c.create_polygon(self.zone_screen_poly(z), fill=self.zone_fill(z),
                              outline="#5d6d7e", width=1, tags=tag)
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
            if self.is_contested(z):
                c.create_polygon(self.zone_screen_poly(z), fill="", outline="#c0392b",
                                  width=3, dash=(6, 3))
            elif self.is_unclaimed(z):        # troops inside, zone not claimed yet
                c.create_polygon(self.zone_screen_poly(z), fill="", outline="#e67e22",
                                  width=3, dash=(2, 4))
        if self.selected_target in self.zones:    # selected zone (info panel)
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
        for name in self.nations:
            cx, cy = self.nation_center_screen(name)
            ctag = "zone_" + self.capital_zone[name].replace(":", "_")
            nf, cf = self.label_font(name_spec), self.label_font(center_spec)
            ny = cy - 6 * scale                  # country name, centered on the country
            gy = ny + self.label_size(name_spec, name)[1] / 2 + self.label_size(center_spec, "X")[1] / 2 - 1
            ctext = "* CENTER *"                 # identifies the country's center zone
            label_rows = ((cx, ny, name, name_spec, MINOR_TEXT if name in MINOR_COUNTRIES else "#000000"),)
            if name not in MINOR_COUNTRIES:
                label_rows += ((cx, gy, ctext, center_spec, "#2c3e50"),)
            for (tx, ty, text, spec, fill) in label_rows:
                w, h = self.label_size(spec, text)
                fixed_rects.append((tx - w / 2 - 2, ty - h / 2 - 1,
                                    tx + w / 2 + 2, ty + h / 2 + 1))
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
        if self.bot_running:
            return                         # no orders while the bots are moving
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
                                            outline="#f1c40f", width=4, tags="hl")
        self.canvas.tag_raise("ghost")

    def on_drag_release(self, event):
        d = self.drag
        self.drag = None
        if self.bot_running:
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
        self.target_var.set(self.zone_label(z))
        sides = self.battle_sides(z, self.current)
        if sides:                          # opposing armies here: offer to fight
            att, dfn = sides
            # every friendly country with air force in this zone can bomb (even if it has
            # no troops here): 1 bombing per country per battle, 3 in total per country
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

    def zoom_at(self, mx, my, factor):
        new_zoom = max(0.4, min(10.0, self.zoom * factor))
        factor = new_zoom / self.zoom
        if abs(factor - 1) < 1e-9:
            return
        self.pan_x = mx - (mx - self.pan_x) * factor
        self.pan_y = my - (my - self.pan_y) * factor
        self.zoom = new_zoom
        self._user_zoomed = True                          # bots must not override a manual zoom
        self.canvas.scale("all", mx, my, factor)         # instant, approximate feedback
        job = getattr(self, "_zoom_job", None)
        if job is not None:
            self.after_cancel(job)
        self._zoom_job = self.after(140, self._finish_zoom)   # exact redraw when it settles

    def _finish_zoom(self):
        self._zoom_job = None
        self.draw_map()

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
        tk.Label(head, text="Grand Strategy Simulation  \u00b7  1938 \u2013 1945",
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
             "for Allied and yellow for Neutral, and flip color when the opposing side's "
             "troops occupy them. Armies are boxes carrying the owner's flag: T = Troops, "
             "anchor = Navy, wing = Air Force. Every January each country whose center zone "
             "is still free is topped up with troops there to match its real historical army "
             "size for that year (1 troop = 250 soldiers)."),
            ("Moving and attacking",
             "There is no movement phase: on your side's War Phase you can both move and "
             "battle. Drag one of your force boxes onto a zone, then choose how much to "
             "send: 10%, 25%, 50% or All. Troops crossing the sea need Navy (1 per troop). "
             "Distant targets take a few turns. There is no limit on attacks per turn, "
             "but units that move or fight must rest until your side's next turn."),
            ("Battles",
             "Moving into an enemy-held zone does not start a fight by itself. Click the "
             "red-outlined zone during a war phase to start the battle. Only troops (on land) "
             "and navy (at sea) fight; air force only bombs (3 per country, 1 per battle, "
             "-10% enemy power each; bombings from different countries stack). The side whose turn "
             f"it is fights at -{penalty}%, so defenders have the edge. Winning takes "
             "territory and a share of the loser's oil."),
            ("Oil and objectives",
             "Oil is your only resource: it is produced each year, can be traded, and is "
             "captured in victory. Achieve your country's objective, then claim its oil "
             "reward during your War Phase."),
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
            p = self.nations[player_name]
            self.current = p
            self.selected_force_loc = self.capital_zone[player_name]
            self.mode_var.set(f"SINGLE PLAYER  \u00b7  you command {player_name}")
            self.mode_label.pack(fill="x", pady=(0, 6), before=self.acting_card)
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
            self.log_msg("The simulation begins in 1938. Position your forces, then pass the "
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
        self.date_var.set(self.date_label())
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
        if self.single_player:
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
        kv("Iron", p.iron)
        kv("Ratings", f"Army {p.army_rating}/10   Navy {p.navy_rating}/10   "
                  f"Air {p.air_rating}/10")
        kv("Bombing uses", f"{p.bombing_uses}/3")
        kv(f"Troops in {int(self.year)}", f"{self.historical_troops(p.name, self.year)} (historical)")
        total = self.nation_units(p.name)
        kv("Forces", f"Troops {total['army']}   Navy {total['navy']}   Air {total['air']}")
        kv("At war with", ", ".join(sorted(p.at_war_with)) if p.at_war_with else "none")
        if self.can_attack_now(p):
            kv("Attack this turn", "unlimited", "good")

        put("Objective\n", "h")
        put(p.objective + "\n")
        if p.objective_claimed:
            put("Reward claimed\n", "good")
        else:
            put(f"Reward: {self.reward_oil(p)} oil (unclaimed)\n", "dim")
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
        if self.game_over or self.bot_running:
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

    def can_enter_center(self, p, z):
        """Troops arriving by sea or air can't land straight in a foreign country's center."""
        return not (self.is_inner_zone(z) and self.zone_nation(z) != p.name)

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
            avail = new_units(navy=avail["navy"])
            if default_kind == "navy" and self.is_sea_zone(src) and not self.is_sea_zone(dest):
                army_stacks = [
                    (loc, self.available_units(loc, p.name)["army"])
                    for loc in self.owned_force_locations(p.name)
                    if not self.is_sea_zone(loc)
                ]
                if army_stacks:
                    transport_source, largest_stack = max(army_stacks, key=lambda item: item[1])
                    transport_avail = min(largest_stack, avail["navy"] * TROOPS_PER_SHIP)
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
        dest_label = self.zone_label(dest)

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

    def action_objective(self):
        p = self.current
        if not p.alive:
            self.show_message(f"{p.name}'s Objective",
                                 f"{p.name} has been defeated and can't claim rewards.")
            return
        if p.objective_claimed:
            self.show_message(f"{p.name}'s Objective",
                                 f"{p.objective}\n\n(Reward already claimed.)")
            return
        progress = p.objective_progress(self.year)
        if not all(met for _, met in progress):
            checklist = "\n".join(f"[{'x' if met else ' '}] {text}"
                                   for text, met in progress)
            self.show_message(f"{p.name}'s Objective",
                                 f"{p.objective}\n\nObjective not yet achieved:\n{checklist}")
            return
        p.objective_claimed = True
        oil = self.reward_oil(p)
        p.oil += oil
        self.show_message(f"{p.name}'s Objective",
                             f"{p.objective}\n\nObjective achieved! "
                             f"Reward claimed: +{oil} oil!")
        self.log_msg(f"{p.name} achieves its objective and claims +{oil} oil.")
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
            if cls.startswith("T") and cls not in ("Tk", "Text", "Toplevel"):
                continue                                  # ttk widgets
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

    def undim_window(self, undo):
        for target, opt, value in reversed(undo):
            try:
                if isinstance(target, tuple):
                    kind, w, ident = target
                    if kind == "tag":
                        w.tag_configure(ident, **{opt: value})
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

        tk.Label(self.send_panel_body,
                 text="Battle events may help or hinder either side by 5–15%.",
                 bg=BG_CARD, fg=DIM, font=(UI_FONT, 9), wraplength=470,
                 justify="left").pack(anchor="w", pady=(8, 0))
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
                               text=f"{o} bombs  ({uses}/3 bombings left)",
                               variable=var, bg=BG_CARD, fg=FG_TEXT,
                               activebackground=BG_CARD, selectcolor=BG_CARD,
                               font=(UI_FONT, 10, "bold")).pack(anchor="w", pady=1)
        actions = tk.Frame(self.send_panel_body, bg=BG_CARD)
        actions.pack(fill="x", pady=(30, 0))

        def start():
            self.close_send_panel()
            counts = {o: 1 for o, var in bomb_vars.items() if var.get()}
            self.fight_battle(zone, attackers, defenders, self.current.name, counts)
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
        # face each other until someone clicks the zone to start the battle.
        self.station(dest, owner_name, units, position)
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
            if o == p.name or self.are_allies(p, self.nations[o]):
                ready = self.attack_units(z, o)       # resting troops can't attack
                if units_total(ready) > 0:
                    att[o] = ready
        dfn = {o: u for o, u in slot.items() if self.is_hostile(p.name, o)}
        return (att, dfn) if att and dfn else None

    def attack_units(self, z, o):
        """The rested units of country o in zone z that are able to attack there. Even a
        single rested troop is enough; troops that are still resting stay out of it."""
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
        """Attack an undefended zone with the given rested troops and claim it. They must
        rest again afterwards."""
        label = self.zone_label(z)
        ctrl = self.controller(z)
        if ctrl is not None and self.is_hostile(p.name, ctrl):
            self.declare_war(p.name, ctrl)
        for o in [o for o, u in self.garrisons.get(z, {}).items()
                  if self.is_hostile(p.name, o)]:
            self.set_force(z, o, new_units())             # leftover enemy air/navy is lost
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

    def fight_battle(self, z, attackers, defenders, lead_name, bombings=None):
        """Resolve a battle in zone z. `attackers` maps each attacking country to the
        rested units it commits; `defenders` maps each defending country to its units
        (all of which defend). The attacking side (whose turn it is) loses army rating."""
        label = self.zone_label(z)
        a_names, d_names = list(attackers), list(defenders)
        for a in a_names:
            for d in d_names:
                self.declare_war(a, d)
        a_fight = {o: dict(u) for o, u in attackers.items()}
        d_units = {o: dict(self.battle_units(z, self.garrisons[z][o])) for o in d_names}
        event_text, power_mod, loss_mod = self.battle_event(a_names, d_names)
        self.log_msg(event_text)
        a_power = (sum(units_power(u, self.nations[o]) for o, u in a_fight.items())
                   * power_mod["attackers"] * ATTACKER_PENALTY)
        d_power = sum(units_power(u, self.nations[o]) for o, u in d_units.items()) \
            * power_mod["defenders"]
        # each country may bomb once per battle (3 in total); bombings from different
        # countries stack, each cutting enemy power by 10%.
        total_bombs = 0
        for o, n_b in (bombings or {}).items():
            n_b = max(0, min(n_b, 1, self.nations[o].bombing_uses))   # max 1 per battle
            if n_b > 0:
                self.nations[o].bombing_uses -= n_b
                total_bombs += n_b
                self.log_msg(f"AIR RAID: {o} flies {n_b} bombing(s) "
                             f"({self.nations[o].bombing_uses} bombing uses remain).")
        if total_bombs:
            d_power *= max(0.0, 1 - 0.1 * total_bombs)
            self.log_msg(f"Bombing cuts the defenders' power by {min(100, total_bombs * 10)}%.")
        a_roll = a_power * random.uniform(0.85, 1.15)
        d_roll = d_power * random.uniform(0.85, 1.15)
        ratio = min(a_roll, d_roll) / max(a_roll, d_roll, 0.01)
        win_loss = min(0.9, 0.05 + 0.7 * ratio)   # share of the winner's force lost
        a_txt, d_txt = ", ".join(a_names), ", ".join(d_names)

        # units of the attacking side that were resting stay put either way
        resting = {o: {k: self.garrisons[z][o][k] - a_fight[o][k] for k in UNIT_KEYS}
                   for o in a_names}

        if a_roll >= d_roll:
            for o in a_names:
                surv = scale_units(a_fight[o],
                                   1 - min(0.95, win_loss * loss_mod["attackers"]))
                self.set_force(z, o, {k: resting[o][k] + surv[k] for k in UNIT_KEYS})
                self.add_lock(z, o, surv)           # fighters must rest afterwards
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
            for o in a_names:
                self.set_force(z, o, resting[o])
            for o in d_names:
                surv = scale_units(d_units[o], 1 - min(0.95, win_loss * loss_mod["defenders"]))
                other = {k: self.garrisons[z][o][k] - d_units[o][k] for k in UNIT_KEYS}
                self.set_force(z, o, {k: other[k] + surv[k] for k in UNIT_KEYS})
                self.nations[o].battles_won += 1
                self.nations[o].victories_over.update(a_names)
            self.log_msg(f"BATTLE in {label}: the attack by {a_txt} (power {a_power:.0f} "
                         f"after the attacker penalty) is crushed by {d_txt} "
                         f"(power {d_power:.0f}). The attacking units are destroyed.")
            winner_side = self.nations[d_names[0]].side
            attacker_side = self.nations[lead_name].side
            self.announce_battle_result(
                f"{attacker_side} Powers Are Defeated - {label} Holds", winner_side)

    def historical_troops(self, name, year):
        """Troops a country historically had at the start of `year` (1 troop =
        SOLDIERS_PER_TROOP soldiers)."""
        row = ARMY_STRENGTH_K[name]
        idx = max(0, min(len(row) - 1, int(year) - START_YEAR))
        return max(1, int(round(row[idx] * 1000 / SOLDIERS_PER_TROOP)))

    def yearly_troops(self, n):
        """Troops that appear in a country's center each new year: enough to bring its
        army (including forces en route) up to its historical size for this year."""
        target = self.historical_troops(n.name, self.year)
        return max(0, target - self.nation_units(n.name)["army"])

    def spawn_reinforcements(self, n):
        """New year: if the country's center zone is not conquered, it is topped up to its
        historical army size for the year."""
        if n.name in MINOR_COUNTRIES:
            return                      # unplayable countries never raise troops
        home = self.capital_zone[n.name]
        if self.zone_occupier.get(home) is not None:
            self.log_msg(f"{n.name}'s center is conquered - no reinforcements this year.")
            return
        troops = self.yearly_troops(n)
        if troops <= 0:
            return                      # already at (or above) its historical strength
        self.add_force(home, n.name, new_units(troops, 0, 0))
        self.log_msg(f"{n.name} mobilizes {troops} new troops at its center "
                     f"(historical army of {int(self.year)}).")

    def economy_tick(self):
        for n in self.nations.values():
            if not n.alive:
                continue
            n.oil += n.oil_income()
            self.spawn_reinforcements(n)
            if n.at_war_with:
                n.stability = max(0, n.stability - 1)
            else:
                n.stability = min(100, n.stability + 1)

    # ---------------- scripted historical events ----------------

    def fire_scripted_events(self):
        y = self.year

        def once(tag, text, fx=None):
            if tag not in self.events_fired:
                self.events_fired.add(tag)
                self.log_msg(f"HISTORICAL EVENT: {text}")
                if fx:
                    fx()
                self.show_message("Historical Event", text)

        if y == 1938:
            once("munich", "Tensions rise across Europe as Germany annexes Austria and "
                            "the Sudetenland. War clouds gather.")
        elif y == 1939:
            once("poland", "Germany invades Poland. Britain and France declare war, "
                            "and World War II formally begins.",
                 lambda: self._war(("Germany", "UK"), ("Germany", "France"),
                                    ("Germany", "Poland")))
        elif y == 1940:
            once("fall_france", "Germany's blitzkrieg overwhelms the Low Countries and "
                                 "France, which falls after a rapid campaign.",
                 lambda: self._occupy_zone("France", "Germany"))
        elif y == 1941:
            once("barbarossa", "Germany launches Operation Barbarossa against the USSR, "
                                "opening the largest front of the war.",
                 lambda: self._war(("Germany", "USSR")))
            once("pearl_harbor", "Japan attacks Pearl Harbor. The United States enters "
                                  "the war against Japan and, soon after, Germany and Italy.",
                 lambda: self._war(("Japan", "USA"), ("Germany", "USA")))
        elif y == 1942:
            once("stalingrad", "Brutal urban warfare rages at Stalingrad as Soviet forces "
                                "grind down the German advance.",
                 lambda: self._attrition("Germany", 0.15))
            once("midway", "The Battle of Midway cripples Japan's carrier fleet, turning "
                            "the tide in the Pacific.",
                 lambda: self._attrition("Japan", 0.3, ("navy", "air")))
        elif y == 1943:
            once("italy_falls", "Allied landings in Sicily and Italy topple Mussolini's "
                                 "government; Italy signs an armistice with the Allies.",
                 lambda: self._occupy_zone("Italy", "UK"))
        elif y == 1944:
            once("dday", "Allied forces storm the beaches of Normandy on D-Day, opening "
                          "a major new front in Western Europe.",
                 lambda: self._attrition("Germany", 0.15))
        elif y == 1945:
            once("berlin", "Soviet forces encircle Berlin as Germany's collapse becomes "
                            "inevitable.",
                 lambda: self._occupy_zone("Germany", "USSR"))
            once("japan_surrender", "A devastating new weapon forces Japan toward "
                                     "surrender, bringing the war to a close.",
                 lambda: self._occupy_zone("Japan", "USA"))

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

    def bot_show(self, z, kind, text, src=None):
        """Pan the map to zone `z` (or to fit the move src -> z), redraw, and hold so the
        person can watch a bot's move (BOT_MOVE_DELAY_MS) or battle (BOT_BATTLE_DELAY_MS).
        A move also gets a temporary arrow from src to z. Does nothing outside a
        single-player bot run."""
        if not (self.bot_running and self.single_player) or self.bot_skip or z not in self.zones:
            return
        if self._bot_last_shown == (kind, src, z):
            return                            # same move repeated: one stop is enough
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
        self.phase_var.set(text.upper())
        self.draw_map()
        self.refresh_info()
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
        """Called once after a single-player game opens: bots whose side moves first go now."""
        if self.single_player and not self.game_over:
            self.play_bot_phases()
            if not self.game_over:
                self.refresh_all()

    def play_bot_phases(self):
        """Let the bots act. Bots on the current phase's side move; if that phase is not
        the player's, the calendar advances and the next side's bots move, until it is
        the player's phase again (the player's allies move first, so you see an
        up-to-date board)."""
        if self.bot_running:
            return
        self.bot_running = True
        self.bot_skip = False
        self._bot_last_shown = None
        self._user_zoomed = False
        saved_view = (self.zoom, self.pan_x, self.pan_y)
        self.btn_skip.pack(side="left", padx=(8, 0))
        for b in (self.btn_trade, self.btn_objectives):
            b.config(state="disabled")
        try:
            while not self.game_over:
                if not self.player.alive:
                    self.log_msg(f"{self.player_name} has been defeated. Your war is over.")
                    self.show_message("Defeated",
                                        f"{self.player_name} has been completely defeated.")
                    self.end_game(f"{self.player_name.upper()} DEFEATED - "
                                  f"{self.date_label().upper()}")
                    break
                self.phase_var.set("BOTS ARE MOVING...")
                self.btn_end.config(state="disabled")
                self.update_idletasks()
                self.run_bot_turns()
                if not self.player.alive:
                    continue                       # handled at the top of the loop
                if self.can_attack_now(self.player):
                    break                          # your move
                if not self.advance_phase():
                    break
        finally:
            self.bot_running = False
            self._bot_wait = None
            self._bot_arrow = None
            self.btn_skip.pack_forget()
            self.zoom, self.pan_x, self.pan_y = saved_view   # back to where you were looking
        if not self.game_over:
            self.refresh_all()

    def run_bot_turns(self):
        bots = [n for n in self.nations.values()
                if self.is_bot(n) and n.alive and self.can_attack_now(n)]
        random.shuffle(bots)
        for bot in bots:
            try:
                self.bot_take_turn(bot)
            except Exception as exc:                 # a bot bug must never crash the game
                import traceback
                traceback.print_exc()
                self.log_msg(f"({bot.name} bot skipped its turn: {exc})")
            if not self.player.alive:
                return

    def bot_take_turn(self, bot):
        self._bot_last_shown = None
        self.bot_claim_objective(bot)
        enemies = self.bot_enemies(bot)
        if not enemies:
            return                                   # at peace: stay home
        self.bot_resolve_battles(bot, enemies)       # finish fights already under way
        self.bot_claim_zones(bot, enemies)           # claim undefended zones we stand in
        self.bot_garrison(bot, enemies)              # cover border zones facing the enemy
        self.bot_attack(bot, enemies)                # strike adjacent enemy zones
        self.bot_amphibious(bot, enemies)            # landings across the sea
        self.bot_advance(bot, enemies)               # march toward the nearest enemy
        self.bot_resolve_battles(bot, enemies)

    def bot_claim_objective(self, bot):
        if bot.alive and not bot.objective_claimed and bot.objective_met(self.year):
            bot.objective_claimed = True
            oil = self.reward_oil(bot)
            bot.oil += oil
            self.log_msg(f"{bot.name} achieves its objective and claims +{oil} oil.")

    def bot_enemies(self, bot):
        """Countries this bot is willing to fight: those it is at war with (scripted
        events, or wars someone started by attacking) plus the historical schedule.
        Bots never pick fights with minor countries or with powers they have no war
        with."""
        names = set(bot.at_war_with)
        for since, group_a, group_b in BOT_WAR_SCHEDULE:
            if self.year >= since:
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
        margin = BOT_ATTACK_MARGIN.get(bot.name, BOT_DEFAULT_MARGIN)
        zones = [only] if only else [z for z in list(self.garrisons) if self.is_contested(z)]
        for z in zones:
            sides = self.battle_sides(z, bot)
            if not sides:
                continue
            att, dfn = sides
            att = {o: u for o, u in att.items() if o != self.player_name}
            if bot.name not in att or any(o not in enemies for o in dfn):
                continue
            a_power = sum(units_power(u, self.nations[o])
                          for o, u in att.items()) * ATTACKER_PENALTY
            d_power = sum(units_power(u, self.nations[o]) for o, u in dfn.items())
            bombers = [o for o, u in self.garrisons[z].items()
                       if u.get("air", 0) > 0 and o != self.player_name
                       and self.nations[o].alive and self.nations[o].bombing_uses > 0
                       and (o == bot.name or self.are_allies(bot, self.nations[o]))]
            bombs = None
            for b in range(len(bombers) + 1):     # use as few bombings as needed
                if a_power >= d_power * max(0.0, 1 - 0.1 * b) * margin:
                    bombs = b
                    break
            if bombs is None:
                continue                          # odds too poor: wait for a better chance
            self.fight_battle(z, att, dfn, bot.name, {o: 1 for o in bombers[:bombs]})
            self.bot_show(z, "battle", f"{bot.name} fights for {self.zone_label(z)}")

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
                    self.execute_send(src, z, bot, False, new_units(army=stacks[src] // 4))

    def bot_attack(self, bot, enemies):
        """Attack adjacent enemy zones, pooling every nearby stack against the weakest
        target first."""
        margin = BOT_ATTACK_MARGIN.get(bot.name, BOT_DEFAULT_MARGIN)
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
                have = self.bot_friendly_power(bot, z) + sum(stacks[l] for l in feeders) * per
                # a bombing run (-10% defenders) is counted on if planes can reach the zone
                air_ok = bot.bombing_uses > 0 and any(
                    self.available_units(l, bot.name)["air"] > 0
                    and self.air_steps(l, z) is not None for l in feeders)
                factor = 0.9 if air_ok else 1.0
                if d <= 0 or have * ATTACKER_PENALTY >= d * margin * factor:
                    options.append((d * factor, z, feeders))
            if not options:
                return
            d, z, feeders = min(options, key=lambda o: o[0])
            tried.add(z)
            if d <= 0:                            # undefended: a detachment walks in (claims next turn)
                loc = max(feeders, key=lambda l: stacks[l])
                plan = [(loc, max(1, int(stacks[loc] * 0.2)))]
            else:                                 # defended: send a comfortable surplus
                need = (d * margin / ATTACKER_PENALTY - self.bot_friendly_power(bot, z)) / per
                goal, got, plan = int(max(1, need) * 1.6) + 1, 0, []
                for loc in sorted(feeders, key=lambda l: -stacks[l]):
                    take = min(stacks[loc], goal - got)
                    if take > 0:
                        plan.append((loc, take))
                        got += take
                    if got >= goal:
                        break
            for loc, n in plan:
                if self.execute_send(loc, z, bot, True, new_units(army=n)):
                    continue
                self.bot_send_air(bot, loc, z)
            self.bot_resolve_battles(bot, enemies, only=z)

    def bot_send_air(self, bot, loc, dest):
        """Fly a few planes along with an attack so they can bomb the battle."""
        if bot.bombing_uses <= 0 or self.air_steps(loc, dest) is None:
            return
        air = self.available_units(loc, bot.name)["air"]
        if air > 0:
            self.execute_send(loc, dest, bot, True, new_units(air=max(1, air // 10)))

    def bot_amphibious(self, bot, enemies):
        """Ferry troops by sea to an enemy zone on another landmass."""
        if any(o["owner"] == bot.name and self.is_sea_zone(o["origin"])
               for o in self.pending_offensives):
            return                                # a landing is already on its way
        fleets = {z: self.available_units(z, bot.name)["navy"]
                  for z in self.owned_force_locations(bot.name) if self.is_sea_zone(z)}
        fleets = {z: n for z, n in fleets.items() if n > 0}
        armies = self.bot_free_troops(bot, enemies)
        if not fleets or not armies:
            return
        home = max(armies, key=armies.get)        # troops are drawn from the biggest stack
        per = max(0.2, bot.army_rating / 5)
        best = None
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
                key = (self.travel_turns(fleet, z), d)
                if best is None or key < best[0]:
                    best = (key, fleet, z, troops)
        if best:
            _, fleet, z, troops = best
            self.execute_send(fleet, z, bot, True, new_units(army=troops, navy=troops),
                              None, home, False)

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
            step = self.bot_next_step(bot, loc, targets, enemies)
            if step:
                self.execute_send(loc, step, bot, False, new_units(army=n))

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
        if self.game_over or self.bot_running:
            return
        if self.single_player and self.player.alive and not self.can_attack_now(self.player):
            self.play_bot_phases()            # not your phase yet: let the bots move first
            return
        if not self.advance_phase():
            return
        if self.single_player:
            self.play_bot_phases()
        if not self.game_over:
            self.refresh_all()

    def advance_phase(self):
        """Move the calendar on one phase (no redraw). Returns False if the war ended."""
        next_phase = {"Axis War Phase": "Allied War Phase",
                      "Allied War Phase": "Axis War Phase"}
        self.phase = next_phase[self.phase]
        self.ticks += 1                       # every End Phase = 2 months
        new_year = self.ticks % TURNS_PER_YEAR == 0

        self.process_pending_offensives()     # forces en route advance one turn
        if new_year:
            self.economy_tick()               # yearly income and oil production

        if self.year >= END_YEAR:
            self.end_game()
            return False

        if new_year:
            self.fire_scripted_events()
        return True

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