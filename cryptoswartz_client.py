import sys
from PyQt4 import QtGui, QtCore
from random import randint
import root
from root import *
data = []
for i in xrange(100):
	data.append([randint(1,200000)])
        data[i].append([])
	for j in xrange(20):
		data[i][1].append([randint(1,200000), randint(1,20), randint(1,20)])

Currency = 1000
Rep = 10.0

BIG = 100000000000000
Currency = int(genesis.get_balance(usrs[0][1]))/BIG

content = get_all_content(genesis, root_contract, usrs[0])
f = lambda x: get_content_title(x, data_contract, genesis)
titles = map(f, content)
print titles


D = [[t, c] for t, c in zip(titles, content)]
print D

for i in xrange(len(D)):
    t = get_tags(D[i][1], tag_contract, genesis)
    D[i].append(t)


'''
print Currency
s = genesis.to_dict()['state']
for k in s.keys():
    print s[k][2].encode('hex')

print get_name(usrs[0][1], users_contract, genesis)
'''

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)
        self.initUI()
    def initUI(self):
        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit',self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        QtGui.QToolTip.setFont(QtGui.QFont('SansSetif',12))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.statusBar().showMessage('Connected to ethereum')

        self.resize(1200, 300) 
        self.move(100,200)
        self.setWindowTitle('CryptoSwartz')
        self.show()


class FormWidget(QtGui.QWidget):
    tags = False
    def __init__(self,parent):
        super(FormWidget, self).__init__(parent)
        self.initUI()
    def initUI(self):
        titleEdit = QtGui.QLineEdit()
        titleEdit.setText('Title your publication')
        self.tagEdit = QtGui.QLineEdit()
        self.tagEdit.setText('Tag a publication')
        fileBtn = QtGui.QPushButton('Browse', self)
        pubBtn = QtGui.QPushButton('Publish', self)
        tagBtn = QtGui.QPushButton('Tag', self)
        upvoteBtn = QtGui.QPushButton('upvote', self)
        downvoteBtn = QtGui.QPushButton('Downvote', self)
        publishtag = QtGui.QLabel('Cryptoswartz publications:')		
        tagtag = QtGui.QLabel('Available tags:')
        netvotetag = QtGui.QLabel('Net votes:')
        upvotetag = QtGui.QLabel('Upvotes:')
        downvotetag = QtGui.QLabel('Downvotes:')
        currencytag = QtGui.QLabel('Total Swartzcoin:')
        reptag = QtGui.QLabel('Total reputation:')
        addresstag = QtGui.QLabel('Receipient address:')
        cointag = QtGui.QLabel('Send amount:')
        self.coinamountEdit = QtGui.QLineEdit()
        self.sendaddressEdit = QtGui.QLineEdit()
        sendBtn = QtGui.QPushButton('Send')


        self.publist = QtGui.QListWidget(self)
        self.taglist = QtGui.QListWidget(self)		

        self.upvotes = QtGui.QLCDNumber(self)
        self.downvotes = QtGui.QLCDNumber(self)
        self.netvotes = QtGui.QLCDNumber(self)
        self.currency = QtGui.QLCDNumber(self)
        self.rep = QtGui.QLCDNumber(self)

        grid = QtGui.QGridLayout()
        grid.addWidget(publishtag, 0, 0)
        grid.addWidget(tagtag,0,4)
        grid.addWidget(titleEdit, 4, 0)
        grid.addWidget(fileBtn,4,2)
        grid.addWidget(pubBtn,4,3)
        grid.addWidget(self.tagEdit,4,4)
        grid.addWidget(tagBtn,4,8)
        grid.addWidget(self.publist, 1, 0, 3, 4)
        grid.addWidget(self.taglist, 1, 4, 3, 6)
        grid.addWidget(self.upvotes, 3, 11)
        grid.addWidget(self.downvotes,3,12)
        grid.addWidget(self.netvotes,1,10,1,11)
        grid.addWidget(upvoteBtn, 4, 11)
        grid.addWidget(downvoteBtn, 4 ,12)
        grid.addWidget(netvotetag, 0, 11)
        grid.addWidget(upvotetag, 2,11)
        grid.addWidget(downvotetag,2,12)
        grid.addWidget(currencytag, 5, 0)
        grid.addWidget(reptag, 5, 8)
        grid.addWidget(self.rep,5,9,6,10)
        grid.addWidget(self.currency,6,0,7,2)
        grid.addWidget(addresstag, 8, 2)
        grid.addWidget(cointag, 9, 2)
        grid.addWidget(self.coinamountEdit,9,3)
        grid.addWidget(self.sendaddressEdit,8,3)
        grid.addWidget(sendBtn,10,3)

        for i in D:
            self.publist.addItem(i[0])

        self.publist.setCurrentRow(0)			
        self.showTags()
        self.taglist.setCurrentRow(0)
        self.showVotes()
        self.rep.display(Rep)
        self.currency.display(Currency) 	

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Choose a file to publish')
        openFile.triggered.connect(self.showDialog)
		
        self.publist.currentItemChanged.connect(self.showTags)
        self.taglist.currentItemChanged.connect(self.showVotes)

        tagBtn.clicked.connect(self.issueTag)
        fileBtn.clicked.connect(self.showDialog)          	
        pubBtn.clicked.connect(self.pubButton)
        upvoteBtn.clicked.connect(self.upvoteButton)
        downvoteBtn.clicked.connect(self.downvoteButton)
        sendBtn.clicked.connect(self.attemptSend)

        self.setLayout(grid)

        #self.tagSinal.connect(parent.publish)

    def attemptSend(self):
        #if(self.currency.value() < float(self.coinamountEdit.text())):
        #    print "Attempted to send more than your balance"
        #elif float(self.coinamountEdit.text()) < 0:
        #    print "Negative transaction balances are invalid" 
        if 0: pass
        else:
            to_send = self.coinamountEdit.text()
            to_send = int(to_send)
            send_money(usrs[1][1], to_send*BIG, genesis, root_contract, usrs[0])
            current = self.currency.value()
            current = current - to_send
            self.currency.display(current) #genesis.get_balance(usrs[0][1])/BIG)             

    def showVotes(self):
		index1 = self.publist.currentRow()
		index2 = self.taglist.currentRow()
		self.upvotes.display(data[index1][1][index2][1])
		self.downvotes.display(data[index1][1][index2][2])
		self.netvotes.display(data[index1][1][index2][1] - data[index1][1][index2][2])
    def upvoteButton(self):
        index1 = self.publist.currentRow()
        index2 = self.taglist.currentRow()
        data[index1][1][index2][1] += 1
        self.showVotes()
    def downvoteButton(self):
        index1 = self.publist.currentRow()
        index2 = self.taglist.currentRow()
        data[index1][1][index2][2] += 1
        self.showVotes()
    def issueTag(self):
        self.taglist.addItem(self.tagEdit.text())
        self.tagEdit.clear()		
    def showTags(self):
		self.taglist.clear()
		index = self.publist.currentRow()
		for j in xrange(len(D[index][2])):
		    self.taglist.addItem(D[index][2][j])                
		self.taglist.setCurrentRow(0)
    def showDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        self.sender().parent().parent().statusBar().showMessage('Staging file: ' + fname)
    def pubButton(self):
        sender = self.sender()
        sender.parent().parent().statusBar().showMessage(sender.text() + ' process pending')


def main():
	app = QtGui.QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
