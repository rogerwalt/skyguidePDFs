from os import walk
import re

class MakeTEX:
    def __init__(self):
        self.texfiles = {}

    def writeTexHeader(self,icaocode):
        print 'writing header for',icaocode
        ftex = open(icaocode+'.tex', 'w+')
        str =  "\documentclass{article}\n\usepackage{pdfpages}\n\usepackage[bookmarks=true]{hyperref}\n\\begin{document}\n"
        ftex.write(str)
        ftex.close()

    def writeTexFooter(self,icaocode):
        ftex = open(icaocode+'.tex', 'a')
        str =  "\end{document}"
        ftex.write(str)
        ftex.close()

    def addPdfToTex(self, f):
        # find ICAO code in filename
        m = re.search('L[SF][A-Z]{2}', f)
        if m:
            icaocode = m.group()
            # check if tex header already written, if not do it
            if icaocode not in self.texfiles:
                self.texfiles[icaocode] = 1
                self.writeTexHeader(icaocode)

            # find out type of document (VAC/AREA/ADINFO) and mode (APP/DEP)
            desc = ''
            adinfo = False
            mhel = re.search('HEL', f)
            if mhel:
                desc = 'HEL '

            mfull = re.search('Full', f)
            if mfull:
                desc += 'ADINFO '
                adinfo = True

            mvac = re.search('VAC', f)
            if mvac:
                desc += 'VAC '

            marea = re.search('AREA', f)
            if marea:
                desc += 'AREA '

            mdep = re.search('_D.pdf', f)
            if mdep:
                desc += 'DEP'

            marr = re.search('_A.pdf', f)
            if marr:
                desc += 'ARR'

            desc = desc.strip()

            ftex = open(icaocode+'.tex', 'a')
            if adinfo:
                ftex.write('\includepdf[pages=-,addtotoc={1,section,1,'+desc+',p'+str(self.texfiles[icaocode])+'}]{'+f+'}\n')
            else:
                ftex.write('\includepdf[landscape,addtotoc={1,section,1,'+desc+',p'+str(self.texfiles[icaocode])+'}]{'+f+'}\n')

            ftex.close()
            self.texfiles[icaocode] += 1
        else:
            print 'didnt match for',f

    def do(self):
        # fetch useful pdfs
        files = []
        for (dirpath, dirnames, filenames) in walk('../Chart'):
            files.extend(['../Chart/'+f for f in filenames])

        for (dirpath, dirnames, filenames) in walk('../Full'):
            files.extend(['../Full/'+f for f in filenames])

        # go trough the files
        for f in files:
            self.addPdfToTex(f)

        # write tex footers
        for x in self.texfiles:
            self.writeTexFooter(x)

m = MakeTEX()
m.do()