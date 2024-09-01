# Cookies and headers to access the Tiki API
from dotenv import load_dotenv
import os

load_dotenv()

cookies = {
    'TIKI_ACCESS_TOKEN' : os.getenv('TIKI_ACCESS_TOKEN'),
    'TOKENS' : os.getenv('TOKENS'),
    # replace all
    '__adm_upl' : os.getenv('__adm_upl'),
    'amp_99d374' : os.getenv('amp_99d374'),
    '_gcl_au' : os.getenv('_gcl_au'),
    'tiki_client_id' : os.getenv('tiki_client_id'),
    '__iid' : os.getenv('__iid'),
    '__uidac' : os.getenv('__uidac'),
    '__utm' : os.getenv('__utm'),
    '__uif' : os.getenv('__uif'),
    '_fbp' : os.getenv('_fbp'),
    '_ga_S9GLR1RQFJ' : os.getenv('_ga_S9GLR1RQFJ'),
    '_gcl_aw' : os.getenv('_gcl_aw'),
    '_gcl_gs' : os.getenv('_gcl_gs'),
    '_trackity' : os.getenv('_trackity'),
    '_tuid' : os.getenv('_tuid'),
}

headers = {
    'User-Agent' : os.getenv('User-Agent'),
    'Accept' : os.getenv('Accept'),
    'Accept-Language' : os.getenv('Accept-Language'),
    'Referer' : os.getenv('Referer'),
    'x-guest-token' : os.getenv('x-guest-token'),
    'Connection' : os.getenv('Connection'),
    'TE' : os.getenv('TE'),
}