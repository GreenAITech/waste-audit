import csv

def create_combined_csv_header(csv_filepath):
    headers = [
        "timestamp",
        "weight", 
        "amount",
        "classname",
        "confidence"
    ]
    with open(csv_filepath,'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

def write_combined_data(csv_filepath, timestamp, weight, amount=0, classname=None, confidence=None):

    with open(csv_filepath,'a',newline='') as csvfile:
        writer = csv.writer(csvfile)
        row = [timestamp, weight, amount]
        if classname is not None:
            row.extend([classname, confidence or 0.0])
        else:
            row.extend(['', ''])
        
        writer.writerow(row)

