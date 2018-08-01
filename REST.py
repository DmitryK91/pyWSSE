from WSSEGen import GetHeader
import os
import pycurl
import json
import sys


res_path = os.path.expanduser(
    os.getenv('USERPROFILE')) + '\\Documents\\Result.txt'
data_path = os.path.expanduser(
    os.getenv('USERPROFILE')) + '\\Documents\\Data.json'


def Header(User, Pass):
    h = GetHeader(User, Pass)
    wsse = ('UsernameToken Username="{}" PasswordDigest="{}" Nonce="{}" '
            'Created="{}"'.format(h[0], h[1], h[2], h[3]))

    return [
        'Accept: application/json; charset=utf-8',
        'Authorization: Authorization profile="UsernameToken"',
        'X-WSSE: ' + wsse,
        'PasswordDigest: ' + h[1],
        'Nonce: ' + h[2],
        'Created: ' + h[3],
    ]


def Request(req_type, header, url):
    with open(res_path, 'wb') as outfile:
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.HTTPHEADER, header)
        curl.setopt(pycurl.WRITEDATA, outfile)

        curl.setopt(pycurl.CUSTOMREQUEST, req_type)

        if req_type == 'PUT':
            curl.setopt(pycurl.POSTFIELDS, GetData())

        curl.setopt(pycurl.VERBOSE, 1)

        curl.perform()

        code = curl.getinfo(pycurl.RESPONSE_CODE)

        curl.close()

    return (code)


def GetData():
    with open(data_path, 'r', encoding='utf-8') as outfile:
        json_data = json.loads(outfile.read())
        outfile.close()

    return json.dumps(json_data)


if __name__ == '__main__':
    if len(sys.argv) < 9:
        print('Use:\n\t'
              'python REST.py -r <GET/PUT> -u <USER> -p <PASSWORD> -a <URI>')
        sys.exit()
    else:
        i = 1
        while i < len(sys.argv):
            if sys.argv[i] == '-u':
                i += 1
                user = sys.argv[i]
            elif sys.argv[i] == '-p':
                i += 1
                password = sys.argv[i]
            elif sys.argv[i] == '-r':
                i += 1
                req_type = sys.argv[i]
            elif sys.argv[i] == '-a':
                i += 1
                uri = sys.argv[i]
            i += 1

    result = Request(req_type, Header(user, password), uri)

    if os.path.exists(res_path):
        os.startfile(res_path)

    print(result)
