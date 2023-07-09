import os
import json
import highlight
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

def create_visualization(filename):
    _, skills = highlight.highlight_important_words(filename)

    # Prepare the skills hierarchy for the sunburst chart
    skills_hierarchy = {"name": "skills", "children": []}
    skills_hierarchy["children"].append({"name": "Candidate Skills", "children": [{"name": skill} for skill in skills]})
    # Save the skills hierarchy as a JSON file
    with open('static/data/skills.json', 'w') as file:
        json.dump(skills_hierarchy, file)

    # load the skills.json file
    with open('static/data/skills.json', 'r') as f:
        data = json.load(f)

    def process_dict(d):
        return {"name": d["name"], "value": len(d["children"]) if "children" in d else 1}

    def dict_to_list(d):
        res = [process_dict(d)]
        if "children" in d:
            for child in d["children"]:
                res.extend(dict_to_list(child))
        return res

    data_list = dict_to_list(data)

    names = [item['name'] for item in data_list]
    sizes = [item['value'] for item in data_list]

    cmap = plt.get_cmap("tab20c")
    outer_colors = cmap(np.arange(3)*4)
    inner_colors = cmap(np.array([1, 2, 5, 6, 9, 10]))

    plt.pie(sizes, labels=names, colors=inner_colors, startangle=90, counterclock=False, radius=1.0)
    plt.savefig("static/images/sunburst.png", format="png")