import random
import requests

# Send request to API and store the response.
WORD_SITE = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(WORD_SITE)

# Split the response content by lines and store them as a list of bytes.
words = response.content.splitlines()

# Fetch 100 random words from the list.
random_words = random.sample(words, 100)

# Decode the bytes into strings and store them in a new list.
random_words = [word.decode('utf-8') for word in random_words]