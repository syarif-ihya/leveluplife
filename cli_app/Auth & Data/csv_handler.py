import csv

def read_csv(path):
    with open(path, newline="") as fl:
        return list(csv.DictReader(fl))

def write_csv(path, fieldnames, data):
    with open(path, "w", newline="") as fl:
        writer = csv.DictWriter(fl, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
