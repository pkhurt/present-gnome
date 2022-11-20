# present-gnome
Present gnome (Geschenke-wichtel) is a program that gambles persons into groups to decide who has to give a gift to each other which should start with a random chosen letter.

## Detail
The present gnome picks a random letter between A and Z.

Secondly, it shuffles all the names and corresponding email adresses in the given list (`names.csv`) and creates groups of 2 two people. These two people have to give a gift each other. 

The clue is, that nobody of the list should know who gives the present to whom. Therefor the gnome takes the email adresses to send the random chosen letter and the matched name to each person.

In order to do that you need to type in your gmail username and password. No worries, it's only sent viar ssl to the server. 

# How to use
1. Change the config to your mail smtp server and Port
2. Add real names and email adresses to the 'names.csv' as shown below
3. run `python3 main.py` and wait for the instructions

## `names.csv` structure
An example structure

Name | MailAdress 
--- | --- | 
Peter | peteriscool@awesome.de | 
Paul | paulisalsocool@awesome.de |

# For Gmail: How to set up a application specific password
1. Go to your Google Account.
2. Select Security.
3. Under "Signing in to Google," select App Passwords. You may need to sign in. ...
4. At the bottom, choose Select app and choose the app you using Select device and choose the device you're using. ...
5. Follow the instructions to enter the App Password. ...
6. Tap Done.

