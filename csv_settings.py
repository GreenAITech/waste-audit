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

def write_weight_data(csv_filepath, timestamp, weight):
    with open(csv_filepath,'a',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, weight])

def write_item_detected_data(csv_filepath, timestamp, classname, confidence):
    with open(csv_filepath,'a',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, classname, confidence])