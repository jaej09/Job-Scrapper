# Comma-Separated Values
import csv

def save_to_file(jobs):
  # Open an File
  # If an file doesn't exist, then it will create a new file
  # mode = w -> only want to write
  # mode = r -> only want to read
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["title", "company", "location", "link"])
  
  for job in jobs:
    # We only want value (remove key)
    # job.values() returns "DICT" Type, so I use list to convert type dist to list
    writer.writerow(list(job.values()))
  return