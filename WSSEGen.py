import base64
import hashlib
import datetime
import random
import sys


def GetNonce():
    nonceChars = '0123456789abcdef'
    random.seed()

    result = ''
    for i in nonceChars:
        result += nonceChars[random.randint(0, len(nonceChars) - 1)]

    return result


def GetHeader(User, Pass):
    created = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    nonce = GetNonce()
    nonce64 = _toBase64(_toBytes(nonce))

    passwordDigest = GetPass(nonce, created, Pass)

    return (User, passwordDigest, nonce64, created)


def GetPass(*args):
    args_str = ''.join(args)
    return _toBase64(hashlib.sha1(_toBytes(args_str)).digest())


def _toBase64(s):
    return _fromBytes(base64.b64encode(s))


def _toBytes(s):
    if not isinstance(s, bytes):
        return bytes(s, 'utf-8')
    return s


def _fromBytes(s):
    if not isinstance(s, str):
        return str(s, 'utf-8')
    return s


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Use:\n\tpython WSSEGen.py -u <USER> -p <PASSWORD>')
    else:
        i = 1
        while i < len(sys.argv):
            if sys.argv[i] == '-u':
                i += 1
                User = sys.argv[i]
            elif sys.argv[i] == '-p':
                i += 1
                Pass = sys.argv[i]
            i += 1

        head = GetHeader(User, Pass)
        print(
            'UsernameToken Username="{}" '
            'PasswordDigest="{}" '
            'Nonce="{}" '
            'Created="{}"'.format(head[0], head[1], head[2], head[3])
        )
