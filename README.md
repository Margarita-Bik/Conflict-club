# **Conflict Club**
#### Video Demo:  https://youtu.be/eT3NwtUkpUg
#### How much can you know about yourself if you've never been in a conflict? Get the chance to yell at people and have them yell back at you! No hard feelings, just Conflict Club fun!


This project is a web application for people who want to get into a conflict, just for the fun of it. The consept follows the principles of severeal dating apps.


Initially the users have to **sign up** by providing the **following information**:
- Name
- Password
- Email
- Upload an avatar
- Country
- City
- Select one or more **interests** from the following list:
    - Politics
    - Sports
    - Food
    - Religion
    - Social issues
    - Science
    - Current affairs
    - TV/Cinema
    - Other


Afterwards the users can **sign in** using their email and password. After signing in, the user is redirected to the **home page**, where the algorithm finds potential matches that have one or more common interests and the data (Name, Avatar, City, Country, interests) of first one is being rendered on the screen. Now the user has to deside whether or not they want to get into a conflict with the current potential match by clicking the buttons "yes" or "no" accordingly.
- **Case 1**, the user clicks **"no"**:
-The decision is stored in the database. The next potential match shows up.
- **Case 2**, the user clicks **"yes"**:
-The decision is stored in the database. If the potential match following the exact same procedure, clicks yes as well, it is considered as a match and a chatroom is created for these two users, where they can talk with each other. The chatroom can be accesed by clicking the "Chat" icon at the top right corner of the screen.


The technologies used are the following:
- Flask
- Python
- Sqlite
- JavaScript
- CSS
- Bootstrap
- HTML

Files description


- static/avatar.jpg
-A default picture for users that havent upload any avatar

- static/styles.css
-A css file containing all the css classes used in tha application

- static/backround.jpg
-The background image that is used in all the pages of the application

- templates/index.html
-The view of the home page of an authorized user

- templates/apology.html
-The view that is being displayed if anything goes wrong like wrong password, system errors etc

- templates/layout.html
-The global layout of the app. All the pages and subpages are being rendered in here.

- templates/chat.html
-The view of the chatrooms available and peer-to-peer chat.

- templates/login_register.html
-An html page containing both the login and registration views.

- app.py
-The controllers, routes and logic of all the application

- more.py
-Some helper functions that are being imported and used into app.py

- fighters.db
-The file of the sqlite database

- README.md
-This file :D