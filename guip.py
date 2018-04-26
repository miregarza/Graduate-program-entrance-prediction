#---------------------------------Imports start--------------------------------
import math
import numpy as np
import random
import tkinter as Tk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
#---------------------------------Imports End--------------------------------

#---------------------------Functions Start--------------------------------
def getData():
	file = open("data.csv","r")
	points = []
	for line in file:
		points.append(line.split(","))
	
	points.pop(0)
	for i in points:
		i[2]= i[2].replace("\r","")
		i[2]= i[2].replace("\n","")
		for j in i:
			j = float(j)
	#split to x, y, and classification
	data = [[],[],[]]
	for i in points:
		data[0].append(float(i[1]))#gre
		data[1].append(float(i[2]))#gpa
		data[2].append(float(i[0]))#acceptance
	return data #[[gre list],[gpa list],[acceptance list]]

def plotter(complete):
	x = complete[0]
	y = complete[1]
	b = complete[2]
	clr = ""
	for i in range(len(x)):
		#print("point", x[i], y[i])
		if(b[i] == 0):
			clr = "red"
		else:
			clr = "green"
		plt.plot(x[i],b[i],marker = '.', markersize = 3, color = clr)

def logRegPlot(b):
	logs = []
	for i in range(820):
		logs.append([1/(1 + math.exp(-(b[1]*i-b[0])))])
	plt.plot(logs, markersize = 1, color = "blue")

def linReg(complete,feature):
	#feature: 0= gre, 1=gpa
	y = complete[2]
	x = complete[feature]
	xin = []
	for i in x:
		xin.append([feature,i])
	w = np.dot(np.linalg.pinv(xin),y)
	b0 = np.mean(complete[2])-(w[1] * np.mean(complete[feature]))
	return([b0,w[1]])

def linear(m,b):
	coord = []
	for i in range(850):
		x = (i*m)+ b
		coord.append(x)
	return(coord)

def logR(b,complete):
	lgr = []
	for i in range (len(complete[0])):
		lgr.append([complete[0][i],1/(1 + math.exp(-(b[1]*complete[0][i]-b[0])))])
	#print(lgr)
	lor = []
	i = 0
	while i <= 820:
		lor.append([i,1/(1 + math.exp(-(b[1]*i-b[0])))])
		i = i +1
	return(lor)

def logRegPoint(b,x):
	point = ([x,1/(1 + math.exp(-(b[1]*x-b[0])))])
	plt.plot(point[0], point[1],marker = 's', markersize = 8, color = "green")
	return(point)

def logRegPer(b,x):
	point = ([x,1/(1 + math.exp(-(b[1]*x-b[0])))])
	return(point[1])

def recommendation(feature, features, gre, gpa, perGPA, perGRE,b,final,complete):
	hit = 0
	if (feature == 1):
		while (logRegPer(b,gre)< .7):
			hit = 1
			gpa = gpa*1.05

		if(hit == 1):
			fin = ("The probability of you being accepted if you increased your GPA to: "+\
				  str(round(gpa,1))+ " is: ", str(round(logRegPer(b,gpa)*100,2))+ "%")
			recs = Label(window, text=fin, fg ="green4",font = ("Arial", 15, "bold"))
			recs.place(relx=0.5, rely=(0.55), anchor = CENTER)
	elif(feature == 0):
		while (logRegPer(b,gre)< .6):
			hit = 1
			gre = gre*1.05

		if(hit == 1):
			fin = ("The probability of you being accepted if you increased your GRE to: "+\
				  str(round(gre,1))+ " is: "+ str(round(logRegPer(b,gre)*100,2))+ "%")
			recs = Label(window, text=fin, fg ="green4",font = ("Arial", 15, "bold"))
			recs.place(relx=0.5, rely=(0.55), anchor = CENTER)
	else:
		allUser = final[0]
		feature = int(allUser[0])
		b1 = linReg(complete,feature)
		while (((logRegPer(b1,gre) + logRegPer(b,gpa))/2) < .7):
			hit = 1
			gre = gre*1.05
			gpa = gpa*1.05

		if(hit == 1):
			fin = ("The probability of you being accepted if you increased your GRE to: "+\
				  str(round(gre,1))+ " is: "+ str(round(logRegPer(b1,gre)*100,2))+ "%")
			fin1 = ("The probability of you being accepted if you increased your GPA to: "+\
				  str(round(gpa,1))+ " is: "+ str(round(logRegPer(b,gpa)*100,2))+ "%")
			fin2 = ("the avg of these two features is: "+ str(round(((logRegPer(b1,gre) + logRegPer(b,gpa))/2)*100,2))+ "%")

			recs = Label(window, text=fin, fg ="green4")
			recs1 = Label(window, text=fin1, fg ="green4")
			recs2 = Label(window, text=fin2, fg ="green4",font = ("Arial", 15, "bold"))

			recs.place(relx=0.5, rely=(0.55), anchor = CENTER)
			recs1.place(relx=0.5, rely=(0.70), anchor = CENTER)
			recs2.place(relx=0.5, rely=(0.85), anchor = CENTER)
	if(hit == 0):
		fin = ("Wow, that's a high probability, you don't even need a recommendation!")
		recs = Label(window, text=fin, fg ="green4", font = ("Arial", 15, "bold"))
		recs.place(relx=0.5, rely=(0.55), anchor = CENTER)


def Onegre():
	singlelbl.destroy()
	grebtn.destroy()
	gpabtn.destroy()
	result = simpledialog.askfloat("GRE input", "What is your GRE score?")
	failedin = 0
	while(result < 0 or result > 800):
		failedin = 1
		warn = Label(window, text="that's not a valid answer", fg = "red")
		warn.grid(column=0, row=3)
		result = simpledialog.askfloat("GRE input", "What is your GRE score?")
	if(failedin == 1):
		warn.destroy()
	allUser = [0,result,"GRE score"]
	feature = int(allUser[0])
	value = int(allUser[1])
	featureToString = allUser[2]
	complete = getData()
	plotter(complete)
	#y = complete[2] = acceptance binary
	#x = complete[0] = gre score
	b = linReg(complete,feature) #gets slope(b1) and intersection(b0) linear regression 
	lineR = linear(b[1],b[0]) #plot array for linear reg [x,y]
	lgr =logR(b, complete)#points of log function from -5k to +5k
	logRegPlot(b)
	percentFeature = logRegPoint(b, value)
	results = ("Your probability of being accepted based on your " + featureToString + " is: " + str(round(percentFeature[1]*100,2)) + "%")
	finals = Label(window, text=results, font = ("Arial", 15))
	finals.place(relx=0.5, rely=(0.4), anchor = CENTER)
	recommendation(feature, featureToString, value, value, percentFeature[1], percentFeature[1],b,0,0)
	plt.xlabel("GRE score")
	plt.ylabel("Accepted")
	plt.ylim(-0.01,1.01)
	plt.xlim(0,820)
	#plt.ion()
	plt.show()

def Onegpa():
	singlelbl.destroy()
	grebtn.destroy()
	gpabtn.destroy()
	result = simpledialog.askfloat("GPA input", "What is your GPA?")
	failedin = 0
	while(result < 0 or result > 4):
		failedin = 1
		warn = Label(window, text="that's not a valid answer", fg = "red")
		warn.grid(column=0, row=3)
		result = simpledialog.askfloat("GPA input", "What is your GPA?")
	if(failedin == 1):
		warn.destroy()
	allUser = [1,result,"GPA"]
	feature = int(allUser[0])
	value = int(allUser[1])
	featureToString = allUser[2]
	complete = getData()
	plotter(complete)
	#y = complete[2] = acceptance binary
	#x = complete[0] = gre score
	b = linReg(complete,feature) #gets slope(b1) and intersection(b0) linear regression 
	lineR = linear(b[1],b[0]) #plot array for linear reg [x,y]
	lgr =logR(b, complete)#points of log function from -5k to +5k
	logRegPlot(b)
	percentFeature = logRegPoint(b, value)
	results = ("Your probability of being accepted based on your " + featureToString + " is: " + str(round(percentFeature[1]*100,2)) + "%")
	finals = Label(window, text=results,font = ("Arial", 15))
	finals.place(relx=0.5, rely=(0.40), anchor = CENTER)
	recommendation(feature, featureToString, value, value, percentFeature[1], percentFeature[1],b,0,0)
	plt.xlabel("GPA score")
	plt.ylabel("Accepted")
	plt.ylim(-0.01,1.01)
	plt.xlim(0,4.1)
	#plt.ion()
	plt.show()

def cl1():
	lbl.destroy()
	btn1.destroy()
	btn2.destroy()
	complete = getData()
	singlelbl.place(relx = 0.5, rely = 0.1, anchor = CENTER)
	grebtn.place(relx = 0.5, rely = 0.25, anchor = CENTER)
	gpabtn.place(relx = 0.5, rely = 0.4, anchor = CENTER)

def cl2():
	lbl.destroy()
	btn1.destroy()
	btn2.destroy()
	final = [[0,0,"GRE score"],[1,0,"GPA"]]#return [feature,value,featureToString]
	#feature = 0 #feature: 0 = gre, 1 = gpa

	#handles GPA
	hit = 0
	final[1][1] = simpledialog.askfloat("GPA input", "What is your GPA?")
	while(final[1][1] < 0 or final[1][1] > 4):
			hit = 1
			warn = Label(window, text="that's not a valid answer", fg = "red")
			warn.grid(column=0, row=3)
			final[1][1] = simpledialog.askfloat("GPA input", "What is your GPA?")
	#handles GRE
	if(hit == 1):
		warn.destroy()
		hit = 0
	final[0][1] = simpledialog.askfloat("GRE input", "What is your GRE score?")
	while(final[0][1] < 0 or final[0][1] > 800):
			hit = 1
			warn = Label(window, text="that's not a valid answer", fg = "red")
			warn.grid(column=0, row=3)
			final[0][1] = simpledialog.askfloat("GRE input", "What is your GRE score?")
	if(hit == 1):
		warn.destroy()
	complete = getData()
	realValue = []
	percents = [0,0]
	for i in range(2):
		allUser = final[i]	
		feature = int(allUser[0])
		value = int(allUser[1])
		featureToString = allUser[2]
		plotter(complete)
		#y = complete[2] = acceptance binary
		#x = complete[0] = gre score
		b = linReg(complete,feature) #gets slope(b1) and intersection(b0) linear regression 
		lineR = linear(b[1],b[0]) #plot array for linear reg [x,y]
		lgr =logR(b, complete)#points of log function from -5k to +5k
		logRegPlot(b)
		percentFeature = logRegPoint(b, value)
		singletext = ("Your probability of being accepted based on your " + featureToString + " is: " + str(round(percentFeature[1]*100,2))  + "%")
		singleRes = Label(window, text=singletext)
		singleRes.place(relx=0.5, rely=(0.15 + (.1*i)), anchor = CENTER)
		percents[i] = percentFeature[1]
		realValue.append(value)
	avg = (percents[0] + percents[1])/2
	results = ("The average of these two values is "+ str((round(avg,2))*100) + "%")
	finals = Label(window, text=results, font = ("Arial", 15, "bold"))
	finals.place(relx=0.5, rely=0.35, anchor = CENTER)
	recommendation(2, featureToString, realValue[0],realValue[1], percents[0], percents[1],b,final,complete)
#---------------------------Functions end--------------------------------

#---------------------------------Main Start--------------------------------
window = Tk()
window.title("Machine Learning Project")
lbl = Label(window, text="This will determine the probability of being accepted based on your GPA and GRE scores", font = ("Arial", 18, "bold"))
lbl2 =Label(window, text = "Please choose if you'd like to compare one feature or two")
lbl.place(relx=0.5, rely=0.05, anchor = CENTER)
lbl2.place(relx=0.5, rely=0.15, anchor = CENTER)
window.geometry('800x400')
btn1 = Button(window, text="single feature", command = cl1, font = ("Arial", 20))
btn1.place(relx=0.5, rely=0.25, anchor = CENTER)
btn2 = Button(window, text="both features", command = cl2, font = ("Arial", 20))
btn2.place(relx=0.5, rely=0.4, anchor = CENTER)
singlelbl = Label(window, text = "Please select a feature",font = ("Arial", 18, "bold"))
grebtn =Button(window, text="GRE", command = Onegre, font = ("Arial", 20))
gpabtn =Button(window, text="GPA", command = Onegpa, font = ("Arial", 20))


# StartAns = int(input("Do you want the probability for one feature (1) or both(2)?: "))
# if(StartAns == 1):
# 	OnePlot()
# elif(StartAns == 2):
# 	twoPlot()
window.mainloop()
#plt.clf()#closes everything
#---------------------------------Main End--------------------------------

