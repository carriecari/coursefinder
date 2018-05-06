import re
from json import loads

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



class inputReader():

    arrayTakenCourses = []
    coursesCanTake = []

    def valid_courses(self, taken):
        if re.match('(\w{4}\s?\w{3,4})', taken):
            return True


    def loadCoursesInput(self, inputCourses):

        self.arrayTakenCourses = []
        self.coursesCanTake = []

        if re.match('(\w{4}\s?\w{3,4})', inputCourses):
            match = re.findall('(\w{4}\s?\w{3,4})', inputCourses)
            self.arrayTakenCourses.append(match)

        return self.findCoursesToTake()


    def findCoursesToTake(self):

        with open('ubcspider/items.jl') as courses:
            for line in courses:
                c = loads(line)   #creates one dict
                if c.get('required') and c.get('andEither') is not None:
                    prereqs = c['required']  #dict also
                    andeithers = c['andEither']

                    if self.contains_required(prereqs) and (self.has_a(andeithers.get('a')) or
                                                            self.has_b(andeithers.get('b'))):
                        self.coursesCanTake.append(c.get('name'))

                elif c.get('required') is not None:
                    prereqs = c['required']  #dict also
                    if self.contains_required(prereqs):
                        self.coursesCanTake.append(c.get('name'))

                elif c.get('andEither') is not None:
                    andeithers = c['andEither']
                    if self.has_a(andeithers.get('a')) or self.has_b(andeithers.get('b')):
                        self.coursesCanTake.append(c.get('name'))

                else:
                    pass

            return self.coursesCanTake



    def contains_required(self, prereqs):

        if prereqs.get('allof') is not None:
            allrequired = prereqs.get('allof')  # array
            if self.containsAllof(allrequired):
                return True
            else:
                return False

        elif prereqs.get('oneof') is not None:
            oneofrequired = prereqs.get('oneof')  # array [[____,____,],[____,____]] or [[____,____]]
            for one in oneofrequired:
                if self.containsOneOf(one):
                    return True
                else:
                    return False

    def has_a(self, dictofA):

        if dictofA.get('allof') is not None:
            allrequired = dictofA.get('allof')  # array
            if self.either_containsAllof(allrequired):
                pass
            else:
                return False
        if dictofA.get('oneof') is not None:
            onerequired = dictofA.get('oneof')
            if self.either_containsOneOf(onerequired):
                pass
            else:
                return False
        return True

    def has_b(self, dictofB):
        if dictofB.get('allof') is not None:
            allrequired = dictofB.get('allof')  # array
            if self.either_containsAllof(allrequired):
                pass
            else:
                return False

        if dictofB.get('oneof') is not None:
            onerequired = dictofB.get('oneof')
            if self.either_containsOneOf(onerequired):
                pass
            else:
                return False
        return True


    def containsAllof(self, allrequired):
        for v in allrequired:
            for course in v:
                if course in self.arrayTakenCourses[0]:
                    pass
                else:
                    return False
            return True

    def containsOneOf(self, oneofrequired):
        for v in oneofrequired:
            for course in v:
                if course in self.arrayTakenCourses[0]:
                    return True
            return False

    def either_containsAllof(self, allrequired):
        for v in allrequired:
            if v in self.arrayTakenCourses[0]:
                pass
            else:
                return False
        return True

    def either_containsOneOf(self, oneofrequired):
        for v in oneofrequired:
            if v in self.arrayTakenCourses[0]:
                return True
        return False
