
import base64
import json
from urllib import parse
import zlib


def decode_lrc_content(lrc, is_lrcx=False):
    '''
    lrc currently is bytes.
    '''
    if len(lrc) < 80:
        return None
    index = lrc.index(b'\r\n\r\n')
    lrc_bytes = lrc[index+4:]
    str_lrc = zlib.decompress(lrc_bytes)
    if is_lrcx is False:
        return str_lrc.decode('gb18030')
    str_bytes = base64.decodebytes(str_lrc)
    return xor_bytes(str_bytes).decode('gb18030')

def xor_bytes(str_bytes, key='yeelion'):
    #key = 'yeelion'
    xor_bytes = key.encode('utf8')
    str_len = len(str_bytes)
    xor_len = len(xor_bytes)
    output = bytearray(str_len)
    i = 0
    while i < str_len:
        j = 0
        while j < xor_len and i < str_len:
            output[i] = str_bytes[i] ^ xor_bytes[j]
            i += 1
            j += 1
    return output

def decode_music_file(filename):
    with open(filename, 'rb') as fh:
        byte_str = fh.read()
    #output = zlib.decompress(byte_str)
    output = xor_bytes(byte_str)
    print(output)
    print(output.decode())
    result = output.decode('gb2312')
    print(result)

def encode_lrc_url(rid):
    '''
    rid is like '928003'
    like this: 
    will get:
    DBYAHlRcXUlcUVRYXUI0MDYlKjBYV1dLXUdbQhIQEgNbX19LSwAUDEMlDigQHwAMSAsAFBkMHBocF1gABgwPFQ0KHx1JHBwUWF1PHAEXAgsNBApTtMqhhk8OHA0MFhhUrbDNlra/Tx0HHVgoOTomLSZXVltRWF1fCRcPEVJf
    '''
    param = 'user=12345,web,web,web&requester=localhost&req=1&rid=MUSIC_' + rid
    str_bytes = xor_bytes(param.encode())
    output = base64.encodebytes(str_bytes).decode()
    return output.replace('\n', '')

def decode_lrc_url(url):
    str_bytes = base64.decodebytes(url.encode())
    output = xor_bytes(str_bytes)
    #print(output.decode('gb2312'))
    return output.decode('gb2312')

def json_loads_single(_str):
    '''
    Actually this is not a good idea.
    '''
    return json.loads(_str.replace('"', '''\\"''').replace("'", '"'))

def encode_uri(text):
    return parse.quote(text, safe='~@#$&()*!+=:;,.?/\'')

def parse_radio_songs(txt):
    if len(txt) == 0:
        return None
    lines = txt.splitlines()
    if len(lines) == 0 or lines[0] != 'success':
        return None
    songs = []
    for line in lines[2:]:
        info = line.split('\t')
        songs.append({
            'rid': info[0],
            'artist': info[1],
            'name': info[2],
            'artistid': 0,
            'album': '',
            'albumid': 0,
            })
    return songs
