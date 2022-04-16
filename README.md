# curhatIn

**CurhatIn is a social networking platform based on the flask framework that is similar to Tweeter. This project was created to fulfill the final project requirement in Psychology and Design Thinking material.**


**🔹Database Model**


»User
	username
	password
	email
	join_at
» Message
	user (foreign Key)
	content
	published_at
» Relationship
	from_user (foreign key)
	to_user (foreign key)
