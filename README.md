# KidSeatingWizard
## About this project

This is my very first contact with programming. 👶  

During my last year as a teacher, a friend working as a school monitor in a nearby primary school complained about a very boring part of his job, telling me that it took him about 15-20 minutes every morning to come up with a seating plan for the lunch.  
  
He always wanted to make sure the kids would not have lunch with the same schoolmates every day, and also needed to comply with some conditions such as the number of adults available to help some kids with specific needs, the ever-evolving friendships between the kids that sometimes made it impossible to sit 2 kids at the same table, and other conditons...

I saw that as a perfect oportunity to try learning a few things about programming, and came up with this little script after a few days, which turned this 15-20 min chore into a single line of command. Even though it's just a very simple task, it makes me quite proud to know that it is still being used daily making at least one person's life a little easier !

## Usage
```
git clone https://github.com/tgrasset/KidSeatingWizard.git
cd KidSeatingWizard
python script.py data.txt 3
```
The script must be given 2 arguments, the first one being a text file containing all the necessary data about the children and the second being the number of available adults (3 in the above example).  

Data about children must follow this pattern, 1 line = 1 child:   
`Name, maternelle/primaire, petite/grande_chaise, other conditions separated by commas`   
Other conditions include :  
- `veg/sans_porc` : Specify menu needs
- `avec_adulte` : This kid must be seated at a table with an adult
- `!Name` : This kid must not be seated with a kid with this name
- `&Name` : This pair of kids will be seated at a table with no adult and considered "leaders" of that table in a situation where there are more tables than adults available. Otherwise this condition will be ignored.

A line can be ignored with a simple `#` character at its beginning, which is of course very useful if a child is absent.

## Output example
The script outputs in the terminal a list of tables with their number of big and small chairs, followed by a recap including the number of special menus to order. Then, as it was requested by my friend, it also pairs the kids for the walk from the playground to the cafeteria, putting primaires and maternelles together if possible, and of course avoiding to pair two kids who share a `!` condition.
```
Table 1  :  ['Adulte1', 'Jade', 'Nathan', 'Alix', 'Louis', 'Rayan']
            Chaises:  3  petite(s) et  2  grande(s)
            Adulte: 1

Table 2  :  ['Adulte2', 'Lea', 'Ines', 'Assia', 'Gabriel']
            Chaises:  1  petite(s) et  3  grande(s)
            Adulte: 1

Table 3  :  ['Adulte3', 'Chloe', 'Mathis', 'Emma', 'Mohammed']
            Chaises:  1  petite(s) et  3  grande(s)
            Adulte: 1

Table 4  :  ['Lucas', 'Sarah', 'Maxime', 'Jules', 'Valentin', 'Eliott']
            Chaises:  5  petite(s) et  1  grande(s)
            Adulte: 0

TOTAL: 
REPARTITION :  11  maternelle(s),  8  primaire(s),  3  adulte(s).
MENUS ENFANTS :  6  sans porc,  6  vegetarien(s),  7  ordinaire(s). 

Rang : 
Gabriel Eliott
Alix Jules
Louis Rayan
Maxime Valentin
Mohammed Emma
Sarah Ines
Jade Assia
Nathan Lea
Chloe Mathis
Lucas
```