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
C:\Users\user1\Documents\GitHub\parariusProject>python pscrapy.py --min 0 --max 600 --city Eindhoven --phone "+14149398617" --email "jovipo3289@adrais.com" --fname "Tyson" --lname "Smithston" --message "I really like this property! Let me know if it is still available."
```
For demo purposes, I just got a fake number from online and a temporary email from https://temp-mail.org/en.
Let some time pass and see the results...

Checking our email, we see we successfully got many replies back:  

![image](https://github.com/connar/Pararius_scraper/assets/87579399/6a1f7272-963b-4bbf-97ef-c98bd5024a08)


and the output from our script is:  
```
C:\Users\user1\Documents\GitHub\parariusProject>python pscrapy.py --min 0 --max 600 --city Eindhoven --phone "+14149398617" --email "jovipo3289@adrais.com" --fname "Tyson" --lname "Smithston" --message "I really like this property! Let me know if it is still available."
- Minimum number: 0
- Maximum number: 600
- City: Eindhoven
- Phone: +14149398617
- Email: jovipo3289@adrais.com
- First Name: Tyson
- Last Name: Smithston
- Message: I really like this property! Let me know if it is still available.

[+] Scraping url:  https://www.pararius.com/apartments/eindhoven/0-600
[+] Scraped data saved to 'pararius_Eindhoven_properies.csv'
[*] Form submitted successfully!
[*] Form submitted successfully!
[*] Form submitted successfully!
[*] Form submitted successfully!
[*] Form submitted successfully!
[*] Form submitted successfully!
[*] Form submitted successfully!
[*] Form submitted successfully!
[*] Form submitted successfully!
[*] Form submitted successfully!

C:\Users\user1\Documents\GitHub\parariusProject>
```

Checking our pararius_Eindhoven_properties.csv we see all the currently available properties for Eindhoven in the price range specified:   

![image](https://github.com/connar/Pararius_scraper/assets/87579399/30bb6fcc-8ef5-4e15-acdf-f0f0d4e8bab6)


### Add in future
Things to add in the future:  
- Mark each property in the .csv as "Done" or "Pending" whether a form was submitted in the past for the property.
- Use scheduling to run every 5 minutes (reference: https://www.geeksforgeeks.org/python-script-that-is-executed-every-5-minutes/)
- Before the script runs, check if the .csv exists. If it is, check whether the pararius uploaded new properties and if so, if they exist on the .csv. If they do not, add them with a "Pending" keyword and then proceed to submit a form for them.
- If a property in the .csv no longer exists in pararius, remove it from the .csv.
