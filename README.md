# Bakery Sim
This bakery sim lets the user manage a bakery. In this bakery there are 4 bakers, 7 pieces of equipment (2 mixers, 3 ovens, and 2 decorating stations), and 3 recipes to can make (cookies, cupcakes, and cake). The goal is to get as much bakery in the dessert case by the end of the day. 

#### Recipes
The 3 recipes each have their own batch yield (e.g. the cookie recipe yields 12 cookies) and distinct times for how long to mix, bake, and decorate.

#### Equipment
Every recipe must go through the 3 stages of the baking process in order (mix, bake, and decorate). If the user tries to move a recipe to a stage before the previous stages have completed, the sim will prompt the user for another decision. 

#### Bakers
Each baker has a defined shift. Some will leave early or arrive later in the day. If they aren't going to be able to complete a task (starting up mixer, loading oven, or decorating) before the end of their shift, the sim will prompt the user to make another decision. Bakers also need to be trained how to use the piece of equipment the user tasks them to use. Bakers only need 5 mins to start a mixer or load an oven, but decorating time will depend on the recipe being decorated.  

## Requirements
Python 3 (developed in 3.9.0)

### Setup Environment
1. Install virtualenv
   `pip install virtualenv`
2. Create virtual environment
   `python -m venv venv`
3. Activate virtual environment
   `./venv/Scripts/activate`
4. Install packages
   `pip install -r requirements.txt`
5. Write packages to requirements.txt file

#### Helpful links on virtualenv and requirement files
https://python.land/virtual-environments/virtualenv
https://learnpython.com/blog/python-requirements-file/

## Running

### From the Command Line
1. Run command
   `python bakery_sim.py`

## Debugging

### From Visual Studio Code
1. With bakery_sim.py selected, go to Run and Debug (Ctrl + Shift + D) and click Run and Debug
   * If prompted, select current active file
