from requests import session
from bs4 import BeautifulSoup as scraping

class siakad(object):
    detail = {}
    list_mk = {}
    list_mk2 = {}
    list_menawar = {}
    user_details = {}
    def __init__(self, u,p):
        self.user = u
        self.pwd = p
        self.webdriver = session()
        self.scraping = scraping
        self.uho = "http://siakad.uho.ac.id/ademik.php"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
        self.link_datas = {"krs":"?syxec=mhswkrs&PHPSESSID=774it60k7m26hhb8p3ti5mcn44",
                           "khs":"?syxec=mhswkhs&thn={}&nim={}&GO=Refres",
                           "menawar":"?syxec=mhswkrs&md=1"}
    def sign(self):
        login = {"exec": "proclogin", "proc": "1", "NIP": self.user, "password": self.pwd, "submit": "login"}
        resp = self.ambel(self.uho, login)
        try:
            for details in resp.findAll("td", {"bgcolor":"white"})[1]:
                details = details.findAll("b")
                sks, ipk = details[1].text.split("dengan")
                return siakad.detail.update({"nama":["Nama: "+details[0].text, sks, ipk.strip()]})
        except AttributeError, e:
            return "[!] Kesalahan dalam mengambil [!]"

    def userdetails(self):
        for keys, (nama,sks, ipk) in siakad.detail.items():
            print nama
            print sks
            print ipk
    def ambel(self, add_url=None, add_data=None):
        try:
            ambels = self.webdriver.post(add_url, data=add_data, headers=self.headers, timeout=10)
            return self.scraping(ambels.text, "html.parser")
        except:
            print "[!]Tidak dapat Terkoneksi ke {}[!]".format(self.uho)
    def kunjungi(self, urls):
        try:
            req = self.webdriver.get(urls, timeout=10).text
            return self.scraping(req, "html.parser")
        except:
            print "[!]Tidak dapat Terkoneksi ke {}[!]".format(self.uho)
    def user_khs(self, ops):
        table_user = self.kunjungi(self.uho+self.link_datas["khs"].format(ops,self.user))
        table1 = table_user.find("table", {"class":"basic", "cellspacing":"0", "cellpadding":"2"})
        table2 = table_user.find("table", {"class":"basic", "cellspacing":"1", "cellpadding":"2"})
        table3 = table_user.find("td", {"width":"*", "bgcolor":"#FFFFFF", "class":"main-part"})
        for i in table1.findAll("tr"):
            print i.contents[0].text, i.contents[1].text
            for sas in i.findAll("input", {"type":"text"}):
                print sas["value"]
        print "===== NILAI RATA {}::=====".format(ops)
        tr = [i.text for i in table2.findAll("th", {"class":"ttl"})[1::]]
        tr2 = [i.text for i in table2.findAll("td", {"class": "lst"})]
        print "\n".join(i[0] + ": " + i[1] for i in zip(tr,tr2))
        print "===== NILAI MATA KULIAH ====="
        for mk in table3.contents[8].contents[3::]:
            try:
                print mk.contents[1].text
                print "     [-]Kode MK: ", mk.contents[0].text
                print "     [-]Dosen: ", mk.contents[3].text
                print "     [-]Grade: ", mk.contents[4].text
            except:
                None
        print "="*29
    def user_krs(self, th):
        user = self.kunjungi(self.uho+self.link_datas['khs'])
        user_td = user.find("td", {"width":"*", "bgcolor":"#FFFFFF", "class":"main-part"})
        for i in user_td.findAll("tr"):
            try:
                siakad.user_details.update({i.contents[0].text:i.contents[1].text})
            except IndexError:
                None
            except AttributeError, e:
                return "[!] Kesalahan dalam mengambil [!]"
        siakad.user_details["NIM"] = self.user
        siakad.user_details["Tahun Akademik"] = th
        return siakad.user_details

    def menawar(self, th):
        t = self.user_krs(th)
        user_menawar = siakad.user_details["Tahun Akademik"], siakad.user_details['NIM']
        print "\n".join([keys+": "+values for keys, values in siakad.user_details.items()])
        url = "syxec=mhswkrs&thn={}&nim={}&GO=Refresh".format(user_menawar[0],user_menawar[1])
        req = self.kunjungi(self.uho+"?"+url)
        mata_kuliah = req.find("table", {"class":"basic", "cellspacing":"0", "cellpadding":"4"})
        count = 0
        for i in mata_kuliah.findAll("tr"):
            count += 1
            try:
                siakad.list_mk2.update({count:[i.findAll("td", {"class":"lst"})[3].text,i.findAll("td", {"class":"lst"})[2].text, i.findAll("td", {"class":"lst"})[4].text, i.findAll("td", {"class":"lst"})[5].text+" - "+i.findAll("td", {"class":"lst"})[6].text, i.findAll("td", {"class":"lst"})[7].text,i.findAll("td", {"class":"lst"})[8].text,i.findAll("td", {"class":"lst"})[10].text]})
            except:
                None
        print "====== [ LIST MATA KULIAH ] ======"
        for number,(mk,sks, dosen,jm,ruangan, kls,smt) in siakad.list_mk2.items():
            print "[*] {}".format(sks)
            print "    sks: {}".format(mk)
            print "    Dosen: {}".format(dosen.strip())
            print "    Jam: {}".format(jm.strip())
            print "    Ruangan: {}".format(ruangan.strip())
            print "    Kelas: {}".format(kls.strip())
            print "    Semester: {}".format(smt.strip())
            print

    def list_menawar(self):
        table = self.kunjungi("http://siakad.uho.ac.id/ademik.php?syxec=mhswkrs&md=1")
        table2 = table.find("table", {"border":"0", "class":"basic", "cellspacing":"0"})
        count = 0
        for i in table2.findAll("tr"):
            count += 1
            try:
               siakad.list_mk.update({
                   count:[i.contents[5].text, i.find("input", {"type":"checkbox"})["value"],
                          i.contents[3].text,
                          i.contents[7].text,
                          i.contents[11].text,
                          i.contents[13].text,
                          i.contents[17].text,
                          i.contents[23].text,
                          i.contents[9].text]})
            except:
                None
        print "=== [ PILIH MATA KULIAH ]==="
        for num,(mk,data,kmk,sks,hari,jam,kls,smt,dosen) in siakad.list_mk.items():
            print "[{}] {}".format(str(num),mk)
            print "    [+]Data Post: "+data
            print "    [+]Kode MK: "+kmk
            print "    [+]SKS: "+sks
            print "    [+]Hari: "+hari
            print "    [+]Jam: "+jam
            print "    [+]Kelas: "+kls
            print "    [+]Semester: "+smt
            print "    [+]Dosen: "+dosen
        print "="*40
        print "Masukkan Nomor mata kuliah: "
        try:
            ops = raw_input("> ")
            for mks in ops.split("@"):
                mks = int(mks)
                try:
                    print "Mata Kuliah yang diambil: ", siakad.list_mk[mks][0]
                    datasi = self.data_mk(siakad.list_mk[mks][1])
                    hajar = self.ambel(self.uho, datasi)
                    hajar.find("th", {"class": "wrn", "colspan": "2"}).text
                    hajar.findAll("td", {"bgcolor": "white"})[1].text
                except:
                    None
        except ValueError:
            return ""
        siakad.list_mk = {}
    def data_mk(self, mk):
        d = {"syxec": "mhswkrs",
             "nim": siakad.user_details["NIM"],
             "thn": siakad.user_details["Tahun Akademik"],
             "ambil[]": mk,
             "prckrs": "Ambil Kuliah"
             }
        return d