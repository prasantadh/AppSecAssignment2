import requests
from bs4 import BeautifulSoup

baseurl = "http://localhost:5000"

def test(m): print(m, end="\n\t")
def passed(): print("Passed Successfully!")
def failed(): print("Failed!")

## test a workflow

for page in ['/', '/login', '/register', '/spell_check', \
    '/history', '/history/query1', '/logout']:
    try:
        test('Test: `' + page + '` is live!')
        resp = requests.get(baseurl + page)
        assert(resp.status_code == 200)
        passed()
    except:
        failed()

try:
    test('Test: `/spell_check` redirects to login')
    resp = requests.get(baseurl + '/spell_check', allow_redirects=False)
    assert(resp.status_code == 302)
    assert(resp.headers['Location'].startswith(baseurl + '/login'))
    passed()
except:
    failed()

try:
    test('Test: CSRF-less submission fails')
    data = {'uname': '123456789', 'pword': '123456789',\
            'twofa': '123456789'}
    resp = requests.post(baseurl + '/register', data=data)
    assert('failure' in resp.text)
    passed()
except:
    failed()

def get_csrf_token(text):
    soup = BeautifulSoup(resp.text, 'lxml')
    csrf_token = soup.select_one('input[name="csrf_token"]')['value']
    return csrf_token


try:
    test('Test: can register a valid new user')
    sess = requests.session()
    resp = sess.get(baseurl + '/register')
    csrf_token = get_csrf_token(resp)
    data['csrf_token'] = csrf_token
    resp = sess.post(baseurl + '/register', data=data)
    assert('Registration success' in resp.text)
    passed()
except Exception as e:
    failed()

try:
    test('Test: can login an existing user')
    resp = sess.get(baseurl + '/login')
    csrf_token = get_csrf_token(resp)
    data['csrf_token'] = csrf_token
    resp = sess.post(baseurl + '/login', data=data)
    assert('Login success' in resp.text)
    passed()
except Exception as e:
    failed()

try:
    test('Test: spell_check return results')
    resp = sess.get(baseurl + '/spell_check')
    csrf_token = get_csrf_token(resp.text)
    inputtext = 'correct\nincorrectwordeh\n'
    text = {'csrf_token' : csrf_token, 'inputtext' : inputtext}
    resp = sess.post(baseurl+'/spell_check', data=text)
    assert(inputtext in resp.text)
    passed()
except Exception as e:
    failed()

try:
    test('Test: user can review a query')
    resp = sess.get(baseurl + '/history/query1')
    assert('queryid' in resp.text)
    assert('username' in resp.text)
    assert('querytext' in resp.text)   
    assert('queryresults' in resp.text)
    passed()
except:
    failed()

try:
    test('Test: user can view their history')
    resp = sess.get(baseurl + '/history')
    assert('id="query1"' in resp.text)
    assert('id="numqueries' in resp.text)
    assert('queryid' in resp.text)
    assert('username' in resp.text)
    assert('querytext' in resp.text)   
    assert('queryresults' in resp.text) 
    assert(inputtext in resp.text)   
    passed()
except:
    failed()

try:
    test('Test: user can review a specific history')
    resp = sess.get(baseurl + '/history/query1')
    assert('id="query1"' in resp.text)
    assert('queryid' in resp.text)
    assert('username' in resp.text)
    assert('querytext' in resp.text)   
    assert('queryresults' in resp.text) 
    assert('correct' in resp.text)
    assert('incorrect' in resp.text)   
    passed()
except:
    failed()

try:
    test('Test: user can logout')
    resp = sess.get(baseurl + '/logout')
    assert('Login' in resp.text)   
    passed()
except:
    failed()

try:
    test('Test: can register a second valid user')
    data = {'uname': '0123456789', 'pword': '0123456789',\
            'twofa': '0123456789'}
    # sess = requests.session()
    resp = sess.get(baseurl + '/register')
    csrf_token = get_csrf_token(resp)
    data['csrf_token'] = csrf_token
    resp = sess.post(baseurl + '/register', data=data)
    assert('Registration success' in resp.text)
    passed()
except Exception as e:
    failed()

try:
    test('Test: second user can not see first user query')
    resp = sess.get(baseurl + '/register')
    csrf_token = get_csrf_token(resp)
    data['csrf_token'] = csrf_token
    resp = sess.get(baseurl + '/history/query1')
    assert('correct' not in resp.text)
    assert('incorrect' not in resp.text)  
    passed()
except Exception as e:
    failed()