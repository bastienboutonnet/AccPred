#Base Functions
# 1. Load Files
# 2. Import Trials
# 3. Load Subject info
#---------------------------
import numpy

from psychopy import prefs
from psychopy import gui

try:
	import winsound
except ImportError:
	print "Warning: winsound not found; will try using pyo/pyaudio"
        try:
                import pyo
                print "Attempting to use pyo for sounds"
                prefs.general['audioLib'] = ['pyo']
                prefs.general['audioDriver'] = ['coreaudio']
        except:
                print 'could not load pyo'
from psychopy import sound,core, visual


if prefs.general['audioLib'][0] == 'pyo':
    print 'initializing pyo'
    sound.init(48000,buffer=128)
print 'Using %s(with %s) for sounds' %(sound.audioLib, sound.audioDriver)

from psychopy import core,logging,event,visual,data,misc
import glob,os,random,sys,gc,time,hashlib,subprocess
from math import *

# try:
# 	import pygame
# 	from pygame.locals import *
# except ImportError:
# 	print "Warning: pygame not found; will be using pyglet for stim presentation"
#pygame.mixer.pre_init(44100,-16,1, 4096) # pre-initialize to reduce the delay
try:
	from scipy import ndimage
except ImportError:
	pass


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
##Get Keyboard response
##________________________
def getKeyboardResponse(validResponses,duration=0):
	event.clearEvents()
	responded = False
	done = False
	rt = '*'
	responseTimer = core.Clock()
	while True:
		if not responded:
			responded = event.getKeys(validResponses, responseTimer)
		if duration>0:
			if responseTimer.getTime() > duration:
				break
		else: #end on response
			if responded:
				break
	if not responded:
		return ['*','*']
	else:
		return responded[0] #only get the first resp


def createRespNew(allSubjVariables,subjVariables,fieldVarNames,fieldVars,**respVars):
	"""Creates  a key and value list of all the variables passed in from various sources (runtime, trial params, dep. vars."""

	def stripUnderscores(keyList):
		return [curKey.split('_')[1] for curKey in keyList]

	trial = [] #initalize array
	header=[]
	for curSubjVar, varInfo in sorted(allSubjVariables.items()):
		header.append(allSubjVariables[curSubjVar]['name'])
		trial.append(subjVariables[varInfo['name']])
	for curFieldVar in fieldVars:
		trial.append(curFieldVar)
	for curRespVar in sortDictValues(respVars):
		trial.append(str(curRespVar))
	header.extend(fieldVarNames)
	header.extend(stripUnderscores(sortDictValues(respVars,'keys')))
	return [header,trial]

def writeHeader(curTrial,headerText,fileName='header'):
	try:
		if curTrial['trialNum']==1:
			if os.path.isfile(fileName+'.txt'): # file already exists
				print 'header file exists'
				return False
			else:
				headerFile = open(fileName+'.txt','w')
				writeToFile(headerFile,headerText)
				return True
	except:
		return False

def writeToFile(fileHandle,trial,sync=True):
	"""Writes a trial (array of lists) to a fileHandle"""
	line = '\t'.join([str(i) for i in trial]) #TABify
	line += '\n' #add a newline
	fileHandle.write(line)
	if sync:
		fileHandle.flush()
		os.fsync(fileHandle)

def sortDictValues(someDict,returnWhat='values'):
	keys = someDict.keys()
	keys.sort()
	if returnWhat=='values':
		return map(someDict.get, keys)
	else:
		return keys
