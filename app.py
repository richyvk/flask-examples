from flask import Flask, url_for, redirect, render_template, request, abort
app = Flask(__name__)

#######################
# Basic routing/views #
#######################


# Simple route/view
@app.route('/')  # index route
def hello_world():
    return "hello, world!"


# Render a template
# variable content is passed to the template as kwargs
# to render_template function following template name
#
# Always add trailing / to route - requests to url without
# it will resolve to it
@app.route('/templated/')
def templated():
    h2 = "<h2>This content is rendered via a template</h2>"
    return render_template('index.html', h2=h2)


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


######################
# The request object #
######################


# Display all request headers
# request.headers is dictionary-like object so standard dict methods apply
# E.g. request.headers.get('some_key')
@app.route('/headers/')
def headers():
    headers = request.headers
    output = ""
    for item in headers:
        item = str(item) + "<br>"
        output += item
    return output


# display single request header (when known)
@app.route('/browser/')
def browser():
    user_agent = request.headers.get('User-Agent')
    return 'Browser is: %s' % user_agent


if __name__ == '__main__':
    app.run(debug=True)
