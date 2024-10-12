people = {
    "Alvin": "+959-400-983-911",
    "Juno": "+959-446-215-841",
    "Oke": "+959-972-403-489",
}


name = input("Name: ")

if name in people:
    print(f"Found {people[name]}")
else:
    print("Not found")
