import os  
import sys  
                 
def displayFile(file):  
    unPath= sys.executable  
    unPath=unPath[ 0 : unPath.rfind( os.sep ) ]  
    newname = file[0:file.rfind('.')] + '.py'  
    command = "python -u "+unPath+"\scripts\uncompyle2 " + file + ">" + newname  
    try:  
        os.system(command)  
    except e:  
        print file  
      
if __name__ == '__main__':  
      
    #print unPath  
    print 'init'  
    displayFile('./BodyTextExtractor.pyc')
    print 'finished' 
