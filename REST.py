from WSSEGen import GetHeader
import os
import pycurl
import json
import sys


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


def Request(req_type, header, url, data, res_path):
    with open(res_path, 'wb') as outfile:
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.HTTPHEADER, header)
        curl.setopt(pycurl.WRITEDATA, outfile)

        curl.setopt(pycurl.CUSTOMREQUEST, req_type)
        curl.setopt(pycurl.VERBOSE, 1)

        if req_type == 'PUT':
            if data == '':
                raise Exception('Data is None')
            curl.setopt(pycurl.POSTFIELDS, data)

        curl.perform()

        code = curl.getinfo(pycurl.RESPONSE_CODE)

        curl.close()

    return (code)


def GetData(data_path):
    with open(data_path, 'r', encoding='utf-8') as outfile:
        json_data = json.loads(outfile.read())
        outfile.close()

    return json.dumps(json_data)


if __name__ == '__main__':
    if len(sys.argv) < 9:
        print('USE:\t\n'
              '\tpython REST.py\t\n'
              '\t\t-r - GET/PUT.\t\n'
              '\t\t-u - username.\t\n'
              '\t\t-p - password hash.\t\n'
              '\t\t-a - URI.\t\n'
              '\t\t-d - file Json format. Only for PUT.\t\n'
              '\t\t-r - results file. Optional, '
              'default: <USERPROFILE>/Documents/Result.txt')
        sys.exit()
    else:
        data = ''
        i = 1
        while i < len(sys.argv):
            if sys.argv[i] == '-u':
                i += 1
                user = sys.argv[i]
            elif sys.argv[i] == '-p':
                i += 1
                password = sys.argv[i]
            elif sys.argv[i] == '-t':
                i += 1
                req_type = sys.argv[i]
            elif sys.argv[i] == '-a':
                i += 1
                uri = sys.argv[i]
            elif sys.argv[i] == '-d':
                i += 1
                data = GetData(sys.argv[i])
            elif sys.argv[i] == '-r':
                i += 1
                res_path = sys.argv[i]
            i += 1

    if res_path is None:
        res_path = os.path.expanduser(
            os.getenv('USERPROFILE')) + '\\Documents\\Result.txt'

    result = Request(req_type, Header(user, password), uri, data, res_path)

    if os.path.exists(res_path):
        os.startfile(res_path)

    print(result)
