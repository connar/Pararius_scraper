# Pararius_scraper
This is a script I developed to automate the process of finding and submitting form requests of new houses on the pararius platform. This is not 100% done as in it is not running as a process on your machine and check for new houses every 20 minutes for example. This is something to add in the future.

## Usage
Upon running the script with the help flag, we get the following output:
```cmd
C:\Users\user1\Documents\GitHub\parariusProject>python pscrapy.py -h
usage: pscrapy.py [-h] --min MIN --max MAX --city CITY --phone PHONE --email EMAIL --fname FNAME --lname LNAME
                  --message MESSAGE

Process some integers.

options:
  -h, --help         show this help message and exit
  --min MIN          Minimum number (integer)
  --max MAX          Maximum number (integer)
  --city CITY        City name (string)
  --phone PHONE      Phone name (string)
  --email EMAIL      Email (string)
  --fname FNAME      First name (string)
  --lname LNAME      Last name (string)
  --message MESSAGE  Message (string)
```

Say I want to look for properties in Eindhoven in the price range of [0,600]. We would run the following command:
```
C:\Users\user1\Documents\GitHub\parariusProject>python pscrapy.py --min 0 --max 600 --city Eindhoven --phone "+14149398617" --email "nepotib597@huleos.com" --fname "Tyson" --lname "Smithston" --message "I really like this property! Let me know if it is still available."

Minimum number: 0
Maximum number: 600
City: Eindhoven
Phone: +14149398617
Email: nepotib597@huleos.com
First Name: Tyson
Last Name: Smithston
Message: I really like this property! Let me know if it is still available.
https://www.pararius.com/apartments/eindhoven/0-600
```
For demo purposes, I just got a fake number from online and a temporary email from https://temp-mail.org/en.
Let some time pass and see the results...

Checking our email, we see we successfully got a reply back:  
![image](https://github.com/connar/Pararius_scraper/assets/87579399/0568f537-7d05-4c9b-8346-26cb12d02992)

and the output from our script is:  
```
C:\Users\user1\Documents\GitHub\parariusProject>python pscrapy.py --min 0 --max 600 --city Eindhoven --phone "+14149398617" --email "nepotib597@huleos.com" --fname "Tyson" --lname "Smithston" --message "I really like this property! Let me know if it is still available."
Minimum number: 0
Maximum number: 600
City: Eindhoven
Phone: +14149398617
Email: nepotib597@huleos.com
First Name: Tyson
Last Name: Smithston
Message: I really like this property! Let me know if it is still available.
https://www.pararius.com/apartments/eindhoven/0-600
Scraped data saved to 'pararius_Eindhoven_properies.csv'

Form submitted successfully!
```

Checking our pararius_Eindhoven_properties.csv we see all the currently available properties for Eindhoven in the price range specified:   
![image](https://github.com/connar/Pararius_scraper/assets/87579399/c3c3ad23-5abf-4ece-928a-c7a9e46be618)
