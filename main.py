file1 = open("d1.txt")
file2 = open("d2.txt")

followers = file1.readlines()
following = file2.readlines()

unfollow = []

def strip_list (lst):
  alt = 2
  newlst = []
  for f in lst:
    if (alt==3):
      f.strip()
      alt = 0
      newlst.append(f)
    else:
      alt+=1
  return newlst

#followers = strip_list(followers)
print("--")
following = strip_list(following)

for account in following:
  if account not in followers:
    unfollow.append(account)
    print(account + "\n")
  