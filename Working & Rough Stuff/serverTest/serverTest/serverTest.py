from bottle import Bottle, run, route, request

app = Bottle()

@app.route('/biznesexp')

def my_listener():
    data = request.query.your_data
    #do_something_with_data(data)
    print "HAHAHAHHAHAHA\n"
    return "hahahahaha"

run(app, host="localhost", port=7724)