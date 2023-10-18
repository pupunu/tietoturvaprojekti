Cyber security course project 1

LINK: [Link to the project repository](https://github.com/pupunu/tietoturvaprojekti)

The project uses Django. You need that installed as well as python package: requests.

FLAW 1:
A02:2021 - Cryptographic Failures

This is not a flaw in the code but rather a reminder that the server needs a proxy for securing and encrypting the data flow. 

With Django server as of now, all http requests are sent in plain text. This makes it easy for a man-in-the-middle attack, for example reading the login credentials from the request.

FIX 1:

This can be fixed by using https connections for everything. For this a https proxy has to be installed. A possible solution would be nstalling a NGINX (on debian/ubuntu systems this can be done with ´sudo apt install nginx´) and adding the following file:

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

to /etc/nginx/sites-enabled. However, getting the https certificates to make the system work, is out of the scope of this course.

---

FLAW 2:
A03:2021 – Injection 

[Flaw location](https://github.com/pupunu/tietoturvaprojekti/blob/413495e1bb3466d4906a157ee4054e5475ff4e1a/notes/views.py#L46)

The sql request is not filtered and the search word is directly added to query as a string. This means that user can send sql commands as the filter text, and they get run on the server as normal sql queries. This way one can for example get all the user passwords from the servers by making a query selecting everything from the table containing passwords ('union SELECT 365 as id, password as text, 0 as owner_id FROM auth_user; --)

FIX 2:

[Fix location]()

Easy to fix by replacing the raw query `notes_list = Note.objects.raw("SELECT * FROM notes_note WHERE owner_id = " + str(request.user.id) + " AND text like '%" + filter_word + "%'")` in views.py line 46 with Django's object.filter query `notes_list = Note.objects.filter(owner = request.user, text__contains=filter_word)`.

With Django’s object.filter query, the search word is not directly executed as part of the query, but actually just used as the search word.

---
FLAW 3:
A01:2021 - Broken access Control

[Flaw location](https://github.com/pupunu/tietoturvaprojekti/blob/413495e1bb3466d4906a157ee4054e5475ff4e1a/notes/views.py#L31-L32)

The user to whom the note will be added is taken from a separate parameter "user" intead of relying on the session. This means that you can add notes to other people, by changing the hidden field in the form in html and then adding the note.


FIX 3:

[Fix location]()

To actually be sure that the user, we must rely on sessions. We must use request.user instead of POST parameter "user". This way the user is actually the one corresponding to the current session. This means replacing lines

```Python3
user = User.objects.filter(username = request.POST.get('user'))[0]
note = Note.objects.create(text = text, owner = user)
```

with `note = Note.objects.create(text = text, owner = request.user)`.

---
FLAW 4:
A05:2021 – Security Misconfiguration 

[Flaw locations]()

The server is set to debug mode, which means that in case of error, the error message is shown to the user. This can reveal overly informative data to the user and that way also pose a possible security threat.

FIX 4:

[Fix location]()

The server needs to be set to debug mode, so that in case of an error, the server gives a ”Server error (500)” message instead of the error’s output meant for developers. In settings.py, we must switch the DEBUG variable to FALSE: `DEBUG = True
` replaced with `DEBUG = False`.

---

FLAW 5:
A10:2021 – Server-Side Request Forgery (SSRF)

[Flaw location](https://github.com/pupunu/tietoturvaprojekti/blob/413495e1bb3466d4906a157ee4054e5475ff4e1a/notes/views.py#L21)

The application allows a feature for the user to add notes directly from, eg. Wikipedia links. However, the urls in the notes are not checked at all. This means that a user can try to make requests to webserver's intranet, and make them into readable notes on the website, thus retrieving data that should not be accessible outside of the intranet.
Fixing requires a list of allowed domains from which the information can be requested from, for example the URL starting with "https://en.wikipedia.org".

FIX 5:
[Fix location]()

We first need to have a list of allowed urls. It can be added to views.py as `allowed_urls = ["https://fi.wikipedia.org", "https://en.wikipedia.org"]` or allowed urls can be stored in a database (which is better in the case that there are a lot of allowed urls).

To only include the allowed urls, we must replace the line `if note.text.startswith("http")` with `if any(note.text.startswith(allowed_url) for allowed_url in allowed_urls)`.

---

FLAW 6:
A07:2021 – Identification and Authentication Failures

[Flaw location](https://github.com/pupunu/tietoturvaprojekti/blob/413495e1bb3466d4906a157ee4054e5475ff4e1a/notes/views.py#L51-L65)

The application allows any passwords. This means that users are not forced to use secure passwords which makes the users vulnerable.

FIX 6:

[Fix location]()

This could be solved in multiple ways. We could consider the bare minimum to be requiring the passwords not to include the username and being more than 5 characters long. This can be made by adding lines:

elif len(password) < 5 or username in password:
	return HttpResponse("Your password should be at least 6 characters long!!!")

However, the system could be made more secure, eg. by banning 100 most common passwords, that could be read from a separate database, and for requiring both lower and upper case letters as well as special characters in the passwords.

---

FLAW 7:
A01:2021 - Broken access Control (part 2)

[Flaw location]()

Other user’s notes can be deleted. Note deletion is only done with note’s id number. The id in request can be changed to anything, and thus you can remove other notes that are not yours.

FIX 7:

[Fix location]()

Issue is fixable by adding a check for session user to match with the note owner. This means that in delete view, line 39 `note = Note.objects.filter(id = note_id)[0]`, should be replaced with `note = Note.objects.filter(id = note_id, owner = request.user)[0]`.