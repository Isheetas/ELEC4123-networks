from flask import Flask
from client import data,  names, numstudents, marks
import json

app = Flask(__name__)


@app.route("/")

@app.route("/api/studentlist")
def function():
    return json.dumps(names)


@app.route("/api/studentmark/<string:variable>")
def function2(variable):
    i = 0
    while(i<numstudents):
        if(names[i] == variable):
            return json.dumps(marks[i])
        i = i + 1

    return "Json Derulo"



if __name__ == "__main__":
    app.run(debug=True)