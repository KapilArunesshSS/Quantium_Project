import csv
import os

DATA_DIRECTORY = "./data"
OUTPUT_FILE_PATH = "./output/output.csv"

# make sure output directory exists
os.makedirs("./output", exist_ok=True)

# collect all processed rows here
rows = []

# iterate through all files in the data directory
for file_name in os.listdir(DATA_DIRECTORY):
    if file_name.endswith(".csv"):  # only process CSVs
        with open(f"{DATA_DIRECTORY}/{file_name}", "r") as input_file:
            reader = csv.reader(input_file)
            row_index = 0
            for input_row in reader:
                if row_index > 0:  # skip header
                    product = input_row[0]
                    raw_price = input_row[1]
                    quantity = input_row[2]
                    transaction_date = input_row[3]
                    region = input_row[4]

                    if product.lower() == "pink morsel":
                        # remove $ from price and convert
                        price = float(raw_price.replace("$", ""))
                        sale = price * int(quantity)

                        rows.append([sale, transaction_date, region])
                row_index += 1

# sort rows by date then region
rows.sort(key=lambda x: (x[1], x[2]))

# write to output file
with open(OUTPUT_FILE_PATH, "w", newline="") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["sales", "date", "region"])  # header
    writer.writerows(rows)

print(f"Cleaned & sorted output saved to {OUTPUT_FILE_PATH}")
