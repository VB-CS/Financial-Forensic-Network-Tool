with open("SPOTIFY_PRIVATE_PLAYLIST_BEST_OF_BEETLES_SONGS.txt", "r") as file:
    collector_name = file.readline().strip()

# Finds Collector
for i in range(100):  
    filename = f"members/member_ID{i}.txt"
    with open(filename, "r") as file:
        first_line = file.readline().strip()
        if first_line == collector_name:
            #print(line)
            collector = i


#Finds all the people Collector sent money to
with open("transactions.txt", "r") as file:
    lines = file.readlines()
to_numbers = []

# Extract all "to:" numbers
for line in lines:
    parts = line.strip().split("|")
    for part in parts:
        part = part.strip()
        if part.startswith("to:") and str(collector) in parts[0]:
            to_number = part.split(":")[1]
            to_numbers.append(to_number)
    


# Find the most common "to:" number
# Find which recipient (to_id) received the highest total amount from the collector
totals = []  # list of tuples (to_id, total_amount)

for line in lines:
    parts = line.strip().split("|")
    if len(parts) >= 3:
        from_id = parts[0].split(":")[1]
        to_id = parts[1].split(":")[1]
        amount = int(parts[2].split(":")[1])

        # Only consider transactions sent by the collector
        if from_id == str(collector):
            found = False
            for i in range(len(totals)):
                if totals[i][0] == to_id:
                    # Update existing total
                    totals[i] = (to_id, totals[i][1] + amount)
                    found = True
                    break
            if not found:
                # Add new entry
                totals.append((to_id, amount))

# Now find the to_id with the highest total amount
most_common = None
highest_total = -1

for to_id, total in totals:
    if total > highest_total:
        highest_total = total
        most_common = to_id
# (Optional) print the result for debugging
# print(f"The collector sent the most money to ID {most_common} with a total of {highest_total}.")

#print(f"Most common 'to:' number is {most_common} with {highest_count} occurrences.\n")

# Finds the balances of the Associates
total_amount = 0

for line in lines:
    parts = line.strip().split("|")
    
    if len(parts) >= 3 and f"to:{most_common}" in parts[1] and str(collector) in parts[0]:
        amount_part = parts[2].strip()
        if amount_part.startswith("amount:"):
            amount_str = amount_part.split(":")[1]
            total_amount += int(amount_str)
    if str(most_common) in parts[1]:
        from_number = part.split(":")[1] 
unique_from_numbers = []

for line in lines:
    parts = line.strip().split("|")
# Finds all the Associates who sent money to the boss
    if len(parts) >= 2 and f"to:{most_common}" in parts[1]:
        from_part = parts[0].strip()
        if from_part.startswith("from:"):
            from_number = from_part.split(":")[1]

            if from_number not in unique_from_numbers:
                unique_from_numbers.append(from_number)

                combined = str(from_number)  
                #print(combined)

#print(f"Total amount sent from collector {collector} to {most_common}: {total_amount}")

# Prints the name of the Associates
for from_id in unique_from_numbers:
    filename = f"members/member_ID{from_id}.txt"
    with open(filename, "r") as file:
        first_line = file.readline().strip()
        #print(f"Member ID {from_id}: {first_line}")


target_id = most_common
include_also = collector

all_ids = []
amounts_sent = []
amounts_received = []
included_ids = []

 # Collect sent/received info
with open("transactions.txt", "r") as file:
    for line in file:
        parts = line.strip().split("|")
        from_id = parts[0].split(":")[1]
        to_id = parts[1].split(":")[1]
        amount = int(parts[2].split(":")[1])


        if from_id in all_ids:
            idx = all_ids.index(from_id)
            amounts_sent[idx] += amount
        else:
            all_ids.append(from_id)
            amounts_sent.append(amount)
            amounts_received.append(0)

 
        if to_id in all_ids:
            idx = all_ids.index(to_id)
            amounts_received[idx] += amount
        else:
            all_ids.append(to_id)
            amounts_sent.append(0)
            amounts_received.append(amount)

# who sent money to boss
with open("transactions.txt", "r") as file:
    for line in file:
        parts = line.strip().split("|")
        from_id = parts[0].split(":")[1]
        to_id = parts[1].split(":")[1]

        if to_id == target_id and from_id not in included_ids:
            included_ids.append(from_id)

# Add the boss and Collector
for id in [target_id, include_also]:
    if id not in included_ids:
        included_ids.append(id)

# creates table
output_data = []

for i in range(len(all_ids)):
    id = all_ids[i]
    if id in included_ids:
        sent = amounts_sent[i]
        received = amounts_received[i]
        balance = received - sent

        with open(f"members/member_ID{id}.txt", "r") as member_file:
            name = member_file.readline().strip()



        output_data.append((int(id), name, balance)) 

# Sort list by ID 
output_data.sort() 

# Write to analysis.txt
with open("analysis.txt", "w") as output_file:
    output_file.write("id\tname\tbalance\n")
    for id, name, balance in output_data:
        output_file.write(f"{id}\t{name}\t{balance}\n")