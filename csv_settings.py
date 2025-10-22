import csv

def create_weight_csv_header(csv_filepath):
    headers = [
        "timestamp",
        "weight"
    ]
    with open(csv_filepath,'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

def create_item_detected_csv_header(csv_filepath):
    headers = [
        "timestamp",
        "classname",
        "confidence"
    ]
    with open(csv_filepath,'w',newline ='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
