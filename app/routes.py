from flask import render_template, request, url_for
from werkzeug.utils import redirect

from app import app
from app.inputForm import inputReader


@app.route('/', methods=['POST', 'GET'])
def my_form_post():

    listcourses = []

    if request.method == 'POST':
        ir = inputReader()
        if ir.valid_courses(request.form['input']):
            text = request.form['input']
            print(text)
            processed_text = text.upper()

            ir.loadCoursesInput(processed_text)
            listcourses = ir.coursesCanTake
            print(ir.coursesCanTake)

            # new_list = []
            #
            # if listcourses:
            #     for courses in listcourses:
            #
            #         new_list.append(courses.pop())

    return render_template('index.html', your_list=listcourses)
