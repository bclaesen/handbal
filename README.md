# Handbal: Convert handbal.be competition calender to iCal format.
## About
Import handball games in your calender. Just download the html file from handbal.be and use html2cal.py to convert to an ics. If you are a true Real Kiewit fan, you don't even have to use the script. Just access it from the repository.

[Real Kiewit Competition Calender 2021](./handbal2021.ics)

Please note that Cup Games are not included.

## Importing
### On iOS
Opening a link such as [Real Kiewit Competition Calender 2021](https://github.com/bclaesen/handbal/raw/master/handbal2021.ics) directly in Mobile Safari on your iPhone will bring up an import dialog. Brave will show this as flat text.

### In Google Calender
Click on add other calenders (+ icon) and either choose import, then upload the file from your computer. Or from url and provide the raw url.


## Using the script
### Quirks and Bugs
If the script cannot find any results, either the input format has changed, or you specified the wrong team name. Please try with a different team name using the `--name` option or let me know if you think the input format has changed.

Default duration for a game is one hour.
### Installation dependencies
* Python >= 3.8 (tested on 3.8.10)
* icalendar package (`pip3 install icalendar`)
* result package (`pip3 install result`)
* Beautiful Soup package (`pip3 install bs4`)
* pytz (`pip3 install pytz`)

or use `pip3 install -r requirements.txt` with the `requirements.txt` from this repository.

### Running from command line
Make sure `html2cal.py` is marked as executable.
```
./html2cal.py --help
usage: Convert handbal.be competition calender to iCal format.
       [-h] [-i INPUT] [-o OUTPUT] [-n TEAMNAME] [-s {0,1}]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT,    --input INPUT
                        Pathname of input html file
  -o OUTPUT,   --output OUTPUT
                        Pathname of output ical file
  -n TEAMNAME, --teamname TEAMNAME
                        Team name to filter for
  -s {0,1},    --strict {0,1}
                        Indicate to fail when encountering an error or attempt
                        to create an incomplete output
```
### Examples
Provided you downloaded the file for your competition as `competitiekalender2021.html` and is in the same folder as the script.

To output Real Kiewit's games to the file named `handbal.ics`:
```
./html2cal.py
```
To output HHV Meeuwen's games to the file named `meeuwen.ics`:
```
./html2cal.py -o meeuwen.ics -n "HHV Meeuwen"
```
