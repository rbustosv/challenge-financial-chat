from flask import Flask, render_template
from form import *

app = Flask(__name__)
app.secret_key = 'replace later'

@app.route("/", methods=['GET','POST'])

def registration():
    
    user_form = userForm()
    if user_form.validate_on_submit():
        return "Great success!"
    return render_template("index.html", form=user_form)

if __name__ == "__main__":
    app.run(debug=True)