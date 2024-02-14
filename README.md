# find-me-a-satellite
Find out, which satellites where above your head at a given time

## Why?
In the amateur satellite community, one occasionally discoveres a signal of an unknown object while tracking a satellite. 
This projects allows you to enter your parameters and narrows down the possible choices for said unknown object.

## Dependencies
To run this, you need to have python3 installed on you machine. To install all requirements, please run `pip install pyorbital datetime tqdm`.

## How it works
Open the script in a editor of your choice and enter your parameters. Save it and execute. The script will now download the latest active.txt file
from celestrak and compare your parameters agains every satellite on this list.
