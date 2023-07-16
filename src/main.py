from os import system, listdir, path 


def quit(c, forced):
    '''
    this function exits the program but before quitting 
    it perform the checks on the files whether they are
    close or not. when the forced flag is true then all 
    then the program quits without performing the checks
    '''
    if forced:
        exit(c)

    for file in fileBuffers:
        if file.closed is False:
            return -1
            
    exit(c)


programDir = '/usr/share/file-alter'
backupDir = f'{programDir}/backups'

if path.isdir(programDir) is False:
    print(f'FATAL: Can\'t find the main program dir {programDir}.')
    quit(0, fileBuffers)


fileBuffers = [] # whenever a new file is opened

# the settings will contain all the config
# of how a file is to be altered 
# right now, there are these types of alter
# - toggle: takes a tuple with only 2 tokens,
#           replaces the first token with other token
settings = {
    'neovim dark mode toggle': {
        'description'   :   'changes the colorscheme in config file of nvim',
        'mode'          :   'toggle',
        'tokens'        :   ( 'kanagawa-dragon', 'kanagawa-lotus' ),
        'fileID'        :   '0',
        'trigger'       :   '19',
        'enable'        :   false
    } ,

    'test': {
        'description'   :   'test',
        'mode'          :   'toggle',
        'tokens'        :   ( 'hello mom', 'hi mom' ),
        'fileID'        :   '1',
        'trigger'       :   '6:00:00 > {time} > 19:00:00',
        'enable'        :   true
    } 
}

filesToAlter = [
    '/home/lupiv/.config/nvim/lua/lupiv/init.lua',
    '/home/lupiv/test.txt',
]

def backup(fp, fn):
    ''' saves the file in the backup folder '''  

    if path.isdir('.file_Alter_Backups') is False:
        system('mkdir .file_Alter_backups')

    file = open(f'{backupDir}/{fn}', 'w+')
    fileBuffers.append(file)
    file.write(fp.read())
    file.close()
    fp.close()
    

def main():
    for key in settings.keys():
        setting = settings[key]

        if setting['enable'] is False:
            continue
        
        print(f'setting: {setting}')

        if 'toggle' in setting.keys():
            file = fileBuffers[setting['fileID']]
            fc = file.read() # file content

            # backing up the content for future 
            fileName =  file.name.split['/'][-1] \
                        if '/' in file.name \
                        else file.name.split['\\'][-1]
            backup(file, fileName)

            # toggling the tokens
            tts = setting['tokens']
            for tt in tts:
                fc.replace(tt[0], tt[1])

            # writing back
            file.seek(0)
            file.write(fc)
            file.close()


if __name__ == '__main__':
    print('File Alter')
    main()

