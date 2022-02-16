#!/usr/bin/python3.8

# This script can make an interaction with the API of coinbase and get queries from it. I only interested in the current exchange rate in the time when the
# script has made, but it works with any other methods as well. Once the exchange rate grabbed,send this in an email.

# Requirements to run the script:
#         - python3.8 must be installed and ready to use (not tested with any other 3.x versions)
#         - coinbase, smtplib, json modules must be pre-installed
#         - .credentials must be exists in the same directory where the script is with the credentials in json format, like: 
#           { 
#             "API_KEY":"HASHED-KEY",
#	            "API_SECRET":"HASHED-SECRET"
#           }
#         - encrypted_data.bin must be exists contains the hashed password to the email login
# The script can run by launching from commandline, but it's more efficient and powerful if we put it into crontab 

from coinbase.wallet.client import Client
from email.parser import BytesParser, Parser
from email.policy import default
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import json
import smtplib, ssl

with open('.credentials',) as file:
  credfile = json.load(file)
  for x, y in credfile.items():
    if x == "API_KEY":
      API_KEY = y
    else:
      API_SECRET = y
file.close()

client = Client(API_KEY, API_SECRET)
#currencies = client.get_currencies()
#rates = client.get_exchange_rates(currency='BTC')
price = client.get_buy_price(currency_pair = 'BTC-USD')
#price = client.get_buy_price(currency_pair = 'BTC-GBP')

#Convert json to str
price_json = json.dumps(price)

if price_json.startswith("{"):
    x = price_json
    y = json.loads(x)

BASE = y["base"]
CURRENCY = y["currency"]
AMOUNT = y["amount"]

EMAILME = """Hello, this is an automatic email, please don't reply. The purpose of this email is informing you
about the current {}-{} currency which is: {}""".format(BASE,CURRENCY,AMOUNT)

# Send the output to my email if currency is bigger than 37.5k

json_dictionary = json.loads(price_json)

for key in json_dictionary:
    if key == 'amount':
        a = json_dictionary[key]
        currency = float(a)
        if currency > 37500:

            smtp_server = "smtp.gmail.com"
            port = 587  # For starttls
            sender_email = "sender.email@mustbe.here"

            # This section below is for fetch my password with rsa encryption method.
            file_in = open("encrypted_data.bin", "rb")

            private_key = RSA.import_key(open("private.pem").read())

            enc_session_key, nonce, tag, ciphertext = [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

            file_in.close()

            # Decrypt the session key with the private RSA key
            cipher_rsa = PKCS1_OAEP.new(private_key)
            session_key = cipher_rsa.decrypt(enc_session_key)

            # Decrypt the data with the AES session key
            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)
            password = data.decode("utf-8")
            receiver_email = "receiver.email@mustbe.here"
            #
            headers = str(Parser(policy=default).parsestr(
                    'Subject: Current BTC currency\n'
                    +EMAILME))
            #
            # Create a secure SSL context
            context = ssl.create_default_context()
            #
            # Try to log in to server and send email
            try:
                server = smtplib.SMTP(smtp_server,port)
                server.ehlo() # Can be omitted
                server.starttls(context=context) # Secure the connection
                server.ehlo() # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, headers)
            except Exception as e:
                # Print any error messages to stdout
                    print(e)
                    #finally:
            server.quit()
            
            
