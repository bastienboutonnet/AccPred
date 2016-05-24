import pandas as pd
import easygui

def generateSplicePattern():
    filename=easygui.fileopenbox(filetypes=['*.csv'])
    df=pd.read_csv(filename)

    grouped=df.groupby('sentID')
    #rezDf=pd.DataFrame({'fileA','fileB'})
    count=0
    for k, gp in grouped:
        curSubTable=grouped.get_group(k)
        #keep Context Test
        val1=curSubTable['fileName'][(curSubTable['keepCont']==1)]
        #splice test
        val2=curSubTable['fileName'][(curSubTable['splice']==1)]
        if count<1:
            res=pd.DataFrame({'fileA':val1.values,'fileB':val2.values})
        else:
            curRow=pd.DataFrame({'fileA':val1.values,'fileB':val2.values})
            res=res.append(curRow)
        count+=1

    res=res.reset_index(drop=True)
    #res['outputFilename']=res.fileB.str.cat('_spliced',sep='')
    res['outputFilename']=res['fileB'].apply(lambda x: x+'_spliced')
    return res

if __name__=='__main__':
    pattern=generateSplicePattern()
    pattern.to_csv('splicePattern.txt', index=False, sep='\t')
