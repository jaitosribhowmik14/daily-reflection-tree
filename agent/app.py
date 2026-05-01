from flask import Flask, render_template, request, session, jsonify
import json
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

app.secret_key = "deepthought_secret_key"

# -----------------------------
# LOAD TREE
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TREE_PATH = os.path.join(BASE_DIR, "..", "tree", "reflection-tree.json")

with open(TREE_PATH, "r") as f:
    tree_data = json.load(f)

nodes = {node["id"]: node for node in tree_data["nodes"]}


# -----------------------------
# HELPERS
# -----------------------------
def initialize_state():
    return {
        "current_node": tree_data["start_node"],
        "answers": {},
        "axis1": {"internal": 0, "external": 0},
        "axis2": {"contribution": 0, "entitlement": 0},
        "axis3": {"self": 0, "other": 0},
        "transcript": []
    }


def apply_signal(signal, state):
    if not signal:
        return

    try:
        axis, value = signal.split(":")
        if axis in state and value in state[axis]:
            state[axis][value] += 1
    except:
        pass


def dominant(axis_dict):
    return max(axis_dict, key=axis_dict.get)


def humanize(axis_name, value):
    mapping = {
        "axis1": {
            "internal": "more internally driven (victor-oriented)",
            "external": "more externally driven (victim-oriented)"
        },
        "axis2": {
            "contribution": "more contribution-oriented",
            "entitlement": "more entitlement-aware"
        },
        "axis3": {
            "self": "more self-focused",
            "other": "more outwardly focused"
        }
    }
    return mapping[axis_name][value]


def interpolate_text(text, state):
    replacements = {
        "{axis1_dominant}": humanize("axis1", dominant(state["axis1"])),
        "{axis2_dominant}": humanize("axis2", dominant(state["axis2"])),
        "{axis3_dominant}": humanize("axis3", dominant(state["axis3"]))
    }

    for key, value in replacements.items():
        text = text.replace(key, value)

    for node_id, answer in state["answers"].items():
        placeholder = "{" + node_id + ".answer}"
        text = text.replace(placeholder, answer)

    return text


def get_current_node(state):
    return nodes[state["current_node"]]


def auto_advance(state):
    """
    Automatically advance through start, bridge, reflection, summary nodes
    until user input is needed or end is reached.
    """
    while True:
        node = get_current_node(state)

        if node["type"] in ["start", "bridge"]:
            state["transcript"].append({
                "type": node["type"],
                "text": interpolate_text(node["text"], state)
            })
            state["current_node"] = node["target"]

        elif node["type"] in ["reflection", "summary"]:
            state["transcript"].append({
                "type": node["type"],
                "text": interpolate_text(node["text"], state)
            })
            break

        else:
            break

    return state


# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def index():
    session["state"] = initialize_state()
    state = session["state"]

    state = auto_advance(state)
    session["state"] = state

    node = get_current_node(state)

    return render_template(
        "index.html",
        node=node,
        transcript=state["transcript"],
        progress=0
    )


@app.route("/next", methods=["POST"])
def next_step():
    state = session.get("state", initialize_state())
    node = get_current_node(state)

    if node["type"] == "question":
        selected = request.form.get("option")

        if not selected:
            return jsonify({"error": "No option selected"}), 400

        selected_option = None
        for option in node["options"]:
            if option["label"] == selected:
                selected_option = option
                break

        if not selected_option:
            return jsonify({"error": "Invalid option"}), 400

        # Save answer
        state["answers"][node["id"]] = selected_option["label"]

        # Apply signal
        apply_signal(selected_option.get("signal", ""), state)

        # Add to transcript
        state["transcript"].append({
            "type": "question",
            "text": node["text"],
            "answer": selected_option["label"]
        })

        # Move to next
        state["current_node"] = selected_option["target"]

    elif node["type"] in ["reflection", "summary"]:
        state["current_node"] = node["target"]

    state = auto_advance(state)

    session["state"] = state

    node = get_current_node(state)

    # Calculate progress
    total_axes = 3
    completed = 0

    if sum(state["axis1"].values()) > 0:
        completed += 1
    if sum(state["axis2"].values()) > 0:
        completed += 1
    if sum(state["axis3"].values()) > 0:
        completed += 1

    progress = int((completed / total_axes) * 100)

    return render_template(
        "index.html",
        node=node,
        transcript=state["transcript"],
        progress=progress
    )


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)