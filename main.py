import webapp2
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def build(username_error, password_error, verify_error, email_error):
    page_header="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Signup</title>
        <style type="text/css">
            label{
                width:180px;
                clear:left;
                text-align:right
                padding-right:10px;
            }
            input, label{
                float:left;
            }
            span{
                color: red;
            }
        </style>
    </head>
    <body>
        <h1>Signup</h1>
    """

    page_footer="""
        </body>
        </html>
        """
    username="<label>Username:</label><input type='text' name='username'>"
    password="<label>Password:</label><input type='password' name='password'>"
    verify="<label>Verify Password:</label><input type='password' name='verify'>"
    email="<label>Email (optional):</label><input type='text' name='email'>"
    submit="<input type='submit' value='submit'>"
    form=(page_header + "<form action='/verify' method='post'>"+
        username + "<span>" + username_error + "</span><br>"+
        password + "<span>" + password_error + "</span><br>"+
        verify + "<span>" + verify_error + "</span><br>"+
        email + "<span>" + email_error + "</span><br><br>"+
        submit + page_footer + "</form>")
    return form


class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = build("","","","")
        self.response.write(content)

class Welcome(webapp2.RequestHandler):

    def post(self):

        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if self.username_check(username):
            username_error = ""
        else:
            username_error = "Invalid username!"

        if self.password_check(password):
            password_error = ""
        else:
            password_error = "Invalid password!"

        if self.password_match(password, verify):
            verify_error = ""
        else:
            verify_error = "Your passwords don't match!"

        if self.email_check(email):
            email_error = ""
        else:
            email_error = "Invalid email!"

        if username_error == password_error == verify_error == email_error:
            self.response.write("<h1>Welcome, {} !</h1>".format(username))
        else:
            error_page = build(username_error, password_error, verify_error, email_error)
            self.response.write(error_page)

    def username_check(self,username):
        return USER_RE.match(username)

    def password_check(self,password):
        return PASS_RE.match(password)

    def password_match(self,password,verify):
        if password == verify:
            return True
        else:
            return False

    def email_check(self,email):
        if email == "":
            return True
        else:
            return EMAIL_RE.match(email)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/verify', Welcome)
], debug=True)
