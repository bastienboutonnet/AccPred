#Stim Presentation Functions
# 1. Present Text Stimuli
# 2. Present Visual/Dawable stimuli
# 3. Play Sentence (sound) + Send Triggers
# 4. Waiting Animation
# 5. Error popup
#---------------------------
from psychopy import visual,core,event,data,info,prefs, parallel

import os
try:
	import winsound
	winSoundLoaded=True
except ImportError:
	print "Warning: winsound can't be imported. Will try to use pyadio"
	winSoundLoaded=False
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

def playSentenceAndTriggerVisual(win,soundFile,trigger1Time, trigger2Time,trigDuration=.3):
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

def playSentenceAndTriggerNonVisual(win,soundFile,onsetDet,waitForDetOffset,waitForNounOffset,waitForEnd,trigDet, trigOffsetNoun, eventFile,curTrial,timer):
	# int1=onsetDet
	# int2=onsetNoun-onsetDet
	# int3=offsetNoun-onsetNoun
	# int4=totalLen-int3

	#triggerWord=visual.TextStim(win, text='+') #Better to implement this via a fixation cross/dot that changes colour.
	#triggerWord.draw()
	sDuration=soundFile.getDuration()
	parallel.setData(1)
	core.wait(.001)
	soundFile.play()
	parallel.setData(0)
	#parallel.setData(0)
	print 'startSent'
	sentStart=timer.getTime()
	#writeToFile(eventFile,[curTrial,timer.getTime(),"sentStart"])

	core.wait(onsetDet) #wait till trigger time
	parallel.setData(trigDet)
	t1=timer.getTime()
	print 'onsetDet'

	#writeToFile(eventFile,[curTrial,timer.getTime(),"onsetDet",trigDet])

	core.wait(waitForDetOffset)
	parallel.setData(0)
	t2=timer.getTime()
	print 'onsetNoun'

	#writeToFile(eventFile,[curTrial,timer.getTime(),"onsetNoun"])

	core.wait(waitForNounOffset)
	parallel.setData(trigOffsetNoun)
	t3=timer.getTime()
	print 'offsetNoun'

	#writeToFile(eventFile,[curTrial,timer.getTime(),"offsetNoun",trigOffsetNoun])

	core.wait(waitForEnd)
	parallel.setData(0)
	t4=timer.getTime()
	print 'endSentence'

	#writeToFile(eventFile,[curTrial,timer.getTime(),"endSentence"])

	writeToFile(eventFile,[curTrial['trialIndex'],curTrial['filename'],curTrial['relatedness'],curTrial['speaker'],curTrial['part'],curTrial['sentID'],sentStart,"sentStart"])
	writeToFile(eventFile,[curTrial['trialIndex'],curTrial['filename'],curTrial['relatedness'],curTrial['speaker'],curTrial['part'],curTrial['sentID'],t1,"onsetDet",trigDet])
	writeToFile(eventFile,[curTrial['trialIndex'],curTrial['filename'],curTrial['relatedness'],curTrial['speaker'],curTrial['part'],curTrial['sentID'],t2,"onsetNoun"])
	writeToFile(eventFile,[curTrial['trialIndex'],curTrial['filename'],curTrial['relatedness'],curTrial['speaker'],curTrial['part'],curTrial['sentID'],t3,"offsetNoun",trigOffsetNoun])
	writeToFile(eventFile,[curTrial['trialIndex'],curTrial['filename'],curTrial['relatedness'],curTrial['speaker'],curTrial['part'],curTrial['sentID'],t4,"endSentence"])
	return

def playSentenceNoTriggerNonVisual(win,soundFile,onsetDet,waitForDetOffset,waitForNounOffset,waitForEnd,trigDet, trigOffsetNoun, eventFile,curTrial,timer):
	# int1=onsetDet
	# int2=onsetNoun-onsetDet
	# int3=offsetNoun-onsetNoun
	# int4=totalLen-int3

	#triggerWord=visual.TextStim(win, text='+') #Better to implement this via a fixation cross/dot that changes colour.
	#triggerWord.draw()
	sDuration=soundFile.getDuration()
	soundFile.play()
	print 'startSent'
	sentStart=timer.getTime()
	#writeToFile(eventFile,[curTrial,timer.getTime(),"sentStart"])

	core.wait(onsetDet) #wait till trigger time
	#parallel.setData(trigDet)
	t1=timer.getTime()
	print 'onsetDet'

	#writeToFile(eventFile,[curTrial,timer.getTime(),"onsetDet",trigDet])

	core.wait(waitForDetOffset)
	#parallel.setData(0)
	t2=timer.getTime()
	print 'onsetNoun'

	#writeToFile(eventFile,[curTrial,timer.getTime(),"onsetNoun"])

	core.wait(waitForNounOffset)
	#parallel.setData(trigOffsetNoun)
	t3=timer.getTime()
	print 'offsetNoun'

	#writeToFile(eventFile,[curTrial,timer.getTime(),"offsetNoun",trigOffsetNoun])

	core.wait(waitForEnd)
	#parallel.setData(0)
	t4=timer.getTime()
	print 'endSentence'

	#writeToFile(eventFile,[curTrial,timer.getTime(),"endSentence"])

	writeToFile(eventFile,[curTrial['trialIndex'],curTrial['filename'],curTrial['relatedness'],curTrial['speaker'],curTrial['part'],curTrial['sentID'],sentStart,"sentStart"])
	writeToFile(eventFile,[curTrial['trialIndex'],curTrial['filename'],curTrial['relatedness'],curTrial['speaker'],curTrial['part'],curTrial['sentID'],t1,"onsetDet",trigDet])
	writeToFile(eventFile,[curTrial['trialIndex'],curTrial['filename'],curTrial['relatedness'],curTrial['speaker'],curTrial['part'],curTrial['sentID'],t2,"onsetNoun"])
	writeToFile(eventFile,[curTrial['trialIndex'],curTrial['filename'],curTrial['relatedness'],curTrial['speaker'],curTrial['part'],curTrial['sentID'],t3,"offsetNoun",trigOffsetNoun])
	writeToFile(eventFile,[curTrial['trialIndex'],curTrial['filename'],curTrial['relatedness'],curTrial['speaker'],curTrial['part'],curTrial['sentID'],t4,"endSentence"])
	return

def playSentenceAndTrigger(self,win,soundFile,trigger1Time, trigger2Time,curTrial,trigDuration=.1):
	#triggerWord=visual.TextStim(win, text='#########')
	#triggerWord.draw()
	sDuration=soundFile.getDuration()
	soundFile.play()
	core.wait(trigger1Time) #wait till trigger time
	#win.flip() #send Trigger
	parallel.setData(122)
	writeToFile(self.experiment.eventTracker,[curTrial,self.expTimer.getTime(),"standard",122])
	core.wait(trigDuration)
	#win.flip() #wait for minimum duration needed for tigger recording
	parallel.setData(0)
	core.wait((trigger2Time-trigger1Time)-trigDuration)
	#triggerWord.draw()
	#win.flip() ########################################################THIS WILL GO AWAY WHEN NO NEED OF VISUAL PRES
	parallel.setData(150)
	writeToFile(self.experiment.eventTracker,[curTrial,self.expTimer.getTime(),"deviant",122])
	core.wait(trigDuration)
	#win.flip()
	parallel.setData(0)
	core.wait((sDuration-trigger2Time)-trigDuration) #wait till end of sentence
	return

def playAndWait(soundFile,soundPath='',winSound=False,waitFor=-1):
	"""Sound (other than winSound) runs on a separate thread. Waitfor controls how long to pause before resuming. -1 for length of sound"""
	if not winSoundLoaded:
		winSound=False
	if prefs.general['audioLib'] == ['pygame']:
				#default to using winsound
				winSound=True
	if winSound:
		print 'using winsound to play sound'
		if waitFor != 0:
			soundFile.play()
		else: #playing asynchronously - need to load the path.
			if soundPath:
				winsound.PlaySound(soundPath, winsound.SND_FILENAME|winsound.SND_ASYNC)
			else:
				sys.exit("sound path not provided to playAndWait")
		return
	else:
		if waitFor<0:
			waitDurationInSecs = sound.getDuration()
		elif waitFor>0:
			waitDurationInSecs = waitFor
		else:
			waitDurationInSecs=0

		if waitDurationInSecs>0:
			sound.play()
			core.wait(waitDurationInSecs)
			sound.stop()
			return
		else:
			sound.play()
			print 'returning right away'
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

def writeToFile(fileHandle,trial,sync=True):
	"""Writes a trial (array of lists) to a fileHandle"""
	line = '\t'.join([str(i) for i in trial]) #TABify
	line += '\n' #add a newline
	fileHandle.write(line)
	if sync:
		fileHandle.flush()
		os.fsync(fileHandle)
