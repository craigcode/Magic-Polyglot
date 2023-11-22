import os
import subprocess
from dotenv import load_dotenv


load_dotenv()

mgrqcmdl_path = os.environ.get('MG_RQ_CMDL_PATH')

parse_start = 'Result :\n========\n'
parse_end = 'Reqid' 


def extract_text(text):
    
    start = text.find(parse_start)
    end = text.rfind(parse_end)

    if start > -1:
        return text[start+len(parse_start):end]
    else:
        return text.replace('\n','')


def call_magic(appname, prgname, args='', vars=''):

    argslist = ''
    if args != '':
        argslist = f'-ARGUMENTS={args}'

    # Mgrqcmdl usage:
    #-ARGUMENTS=string value,-N1000,-LTRUE,-Bc:\temp.txt,-U
    #-VARIABLES=var 1=string value,var 2=-N1000,var 3=-LTRUE

    result = subprocess.run([mgrqcmdl_path, 
    f'-APPNAME={appname}', 
    f'-PRGNAME={prgname}',
    argslist],
    capture_output=True, text=True)    

    mgresult = result.stdout

    mgtext = extract_text(mgresult)
    
    if mgtext:
        return mgtext
    else:
        return 'Error: Nothing returned by Requester'