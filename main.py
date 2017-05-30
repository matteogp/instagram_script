file1 = open("d1.txt")
file2 = open("d2.txt")

following = file2.readlines()
followers = file1.readlines()

outliers = []

def  cleanup(lst):
  name = False
  for f in lst:
    f.strip()
    if (f == "" or f ==" "):
      del f
    elif (f == "Verified"):
      del f
    elif (name == False):
      name = True
    else:
      del f
      name = False

cleanup(followers)
cleanup(following)

print("stripped!")

for account in following:
  if account not in followers:
    outliers.append(account)
    
print ("read!\n")

for decision in outliers:
  print(decision)
