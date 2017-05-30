followers = open("d1.txt")
following = open("d2.txt")

followers.strip()
following.strip()

outliers = []

for dude in following:
  if dude not in followers:
    outliers.append(dude)
    
for decision in outliers:
  print(decision + "\n")
