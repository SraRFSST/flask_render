from flask import Flask

app = Flask(__name__)

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
