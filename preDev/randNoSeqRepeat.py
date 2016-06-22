prevMaskNum= curMaskNum = False
while not done:
    while prevMaskNum==curMaskNum:
        curMaskNum = random.randint(0,40) #or whatever it is
    prevMaskNum = curMaskNum

prevMaskNum= curMaskNum = False

for i in xrange(20):
    curMaskNum=random.randint(0,3)
    while prevMaskNum==curMaskNum:
        curMaskNum=random.randint(0,3)
    prevMaskNum=curMaskNum
    print "curMask= %i" % curMaskNum
