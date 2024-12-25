from flask import Flask, render_template, request
import random as r

app = Flask(__name__)

# Your existing code
def make_lists(golfers):
    num_golfers = len(golfers)
    groups = []
    num_groups = (num_golfers + 4 - 1) // 4
    for _ in range(1, num_groups + 1):
        groups.append([])
    return groups

def generate_round(golfers, golfer_history):
    round = make_lists(golfers)
    r.shuffle(golfers)
    p = 0
    g = 0
    while p < len(golfers):
        if g >= len(round):
            clear_history(golfer_history)
            g = 0
        if len(round[g]) < 4 and check_history(round[g], golfers[p], golfer_history) and golfers[p] not in round:
            round[g].append(golfers[p])
            p += 1
            g = 0
        else:
            g += 1
    update_history(round, golfer_history)
    return round

def update_history(groups, golfer_history):
    for group in groups:
        for golfer in group:
            for teammate in group:
                if teammate != golfer and teammate not in golfer_history[golfer]:
                    golfer_history[golfer].append(teammate)

def clear_history(golfer_history):
    for key in golfer_history:
        if len(golfer_history[key]) != 0:
            golfer_history[key].remove(golfer_history[key][0])

def check_history(group, key, golfer_history):
    for golfer in group:
        if golfer in golfer_history[key]:
            return False
    return True

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        names = request.form.get("names").title()
        num_rounds = int(request.form.get("num_rounds"))
        golfers = names.split(", ")
        
        golfer_history = {golfer: [] for golfer in golfers}
        rounds_output = []
        
        for i in range(1, num_rounds + 1):
            round = generate_round(golfers, golfer_history)
            rounds_output.append({"round": i, "groups": round})
        
        result = rounds_output
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
