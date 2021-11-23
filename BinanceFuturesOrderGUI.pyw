import time,os,tkinter as tk
from tkinter import Tk, Label,Button,Frame,Entry,Spinbox,StringVar
from OrderMaker import gen_orders,orders_exec
import pyautogui
from mxproxy import mx
import Defaults

COINS=['BTC','ETH','BNB']
currentcoin='ETH'
# 
'''BUTTON STYLING'''
BTN_BASIC={'height':1,'width':12,'font':('monserrat', '20')}
BTN_SHORT_STYLE={'fg':'white','bg':'RED',**BTN_BASIC}
BTN_LONG_STYLE=	{'fg':'white','bg':'GREEN',**BTN_BASIC}

def mode_switcher():
	global mode
	if mode == 'demo':
		mode='live'
	else :
		mode='demo'
	modebtn['text']='MODE :: '+ mode
	print("ORDER EXEC MODE =>",mode)

def order(direction=''):
	global mode
	orderConfig=eval(f'Defaults.{currentcoin}_BASE')
	if stepsize.get()!='default':
		orderConfig.update({'stepsize':stepsize.get()})

	if delta.get()!='default':
		orderConfig.update({'delta':delta.get()})

	if sizeAccleration.get()!='default':
		orderConfig.update({'sizeAccleration':sizeAccleration.get()})

	if count.get()!='default':
		orderConfig.update({'count':count.get()})

	orders_exec(gen_orders(direction=direction,**orderConfig),mode=mode)

mx.touch('data/COINSETTINGS.json',data='{}')
def sync_value(context,var,val):
	d=mx.jload('data/COINSETTINGS.json')
	if d.get('ETH_BASE'):
		print('ETH_BASE not found')
	print(d.get('ETH_BASE'))
	pass


def set_currentcoin(c):
	def f(coin):
		global currentcoin
		currentcoin=coin
		return print(currentcoin)
	return lambda: f(c)

if __name__ == '__main__':

	lastrow=0
	mode='live'
	root = Tk()
	root.title('Binance Command Center')
	# root.grid_columnconfigure(0,weight=1)
	root.maxsize(800,600)
	root.iconbitmap('./images/binance-icon.ico')
	#______________________________________________
	warnings='\n-'.join([
	'- triple streak rule, place order if 3 greens/reds in a row',
	'NEVER exceed hedge ratio 10%',
	'your enemy is fear of loss and greed for gains'])
	warningBox = Label (root,text=warnings,justify='left',wraplength='400')
	warningBox.grid(row=0,columnspan=2,sticky='w')
	#______________________________________________
	frame1 = Frame(root, background="#000")
	frame1.grid(row=1, columnspan=2,sticky='ew',pady=(0))
	#______________________________________________
	lblconf={'bg':'#000','fg':'#fff','justify':tk.LEFT,'anchor':"w"}
	COIN=Defaults.ETH_BASE
	#______________________________________________
	lastrow+=1
	Label(frame1, text="stepsize", **lblconf).grid(row=lastrow,column=0,sticky='w')
	stepsizeVar=StringVar(root,COIN['stepsize'])
	stepsize= Spinbox(frame1,from_=1,to=20,textvariable=stepsizeVar)
	stepsize.grid(row=lastrow,column=1,)
	#______________________________________________
	Label(frame1, text="delta", **lblconf).grid(row=lastrow,column=2,sticky='w')
	deltaVar=StringVar(root,COIN['delta'])
	delta= Spinbox(frame1,from_=1,to=20,textvariable= deltaVar )
	delta.grid(row=lastrow,column=3)
	#______________________________________________
	lastrow+=1
	Label(frame1,text="sizeAccl",**lblconf).grid(row=lastrow,column=0,sticky='w')
	sizeAcclerationVar=StringVar(root,COIN['sizeAccleration'])
	(sizeAccleration:=
		Spinbox(frame1,
		from_=0,to=3,
		command=lambda:sync_value('ETH','sizeAccleration',sizeAccleration.get()),
		textvariable=sizeAcclerationVar,
		)).grid(row=lastrow,column=1)
	#______________________________________________
	Label(frame1,text="count",**lblconf).grid(row=lastrow,column=2,sticky='w')
	countvar=StringVar(root,COIN['count'])
	(count:= 
		Spinbox(frame1,
		from_=1,to=10,
		command=lambda:sync_value('ETH','count',count.get()),
		textvariable=countvar
		)).grid(row=lastrow,column=3)
	#______________________________________________


	lastrow+=1
	w = Button(root,command=lambda:order(direction='long')	,text="LONG▲",	**BTN_LONG_STYLE)
	w.grid(row=lastrow,column=0)
	w = Button(root,command=lambda:order(direction='short')	,text="SHORT▼",	**BTN_SHORT_STYLE)
	w.grid(row=lastrow,column=1)

	#______________________________________________
	lastrow+=1
	coinsOptionFrame=Frame(root,)
	coinsOptionFrame.grid(row=lastrow,columnspan=1,sticky='w')
	blist_conf={'justify':tk.CENTER}
	btlist=[Button(coinsOptionFrame,text=c,**blist_conf,command=set_currentcoin(c)) for c in COINS]
	[b.grid(row=lastrow,column=i,) for i,b in enumerate(btlist)]

	# lastrow+=1
	modebtn = Button(root,command=lambda : mode_switcher(), text='MODE :: '+mode ,fg="white", bg="BLUE",)
	modebtn.grid(row=lastrow,column=1,sticky='e')

	root.mainloop()
	
	# mx.touch()
	#change 1212