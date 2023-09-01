f = open("file_to_read.txt")
txt=f.read()

count_num = txt.count("terrible")#Count the number of occurrences of terrible
print('The number of "terrible":',count_num)

for i in range(count_num):
 
  if (i+1)%2==0:#If the current number of occurrences is even
        txt= txt.replace("terrible", "pathetic",1)#Replace the current "terrible" as "pathetic"
  else:
        txt = txt.replace("terrible", "marvellous",1)#Replace the current "terrible" as "marvellous"
#print(txt)
f.close()

with open("result.txt","w") as f:
  f.write(txt)#write "txt" to file
  
