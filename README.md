# **The No Fun League**


<img src="/static/no_fun_league.png" width="200" height="200"/>

---
### **Description**
The [No Fun League](https://no-fun-league.herokuapp.com/) is a full stack web application I built for a fantasy football league I have been a member of for 10+ years. All of the roster, draft, and player data is sourced from the [Sleeper API](https://docs.sleeper.app/). The site serves the members of the league by providing them with updated information about their rosters and past league drafts. Additionally, the site allows league members to edit their manager profile information, create blog posts, propose rule changes, and vote on those proposed rule changes.


---
### **Features**
* User authentication and authorization
* Create, Read, Update, and Delete functionality
* Population of database with data from [Sleeper API](https://docs.sleeper.app/) calls that will update information as future NFL seasons unfold
* Displaying all that information from the API on roster and draft pages
* Voting system for league members to decide rule changes


---
### **User Flow**
1. Users create an account by registering
   * On registration page, users select which sleeper account they own from a select input. Once a sleeper account has been chosen, it is removed from the select options since that sleeper account is now taken by a particular user.
   * Users also provide their name, email, and a password which is encrypted and stored in database to allow for future logins using email and password
2. After account creation, the user is redirected to their personal page where they are able to edit details about themselves including bio, team philosophy, favorite team, favorite player, ect.
3. Logged in users have the opportunity to create blog posts that are all displayed on the blog page
  * Only the user who created a specific blog post is authorized to edit or delete the post
4. Logged in users have the ability to propose rule changes on the polls page
  * All users who are logged in are permitted to vote on each rule change proposition.
  * Rule changes may not be edited or deleted to prevent tampering since other users may have already voted.


---
### **Technology Stack**
- Python
- Flask
- Jinja
- WTForms
- PostgresSQL
- SQLAlchemy
- Bcrypt
- Bootstrap
