	# -*- coding: utf-8 -*-
import time, socket
import numpy
import glob,os,random,sys,gc,time
import psychopy
from psychopy import prefs
psychopy.prefs.general['audioLib'] = [u'pygame']
from psychopy import core, visual,sound,event,data,gui,misc, logging
import generateTrials# -*- coding: utf-8 -*-
from stimPresFoo import *
from baseFoo import *


#SetUp Experiment class
#Set up experimental settings, subject variable, presnetation rate etc.
#-------------------------

class Exp:
	def __init__(self):

		self.expName = 'AccPred'
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
									'type' : int}
								}
		optionsReceived=False
		fileOpened=False

        ##Wait & Listen for User info and set up datafiles
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

        self.presRate = .096 ########### Might be un-necessary for this particular procedure.

        self.instructions = "In this task, you will hear a series of 'beeps'.\nYour task is to try and catch the 'high' pitched beeps as fast as you can by pressing the SPACE bar.\n\nIt's that simple!\n\nWhen you are ready press any key to Start."
		self.finalText = "This is the end of experiment :) Thank you for your participation!"
		self.takeBreakEveryXTrials=self.subjVariables['breakEvery']
		self.takeBreak = "Please take a short break.  Press one of the response keys to continue"

		generateTrials.main(self.subjVariables['subjCode'],self.subjVariables['seed'])

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
		showText(self.experiment.win, "caching soundfiles... please wait",color='black',waitForKey=False)
		"""This loads all the stimili and initializes the trial sequence"""
		self.fixSpot = visual.TextStim(self.experiment.win,text="+",height = 30,color="black")
		self.fixSpotReady = visual.TextStim(self.experiment.win,text="+",height = 50,color="red")
		self.fixSpotPlay = visual.TextStim(self.experiment.win,text="+",height = 30,color="blue")
		self.pictureMatrix = loadFiles('stimuli','png','image',self.experiment.win)
		self.soundMatrix = loadFiles('stimuli','wav',fileType="sound")
		(self.trialList,self.fieldNames) = importTrials('trials/trialList_'+self.experiment.subjVariables["subjCode"]+'.csv',method="sequential")
		self.locations = {'top':[0,275], 'bottom':[0,-275], 'left':[-275,0], 'right':[275,0], 'center':[0,0]}

	def showTestTrial(self,curTrial, trialIndex):
		#s=sound.Sound(self.soundMatrix[curTrial['label']])
		print curTrial['soundFile']
		playSentenceAndTrigger(self.experiment.win,self.soundMatrix[curTrial['filename']],curTrial['onsetDet'],,curTrial['onsetNoun'],curTrial['offsetNoun'],curTrial['totalLen'])


	def cycleThroughExperimentTrials(self): #CHECK OUT PRACTICE STUFF
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

###Experiment Step Launching
#---------------------------
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
