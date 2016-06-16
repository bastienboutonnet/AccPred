	# -*- coding: utf-8 -*-
import time, socket
import numpy
import glob, os, random, sys, gc, time
import psychopy
from psychopy import gui
from psychopy import prefs
psychopy.prefs.general['audioLib'] = [u'pygame']
from psychopy import core, visual,sound,event,data,misc, logging
from psychopy import visual
import generateTrials
from baseFoo import *
from stimPresFoo import *

#parallel.setPortAddress(address=0xD010)


#SetUp Experiment class
#Set up experimental settings, subject variable, presnetation rate etc.
#-------------------------

class Exp:
	def __init__(self):

		self.expName = 'lexRecall'
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
							'3' : { 'name' : 'subjCode',
									'prompt' : 'subject Code',
									'options' : 'any',
									'default' : 's1',
									'type' : str},
							'4' : { 'name' : 'breakEvery',
									'prompt' : 'Trials per block?',
									'options' : 'any',
									'default' : 15,
									'type' : int},
							'5' : { 'name' : 'useParallel',
									'prompt' : 'paralel port use',
									'options' : 'any',
									'default' : 'no',
									'type' : str},
								}
		optionsReceived=False
		fileOpened=False

		##Wait & Listen for User info and set up datafiles
		while not optionsReceived or not fileOpened:
			[optionsReceived,self.subjVariables] = enterSubjInfo(self.expName,self.optionList)
			if not optionsReceived:
				popupError(self.subjVariables)
			#try:
			if os.path.isfile('data/'+self.expName+'_'+self.subjVariables['subjCode']+'.txt'):
				print 'Error: That subject code already exists'
				fileOpened=False
			else:
				#self.eventTracker = open('data/'+self.subjVariables['subjCode']+'_eventTracker.txt','w')
				#self.practFile = open('data/practTrials'+self.expName+self.subjVariables['subjCode']+'.txt','w')
				self.testFile = open('data/'+self.expName+'_'+self.subjVariables['subjCode']+'.txt','w')

				fileOpened=True
			#except:
				#pass
		self.inputDevice = "keyboard"
		self.validResponses = {'z':0,'slash':1}

		if self.subjVariables['screenMode']=='fs':
			self.win = visual.Window(fullscr=True, color='gray', allowGUI=False, monitor='testMonitor',units='pix',screen=1)
		else:
			self.win = visual.Window([800,800], color='gray', allowGUI=False, monitor='testMonitor',units='pix',screen=1)

		self.presRate = .096 ########### Might be un-necessary for this particular procedure.

		self.instructions = "In this task, you will hear a series of 'beeps'.\nYour task is to try and catch the 'high' pitched beeps as fast as you can by pressing the SPACE bar.\n\nIt's that simple!\n\nWhen you are ready press any key to Start."
		self.practiceTrials = "The next part is practice.\n\nPress the space-bar to start."
		self.realTrials = "Now for the real trials.\n\nReady?\n\nPress the space-bar to continue."
		self.finalText = "This is the end of experiment :) Thank you for your participation!"
		self.takeBreakEveryXTrials=self.subjVariables['breakEvery']
		self.takeBreak = "Please take a short break.  Press one of the response keys to continue"
		self.afterSentenceDelay=3
		self.afterQuestionDelay=3
		self.responseInfoReminder = "z = No    / = Yes"

		generateTrials.main(self.subjVariables['subjCode'],self.subjVariables['seed'])
		if self.subjVariables['useParallel']=='yes':
			parallel.setPortAddress(address=0xD010)

### COME BACK TO THIS ONE NOT SURE WHAT IT DOES
class trial(Exp):
	def __init__(self):
		firstStim=''

## Sets Up Routines and Settings for Stimuli Presentation
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
		#showText(self.experiment.win, "caching soundfiles... please wait",color='black',waitForKey=False)
		"""This loads all the stimili and initializes the trial sequence"""
		self.fixSpot = visual.TextStim(self.experiment.win,text="+",height = 30,color="black")
		self.fixSpotReady = visual.TextStim(self.experiment.win,text="+",height = 50,color="red")
		self.fixSpotPlay = visual.TextStim(self.experiment.win,text="+",height = 30,color="blue")
		#self.pictureMatrix = loadFiles('stimuli','png','image',self.experiment.win)
		#self.soundMatrix = loadFiles('stimuli','wav',fileType="sound")
		(self.trialList,self.fieldNames) = importTrials('trials/trialListLex_'+self.experiment.subjVariables["subjCode"]+'.xlsx',method="sequential")
		#(self.practTrialList,self.fieldNamesPract) = importTrials('trials/trialListPract_'+self.experiment.subjVariables["subjCode"]+'.csv',method="sequential")
		self.locations = {'top':[0,275], 'bottom':[0,-275], 'left':[-275,0], 'right':[275,0], 'center':[0,0]}



	def showTestTrial(self,curTrial, trialIndex,whichPart):
		#s=sound.Sound(self.soundMatrix[curTrial['label']])
		print curTrial['filename']
		responseInfoReminder = visual.TextStim(self.experiment.win,text=self.experiment.responseInfoReminder,pos=(0,-200), height = 30,color="blue")

		if curTrial['relatedness']=='related':
			wordToPrez=visual.TextStim(self.experiment.win,text=curTrial['compLower'],pos=(0,0),height=30,color="black")

		if curTrial['relatedness']=='unrelated':
			wordToPrez=visual.TextStim(self.experiment.win,text=curTrial['unrelOppositeGender'],pos=(0,0),height=30,color="black")

		#### This may need to change when I know exactly how to figure out this part/
		if curTrial['relatedness']=='control':
			wordToPrez=visual.TextStim(self.experiment.win,text=curTrial['newWord1'],pos=(0,0),height=30,color="black")

		# if self.experiment.subjVariables['useParallel']=='yes':
		# 	playSentenceNoTriggerNonVisual(self.experiment.win,self.soundMatrix[curTrial['filename']],curTrial['onsetDet'], curTrial['waitForDetOffset'], curTrial['waitForNounOffset'],curTrial['waitForEnd'], curTrial['trigDet'],curTrial['trigOffsetNoun'],self.experiment.eventTracker,curTrial,self.expTimer)
		# else:
		# 	playSentenceNoTriggerNonVisual(self.experiment.win,self.soundMatrix[curTrial['filename']],curTrial['onsetDet'], curTrial['waitForDetOffset'], curTrial['waitForNounOffset'],curTrial['waitForEnd'], curTrial['trigDet'],curTrial['trigOffsetNoun'],self.experiment.eventTracker,curTrial,self.expTimer)
		response=99
		isRight=99
		rt=99
		setAndPresentStimulus(self.experiment.win,[responseInfoReminder,wordToPrez])
		(response,rt) = getKeyboardResponse(self.experiment.validResponses.keys())

		if self.experiment.validResponses[response]==curTrial['isOld']:
			isRight=1
		else:
			isRight=0

		fieldVars=[]
		for curField in self.fieldNames:
			fieldVars.append(curTrial[curField])
		[header, curLine] = createRespNew(self.experiment.optionList, self.experiment.subjVariables, self.fieldNames, fieldVars,
		a_expTimer = self.expTimer.getTime(),
		b_whichPart = curTrial['part'],
		c_trialIndex = trialIndex,
		f_response = response,
		g_isRight = isRight,
		h_rt = rt*1000)
		writeToFile(self.experiment.testFile,curLine)

		#write the header with col names to the file
		if trialIndex==0:
			print "Writing header to file..."
			dirtyHack = {}
			dirtyHack['trialNum']=1
			writeHeader(dirtyHack, header,'header_lex'+self.experiment.expName)

	def cycleThroughExperimentTrials(self,whichPart): #CHECK OUT PRACTICE STUFF
		curTrialIndex=0

		for curTrial in self.trialList:
			if curTrialIndex==0:
				waitingAnimation(currentExp.win,color="PowderBlue")
			if curTrialIndex>0 and curTrialIndex % self.experiment.takeBreakEveryXTrials == 0:
				showText(self.experiment.win,self.experiment.takeBreak,color=(-1,-1,-1),inputDevice=self.experiment.inputDevice) #take a break
				waitingAnimation(currentExp.win,color="PowderBlue")
			setAndPresentStimulus(self.experiment.win,[self.fixSpot])
			core.wait(.5)
			self.showTestTrial(curTrial,curTrialIndex,whichPart)
			curTrialIndex+=1
			self.experiment.win.flip()
			core.wait(.5)
		self.experiment.eventTracker.close()
		self.experiment.testFile.close()

###Experiment Step Launching
#---------------------------
currentExp = Exp()
currentPresentation = ExpPresentation(currentExp)
currentPresentation.initializeExperiment()


#Start Instructions
showText(currentExp.win,currentExp.instructions,color="black",inputDevice=currentExp.inputDevice)
showText(currentExp.win,currentExp.practiceTrials,color='black',inputDevice=currentExp.inputDevice,waitForKey=True)
#Start Practice Presentation
currentPresentation.cycleThroughExperimentTrials("practice")
#Start realTrials Presentation
showText(currentExp.win,currentExp.realTrials,color='black',inputDevice=currentExp.inputDevice,waitForKey=True)
currentPresentation.cycleThroughExperimentTrials("experiment")
#Goodbye Text
showText(currentExp.win,currentExp.finalText,color='black',waitForKey=False)

core.wait(2)
#currentExp.win.close()
#Exit Window
