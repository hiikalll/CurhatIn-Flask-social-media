# curhatIn

**CurhatIn is a Social sharing platform that build based on the flask framework. This project was created to fulfill the final project requirement in Psychology and Design Thinking subject.**

CurhatIn is a platform for sharing our thoughts and experiences with others . This app has some fitures such as :

<ul>
  <li>Registration</li>
  <li>Login </li>
  <li>Logout</li>
</ul>

Use basic crud operations like :

<ul>
  <li>Make a post</li>
  <li>Edit post</li>
  <li>Delete post</li>
</ul>

Using peewee which is si ple and light ORM 

And bootstrap as our frontend framework.

<hr>

**We use SQLite as our database for this project. The schema in our database is as follows:**

<h6>user</h6>
<ul>
<li>id</li>
<li>username</li>
<li>password</li>
<li>email</li>
<li>joint_at</li>
</ul>

<h6>message</h6>
<ul>
<li>id</li>
<li>user_id</li>
<li>content</li>
<li>publihed_at</li>
</ul>

<h6>relationship</h6>
<ul>
<li>id</li>
<li>from_user_id</li>
<li>to_user_id</li>
</ul>

![1651015895916.png](image/README/1651015895916.png)

<hr>

# Display

#### Landing Page

![1651016085080.png](image/README/1651016085080.png)

#### Register page

![1651016181849.png](image/README/1651016181849.png)

#### Login page

![1651016256271.png](image/README/1651016256271.png)

#### Home page

![1651016324864.png](image/README/1651016324864.png)

![1651016334046.png](image/README/1651016334046.png)

#### Make  and editpost function

![1651016381728.png](image/README/1651016381728.png)

##### Profile page

![1651016524817.png](image/README/1651016524817.png)

#### followers list page

![1651016578096.png](image/README/1651016578096.png)

#### following list page

![1651016618312.png](image/README/1651016618312.png)
