from datetime import date

today = date.today()
print(str(today)[2:4]+str(today)[5:7] + str(today)[8:10])
print("Today's date:", today)