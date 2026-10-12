"""Where Towns and Haliburton went in every committed slot-10 room (mocks 51-75), and whether each lasted through picks
#11-#14 when he was still on the board at #10 and the owner left him there. Room type from arena/mocks/README.md: mocks 55,
62-66 and 69-72 are the deck's MOCK mode against the modeled league-mates (62-66 and 69-72 on the real 2026-27 seating:
Cayas at 11, Hegi at 12); every other room is a public Yahoo room of random humans."""
import json, os, sys
DECK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CAST = {55, 62, 63, 64, 65, 66, 69, 70, 71, 72}
K, H = "Karl-Anthony Towns", "Tyrese Haliburton"
out = dict(rooms=[], summary={})
for m in range(51, 76):
    f = f"{DECK}/arena/data/states/draft_state_{m}.json"
    if not os.path.exists(f): continue
    s = json.load(open(f)); P = s["picks"]; cast = dict((a, b) for a, b in s.get("cast", []))
    names = [p["player"] for p in P]
    row = dict(mock=m, room="cast" if m in CAST else "public", owner10=names[9], owner15=names[14])
    for tag, n in (("towns", K), ("haliburton", H)):
        i = names.index(n) if n in names else None
        pk = i + 1 if i is not None else None
        on10 = pk is not None and pk >= 10
        left = on10 and pk != 10                     # on the board at #10 and the owner did not take him there
        row[tag] = dict(pick=pk, by=("owner" if pk and P[i]["slot"] == s["slot"] else (cast.get(P[i]["slot"]) or f"seat {P[i]['slot']}") if pk else None),
                        on_board_at_10=on10, left_at_10=left, lasted_to_15=(pk is None or pk >= 15) if left else None)
    out["rooms"].append(row)
for room in ("public", "cast"):
    rs = [r for r in out["rooms"] if r["room"] == room]
    out["summary"][room] = {tag: dict(rooms=len(rs), on_board_at_10=sum(1 for r in rs if r[tag]["on_board_at_10"]),
                                     left_at_10=sum(1 for r in rs if r[tag]["left_at_10"]),
                                     lasted_to_15=sum(1 for r in rs if r[tag]["lasted_to_15"]),
                                     gone_11_14=[(r["mock"], r[tag]["pick"], r[tag]["by"]) for r in rs if r[tag]["left_at_10"] and not r[tag]["lasted_to_15"]])
                            for tag in ("towns", "haliburton")}
json.dump(out, open(sys.argv[1], "w"), indent=1)
for room, d in out["summary"].items():
    for tag, v in d.items():
        print(f"{room:6} {tag:10} rooms {v['rooms']:2} on board at #10 {v['on_board_at_10']:2} left there {v['left_at_10']:2} lasted to #15 {v['lasted_to_15']:2}  gone at 11-14: {v['gone_11_14']}")
