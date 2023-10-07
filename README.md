Cyber security course project 1

LINK: https://github.com/pupunu/tietoturvaprojekti

FLAW 1:
A02:2021 - Cryptographic Failures
No exact location of the flaw in the current code
All http requests are sent in plain text. This makes it easy for a man-in-the-middle attack, for example reading the login credentials from the request.
This can be fixed by using https connections for everything. For this a https proxy has to be installed. A possible solution would be nstalling a NGINX (on debian/ubuntu systems this can be done with ´sudo apt install nginx´) and adding the following file:

´
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
´

to /etc/nginx/sites-enabled. Getting the https certificates is out of the scope of this course.

FLAW 2:
A03:2021 – Injection 
Flaw location: sivuni/notes/views.py
The sql request is not filtered and by adding sql commands to the filter text, one can for example get all the user passwords.
Easy to fix by replacing the raw query with Django's object.filter query (explicit fix commented in the code below flaw).


FLAW 3:
A01:2021 - Broken access Control
Flaw location: sivuni/note/views.py 
The user to whom the note will be added is taken from a separate parameter "user" intead of relying on the session. This means you can add notes tho other people.
Can be fixed with using request.user instead of POST parameter "user". See further in the code.


FLAW 4:
A05:2021 – Security Misconfiguration
Flaw location: sivuni/manage.py 
Django server listens to requests from any ip address (instead of only localhost with a proxy). This means that server can be communicated with http, instead of https, even if a ssl proxy is used. This means also that users can be fooled to use the unencrypted connection with the server if given the http address instead of https.
Fixing requires removing the hardcoded default port and ip address from manage.py.

FLAW 5:
A10:2021 – Server-Side Request Forgery (SSRF)
Flaw location: sivuni/notes/views.py (index)
The application allows a feature for the user to add notes directly from, eg. Wikipedia links. However, the urls in the notes are not checked at all. This means that a user can try to make requests to webserver's intranet, and make them into readable notes on the website, thus retrieving data that should not be accessible outside of the intranet.
Fixing requires a list of allowed domains from which the information can be requested from, for example the URL starting with "https://en.wikipedia.org".

FLAW 6:
A07:2021 – Identification and Authentication Failures
Flaw location views -> register
The application allows any passwords. This means that users are not forced to use secure passwords which makes the users vulnerable.
The solutions could, eg. be checking if the password is in a list of most used passwords and to require special characters.

