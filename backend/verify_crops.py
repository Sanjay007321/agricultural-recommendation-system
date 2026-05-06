import json

with open('app/data/crops.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

crops = data['crops']
print(f'Total crops: {len(crops)}\n')
for crop in crops:
    print(f'{crop["name"]}: {len(crop["varieties"])} varieties')
