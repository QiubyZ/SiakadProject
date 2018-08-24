from qsiakadModulz.siakad import *
import os
root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, "qsiakadModulz"))

def banner():
    print "================================="
    print " PYTHON SCRIPT SIAKAD.UHO.AC.ID"
    print "     Author: Qiuby Zhukhi"
    print "================================="

def login():
    global web
    while True:
        try:
            user = raw_input("User: ")
            pwd = raw_input("Password: ")
            web = siakad(user, pwd)
            web.sign()
            if web.sign() != "[!] Kesalahan dalam mengambil [!]":
                web.userdetails()
            else:
                print "Login Ulang"
                print web.sign()
                continue
            break
        except:
            print "opssss"
            continue

def menawar(ops2):
    print "Menawar"
    web.menawar(ops2)
    ops = menu1()
    if ops == 1:
        web.list_menawar()

def menu():
    while True:
        print " ==== [ MENU ] ===="
        print "[1] Lihat Nilai"
        print "[2] Menawar "
        print "[?] Masukkan Angka Pilihan [?]"
        try:
            ops = int(raw_input("> "))
            if ops >= 3:
                print "Oops pilihan {} tidak ada".format(ops)
                continue
            elif ops == 1 or 2:
                return ops
                break
        except:
            print "[!] Pilihan Salah [!]"
def menu1():
    while True:
        print "[1] Tambah Mata kuliah"
        print "[2] Menu Awal"
        print "[?] Masukkan Angka Pilihan [?]"
        try:
            ops = int(raw_input("> "))
            if ops >= 3:
                print "Angka melebihi dari pilihan"
                continue
            elif ops == 1:
                return ops
            elif ops == 2:
                break
        except:
            print "[!] Pilihan Salah [!]"
            continue

def start_new():
    while True:
        ops = menu()
        if ops == 1:
            while True:
                print "e untuk [e]xit"
                ops1 = raw_input("Tahun Akademik: ")
                if ops1 != "e":
                    try:
                        web.user_khs(ops1)
                        continue
                    except:
                        break
                else:
                    break
        elif ops == 2:
            while True:
                ops2 = raw_input("Tahun Akademik: ")
                try:
                    if ops2 != "e":
                        menawar(ops2)
                        continue
                    else:
                        break
                    pass
                except:
                    print "[!] Masukkan Tahun Akademik [!]"
                    print "[!] tekan e untuk [e]xit [!]"
                    continue

if __name__ == '__main__':
    banner()
    login()
    start_new()