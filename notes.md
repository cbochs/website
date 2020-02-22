
## Website Notes

### To-Do
* [Major] Probably need to rework OAuth framework (again) to integrate with MySQL more tightly
  * [Major] Need to handle case where user revokes app access and invalidates stored token
  * [Major] Handle race conditions where spotify token expires and several refresh requests are made simultaneously

### MongoDB

**Config File `/usr/local/etc/mongod.conf`**
**Default DB http://localhost:27017**

##### Installation

```
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

* [Installing MongoDB on MacOS](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
* [brew install mongodb is deprecated](https://stackoverflow.com/questions/55986597/brew-install-mongodb-vs-mongodb-community4-0)

##### Commands

```
show databases
```

### MySQL

**Config File `/usr/local/etc/my.cnf`**
**Default DB http://localhost:3306**

##### Installation

```
brew install mysql
brew services start mysql
```

##### Commands

```
show databases;
show tables;
use <db>;

SELECT User from mysql.user;
```

### Spotify Authorization Flow
**Endpoint `/api/spotify/authorize`**

```
- Does the session have a 'spotify_id'?
  - Refresh token if needed
  - 200 OK
- Does the user have an account with a spotify_user?
  - Refresh token if needed
  - Set the session 'spotify_id' to the spotify_user
  - 200 OK
- Is this the first time /authorize is hit? (else)
  - Redirect to Spotify's OAuth2.0 url
  - Or, return the url to the client
- Is there an 'error' argument? (returned from redirect)
  - 401 Unauthorized.
- Is there a 'code' argument? (returned from redirect)
  - Request a new access token with the 'code'
  - Get the user's basic spotify information
  - Does this spotify_user already exist?
    - Refresh token
    - Set the session 'spotify_id' to the spotify_user
    - 200 OK
  - No?
    - Create new spotify_user with me and (optional) authenticated user
    - Create new access_token with token_info and the spotify_user
    - Commit them to the MySQL database
    - Set the session 'spotify_id' to the spotify_user
    - 200 OK
```

### Flask Stuff

##### Security
* [stackoverflow | security consideration when deploying flask app to server](https://stackoverflow.com/questions/32813861/security-considerations-when-deploying-flask-app-to-server)
* [cyberciti | 40 linux server hardening security tips](https://www.cyberciti.biz/tips/linux-security.html)
* [auth0 | json web tokens](https://jwt.io/)
  * [RFC-7519 | json web token (jwt)](https://tools.ietf.org/html/rfc7519)
  * [readthedocs | PyJWT](https://pyjwt.readthedocs.io/en/latest/)

##### Logging
* [medium | the boring stuff - flask logging](https://medium.com/tenable-techblog/the-boring-stuff-flask-logging-21c3a5dd0392)

##### Sessions
* [hackersandslackers | managing user session variables with flask sessions and redis](https://hackersandslackers.com/managing-user-session-variables-with-flask-sessions-and-redis/)

##### Job Scheduling
* [readthedocs | APScheduler](https://apscheduler.readthedocs.io/en/latest/index.html)

##### Misc.
* [flask | config](https://flask.palletsprojects.com/en/1.1.x/config/)
* [flask | logging](https://flask.palletsprojects.com/en/1.1.x/logging/)
* [Flask-CORS](https://flask-cors.corydolphin.com/en/latest/index.html)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/#)
* [Flask-Session](https://pythonhosted.org/Flask-Session/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/#)
* [medium | field validation for backend apis with python flask and sqlalchemy](https://medium.com/@ed.a.nunes/field-validation-for-backend-apis-with-python-flask-and-sqlalchemy-30e8cc0d260c)
* [medium | the table naming dilemma - singular vs plural](https://medium.com/@fbnlsr/the-table-naming-dilemma-singular-vs-plural-dc260d90aaff)
* [spotify | authorization guide](https://developer.spotify.com/documentation/general/guides/authorization-guide/)
* [stackoverflow | what should rest PUT/POST/DELETE calls should return by a convention](https://stackoverflow.com/questions/4268707/what-rest-put-post-delete-calls-should-return-by-a-convention)
  * [RFC-7231 | semantics and content](https://tools.ietf.org/html/rfc7231#section-4.3)

##### Tutorials
* [w3schools | MySQL](https://www.w3schools.com/sql/)
* [tutorialspoint | MongoDB](https://www.tutorialspoint.com/mongodb/)
* [youtube | flask tutorial #5 sessions](https://www.youtube.com/watch?v=iIhAfX4iek0)

### Vue / JavaScript
* [tutorialspoint | difference between regular functions and arrow functions in javascript](https://www.tutorialspoint.com/difference-between-regular-functions-and-arrow-functions-in-javascript)

### Setup Problems

**Problem** No MySQL database driver/dialect specified
```
ModuleNotFoundError: No module named 'MySQLdb'
```
**Solution** Install a python driver/dialect for MySQL
* [stackoverflow | i can't connect to mysql database](https://www.reddit.com/r/flask/comments/6a35tn/i_started_building_a_flask_api_service_using/)
* [sqlalchemy | support for the mysql database](https://docs.sqlalchemy.org/en/13/dialects/mysql.html)
* [github | mysqlclient-python](https://github.com/PyMySQL/mysqlclient-python)
```python
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/<db>'
```

-------------------------------------------------------------------------------

**Problem** Cannot pip install mysqlclient
```
$ pipenv install mysqlclient
Installing mysqlclient…
✔ Installation Succeeded 
Installing dependencies from Pipfile.lock (e7ba11)…
An error occurred while installing mysqlclient==1.4.2.post1
...
```
**Solution** Add missing OpenSSL lib and include flags to LDFLAGS and CPPFLAGS
* [issues | can't install 'mysqlclient'](https://github.com/pypa/pipenv/issues/3873)
```
export LDFLAGS="-L/usr/local/opt/openssl/lib $LDFLAGS"
export CPPFLAGS="-I/usr/local/opt/openssl/include $CPPFLAGS"
```

-------------------------------------------------------------------------------

**Problem** Werkzeug has deprecated 'werkzeug.contrib' in 1.0.0 (RECENT)
```
ModuleNotFoundError: No module named 'werkzeug.contrib' 
```
**Solution** Downgrade werkzeug from 1.0.0 to 0.16.0
* [issues | modulenotfounderror: no module named 'werkzeug.contrib'](https://github.com/Azure-Samples/ms-identity-python-webapp/issues/16)
* [readthedocs | pipenv basics - specifying versions of a package](https://pipenv-fork.readthedocs.io/en/latest/basics.html)
```
$ pipenv uninstall werkzeug
$ pipenv install "werkzeug==0.16.0"
```

-------------------------------------------------------------------------------

**Problem** Sessions do not persist accross requests
```
[2020-02-21 23:42:09,958] INFO in authenticate: session <user_id: 2>
[2020-02-21 23:42:09,960] INFO in authenticate: Authenticated user <username: bobby, email: c.b@gmail.com, id: 2>
127.0.0.1 - - [21/Feb/2020 23:42:09] "POST /api/login HTTP/1.1" 200 -
[2020-02-21 23:42:23,451] INFO in authenticate: session <user_id: None>
[2020-02-21 23:42:23,451] INFO in authenticate: User is not logged in
127.0.0.1 - - [21/Feb/2020 23:42:23] "GET /api/user HTTP/1.1" 200 -
```
**Solution** Set `Access-Control-Allow-Credentials` header to true in server response
* [geeksforgeeks | access-control-allow-credentials](https://www.geeksforgeeks.org/http-headers-access-control-allow-credentials/)
* [stackoverflow | http requests withcredentials what is this and why use it?](https://stackoverflow.com/questions/27406994/http-requests-withcredentials-what-is-this-and-why-using-it/27407440)
```python
CORS(app, supports_credentials=True)
```
```javascript
axios.defaults.withCredentials = true
```
