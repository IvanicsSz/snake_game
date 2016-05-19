q,vertical,horizontal=-1,1,1
screen.addstr(y,x,message)
y+=vertical
x+=horizontal
if y==dims[0]-1:
  vertical=-1
elif y==0:
  vertical=1
if x== dims[1]-len(message)-1:
  horizontal=-1
elif x==0:
  horizontal=1
