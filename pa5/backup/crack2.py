
from misc import *
import crypt

def strip_newlines(l):
    """Strips newline characters from the end of all strings in list l"""
    for w in range(len(l)):
        l[w] = l[w].rstrip("\n")
    return l

def load_words(filename,regexp):
    """Load the words from the file filename that match the regular
       expression regexp.  Returns a list of matching words in the order
       they are in the file."""
    wordsf = open(filename).readlines()
    regexp = re.compile(regexp)
    words = []
    for w in wordsf:
        word = w.rstrip("\n")
        if re.match(regexp, word):
            words.append(word)
    return words

def transform_reverse(str):
    """Returns a list containing str and the reverse of string"""
    wr = [str]
    w = ""
    for c in range(len(str)):
        w = w+str[len(str)-c-1]
    wr.append(w)
    return wr

def transform_capitalize(str):
    """Returns a list containing all possible ways to capitalize str."""
    words = [""]
    cr = []
    for c in str.lower():
        for s in words:
            cr.append(s+c)				#adds a lowercase c to each word in list
            if (c.isalpha()):
                cr.append(s+c.capitalize()) #adds uppercase to each
        words = cr[:]					#copies the cr list to words
        cr = []							#resets cr
    return words

def transform_digits(str):
    """Returns a list containing all possible ways to letters can be replaced
       similar looking numbers. Possible mappings are defined as follows:
       o->0, z->2, a->4, b->6, b->8, i->1, l->1, e->3, s->5, t->7, g->9, q->9"""
    words = [""]
    cr = []
    code = {"o":"0","z":"2","a":"4","b":("6","8"),"i":"1","l":"1","e":"3","s":"5","t":"7","g":"9","q":"9"}
    for c in str:
        for s in words:
            cr.append(s+c)
            if code.has_key(c.lower()):
                for co in code[c.lower()]:
                    cr.append(s+co)
        words = cr[:]
        cr = []
    return words

def check_pass(plain,enc):
    """Check to see if the plaintext plain encrypts to the encrypted
       text enc"""
    if enc == crypt.crypt(plain,enc[:2]):
        return True
    else:
        return False
    

def load_passwd(filename):
    """Load the password file filename and returns a list of
       dictionaries with fields "account", "password", "UID", "GID",
       "GECOS", "directory", and "shell", each mapping to the
       corresponding field of the file."""
    lines = open(filename).readlines()
    users = []
    for line in lines:
        u = line.split(":")
        users.append({'account':u[0],'password':u[1],'UID':u[2],'GID':u[3],'GECOS':u[4],'directory':u[5],'shell':u[6].rstrip("\n")})
    return users

def transform_combinations(w):
    """Returns a list of all combinations of w defined by the functions
       transform_digits, transform_capitalize, and transform_reverse."""
    l = []
    for td in transform_digits(w):
        for tc in transform_capitalize(td):
            for tr in transform_reverse(tc):
                l.append(tr)
    return l

def transform_reverse_caps(w):
    """Returns a list of all random capitalizations of the word w reversed."""
    l = []
    for tc in transform_capitalize(w):
        l.append(transform_reverse(tc)[1])
    return l

def transform_reverse_only(w):
    """Returns a list of a single item, the reverse of w."""
    return [transform_reverse(w)[1]]

def crack_given_transform(fn,ws,pword):
    """Takes a function, a word list, and an encrypted password. The function
       passed should take a single word and return a list of transformations of
       that word. If the password is found, a tuple is returned with the first
       element as True and the second element as the password."""
    for w in ws:
        if len(w) < 9 and len(w)>5:
            for code in fn(w):
                if check_pass(code, pword):
                    return (True,code)
    return (False, "")

def crack_pass_file(fn_pass,words,out):
    """Crack as many passwords in file fn_pass as possible using words
       in the file words"""
    users = load_passwd(fn_pass)
    ws = strip_newlines(open(words).readlines())
    f = open(out, "w")

    transform_fns = [lambda x: [x],
                     transform_reverse_only,
                     transform_digits,
                     transform_reverse_caps,
                     transform_capitalize,
                     transform_combinations]
    transform_explain = ["Checking for un-transformed passwords",
                         "Checking for reversed word passwords",
                         "Checking for digit transformed passwords",
                         "Checking for randomly capitalized passwords reversed",
                         "Checking for randomly capitalized passwords",
                         "Checking for all combination passwords"]

    for tf,te in zip(transform_fns,transform_explain):
        for user in users:
            if user.has_key("account") and tf <> transform_capitalize:
                print te+" for account: "+user["account"]
                result = crack_given_transform(tf,ws,user["password"])
                if result[0]:
                    print user["account"]+"="+result[1]
                    f.write(user["account"]+"="+result[1]+"\n")
                    f.flush()
                    del user["account"]
