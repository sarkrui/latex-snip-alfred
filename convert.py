import csv

# Open the input and output files
with open('latex.csv', 'r') as input_file, open('latex-alfred.csv', 'w', newline='') as output_file:
    csv_reader = csv.reader(input_file)
    csv_writer = csv.writer(output_file)

    # Skip the first row (header) of csv_reader
    next(csv_reader)
    
    for row in csv_reader:
        row.insert(1, row[0]) 
        row.insert(0, row.pop(1)) 

        csv_writer.writerow(row)
