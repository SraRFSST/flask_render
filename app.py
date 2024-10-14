from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title>Flask-Backend-Experience</title>
        </head>
        <body>
            <a href="hallo">Versuche jetzt auch die Route /hallo</a>
        </body>
    </html>
    '''

@app.route('/hallo')
def hallo():
    return '''
    <html>
        <head>
            <title>Hallo Seite</title>
        </head>
        <body>
            <h1>Hallo, du da!</h1>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
