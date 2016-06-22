# -*- coding: utf-8 -*-
import time, socket
import numpy
import glob,os,random,sys,gc,time
import psychopy
from psychopy import prefs
psychopy.prefs.general['audioLib'] = [u'pygame']
from psychopy import core, visual,sound,event,data,gui,misc, logging
import generateTrials
#from baseDefsPsychoPy import *
#from stimPresPsychoPy import *

#Stim Presentation Functions
#---------------------------
##Present Text Stimuli
def showText(win,textToShow,color=[-1,-1,-1],waitForKey=True,acceptOnly=0,inputDevice="keyboard",mouse=False,pos=[0,0],scale=1):
	global event
	#event.clearEvents() #clear all events just in case
	win.flip()
	if win.units == "pix":
		height = 30*scale
		wrapWidth=int(win.size[0]*.8)
	elif win.units == "deg":
		height=.7*scale
		wrapWidth=30
	else:
		wrapWidth=None
	textStim = visual.TextStim(win, pos=pos,wrapWidth=wrapWidth,color=color,height=height,text=textToShow)
	textStim.draw()
	win.flip()
	if mouse:
		while any(mouse.getPressed()):
			core.wait(.1) #waits for the user to release the mouse
		while not any(mouse.getPressed()):
			pass
		return
	elif inputDevice=="keyboard":
		if waitForKey:
			if acceptOnly==0:
				event.waitKeys()
			else:
				#event.waitKeys(keyList=list(str(acceptOnly)))
				event.waitKeys(keyList=[acceptOnly])
			return
		else:
			event.clearEvents(eventType='keyboard')
			return
	elif inputDevice=="gamepad": #also uses mouse if mouse is not false
		while True:
			for event in pygame.event.get(): #check responses
				if mouse:
					if event.type==pygame.MOUSEBUTTONDOWN:
						pygame.event.clear()
						return
				if event.type==pygame.KEYDOWN or event.type==pygame.JOYBUTTONDOWN:
					pygame.event.clear()
					return

##Present Visual/Drawable Stimulus
def setAndPresentStimulus(win,stimuli,duration=0):
	"""Stimuli can be a list or a single draw-able stimulus"""
	if type(stimuli).__name__=="list":
		for curStim in stimuli:
			curStim.draw()
	else:
		stimuli.draw()
	if duration==0: #single frame
		#t=core.getTime()
		win.flip()
		#t2=core.getTime()
		#print 'delay: %f' % (t2-t)
	else:
		#t=core.getTime()
		win.flip()
		core.wait(duration)
		#t2=core.getTime()
		#print 'delay: %f' % t2-t
	return

def playSentenceAndTrigger(win,soundFile,trigger1Time, trigger2Time,trigDuration=.3):
	triggerWord=visual.TextStim(win, text='#########')
	triggerWord.draw()
	sDuration=soundFile.getDuration()
	soundFile.play()
	core.wait(trigger1Time) #wait till trigger time
	win.flip() #send Trigger
	core.wait(trigDuration)
	win.flip() #wait for minimum duration needed for tigger recording
	core.wait((trigger2Time-trigger1Time)-trigDuration)
	triggerWord.draw()
	win.flip() ########################################################THIS WILL GO AWAY WHEN NO NEED OF VISUAL PRES
	core.wait(trigDuration)
	win.flip()
	core.wait((sDuration-trigger2Time)-trigDuration) #wait till end of sentence
	return

def waitingAnimation(win,size=20,distanceBetweenElements=3,numElements=8,delay=.5,color="#333333"):
	totalWidth = numElements*(size+distanceBetweenElements)
	positions = range(totalWidth/-2,totalWidth/2,(size+distanceBetweenElements))
	for curFrame in range(numElements,-1,-1):
		for curElement in range(curFrame):
			if curFrame>3:
				visual.GratingStim(win,color=color,size=size,tex='None', mask='circle',pos=[positions[curElement],0]).draw()
			else:
				visual.GratingStim(win,color='red',size=size,tex='None', mask='circle',pos=[positions[curElement],0]).draw()
		win.flip()
		core.wait(delay)

def popupError(text):
	errorDlg = gui.Dlg(title="Error", pos=(200,400))
	errorDlg.addText('Error: '+text, color='Red')
	errorDlg.show()

#Base Functions
#---------------------------
##Load Files
def loadFiles(directory,extension,fileType,win='',whichFiles='*',stimList=[]):
	""" Load all the pics and sounds"""
	path = os.getcwd() #set path to current directory
	if isinstance(extension,list):
		fileList = []
		for curExtension in extension:
			fileList.extend(glob.glob(os.path.join(path,directory,whichFiles+curExtension)))
	else:
		fileList = glob.glob(os.path.join(path,directory,whichFiles+extension))
	fileMatrix = {} #initialize fileMatrix  as a dict because it'll be accessed by picture names, cound names, whatver
	for num,curFile in enumerate(fileList):
		fullPath = curFile
		fullFileName = os.path.basename(fullPath)
		stimFile = os.path.splitext(fullFileName)[0]
		if fileType=="image":
			try:
				surface = pygame.image.load(fullPath) #gets height/width of the image
				stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
				fileMatrix[stimFile] = ((stim,fullFileName,num,surface.get_width(),surface.get_height(),stimFile))
			except: #no pygame, so don't store the image dims
				stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
				fileMatrix[stimFile] = ((stim,fullFileName,num,'','',stimFile))
		elif fileType=="sound":
			soundRef = sound.Sound(fullPath)
			fileMatrix[stimFile] = ((soundRef))
		elif fileType=="winSound":
			soundRef = open(fullPath,"rb").read()
			fileMatrix[stimFile] = ((soundRef))
			fileMatrix[stimFile+'-path'] = fullPath #this allows asynchronous playing in winSound.

	#check
	if stimList and set(fileMatrix.keys()).intersection(stimList) != set(stimList):
		popupError(str(set(stimList).difference(fileMatrix.keys())) + " does not exist in " + path+'\\'+directory)
	return fileMatrix
##Import Trials
def importTrials(fileName,method="sequential",seed=random.randint(1,100)):
	(stimList,fieldNames) = data.importConditions(fileName,returnFieldNames=True)
	trials = data.TrialHandler(stimList,1,method=method,seed=seed) #seed is ignored for sequential; used for 'random'
	return (trials,fieldNames)
##Load Subject Information
def enterSubjInfo(expName,optionList):
	""" Brings up a GUI in which to enter all the subject info."""

	def inputsOK(optionList,expInfo):
		for curOption in sorted(optionList.items()):
			if curOption[1]['options'] != 'any' and expInfo[curOption[1]['name']] not in curOption[1]['options']:
				return [False,"The option you entered for " + curOption[1]['name'] + " is not in the allowable list of options: " + str(curOption[1]['options'])]
		print "inputsOK passed"
		return [True,'']

	try:
		expInfo = misc.fromFile(expName+'_lastParams.pickle')
	except:
		expInfo={} #make the kind of dictionary that this gui can understand
		for curOption in sorted(optionList.items()):
			expInfo[curOption[1]['name']]=curOption[1]['default']
	#load the tips
	tips={}
	for curOption in sorted(optionList.items()):
		tips[curOption[1]['name']]=curOption[1]['prompt']
	expInfo['dateStr']= data.getDateStr()
	expInfo['expName']= expName
	dlg = gui.DlgFromDict(expInfo, title=expName, fixed=['dateStr','expName'],order=[optionName[1]['name'] for optionName in sorted(optionList.items())],tip=tips)
	if dlg.OK:
		misc.toFile(expName+'_lastParams.pickle', expInfo)
		[success,error] = inputsOK(optionList,expInfo)
		if success:
			return [True,expInfo]
		else:
			return [False,error]
	else:
		core.quit()


class Exp:
	def __init__(self):

		#this is where the subject variables go.  'any' means any value is allowed as long as it's the correct type (str, int, etc.) the numbers 1 and 2 control the order in which the prompts are displayed (dicts have no natural order)

		self.expName = 'oddballSoundFile'
		self.optionList = {	'1':  {	'name' : 'screenMode',
									'prompt' : 'debug or fs',
									'options': ('debug','fs'),
									'default':'fs',
									'type' : str},
							'2' : { 'name' : 'seed',
									'prompt' : 'random Number',
									'options' : 'any',
									'default' : 10,
									'type' : int},
							'3' : { 'name' : 'numTrials',
									'prompt' : 'number of trials',
									'options' : 'any',
									'default' : 50,
									'type' : int},
							'4' : { 'name' : 'subjCode',
									'prompt' : 'subject Code',
									'options' : 'any',
									'default' : 's1',
									'type' : str},
							'5' : { 'name' : 'breakEvery',
									'prompt' : 'Trials per block?',
									'options' : 'any',
									'default' : 15,
									'type' : int}
								}
		optionsReceived=False
		fileOpened=False

		while not optionsReceived or not fileOpened:
			[optionsReceived,self.subjVariables] = enterSubjInfo(self.expName,self.optionList)
			if not optionsReceived:
				popupError(self.subjVariables)
			#try:
			if os.path.isfile('data/'+self.subjVariables['subjCode']+'_eventTracker.txt'):
				print 'Error: That subject code already exists'
				fileOpened=False
			else:
				self.eventTracker = open('data/'+self.subjVariables['subjCode']+'_eventTracker.txt','w')

				fileOpened=True
			#except:
				#pass

		self.inputDevice = "keyboard"

		if self.subjVariables['screenMode']=='fs':
			self.win = visual.Window(fullscr=True, color='gray', allowGUI=False, monitor='testMonitor',units='pix')
		else:
			self.win = visual.Window([800,800], color='gray', allowGUI=False, monitor='testMonitor',units='pix')

		self.presRate = .096

		self.instructions = "In this task, you will hear a series of 'beeps'.\nYour task is to try and catch the 'high' pitched beeps as fast as you can by pressing the SPACE bar.\n\nIt's that simple!\n\nWhen you are ready press any key to Start."
		self.finalText = "This is the end of experiment :) Thank you for your participation!"
		self.takeBreakEveryXTrials=self.subjVariables['breakEvery']
		self.takeBreak = "Please take a short break.  Press one of the response keys to continue"

		generateTrials.main(self.subjVariables['subjCode'],self.subjVariables['seed'],self.subjVariables['numTrials'])

class trial(Exp):
	def __init__(self):
		firstStim=''

class ExpPresentation(trial):
	def __init__(self,experiment):
		self.experiment = experiment

	def initializeExperiment(self):
		# Experiment Clocks
		self.expTimer = core.Clock()
		splash = visual.ImageStim(self.experiment.win, image='splash.png',mask=None,interpolate=False)
		splash.draw()
		self.experiment.win.flip()
		core.wait(2)
		showText(self.experiment.win, "caching soundfiles... please wait",color='black',waitForKey=False)
		"""This loads all the stimili and initializes the trial sequence"""
		self.fixSpot = visual.TextStim(self.experiment.win,text="+",height = 30,color="black")
		self.fixSpotReady = visual.TextStim(self.experiment.win,text="+",height = 50,color="red")
		self.fixSpotPlay = visual.TextStim(self.experiment.win,text="+",height = 30,color="blue")
		self.pictureMatrix = loadFiles('stimuli','png','image',self.experiment.win)
		self.soundMatrix = loadFiles('stimuli','wav',fileType="sound")
		(self.trialList,self.fieldNames) = importTrials('trials/trialList_'+self.experiment.subjVariables["subjCode"]+'.csv',method="sequential")
		#(self.trialListMatrixTest,self.fieldNamesTest) = importTrials('trials/trialList_test_'+self.experiment.subjVariables["subjCode"]+'.csv',method="sequential")
		self.locations = {'top':[0,275], 'bottom':[0,-275], 'left':[-275,0], 'right':[275,0], 'center':[0,0]}

	def showTestTrial(self,curTrial, trialIndex):
		#s=sound.Sound(self.soundMatrix[curTrial['label']])
		print curTrial['soundFile']
		playSentenceAndTrigger(self.experiment.win,self.soundMatrix[curTrial['soundFile']],curTrial['stdTrig'],curTrial['devTrigg'])


		# prevMaskNum= curMaskNum = False
		# t=core.getTime()
		# for i in xrange(30):
		#	 curMaskNum=random.randint(2,20)
		#	 while prevMaskNum==curMaskNum:
		#		 curMaskNum=random.randint(2,20)
		#	 prevMaskNum=curMaskNum
		#	 #self.pictureMatrix[str(curMaskNum)+'_'+curTrial['objectName']+'-right-1.png'][0].setPos(self.locations['center'])
		#	 #setAndPresentStimulus(self.experiment.win,self.pictureMatrix[str(curMaskNum)+'_'+curTrial['objectName']+'-right-1'])
		#	 #setAndPresentStimulus(self.experiment.win,[self.pictureMatrix[str(curMaskNum)+'_'+curTrial['objectName']+'-left-1'][0]])
		#	 if curTrial['objectName']=='anaglyphGray':
		#		 setAndPresentStimulus(self.experiment.win,[self.pictureMatrix[str(curMaskNum)+'_'+curTrial['objectName']+'-left'][0]])
		#	 else:
		#		 setAndPresentStimulus(self.experiment.win,[self.pictureMatrix[str(curMaskNum)+'_'+curTrial['objectName']+'-right-'+str(self.experiment.subjVariables['contrast'])][0]])
		#	 t1=core.getTime()
		#	 #self.pictureMatrix['mask_'+str(curMaskNum)][0]
		#	 core.wait(self.experiment.presRate)
		#	 t2=core.getTime()
		# t3=core.getTime()
		# print 'duration: %f' % (t3-t)
		# print 'singel img: %f' % (t2-t1)

	def cycleThroughExperimentTrials(self):
		curTrialIndex=0

		for curTrial in self.trialList:
			if curTrialIndex==0:
				waitingAnimation(currentExp.win,color="PowderBlue")
			if curTrialIndex>0 and curTrialIndex % self.experiment.takeBreakEveryXTrials == 0:
				showText(self.experiment.win,self.experiment.takeBreak,color=(-1,-1,-1),inputDevice=self.experiment.inputDevice) #take a break
				waitingAnimation(currentExp.win,color="PowderBlue")
			setAndPresentStimulus(self.experiment.win,[self.fixSpot])
			self.showTestTrial(curTrial,curTrialIndex)
			curTrialIndex+=1
			self.experiment.win.flip()
			core.wait(.2)
		self.experiment.eventTracker.close()

currentExp = Exp()
currentPresentation = ExpPresentation(currentExp)
currentPresentation.initializeExperiment()


#Start Instructions
showText(currentExp.win,currentExp.instructions,color="black",inputDevice=currentExp.inputDevice)

#Start Trial Presentation
currentPresentation.cycleThroughExperimentTrials()
#Goodbye Text
showText(currentExp.win,currentExp.finalText,color='black',waitForKey=False)
core.wait(2)
#currentExp.win.close()
#Exit Window
