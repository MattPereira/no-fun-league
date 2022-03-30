# **The No Fun League**


<img src="static/no_fun_league.png" width="200" height="200"/>

The [No Fun League](https://no-fun-league.herokuapp.com/) is a website I built for a fantasy football league I have been a member of for 10+ years. All of the roster, draft, and player data is sourced from the [Sleeper API](https://docs.sleeper.app/)

---
### **Description**
The website serves the members of the No Fun League by providing them with updated information about their rosters and past league drafts. Additionally, the site allows league members to edit their personal profile information, create blog posts, propose rule change, and vote on those proposed rule changes.


---
### **Features**
1. Users register by choosing their specific sleeper fantasy account and providing a name, email, and password.
2. Users can create, edit, and delete blog posts that are displayed on the blog page.
3. Users can create rule change proposals that can be voted on by other users.
4. Display draftboard with all picks from 2021 fantasy football draft
5. Display each roster with information about points scored, wins, losses, average age, average height, and all players' positions, name, and team

---
### **Standard User Flow**
- Users create an account by registering
   1. On registration page, users must select which sleeper account they own from select input. Once a sleeper account has been chosen, it is removed from the select options since that sleeper account is now taken.
   2. Users also provide their name, email, and a password which is encrypted and stored in database to allow for future logins using email and password
- After account creation, a user is redirected to their personal page where they are able to edit details about themselves including bio, team philosophy, favorite team, favorite player, ect.
- Logged in users have the opportunity to create blog posts that are all displayed on the blog page
  1. Only the user who created a specific blog post is allowed to edit or delete the post
- Logged in users have the ability to propose rule changes on the polls page
  1. All users who are logged in are permitted to vote on each rule change proposition.
  2. Rule changes may not be edited or deleted to prevent tampering since other users may have already voted.
- Users can also see each roster of the fantasy football leauge with details about each roster provided by sleeper.

---
### **Technology Stack**
#### Front End
- HTML
- CSS
- Bootstrap
- Jinja

#### Back End
- Flask
- WTForms
- Python

#### Database
- PostgresSQL
- SQLAlchemy

#### Tools
- Bcrypt