import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class Rot13(BaseHandler):
    def get(self):
        self.render('rot13-form.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('rot13-form.html', text = rot13)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(BaseHandler):

    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        probe_name = self.request.get('probe_name')
        target = self.request.get('target')
        probes_to_send = self.request.get('probes_to_send')
        time_between_probes = self.request.get('time_between_probes')
        time_between_tests = self.request.get('time_between_tests')
        successive_loss = self.request.get('successive_loss')
        destination_interface = self.request.get('destination_interface')
        target_next_hop = self.request.get('target_next_hop')
        failover_destination = self.request.get('failover_destination')
        failover_next_hop = self.request.get('failover_next_hop')

        params = dict(probe_name = probe_name, target = target, 
		      probes_to_send = probes_to_send,
        time_between_probes = time_between_probes,
        time_between_tests = time_between_tests,
        successive_loss = successive_loss,
        destination_interface = destination_interface,
        target_next_hop = target_next_hop,
        failover_destination = failover_destination,
        failover_next_hop = failover_next_hop
                      )

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.render('ip_monitor.j2',  **params)

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            ##self.render('ip_monitor.j2', username = username)
            self.redirect('/unit2/signup')

app = webapp2.WSGIApplication([('/unit2/rot13', Rot13),
                               ('/unit2/signup', Signup),
                               ('/unit2/welcome', Welcome)],
                              debug=True)
