"""Check the distributed finite counterexample using Python 3 standard library.

Run from the package root: python checker/check.py
Results are emitted as JSON on stdout; package files are never modified.
The CSV uses labels 1..32; the Lean literals use labels 0..31.
The Lean source comparison checks data transcription, not Lean proof validity.
"""
import csv
import hashlib
import io
import json
import platform
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(relative):
    try:
        return (ROOT / relative).read_bytes()
    except OSError:
        raise ValueError("Cannot read " + relative) from None


def closure(seeds, adjacency):
    found, pending = set(seeds), list(seeds)
    while pending:
        for y in adjacency[pending.pop()]:
            if y not in found:
                found.add(y)
                pending.append(y)
    return frozenset(found)


def labels(text, smallest, largest, label):
    values = [int(x) for x in text.split()]
    require(values == sorted(set(values)), label + ": labels must be sorted and unique")
    require(all(smallest <= x <= largest for x in values), label + ": label out of range")
    return frozenset(values)


def lean_array(text, name, type_text):
    pattern = (r"\bdef\s+" + name + r"\s*:\s*Array\s+" + type_text
               + r"\s*:=\s*#\[(.*?)\n\]")
    matches = re.findall(pattern, text, flags=re.DOTALL)
    require(len(matches) == 1, "Cannot identify Lean array " + name)
    return matches[0]


def check():
    a, t, n = 3, 11, 32
    vertices = frozenset(range(1, n + 1))
    predecessors = {x: set() for x in vertices}
    successors = {x: set() for x in vertices}
    segments, covers, left = [], [], 1
    # End segments have a vertices; internal segments have a+1 vertices.
    for j, length in enumerate([a - 1] + [a] * (t - 2) + [a - 1]):
        segments.append(frozenset(range(left, left + length + 1)))
        for x in range(left, left + length):
            lo, hi = (x, x + 1) if j % 2 == 0 else (x + 1, x)
            predecessors[hi].add(lo)
            successors[lo].add(hi)
            covers.append((lo, hi))
        left += length
    require(left == n and len(covers) == len(set(covers)) == n - 1, "Incorrect fence path")
    below = {x: closure([x], predecessors) for x in vertices}
    require(all(x == y or x not in below[y] or y not in below[x]
                for x in vertices for y in vertices), "Relation is not antisymmetric")
    incidence = Counter(x for segment in segments for x in segment)
    shared = frozenset(x for x in vertices if incidence[x] == 2)
    parameters = [1 + sum(incidence[x] == 1 for x in segment) for segment in segments]
    require(n == a * t - 1 and t % 2 == 1 and parameters == [a] * t, "Incorrect paper parameters")
    # Check the eleven segments really are maximal chains in the constructed order.
    comparable = lambda x, y: x in below[y] or y in below[x]
    for segment in segments:
        require(all(comparable(x, y) for x in segment for y in segment), "Segment is not a chain")
        require(all(any(not comparable(x, y) for y in segment)
                    for x in vertices - segment), "Segment is not maximal")

    csv_bytes = read("data/orbit.csv")
    reader = csv.DictReader(io.StringIO(csv_bytes.decode("utf-8"), newline=""))
    require(reader.fieldnames == ["step", "ideal_vertices", "cardinality",
                                  "maximal_antichain", "mask_hex"], "Incorrect CSV schema")
    rows = list(reader)
    require(len(rows) == 237, "Incorrect CSV length")
    states, masks = [], []
    for k, record in enumerate(rows):
        require(int(record["step"]) == k, "Incorrect CSV step " + str(k))
        ideal = labels(record["ideal_vertices"], 1, n, "CSV ideal " + str(k))
        require(closure(ideal, predecessors) == ideal, "Not a lower ideal at step " + str(k))
        require(len(ideal) == int(record["cardinality"]), "Incorrect CSV cardinality")
        maxima = frozenset(x for x in ideal if not (successors[x] & ideal))
        require(maxima == labels(record["maximal_antichain"], 1, n, "CSV antichain"),
                "Incorrect CSV maximal antichain")
        mask = sum(1 << (x - 1) for x in ideal)
        require(mask == int(record["mask_hex"], 16), "Incorrect CSV mask")
        states.append(ideal)
        masks.append(mask)
    require(states[0] == {5, 6, 7, 8, 12}, "Incorrect initial ideal")
    require(len(set(states)) == len(states), "Repeated state before closure")
    for k, ideal in enumerate(states):
        # For a lower ideal, all strict predecessors in I characterize min(P\I).
        minima = {x for x in vertices - ideal if below[x] - {x} <= ideal}
        following = closure(minima, predecessors)
        require(following == states[(k + 1) % len(states)], "Incorrect rowmotion step " + str(k))
    # Distinct listed states and all successor equalities, including closure,
    # prove that 237 is the least positive return time, not just a return time.
    total = sum(map(len, states))
    require(total == 3774 and 2 * total != n * len(states), "Incorrect orbit sum")

    lean_bytes = read("lean/W04/Orbit.lean")
    lean_text = lean_bytes.decode("utf-8")
    body = lean_array(lean_text, "orbitData", r"\(Finset\s+Vertex\)")
    lean_states = []
    for line in body.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"\s*\{([0-9,\s]+)\},?\s*", line)
        require(match is not None, "Unsupported Lean orbit literal syntax")
        zero_based = labels(match.group(1).replace(",", " "), 0, n - 1, "Lean ideal")
        lean_states.append(frozenset(x + 1 for x in zero_based))
    require(lean_states == states, "CSV differs from Lean orbitData")
    code_body = lean_array(lean_text, "orbitCodeData", "Nat")
    require(re.fullmatch(r"\s*[0-9]+(?:\s*,\s*[0-9]+)*\s*", code_body) is not None,
            "Unsupported Lean code literal syntax")
    require([int(x) for x in code_body.split(",")] == masks, "CSV differs from Lean orbitCodeData")

    return {
        "status": "PASS", "python_version": platform.python_version(),
        "vertex_count": n, "segment_count": t, "paper_segment_parameters": parameters,
        "shared_vertices": sorted(shared), "initial_ideal": sorted(states[0]),
        "checked_lower_ideals": len(states), "distinct_states": len(set(states)),
        "checked_rowmotion_steps_including_closure": len(states),
        "least_positive_period": len(states), "ideal_cardinality_sum": total,
        "conjectured_sum": n * len(states) // 2,
        "mean": str(Fraction(total, len(states))),
        "deviation_from_half_vertex_count": str(Fraction(total, len(states)) - Fraction(n, 2)),
        "all_csv_fields_checked": True, "lean_orbit_literals_match": True,
        "lean_code_literals_match": True,
        "sha256": {
            "data/orbit.csv": hashlib.sha256(csv_bytes).hexdigest(),
            "lean/W04/Orbit.lean": hashlib.sha256(lean_bytes).hexdigest(),
            "checker/check.py": hashlib.sha256(read("checker/check.py")).hexdigest(),
        },
        "scope": "Exact finite certificate and Lean data transcription; no Lean proof execution or priority determination."
    }


def main():
    try:
        result = check()
    except (ValueError, KeyError, TypeError, csv.Error, UnicodeError) as error:
        result = {"status": "FAIL", "error": str(error)}
    output = json.dumps(result, indent=2) + "\n"
    print(output, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
