import crypt

def add_entries():
    ap_dict = {"test1":"wo11iw","test2":"yankee","test3":"yAnkee","test4":"f15h3r"}
    f = open("passwd2","a")
    for account,pword in ap_dict.items():
        pwordc = crypt.crypt(pword,"s2")
        f.write(account+":"+pwordc+":9:9:Lerwa Tieton:/home/tieton:/bin/bash\n")
