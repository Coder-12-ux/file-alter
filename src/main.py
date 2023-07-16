from os import system, listdir, path 
from datetime import datetime as dt


def quit(c=0, forced=False):
    '''
    this function exits the program but before quitting 
    it perform the checks on the files whether they are
    close or not. when the forced flag is true then all 
    then the program quits without performing the checks
    '''
    if forced:
        for file in fileBuffers:
            if file.closed is False:
                file.close()
        exit(c)

    for file in fileBuffers:
        if file.closed is False:
            return -1
            
    exit(c)


programDir = '/usr/share/file-alter'
backupDir = f'{programDir}/backups'

if path.isdir(programDir) is False:
    system(f'mkdir {programDir}')


fileBuffers = [] # whenever a new file is opened, it's to be put in this list

# the settings will contain all the config
# of how a file is to be altered 
# right now, there are these types of alter
# - toggle: takes a tuple with only 2 tokens,
#           replaces the first token with other token
settings = {
    'neovim dark mode toggle': {
        'description'   :   'changes the colorscheme in config file of nvim',
        'mode'          :   'toggle',
        'tokens'        :   ( ( 'kanagawa-dragon', 'kanagawa-lotus' ), ),
        'filePath'      :   '/home/lupiv/.config/nvim/lua/lupiv/init.lua',
        'trigger'       :   ('7:00:00 < [time] < 19:00:00',),
        'enable'        :   False
    } ,
    'neovim light mode toggle': {
        'description'   :   'changes the colorscheme in config file of nvim',
        'mode'          :   'toggle',
        'tokens'        :   ( ( 'kanagawa-lotus', 'kanagawa-dragon' ), ),
        'filePath'      :   '/home/lupiv/.config/nvim/lua/lupiv/init.lua',
        'trigger'       :   ('19:00:00 < [time] < 7:00:00',),
        'enable'        :   True
    } ,
    'test': {
        'description'   :   'test',
        'mode'          :   'toggle',
        'tokens'        :   ( ( 'hello', 'hi'), ),
        'filePath'      :   '/home/lupiv/test.txt',
        'trigger'       :   ('2:00:00 < [time] < 19:00:00',),
        'enable'        :   True 
    } 
}


def backup(fc, fn):
    ''' saves the string passed in the backup folder '''  

    if path.isdir(backupDir) is False:
        system(f'mkdir {backupDir}')

    if path.isfile(f'{backupDir}/{fn}') is False:
        file = open(f'{backupDir}/{fn}', 'x')

    file = open(f'{backupDir}/{fn}', 'a')
    fileBuffers.append(file)
    file.write(fc)
    file.close()
    

def checkTrigger(trigger):
    # time based trigger
    trigger.strip()

    if '[time]' in trigger:
        cTime = dt.now()

        if '<' in trigger:
            timesOfTrigger = trigger.split('<')

            if len(timesOfTrigger) == 3:
                lTimeStr, rTimeStr = timesOfTrigger[::2]
                lTimeStr = lTimeStr.lstrip().rstrip().split(':')
                rTimeStr = rTimeStr.lstrip().rstrip().split(':')
                
                lTime = cTime.replace(
                        hour=int(lTimeStr[0]),
                        minute=int(lTimeStr[1]),
                        second=int(lTimeStr[2]),
                    )
                rTime = cTime.replace(
                        hour=int(rTimeStr[0]),
                        minute=int(rTimeStr[1]),
                        second=int(rTimeStr[2]),
                    )

                return lTime < cTime and cTime < rTime \
                        if rTime > lTime else \
                        lTime < cTime or cTime < rTime

            elif len(timesOfTrigger) == 2:
                lTime = timesOfTrigger[0] \
                        if '[time]' == timesOfTrigger[1] \
                        else cTime.replace( hour=0, minute=0, second=0 )

                rTime = timesOfTrigger[1] \
                        if '[time]' == timesOfTrigger[0] \
                        else cTime.replace( hour=0, minute=0, second=0 )

                return lTime < cTime and cTime < rTime

        elif '=' in trigger:
            time = trigger.split('=')[1]
            return time == cTime

        else:
            return -1

    return False


def main():
    for key in settings.keys():
        setting = settings[key]

        if setting['enable'] is False:
            continue
        
        breakpoint()
        triggered = list(map(checkTrigger, setting['trigger']))
        
        if -1 in triggered:
            print(f"ERROR: invalid trigger of {key}")

        if False in triggered:
            continue
        
        file = open(setting['filePath'], 'r')
        fc = file.read() # file content
        file.close()
        
        print(f'setting: {key}')

        if 'toggle' == setting['mode']:
            # backing up the content for future 
            fileName =  file.name.split('/')[-1] \
                        if '/' in file.name \
                        else file.name.split('\\')[-1]
            backup(fc, fileName)

            # toggling the tokens
            tts = setting['tokens']
            for tt in tts:
                fc = fc.replace(*tt)

            # writing back
            file = open(setting['filePath'], 'w')
            file.write(fc)
            file.close()


if __name__ == '__main__':
    print('File Alter')
    main()
    quit()

