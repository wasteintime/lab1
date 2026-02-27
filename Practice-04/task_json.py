import json

#1. Download data from a file
with open("sample-data.json", "r") as file:
    data = json.load(file)

#2. Print the title
print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<7} {'MTU':<6}")
print("-" * 50, "-" * 20, "-" * 6, "-" * 6)

# 3. Go through the list of interfaces
# In the Cisco ACI structure, data is usually stored in ['imdata']
interfaces = data.get("imdata", [])

for item in interfaces:
    # Extracting attributes (structure: item -> 'l1PhysIf' -> 'attributes')
    attrs = item["l1PhysIf"]["attributes"]
    
    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "inherit")
    mtu = attrs.get("mtu", "")

    # Print the line with alignment
    print(f"{dn:<50} {descr:<20} {speed:<7} {mtu:<6}")