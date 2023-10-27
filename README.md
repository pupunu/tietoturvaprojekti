# Cyber security course project 1

This is the course project 1 for cyber security base course. In this web application, users can add notes to their account. The notes can be then filtered, so the user only sees certain types of notes, or deleted.

There is also functionality to add notes directly from links. You can test this functionality by adding a note that is an URL (eg. "https://fi.wikipedia.org/wiki/Pistetulo"). Note that most URLs return HTML files, which might not be the most useful of notes.

---

LINK: [Link to the project repository](https://github.com/pupunu/tietoturvaprojekti)

This project report is also part of the README.md file on github. It might be more convenient to read there.

The project uses Django. You need that installed as well as python package: `requests`.

You can make your own test users for testing the application, or use users `testi1:testi` and `testi2:testi`

---

FLAW 1:
A02:2021 - Cryptographic Failures

This is not a flaw in the existing code, but rather a reminder that the server needs a proxy for securing and encrypting the data flow. 

With Django server as of now, all http requests are sent in plain text. This makes it easy for a man-in-the-middle attack, for example reading the login credentials from the request.

FIX 1:

This can be fixed by using https connections for everything. For this a https proxy has to be installed. A possible solution would be installing a NGINX (on debian/ubuntu systems this can be done with ´sudo apt install nginx´) and adding the following file:

```Python3
server {
listen 80;
listen [::]:80;
server_name example.com;

return 302 https://$server_name$request_uri;
}

server {
listen 443 ssl;
listen [::]:443 ssl;
ssl_certificate /etc/ssl/certs/selfsigned.crt;
ssl_certificate_key /etc/ssl/private/selfsigned.key;

ssl_dhparam /etc/nginx/dhparam.pem;
location / {
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header HOST $http_host;
proxy_pass http://127.0.0.1:8080;
proxy_redirect off;
}
}
```

to `/etc/nginx/sites-enabled`. However, getting the https certificates to make the system work, is out of the scope of this course.

---

FLAW 2:
A03:2021 – Injection 

[Flaw location](https://github.com/pupunu/tietoturvaprojekti/blob/f96797e2c5f3eda735aba24d1ee1a45dcc8fa735/notes/views.py#L46)

Users can filter their notes to show only notes that include a certain string. However, the sql request that fetches the notes is not filtered and the search word is directly added to query as a string. This means that a user can send sql commands to the server, and they get run on the server as normal sql queries. This way one can for example get all the user passwords from the servers by making a query selecting everything from the table containing passwords. This is possible by putting this string in the filter form on the website: `('union SELECT 365 as id, password as text, 0 as owner_id FROM auth_user; --)`.

FIX 2:

[Fix location](https://github.com/pupunu/tietoturvaprojekti/blob/f96797e2c5f3eda735aba24d1ee1a45dcc8fa735/notes/views.py#L46-L47)

Easy to fix in the view. We must replace the raw query `notes_list = Note.objects.raw("SELECT * FROM notes_note WHERE owner_id = " + str(request.user.id) + " AND text like '%" + filter_word + "%'")` in notes/views.py line 46 with Django's object.filter query `notes_list = Note.objects.filter(owner = request.user, text__contains=filter_word)`.

With Django’s object.filter query, the search word is not directly executed as part of the query, but actually just used as the search word. This way the search word cannot be used to run queries on the server.

---
FLAW 3:
A01:2021 - Broken access Control

[Flaw location](https://github.com/pupunu/tietoturvaprojekti/blob/f96797e2c5f3eda735aba24d1ee1a45dcc8fa735/notes/views.py#L31-L32)

The user to whom the note will be added is taken from a separate parameter "user" intead of relying on the session. This means that users can add notes to other people, eg. by changing the hidden field in the form in html and then adding a note.


FIX 3:

[Fix location](https://github.com/pupunu/tietoturvaprojekti/blob/f96797e2c5f3eda735aba24d1ee1a45dcc8fa735/notes/views.py#L31-L34C71)

To actually be sure of the user, we must rely on sessions. In the add view, we must use request.user instead of POST parameter "user". This way the user is actually the one corresponding to the current session. This means changes in add view in notes/views.py. We must replace lines 31 and 32

```Python3
user = User.objects.filter(username = request.POST.get('user'))[0]
note = Note.objects.create(text = text, owner = user)
```

with `note = Note.objects.create(text = text, owner = request.user)`.

Now we can be sure that the user to whom the note will be added to, is the one who was logged in to send the note addition. This also requires that the session cookie is not predictable and thus obtainable without logging in. For the purpose of this flaw, we will assume that Django's default session id's are adequite.

---

FLAW 4:
A05:2021 – Security Misconfiguration 

[Flaw locations](https://github.com/pupunu/tietoturvaprojekti/blob/f96797e2c5f3eda735aba24d1ee1a45dcc8fa735/sivuni/settings.py#L26)

The server is set to debug mode, which means that in case of an error, the error message is shown to the user. This can reveal overly informative data (like file names and directory structure) to the user, which can then be used in malicious ways and pose a security threat.

FIX 4:

[Fix location](https://github.com/pupunu/tietoturvaprojekti/blob/f96797e2c5f3eda735aba24d1ee1a45dcc8fa735/sivuni/settings.py#L26)

The server needs to be set to non-debug mode, so that in case of an error, the server gives a ”Server error (500)” message instead of the error’s output meant for developers. In sivuni/settings.py, we must switch the DEBUG variable to FALSE: `DEBUG = True` replaced with `DEBUG = False`. Now the server will only redirect the user to a simple error html, that does not reveal any sensitive information of the server.

---

FLAW 5:
A10:2021 – Server-Side Request Forgery (SSRF)

[Flaw location](https://github.com/pupunu/tietoturvaprojekti/blob/f96797e2c5f3eda735aba24d1ee1a45dcc8fa735/notes/views.py#L21C1-L21C161)

The application allows a feature for the user to add notes directly from, eg. Wikipedia links. It's done by checking if the note starts with "http", and in the case of true, it will make a request to the URL, and show the answer as the note's content. However, the urls in the notes are not checked at all. This means that a user can try to make requests to webserver's intranet, which might include other servers that are not supposed to be obtainable outside of the intranet, and turn the requests into readable notes on the website, thus retrieving data that should not be accessible outside of the intranet.
Fixing requires having a list of allowed domains from which the information can be requested from, for example the URL starting with "https://en.wikipedia.org".

FIX 5:

[Fix location 1](https://github.com/pupunu/tietoturvaprojekti/blob/f96797e2c5f3eda735aba24d1ee1a45dcc8fa735/notes/views.py#L14) – 
[Fix location 2](https://github.com/pupunu/tietoturvaprojekti/blob/f96797e2c5f3eda735aba24d1ee1a45dcc8fa735/notes/views.py#L21C1-L21C161)

We first need to have a list of allowed urls (fix location 1). It can be added to notes/views.py as `allowed_urls = ["https://fi.wikipedia.org", "https://en.wikipedia.org"]` or allowed urls can be stored in a database (which is better in the case that there are a lot of allowed urls). However, for the purpose of showing the main idea of the solution, we will use a simple list in the notes/views.py file.

To only allow notes' content be requested directly from URLs that are listed as allowed urls, we need to check if the url starts with any of the allowed URLs (fix location 2). Thus is notes/views.py, we must replace the line 21 `if note.text.startswith("http")` with `if any(note.text.startswith(allowed_url) for allowed_url in allowed_urls)` (if we had not a list but a database for the urls, we would need to implement a way to go through all the allowed urls from the database). This way the request for the content of a note, is done only if the URL is one of the allowed urls. If the URL is not one of the allowed urls, the note's content will just be the URL as a string. This means that we can manage the allowed urls fairly easily and block users from requesting information from possible servers in the intranet that should not be obtained outside of it.

---

FLAW 6:
A07:2021 – Identification and Authentication Failures

[Flaw location](https://github.com/pupunu/tietoturvaprojekti/blob/f96797e2c5f3eda735aba24d1ee1a45dcc8fa735/notes/views.py#L51-L64)

The application allows any passwords, also not having a password at all. This means that users are not forced to use secure passwords which makes the users vulnerable to account theft and automated attacks that just try to guess most common passwords.

FIX 6:

[Fix location](https://github.com/pupunu/tietoturvaprojekti/blob/f96797e2c5f3eda735aba24d1ee1a45dcc8fa735/notes/views.py#L58-L60)

This could be solved in multiple ways. We could consider the bare minimum to be requiring the passwords not to include the username and being more than 5 characters long. This can be done by adding the following lines to the registration view on line 58 in notes/views.py:

```Python
elif len(password) < 5 or username in password:
	return HttpResponse("Your password should be at least 6 characters long and not include your username!!!")
```

Now if the password is less than 6 characters or includes the username, the user will not be created and an error message with "Your password should be at least 6 characters long" is shown to the user.

However, the system could be made more secure, eg. by banning most common passwords (like "password" and "password123"), that could be read from a separate database, and for requiring both lower and upper case letters as well as special characters in the passwords. For this website, I have decided that the level of security implemented with the fixes is enough.

---

FLAW 7:
A01:2021 - Broken access Control (part 2)

[Flaw location](https://github.com/pupunu/tietoturvaprojekti/blob/f96797e2c5f3eda735aba24d1ee1a45dcc8fa735/notes/views.py#L39-L40)

Other user’s notes can be deleted. Note deletion is only done with note’s id number. The id in request can be changed to anything, and thus you can remove other notes that are not yours.

FIX 7:

[Fix location](https://github.com/pupunu/tietoturvaprojekti/blob/f96797e2c5f3eda735aba24d1ee1a45dcc8fa735/notes/views.py#L39)

Issue is fixable by adding a check for session user to match with the note owner. This means that with delete view in notes/vies.py on line 39 `note = Note.objects.filter(id = note_id)[0]`, should be replaced with `note = Note.objects.filter(id = note_id, owner = request.user)[0]`. Thus we will only delete notes that the user making the request owns.