from datasets import load_dataset
import json

ds = load_dataset("Nithins03/us-architectural-floorplan-sft")

print(ds['train'][13])

# print(json.dumps(ds['train'][13]['messages'][2]['content'], indent=1))

content = ds['train'][13]['messages'][2]['content']
scene_graph = json.loads(content.split('```')[1].split('json')[1])


print(json.dumps(scene_graph, indent=1))
