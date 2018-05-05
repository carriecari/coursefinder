from flask import render_template, request
from app import app
from app.inputForm import inputReader

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    ir = inputReader()

    if request.method == 'POST':
        if ir.valid_courses(request.form['input']):
            text = request.form['input']
            option = request.form.get('option')

            processed_text = text.upper()


            listcourses = ir.loadCoursesInput(processed_text)
            new_list = []

            if listcourses is not None:
                for courses in listcourses:
                    new_list.append(courses.pop())
        else:
            return render_template('index.html')

        return render_template('list.html', your_list=new_list)