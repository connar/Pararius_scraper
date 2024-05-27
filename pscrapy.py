import requests
from bs4 import BeautifulSoup
import csv
import cfscrape
import re
import time
import argparse

# https://github.com/Anorov/cloudflare-scrape/issues/264
# https://github.com/Anorov/cloudflare-scrape/issues/268

def init():
    global scraper
    scraper = cfscrape.create_scraper()

    scraper.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'})
    cfscrape.DEFAULT_CIPHERS = 'TLS_AES_256_GCM_SHA384:ECDHE-ECDSA-AES256-SHA384'
    response = scraper.get('https://www.pararius.com/cgi-bin/fl/js/verify')

def scrape_pararius(url):
    response = scraper.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        properties = {'Studio': [], 'Room': [], 'Flat': []}
        form_urls = []  # List to store form URLs

        # Find all property listings
        listings = soup.find_all('li', class_='search-list__item')

        for listing in listings:
            property_name_elem = listing.find('a', class_='listing-search-item__link--title')

            # Extract property name
            property_name = property_name_elem.text.strip() if property_name_elem else 'Unknown Property Name'

            # Skip properties with unknown names
            if property_name == 'Unknown Property Name':
                continue

            # Extract property URL
            property_url = 'https://www.pararius.com' + property_name_elem['href'] if property_name_elem else '-'

            # Determine property type (Studio, Room, Flat)
            if 'studio' in property_name.lower():
                property_type = 'Studio'
            elif 'room' in property_name.lower():
                property_type = 'Room'
            elif 'flat' in property_name.lower():
                property_type = 'Flat'
            else:
                property_type = 'Unknown'

            # Extract property price
            property_price_elem = listing.find('div', class_='listing-search-item__price')
            property_price_raw = property_price_elem.text.strip() if property_price_elem else '€?'
            property_price_per_month = int(property_price_raw[1:-10]) if (property_price_raw.endswith(' per month') and property_price_raw.startswith('€')) else -1

            # Visit property URL to extract request-details URL
            property_response = scraper.get(property_url)
            if property_response.status_code == 200:
                property_soup = BeautifulSoup(property_response.text, 'html.parser')
                request_details_link = property_soup.find('a', class_='agent-summary__agent-contact-request')
                if request_details_link:
                    request_details_url = 'https://www.pararius.com' + request_details_link['href']
                    form_urls.append(request_details_url)  # Add form URL to the list
                else:
                    request_details_url = 'Not found'

                # Store in dictionary based on property type
                properties[property_type].append({
                    'name': property_name,
                    'url': property_url,
                    'price_raw': property_price_raw,
                    'ppm': property_price_per_month,
                    'request_details_url': request_details_url
                })

        return properties, form_urls
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
        return None, None



def get_form_values(html_content):
    # Use regular expressions to find the token and recaptcha key
    token_match = re.search(r'name="listing_contact_agent_form\[_token\]" value="(.+?)"', html_content)
    recaptcha_match = re.search(r'name="listing_contact_agent_form\[recaptcha_token\]" value="(.+?)"', html_content)

    if token_match:
        token_value = token_match.group(1)
        recaptcha_key = recaptcha_match.group(1)
        return token_value, recaptcha_key
    else:
        return None, None

def submit_form(html_content, action_url, first_name, last_name, email, phone, message):
    # Get the form values
    token_value, recaptcha_key = get_form_values(html_content)
    if token_value is None or recaptcha_key is None:
        print("Failed to extract form values.")
        return

    # Construct the form data
    form_data = {
        'listing_contact_agent_form[_token]': token_value,
        'listing_contact_agent_form[recaptcha_token]': "",
        'listing_contact_agent_form[first_name]': first_name,
        'listing_contact_agent_form[last_name]': last_name,
        'listing_contact_agent_form[email]': email,
        'listing_contact_agent_form[phone]': phone,
        'listing_contact_agent_form[message]': message
    }

    # Submit the form
    response = scraper.post(action_url, data=form_data)
    print(response.text)
    # Check the response
    if response.status_code == 200:
        print("Form submitted successfully!")
    else:
        print("Error submitting form. Status code:", response.status_code)

def get_html_content(url):
    response = scraper.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch HTML content for URL: {url}")
        return None

def get_args():
    # URL to scrape
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--min', type=int, required=True, help='Minimum number (integer)')
    parser.add_argument('--max', type=int, required=True, help='Maximum number (integer)')
    parser.add_argument('--city', type=str, required=True, help='City name (string)')
    parser.add_argument('--phone', type=str, required=True, help='Phone name (string)')
    parser.add_argument('--email', type=str, required=True, help='Email (string)')
    parser.add_argument('--fname', type=str, required=True, help='First name (string)')
    parser.add_argument('--lname', type=str, required=True, help='Last name (string)')
    parser.add_argument('--message', type=str, required=True, help='Message (string)')

    args = parser.parse_args()

    # Step 4: Access and validate the arguments
    min_number = args.min
    max_number = args.max
    city_name = args.city
    phone_number = args.phone
    email_address = args.email
    first_name = args.fname
    last_name = args.lname
    message = args.message


    available_cities = ["amsterdam", "rotterdam", "den-haag", "eindhoven", "utrecht", "maastricht", "groningen", "amstelveen", "haarlem", "breda", "leiden", "tilburg", "arnhem", "almere", "den-bosch"]

    if city_name.lower() not in available_cities:
        parser.error(f"'--city' does not exist inside the list of available cities: {available_cities}")

    # Custom validation logic
    if min_number > max_number:
        parser.error("'--min' should not be greater than '--max'")

    print(f"Minimum number: {min_number}")
    print(f"Maximum number: {max_number}")
    print(f"City: {city_name}")
    print(f"Phone: {phone_number}")
    print(f"Email: {email_address}")
    print(f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Message: {message}")

    return min_number, max_number, city_name, phone_number, email_address, first_name, last_name, message

if __name__ == "__main__":
    init()
    min_, max_, city, phone, email, fname, lname, msg = get_args()

    url = f'https://www.pararius.com/apartments/{city.lower()}/{min_}-{max_}'
    print(url)
    results, form_urls = scrape_pararius(url)

    if results:
        # Define CSV file path
        csv_file = f'pararius_{city}_properies.csv'

        # Open CSV file in write mode
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Name', 'Url', 'Price', 'Type', 'RequestDetailsUrl'])
            writer.writeheader()

            # Write data to CSV file
            for property_type in ['Studio', 'Room', 'Flat']:
                for p in results[property_type]:
                    writer.writerow({
                        'Name': p['name'],
                        'Url': p['url'],
                        'Price': p['ppm'],
                        'Type': property_type,
                        'RequestDetailsUrl': p['request_details_url']
                    })

        print(f"Scraped data saved to '{csv_file}'")

        for url in form_urls[:1]:
            time.sleep(20)
            html_content = get_html_content(url)
            if html_content:
                submit_form(html_content, url, fname, lname, email, phone, msg)
            else:
                print("No html content was found")


    else:
        print("No results found.")
