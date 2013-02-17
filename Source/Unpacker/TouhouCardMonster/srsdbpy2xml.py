import os, sys, struct, traceback
from ctypes import windll

if len(sys.argv) < 2:
    sys.exit(0)

class Srsdatabase:
    def __init__(self, filename):
        self.msg = []
        self.name = []
        self.filename = filename

        self.syscmd = ['STOP', 'COMMAND']

    def AppendImageBlock(self, blockname, blockvalue):
        pass

    def AppendTextBlock(self, blockname, valuelist):
        if blockname == 'msg':
            self.msg = valuelist
        elif blockname == 'name':
            self.name = valuelist

    def AppendCommentBlock(self, blockname, blockvalue):
        pass

    def Flush(self):
        if len(self.msg) == 0:
            return

        filename = os.path.splitext(self.filename)[0]
        filename = os.path.splitext(filename)[0] + '.xml'

        xml = []
        xml.append('<?xml version="1.0" encoding="utf-8"?>')
        xml.append('<srsdb>')

        for i in range(len(self.msg)):
            if len(self.msg[i]) == 0 or self.msg[i] in self.syscmd:
                continue

            xml.append('    <Text Index = "%d" Type = "Name">' % i)
            xml.append('        <jp><![CDATA[%s]]></jp>' % self.name[i])
            xml.append('        <sc><![CDATA[%s]]></sc>' % self.name[i])
            xml.append('    </Text>')

            xml.append('    <Text Index = "%d" Type = "Message">' % i)
            xml.append('        <jp><![CDATA[%s]]></jp>' % self.msg[i])
            xml.append('        <sc><![CDATA[%s]]></sc>' % self.msg[i])
            xml.append('    </Text>')

        xml.append('</srsdb>')

        fp = os.path.dirname(os.path.abspath(__file__)) + '\\' + filename
        open(fp, 'wb').write('\r\n'.join(xml).encode('UTF8'))

def CreateSrsdatabase(filename):
    return Srsdatabase(filename)

def PeekTextFromSrsdbPy(pyfile):
    selfmodule = os.path.basename(os.path.splitext(sys.argv[0])[0])
    py = open(pyfile, 'rb').read().decode('UTF8').replace('from py2srsdb import *', 'from %s import *' % selfmodule)
    py = compile(py, '', 'exec')
    exec(py)

if __name__ == '__main__':
    i = 1
    n = len(sys.argv) - 1
    while i <= n:
        try:
            windll.kernel32.SetConsoleTitleW(sys.argv[i])
            msg = PeekTextFromSrsdbPy(sys.argv[i])
            msg = msg if msg else 'done'
            print('%s: %s' % (sys.argv[i], msg))
        except Exception as e:
            print(sys.argv[i] + ': ' + str(e))
            traceback.print_exception(type(e), e, e.__traceback__)
            input()

        i = i + 1
