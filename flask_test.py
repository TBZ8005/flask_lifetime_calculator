from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_bootstrap import Bootstrap
from scipy import integrate
import numpy as np

app = Flask(__name__, static_url_path='')

manager = Manager(app)
app.config['BOOTSTRAP_SERVE_LOCAL']=True
bootstrap = Bootstrap(app)

@app.route('/', methods = ["GET", "POST"])
def index():
    return render_template('input.html')

@app.route('/calc', methods = ["POST"])
def calc():
    x = [0, 0, 0, 0]
    y = [0, 0, 0, 0]
    k = [0, 0, 0]
    b = [0, 0, 0]
    request_json = request.get_json(force = True)
    x[0] = float(request_json['x0'])
    x[1] = float(request_json['x1'])
    x[2] = float(request_json['x2'])
    x[3] = float(request_json['x3'])
    y[0] = float(request_json['y0'])
    y[1] = float(request_json['y1'])
    y[2] = float(request_json['y2'])
    y[3] = float(request_json['y3'])
    for i in range(3):
        k[i] = (y[i]-y[i+1])/(x[i]-x[i+1])
        b[i] = y[i]-k[i]*x[i]

    func1, abser1 = integrate.quad(lambda t:np.exp(15000/383-15000/(k[0]*t+b[0]+273)), x[0], x[1])
    func2, abser1 = integrate.quad(lambda t:np.exp(15000/383-15000/(k[1]*t+b[1]+273)), x[1], x[2])
    func3, abser1 = integrate.quad(lambda t:np.exp(15000/383-15000/(k[2]*t+b[2]+273)), x[2], x[3])
    S = func1+func2+func3
    L = 20.55*x[3]/S
    return jsonify({'lifetime': str(L)})

@app.route('/hello')
def hello():
    return '<h1>Hello World</h1>'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return render_template('user.html', name = username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

if __name__ == '__main__':
    manager.run()