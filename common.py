import datetime
    

def changeToCurrentTime(strOld, mode):
    if mode == 'access':
        substr = strOld[strOld.find('[')+1 : strOld.find('[')+21]
        return strOld.replace(substr, getCurrentTime(mode)) 
    elif mode == 'sys':
        substr = strOld[ : 15]
        return strOld.replace(substr, getCurrentTime(mode))


def getCurrentTime(mode): 
    if mode == 'access':
        today = datetime.datetime.today().strftime("%d/%b/%Y")   
        now = datetime.datetime.now().strftime("%H:%M:%S")
        return ( today + ':' + now )
    elif mode == 'sys':
        today = datetime.datetime.today().strftime("%b %d")   
        now = datetime.datetime.now().strftime("%H:%M:%S")
        return ( today + ' ' + now )
