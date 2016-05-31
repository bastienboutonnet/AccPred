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
