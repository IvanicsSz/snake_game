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
# gameoverhez
screen.clear()
message1='Game Over'
message2='press space to play again'
message3='press enter to quit'
#screen.addstr(dims[0]/2,(dims[1]-len(message1))/2,message1
#..........
#https://www.youtube.com/user/IsharaComixVideos/videos?sort=dd&view=0&shelf_id=0
# érdemes kitenni a változókat initialize -ba mint global
