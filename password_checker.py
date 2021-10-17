# NOTE: pwned means hacked.
import requests
import hashlib 
import sys

def request_api_data(five_character):
    url = 'https://api.pwnedpasswords.com/range/' + five_character
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {req.status_code}, check the api and try again')
    return res 

def get_password_leaks_count(hashes, hashes_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hashes_to_check:
            return count    
    return 0 

def pwned_api_checker(password):
    # 1 first we need to hash our password using sha1 algorithm
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    # 2 separated first five characters 
    first5_char, tail = sha1password[:5], sha1password[5:]
    # 3 used the prequest_api_data(first5_char) to get all pwned(hacked) hashed password list of first five characters, when it will give the list to us, it will omit the first five characters (as they are going to be same through out the list).
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail) # returns the count

def main(args):
    for password in args:
        count = pwned_api_checker(password)
        if count:
            print(f'{password} was found {count} times... YOU SHOULD PROBABLY CHANGE YOUR PASSWORD!')
        else:
            print(f'{password} was not found. Carry ON!')
    return 'DONE!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:])) 
    # to exit from main program when we finished, because of which we can see the return 'DONE!'

# ~~~~~~ OUTPUT ~~~~~~~~~
#   C:\Users\HP\Desktop\4. Password Checker>password_checker.py Hanamontena123 Passmethebucket brocklesnar friends
#   Hanamontena123 was not found. Carry ON!
#   Passmethebucket was not found. Carry ON!
#   brocklesnar was found 683 times... YOU SHOULD PROBABLY CHANGE YOUR PASSWORD!
#   friends was found 224062 times... YOU SHOULD PROBABLY CHANGE YOUR PASSWORD!
#   DONE!
#
