#!/usr/bin/env python3
"""
Daily Reflection Tree — CLI Agent (Part B)
DeepThought Fellowship Assignment

Loads reflection-tree.json and walks the employee through a deterministic
conversation. No LLM calls at runtime. No randomness. Pure tree traversal.

Usage:
    python agent.py [path/to/reflection-tree.json]
    python agent.py                          # defaults to ../tree/reflection-tree.json
"""

import json
import sys
import time
import os
import textwrap


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def load_tree(path: str) -> dict:
    """Load and index the tree from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        tree = json.load(f)
    # Build a fast-lookup dict by node id
    tree["_index"] = {n["id"]: n for n in tree["nodes"]}
    return tree


def interpolate(text: str, state: dict) -> str:
    """Replace {PLACEHOLDER} tokens in text with values from state['answers']."""
    for key, val in state["answers"].items():
        text = text.replace(f"{{{key}}}", str(val))
    return text


def record_signal(signal: str | None, state: dict) -> None:
    """Parse 'axis1:internal' and increment the corresponding tally."""
    if not signal:
        return
    parts = signal.split(":")
    if len(parts) == 2:
        axis, pole = parts
        state["signals"].setdefault(axis, {})
        state["signals"][axis][pole] = state["signals"][axis].get(pole, 0) + 1


def dominant_pole(state: dict, axis: str) -> str | None:
    """Return the pole with the highest tally for the given axis, or None if tied/empty."""
    poles = state["signals"].get(axis, {})
    if not poles or sum(poles.values()) == 0:
        return None
    max_val = max(poles.values())
    winners = [p for p, v in poles.items() if v == max_val]
    # If strictly dominant, return it; if tied, return the first (alphabetical)
    return sorted(winners)[0]


def wrap(text: str, width: int = 64, indent: str = "  ") -> str:
    """Word-wrap text for clean terminal rendering."""
    lines = []
    for paragraph in text.split("\n"):
        if paragraph.strip() == "":
            lines.append("")
        else:
            wrapped = textwrap.fill(paragraph, width=width,
                                    initial_indent=indent,
                                    subsequent_indent=indent)
            lines.append(wrapped)
    return "\n".join(lines)


def hr(char: str = "─", width: int = 64) -> str:
    return "  " + char * width


# ─────────────────────────────────────────────
#  Node Handlers
# ─────────────────────────────────────────────

def handle_start(node: dict, state: dict) -> str:
    print()
    print(hr("═"))
    print(wrap(node["text"]))
    print(hr("═"))
    print()
    input("  [ Press Enter to begin ]")
    return node["next"]


def handle_question(node: dict, state: dict) -> str:
    print()
    print(hr())
    print()
    print(wrap(interpolate(node["text"], state)))
    print()
    options = node["options"]
    for i, opt in enumerate(options, 1):
        print(wrap(f"{i}.  {opt['label']}", indent="     "))
    print()

    while True:
        try:
            raw = input("  Your choice (1–{}): ".format(len(options))).strip()
            choice = int(raw)
            if 1 <= choice <= len(options):
                break
            print(f"  Please enter a number between 1 and {len(options)}.")
        except (ValueError, EOFError):
            print("  Please enter a number.")

    selected = options[choice - 1]
    state["answers"][node["id"]] = selected["label"]
    record_signal(selected.get("signal"), state)
    return selected["next"]


def handle_decision(node: dict, state: dict) -> str:
    """Evaluate routing rules and return the next node id."""
    for route in node["routes"]:
        cond = route["condition"]

        if cond["type"] == "answer":
            answer_node = cond["node"]
            given_answer = state["answers"].get(answer_node)
            if given_answer in cond["values"]:
                return route["next"]

        elif cond["type"] == "signal_dominant":
            axis = cond["axis"]
            dom = dominant_pole(state, axis)
            if dom == cond["dominant"]:
                return route["next"]

    # Fallback: last route
    return node["routes"][-1]["next"]


def handle_reflection(node: dict, state: dict) -> str:
    print()
    print(hr("─"))
    print()
    print(wrap("💭  " + interpolate(node["text"], state)))
    print()
    input("  [ Press Enter to continue ]")
    return node["next"]


def handle_bridge(node: dict, state: dict) -> str:
    print()
    print(hr("·"))
    print()
    print(wrap("↓   " + interpolate(node["text"], state)))
    print()
    time.sleep(1.2)
    return node["next"]


def handle_summary(node: dict, state: dict, tree: dict) -> str:
    # Compute readable axis summaries
    axis_labels = {
        "axis1": {"internal": "with agency",     "external": "reactively"},
        "axis2": {"contribution": "with a contribution mindset", "entitlement": "with entitlement in the mix"},
        "axis3": {"altro": "with a wide radius", "self": "with a narrow lens"},
    }
    for axis, labels in axis_labels.items():
        dom = dominant_pole(state, axis)
        state["answers"][f"{axis}_summary"] = labels.get(dom, "in a balanced way") if dom else "in a balanced way"

    # Pick summary reflection from lookup table
    axis1_dom = dominant_pole(state, "axis1") or "external"
    axis2_dom = dominant_pole(state, "axis2") or "entitlement"
    axis3_dom = dominant_pole(state, "axis3") or "self"
    key = f"{axis1_dom}|{axis2_dom}|{axis3_dom}"
    summary_reflections = tree.get("summary_reflections", {})
    state["answers"]["summary_reflection"] = summary_reflections.get(
        key,
        "Thank you for taking the time to look at your day honestly."
    )

    print()
    print(hr("═"))
    print()
    print("  YOUR DAILY REFLECTION")
    print()
    print(wrap(interpolate(node["text"], state)))
    print()
    print(hr("═"))
    print()
    input("  [ Press Enter to close ]")
    return node["next"]


def handle_end(node: dict, state: dict) -> None:
    print()
    print(wrap(node["text"]))
    print()


# ─────────────────────────────────────────────
#  Main walker
# ─────────────────────────────────────────────

def walk(tree: dict) -> None:
    index = tree["_index"]
    state = {
        "answers": {},
        "signals": {
            "axis1": {"internal": 0, "external": 0},
            "axis2": {"contribution": 0, "entitlement": 0},
            "axis3": {"altro": 0, "self": 0},
        },
    }

    current_id = "START"

    while current_id:
        node = index[current_id]
        t = node["type"]

        if t == "start":
            current_id = handle_start(node, state)
        elif t == "question":
            current_id = handle_question(node, state)
        elif t == "decision":
            current_id = handle_decision(node, state)
        elif t == "reflection":
            current_id = handle_reflection(node, state)
        elif t == "bridge":
            current_id = handle_bridge(node, state)
        elif t == "summary":
            current_id = handle_summary(node, state, tree)
        elif t == "end":
            handle_end(node, state)
            break
        else:
            # Unknown node type — skip gracefully
            print(f"  [Unknown node type: {t}]")
            break


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────

def main():
    if len(sys.argv) > 1:
        tree_path = sys.argv[1]
    else:
        # Default: ../tree/reflection-tree.json relative to this file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        tree_path = os.path.join(script_dir, "..", "tree", "reflection-tree.json")

    if not os.path.exists(tree_path):
        print(f"Error: Tree file not found at '{tree_path}'")
        print("Usage: python agent.py [path/to/reflection-tree.json]")
        sys.exit(1)

    tree = load_tree(tree_path)
    walk(tree)


if __name__ == "__main__":
    main()
