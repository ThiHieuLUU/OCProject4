# Project 4
## About the project 4
This project is realized with MVC pattern in order to manage a chess tournament.
The goal is to create an offline python application which:
* Build a new tournament and take place it (build pairs for matches, update the scores and save the state of the 
tournament)
* See information of the tournaments in the past which are saved in the database.
* See information of all actors saved in the database.

## About main modules
1. player.py:
this module is used to represent a chess player with the player's individual information.

2. match.py:
this module is used to represent a chess match with two players and theirs scores via a tuple of two lists.

3. chess_round.py:
this module is used to represent a chess round associated with a list of matches.

4. tournament.py:
this module is used to represent a chess tournament with all information about the location, the date, the 
players, its rounds, its matches.

5. location.py:
this module is used to represent a location, e.g. location for a tournament.

6. basic_backend.py:
this module is used to do the general tasks for a class:
- create an object from a given dictionary.
- get all attributes and theirs values to put in a dictionary.
- set attributes from a given dictionary.
- print /repr an object of the class.
(the dictionary's keys are attribute names of the class).

7. constants.py:
these are some constants used for the project.

8. mvc_exceptions.py:
this script implements the exception handling for many exception cases in the project.

9. db_tinydb.py: 
this module is used to serialize or deserialize an object/item (here: player, tournament).

10. model.py:
this module takes into account all elements (players, rounds, matches) to take place a new tournament. It also 
accesses and handles the database (here for tournaments and actors).
	
11. controller.py:
this module connects the View and Model in MVC pattern.

12. view.py:
this module is used to display messages, information to user.

13. project4_cli.py:
this module is used as a CLI (command line interface) for user in order to:
- create and take place a new tournament
- See information of previous tournaments (players, rounds, matches, ranking)1. scraping_one_book.py:
- See information of all players (actors) coming from previous tournaments.	this script is used to extract information of a book. 

## Code organization
In this project 4, including:

1. README.md
2. requirements.txt
3. .gitignore
4. 13 above python modules

## Process
1. Create a virtual environment python for the project 4
```bash
sudo apt install -y python3-venv
mkdir project4
cd project4
python3 -m venv venv
source venv/bin/activate
```
2. Install the packages used for the project
```bash
pip install -r requirements.txt
```
3. Check code with flake8
```bash
flake8 --max-line-length=119 --ignore=E128,W503 --format=html --htmldir=flake8-rapport *.py
```
4. Launch
```bash
python3 project4_cli.py
```

## Results
1. Checking code:
result of checking code with flake8 is in the flake-rapport directory.
Example of opening this result:
```bash
firefox flake-rapport/index.html &
```
2. Database:
tournaments and actors are serialized in the 'db.json' database.
