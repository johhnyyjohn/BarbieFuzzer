from concurrent.futures import ThreadPoolExecutor
import argparse
import requests
import pyfiglet

parser = argparse.ArgumentParser(description="Fuzzer made by me")
parser.add_argument("-w", default="/usr/share/wordlists/dirb/common.txt", help="wordlist")
parser.add_argument("-u", required=True, type=str, help="target")
parser.add_argument("-t", default=40, type=int, help="number of threads")
parser.add_argument("-fc", type=int, help="filter out status codes that you dont want")
parser.add_argument("-fl", type=int, help="filter out based on number of lines")
parser.add_argument("-fs", type=int, help="filter out based on size of response")
parser.add_argument("-fw", type=int, help="filter out based on number of words")



#parse those command line arguments into args
args = parser.parse_args()

banner = pyfiglet.figlet_format("Barbie Fuzzer", font="slant")
print(banner)
print("-" * 50)

print( ":: Method           : GET")
print(f":: URL              : {args.u}")
print(f":: Wordlist         : {args.w}")
print(f":: Threads          : {args.t}")
print("-" * 50)
print()

def fuzzer(current_word):
    newURL = str(args.u).replace('FUZZ', current_word)

    try:
        response = requests.get(newURL, timeout=5, verify=False)
        size = len(response.content)
        words = len(response.text.split())
        lines = len(response.text.splitlines())

        display_result = True

        if response.status_code == 404:
            return

        if args.fc is not None and response.status_code == args.fc:
            return

        if args.fl is not None and lines == args.fl:
            return

        if args.fw is not None and words == args.fw:
            return

        if args.fs is not None and size == args.fs:
            return

        if display_result:
            print(f"{current_word:10} [Status: {response.status_code}, Size: {size}, Words: {words}, Lines: {lines}, Duration: {response.elapsed}]")


    except requests.exceptions.RequestException as e:
        print(f"Error with word : {current_word}")

    

try:
    with open(args.w, 'r') as f:
        word_from_file = (line.strip() for line in f)
        with ThreadPoolExecutor(max_workers=args.t) as executor:
            executor.map(fuzzer, word_from_file)
except KeyboardInterrupt:
    print("\n[!] User interrupted. Exiting... ")
    exit()



