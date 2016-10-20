from flask import Flask, url_for, redirect, render_template, request, abort
app = Flask(__name__)

#######################
# Basic routing/views #
#######################


# Simple route/view
@app.route('/')  # index route
def hello_world():
    return "hello, world!"


# Route to variable URL
# E.g. request to /user/john would resolve to page containing Hello, john.
@app.route('/user/<username>/')
def user(username):
    return 'Hello, %s' % username


# Optional converter, only accepts integers as varible part of URL
# can also use float or path (as default but accepts /s)
@app.route('/post/<int:post_id>/')
def show_post(post_id):
    return 'This is post %d' % post_id


# Redirect to another view function
@app.route('/old-posts/')
def old_posts():
    return redirect(url_for('show_post', post_id=12345))


# Multiple routes to same view function
# you can tell which route is being used with request.url_rule
@app.route('/url/')
@app.route('/url2/')
def url():
    url = request.url_rule
    return 'route being used is: %s' % url


# Route to a number of pages if matching varible portion of route or cause 404
@app.route('/pages/<variable_part>')
def var_page(variable_part):
    variable_parts = ['123', '456', 'hello-world', 'readifying-austlii']
    if variable_part in variable_parts:
        return "your page is: %s" % variable_part
    else:
        abort(404)


# Custom 404 handling
@app.errorhandler(404)
def not_found(error):
    return '404: Page Not Found :(', 404


#######################
# Rendering templates #
#######################


# Simple template render
# variable content is passed to the template as render_template() kwarg
@app.route('/simple-template/')
def templated():
    h2_content = "This content is rendered via a template"
    return render_template('simple-template.html', h2_content=h2_content)


# Inherited template
# See base.html and extends-base.html templates for explanation
@app.route('/extended-base-template/')
def extends_base():
    return render_template('extends-base.html')


######################
# The request object #
######################


# Display all request headers
# request.headers is dictionary-like object so standard Dict methods apply
# E.g. request.headers.get('some_key')
@app.route('/headers/')
def headers():
    headers = request.headers
    output = ""
    for item in headers:
        item = str(item) + "<br>"
        output += item
    return output


# Display single request header (when known)
@app.route('/browser/')
def browser():
    user_agent = request.headers.get('User-Agent')
    return 'Browser is: %s' % user_agent


# Get url params
# e.g. browse to http://localhost:5000/params?some_param=hello, world!
# request.args is a Werkzeug MultiDict containing all params as k,v pairs
# See http://werkzeug.pocoo.org/docs/0.11/datastructures/
@app.route('/params/')
def params():
    param = request.args.get('some_param')
    if param:
        return param
    else:
        abort(404)  # handle missing param


if __name__ == '__main__':
    app.run(debug=True)
