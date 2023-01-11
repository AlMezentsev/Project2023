import random
import sys
#import PySimpleGUI as sg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton,QLabel
from PyQt5.QtWidgets import *

import math


alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?;: "
nAlphabet=len(alphabet)


def generatePrime(self):
    primes = []
    for target_num in range(3, 500):
        is_prime = True
        for i in range(2, target_num):
            if target_num % i == 0:
                is_prime = False
        if is_prime:
            primes.append(target_num)
    random_index = random.randint(0, len(primes) - 1)
    prime = primes[random_index]
    return prime


def isPrime(self, n):
    d = 2
    while d * d <= n and n % d != 0:
        d += 1
    return d * d > n


def generateModule(self):
    p = self.generatePrime()
    q = self.generatePrime()
    while (self.isPrime(p) == False and self.isPrime(q) == False):
        p = self.generatePrime()
        q = self.generatePrime()
    n = p * q
    return [n, p, q]


# функция Эйлера
def generateFi(self, p, q):
    return (p - 1) * (q - 1)


# алгоритм Эвклида для поиска НОД
def NOD(self, a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return (a + b)

#генерация закрытого ключа D
def generatePrivateKey(e,n,fi):
    d_list=[]
    for d in range(1, n):
        if (((e * d)%fi==1) and d!=e):
            d_list.append(d)
    print(len(d_list))
    random_index = random.randint(0, len(d_list) - 1)
    d = d_list[random_index]
    return d
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)


# x = mulinv(b) mod n, (x * b) % n == 1
def generatePrivacyKey(b, n):
    g, x, _ = egcd(b, n)
    #print(g, x, _)
    if g == 1:
        return x % n

#шифрование текста
def encode(text,n):
    encodeString=[]
    for i in text:
        code=alphabet.find(i)+1
        encodeString.append(code)
    return encodeString

#подпись закрытым ключом
def signatureByPrivacyKey(text,d,n):
    c=[]
    for i in range(0,len(text)):
        ci=pow(text[i],d)%n
        c.append(ci)
    return c

#подпись открытым ключом
def encodeByPublicKey(c,e,n):
    g=[]
    for i in range(len(c)):
        gi=pow(c[i],e)%n
        g.append(gi)
    return g

#проверка подлинности подписи
def checkSignature(g,d,n):
    c=[]
    for i in range(len(g)):
        ci=pow(g[i],d)%n
        c.append(ci)
    return c

#восстановление исходного текста
def decodeText(c,e,n):
    m=[]
    for i in range(len(c)):
        mi=pow(c[i],e)%n
        m.append(mi)
    return m
#декодирование восстановленного текста
def decoder(text, n):

    finalString=[]
    for i in range(0,len(text)):
        newSimbol=alphabet[text[i]-1]
        finalString.append(newSimbol)
    str=''.join(finalString)
    return str


#тест ферма
def testFerma(n):
    a = random.randint(20, 100)

    while(a>n):
        a = random.randint(20, 100)
    isPrime=False
    print(a)
    for i in range(int(a/2)):
        if (pow(a,n-1)%n==1):
            isPrime=True
            break

    return isPrime

class Sender(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.initUI()

        global nSenders
        nSenders, self.pSender, self.qSender = self.generateModule()

        fiSender = self.generateFi(self.pSender, self.qSender)
        global eSender
        eSender = self.generatePublicKey(fiSender)


        print("Отправитель: p= ", self.pSender, " q= ", self.qSender, " n=", nSenders, " фи= ", fiSender)
        print("Открытый ключ отправителя:")
        print("(", eSender, ";", nSenders, ")")
        self.dSender = generatePrivacyKey(eSender, fiSender)
        print("Закрытый ключ отправителя:")
        print("(", self.dSender, ";", nSenders, ")")

        labelPublicKeySenderText = QLabel("Открытый ключ отправителя:", self)
        labelPublicKeySenderText.move(20, 30)
        labelPublicKeySenderText.show()

        labelNSender=QLabel("N отправителя:",self)
        labelNSender.move(20,60)
        labelNSender.show()


        btnGenerateKeys = QPushButton("Сгенерировать ключи", self)
        btnGenerateKeys.move(20, 140)
        btnGenerateKeys.show()
        btnGenerateKeys.clicked.connect(lambda:self.buttonGenerateKeysClicked(eSender,nSenders))

        btnExchange = QPushButton("Обменяться ключами", self)
        btnExchange.move(165, 140)
        btnExchange.show()
        btnExchange.clicked.connect(self.buttonExchangeClicked)

        btnCrypt = QPushButton("Подписать и зашифровать текст", self)
        btnCrypt.move(305, 140)
        btnCrypt.show()
        btnCrypt.clicked.connect(self.buttonCryptClicked)

        btnSend = QPushButton("Отправить", self)
        btnSend.move(510, 140)

        self.textLineEdit = QLineEdit( self, placeholderText='Введите текст')
        self.textLineEdit.setAlignment(Qt.AlignTop)
        self.textLineEdit.move(30, 200)
        self.textLineEdit.resize(500, 300)
        self.textLineEdit.show()



    def generatePrime(self):
        primes = []
        for target_num in range(3, 500):
            is_prime = True
            for i in range(2, target_num):
                if target_num % i == 0:
                    is_prime = False
            if is_prime:
                primes.append(target_num)
        random_index = random.randint(0, len(primes) - 1)
        prime = primes[random_index]
        return prime

    def isPrime(self,n):
        d = 2
        while d * d <= n and n % d != 0:
            d += 1
        return d * d > n

    def generateModule(self):
        p = self.generatePrime()
        q = self.generatePrime()
        while (self.isPrime(p) == False and self.isPrime(q) == False):
            p = self.generatePrime()
            q = self.generatePrime()
        n = p * q
        return [n, p, q]

    # функция Эйлера
    def generateFi(self,p, q):
        return (p - 1) * (q - 1)

    # алгоритм Эвклида для поиска НОД
    def NOD(self,a, b):
        while a != 0 and b != 0:
            if a > b:
                a = a % b
            else:
                b = b % a
        return (a + b)

    # генерация откытрого ключа Е
    def generatePublicKey(self,fi):
        e_list = []
        for i in range(1, fi):
            if (self.NOD(i, fi) == 1 and self.isPrime( i) == True):
                e_list.append(i)
        random_index = random.randint(0, len(e_list) - 1)
        e = e_list[random_index]
        return e

    # генерация закрытого ключа D
    def generatePrivateKey(e, n, fi):
        d_list = []
        for d in range(1, n):
            if (((e * d) % fi == 1) and d != e):
                d_list.append(d)
        print(len(d_list))
        random_index = random.randint(0, len(d_list) - 1)
        d = d_list[random_index]
        return d

    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, x, y = egcd(b % a, a)
            return (g, y - (b // a) * x, x)

    # x = mulinv(b) mod n, (x * b) % n == 1
    def generatePrivacyKey(b, n):
        g, x, _ = egcd(b, n)
        # print(g, x, _)
        if g == 1:
            return x % n

    # шифрование текста
    def encode(text, n):
        encodeString = []
        for i in text:
            code = alphabet.find(i) + 1
            encodeString.append(code)
        finalEncodeString = []

        for i in range(1, len(encodeString)):
            newSimbol = (encodeString[i] + encodeString[i - 1]) % n
            finalEncodeString.append(newSimbol)
        finalEncodeString.insert(0, encodeString[0])
        return finalEncodeString

    # подпись закрытым ключом
    def signatureByPrivacyKey(text, d, n):
        c = []
        for i in range(0, len(text)):
            ci = pow(text[i], d) % n
            c.append(ci)
        return c

    # подпись открытым ключом
    def encodeByPublicKey(c, e, n):
        g = []
        for i in range(len(c)):
            gi = pow(c[i], e) % n
            g.append(gi)
        return g

    # проверка подлинности подписи
    def checkSignature(g, d, n):
        c = []
        for i in range(len(g)):
            ci = pow(g[i], d) % n
            c.append(ci)
        return c

    # восстановление исходного текста
    def decodeText(c, e, n):
        m = []
        for i in range(len(c)):
            mi = pow(c[i], e) % n
            m.append(mi)
        return m

    def initUI(self):
        labelPublicKeyReciverText=QLabel("Открытый ключ получателя:",self)
        labelPublicKeyReciverText.move(320, 30)
        labelPublicKeyReciverText.show()

        labelNReciver = QLabel("N получателя:", self)
        labelNReciver.move(320, 60)
        labelNReciver.show()


        self.setGeometry(200, 150, 610, 600)
        self.setWindowTitle('Отправитель')
        self.show()

    def buttonGenerateKeysClicked(self, eSender,nSender):

        if(testFerma(self.qSender)==True and testFerma(self.pSender)==True):
            msg = QMessageBox()
            msg.setWindowTitle("Проверка на простоту")
            msg.setText("Сгенерированы числа p="+str(self.pSender)+" и q=" +str(self.qSender)+". Являются простыми по тесту Ферма")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

        self.labelPublicKeySenderText = QLabel("Открытый ключ отправителя:",self)
        self.labelPublicKeySenderText.setText("Открытый ключ отправителя:"+str(eSender))
        self.labelPublicKeySenderText.move(20, 30)
        self.labelPublicKeySenderText.show()

        self.labelNSender = QLabel("N отправителя:", self)
        self.labelNSender.setText("N отправителя:" + str(nSender))
        self.labelNSender.move(20, 60)
        self.labelNSender.show()

    def buttonCryptClicked(self):

        inputText=self.textLineEdit.text()
        global encodeText
        encodeText=encode(inputText,nAlphabet)
        global textWithSignature
        textWithSignature=signatureByPrivacyKey(encodeText,self.dSender,nSenders)
        global encText
        encText=encodeByPublicKey(encodeText,eReciever,nReciever)
        self.textLineEdit.setText(str(encText))

    def buttonExchangeClicked(self):

        labelPublicKeyReciverText = QLabel("Открытый ключ получателя:", self)
        labelPublicKeyReciverText.move(320, 30)
        labelPublicKeyReciverText.setText("Открытый ключ получателя:"+ str(eReciever))
        labelPublicKeyReciverText.show()

        labelNReciver = QLabel("N получателя :", self)
        labelNReciver.setText("N получателя:"+ str(nReciever))
        labelNReciver.move(320, 60)
        labelNReciver.show()

class Reciver(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        global nReciever
        nReciever, self.pReciever, self.qReciever = self.generateModule()

        fiReciever = self.generateFi(self.pReciever, self.qReciever)
        global eReciever
        eReciever = self.generatePublicKey(fiReciever)
        print("Получатель: p= ", self.pReciever, " q= ", self.qReciever, " n=",nReciever, " фи= ", fiReciever)
        print("Открытый ключ получателя:")
        print("(",eReciever, ";", nReciever, ")")
        self.dReciever = generatePrivacyKey(eReciever, fiReciever)
        print("Закрытый ключ получателя:")
        print("(",self. dReciever, ";", nReciever, ")")

        labelPublicKeySenderText = QLabel("Открытый ключ получателя:", self)
        labelPublicKeySenderText.move(20, 30)
        labelPublicKeySenderText.show()

        labelNSender = QLabel("N получателя:",self)
        labelNSender.move(20, 60)
        labelNSender.show()

        btnGenerateKeys = QPushButton("Сгенерировать ключи", self)
        btnGenerateKeys.move(20, 140)
        btnGenerateKeys.show()
        btnGenerateKeys.clicked.connect(lambda: self.buttonGenerateKeysClicked(eReciever, nReciever))

        btnExchange = QPushButton("Обменяться ключами", self)
        btnExchange.move(165, 140)
        btnExchange.show()
        btnExchange.clicked.connect(self.buttonExchangeClicked)

        btnGetText = QPushButton("Получить текст", self)
        btnGetText.move(305, 140)
        btnGetText.show()
        btnGetText.clicked.connect(self.buttonGetTextClicked)

        self.textLineEdit = QLineEdit(self)
        self.textLineEdit.move(30, 200)
        self.textLineEdit.resize(500, 300)
        self.textLineEdit.setAlignment(Qt.AlignTop)
        self.textLineEdit.show()


    def initUI(self):
        labelPublicKeyReciverText = QLabel("Открытый ключ отправителя:", self)
        labelPublicKeyReciverText.move(320, 30)
        labelPublicKeyReciverText.show()

        labelNReciver = QLabel("N отправителя :", self)
        labelNReciver.move(320, 60)
        labelNReciver.show()

        self.setGeometry(1000, 150, 610, 600)
        self.setWindowTitle('Получатель')
        self.show()

    def buttonGetTextClicked(self):
        self.textLineEdit = QLineEdit(self)
        self.textLineEdit.move(30, 200)
        self.textLineEdit.resize(500, 300)
        self.textLineEdit.setText(str(encodeText))
        self.textLineEdit.show()

        self.check=checkSignature(textWithSignature,eSender,nSenders)
        self.textLineEdit.setText(str(self.check))


        if (str(encodeText)==str(self.check)):
            msg = QMessageBox()
            msg.setWindowTitle("Проверка подписи")
            msg.setText("Подпись верна")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

            self.decText=decodeText(encText,self.dReciever,nReciever)
            self.text  = decoder(self.decText,nAlphabet)
            self.textLineEdit.setText(str(self.text))
            self.textLineEdit.setAlignment(Qt.AlignTop)



    def buttonExchangeClicked(self):

        labelPublicKeyReciverText = QLabel("Открытый ключ отправителя:", self)
        labelPublicKeyReciverText.move(320, 30)
        labelPublicKeyReciverText.setText("Открытый ключ отправителя:"+ str(eSender))
        labelPublicKeyReciverText.show()

        labelNReciver = QLabel("N отправителя :", self)
        labelNReciver.setText("N отправителя :"+ str(nSenders))
        labelNReciver.move(320, 60)
        labelNReciver.show()

    def buttonGenerateKeysClicked(self, eReciever, nReciever):

        if (testFerma(self.qReciever) == True and testFerma(self.pReciever) == True):
            msg = QMessageBox()
            msg.setWindowTitle("Проверка на простоту")
            msg.setText("Сгенерированы числа p=" + str(self.pReciever) + " и q=" + str(self.qReciever) + ". Являются простыми по тесту Ферма")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

        self.labelPublicKeySenderText = QLabel("Открытый ключ получателя:", self)
        self.labelPublicKeySenderText.setText("Открытый ключ получателя:" + str(eReciever))
        self.labelPublicKeySenderText.move(20, 30)
        self.labelPublicKeySenderText.show()

        self.labelNSender = QLabel("N получателя:", self)
        self.labelNSender.setText("N получателя:" + str(nReciever))
        self.labelNSender.move(20, 60)
        self.labelNSender.show()

    def generatePrime(self):
        primes = []
        for target_num in range(3, 500):
            is_prime = True
            for i in range(2, target_num):
                if target_num % i == 0:
                    is_prime = False
            if is_prime:
                primes.append(target_num)
        random_index = random.randint(0, len(primes) - 1)
        prime = primes[random_index]
        return prime

    def isPrime(self, n):
        d = 2
        while d * d <= n and n % d != 0:
            d += 1
        return d * d > n

    def generateModule(self):
        p = self.generatePrime()
        q = self.generatePrime()
        while (self.isPrime(p) == False and self.isPrime(q) == False):
            p = self.generatePrime()
            q = self.generatePrime()
        n = p * q
        return [n, p, q]

        # функция Эйлера
    def generateFi(self, p, q):
        return (p - 1) * (q - 1)

        # алгоритм Эвклида для поиска НОД
    def NOD(self, a, b):
        while a != 0 and b != 0:
            if a > b:
                a = a % b
            else:
                b = b % a
        return (a + b)

        # генерация откытрого ключа Е
    def generatePublicKey(self, fi):
        e_list = []
        for i in range(1, fi):
            if (self.NOD(i, fi) == 1 and self.isPrime(i) == True):
                e_list.append(i)
        random_index = random.randint(0, len(e_list) - 1)
        e = e_list[random_index]
        return e

        # генерация закрытого ключа D
    def generatePrivateKey(e, n, fi):
        d_list = []
        for d in range(1, n):
            if (((e * d) % fi == 1) and d != e):
                d_list.append(d)
        print(len(d_list))
        random_index = random.randint(0, len(d_list) - 1)
        d = d_list[random_index]
        return d

    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, x, y = egcd(b % a, a)
            return (g, y - (b // a) * x, x)

        # x = mulinv(b) mod n, (x * b) % n == 1
    def generatePrivacyKey(b, n):
        g, x, _ = egcd(b, n)
            # print(g, x, _)
        if g == 1:
            return x % n

        # шифрование текста
    def encode(text, n):
        encodeString = []
        for i in text:
            code = alphabet.find(i) + 1
            encodeString.append(code)
        finalEncodeString = []

        for i in range(1, len(encodeString)):
            newSimbol = (encodeString[i] + encodeString[i - 1]) % n
            finalEncodeString.append(newSimbol)
        finalEncodeString.insert(0, encodeString[0])
        return finalEncodeString

        # подпись закрытым ключом
    def signatureByPrivacyKey(text, d, n):
        c = []
        for i in range(0, len(text)):
            ci = pow(text[i], d) % n
            c.append(ci)
        return c

        # подпись открытым ключом
    def encodeByPublicKey(c, e, n):
        g = []
        for i in range(len(c)):
            gi = pow(c[i], e) % n
            g.append(gi)
        return g

        # проверка подлинности подписи
    def checkSignature(g, d, n):
        c = []
        for i in range(len(g)):
            ci = pow(g[i], d) % n
            c.append(ci)
        return c

        # восстановление исходного текста
    def decodeText(c, e, n):
        m = []
        for i in range(len(c)):
            mi = pow(c[i], e) % n
            m.append(mi)
        return m

    def decoder(text, n):
        decodeString = []
        for i in range(1, len(text)):
            newSimbol = (text[i] - text[i - 1]) % n
            decodeString.append(newSimbol)
        decodeString.insert(0, text[0])

        finalString=[]
        for i in range(0,len(decodeString)):
            newSimbol=alphabet[decodeString[i]]
            finalString.append(newSimbol)
        return finalString


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Sender()
    ex2= Reciver()
    ex.show()
    #ex2.show()
    print(eReciever)
    sys.exit(app.exec_())




