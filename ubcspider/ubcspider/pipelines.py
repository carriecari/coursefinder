# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from json import loads
import re

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import json
from sqlalchemy.orm import sessionmaker

#from CScourseHelper.SQLdb.Courses import *

class UbcspiderPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        #self.add_to_db()
        self.file.close()

    def process_item(self, item, spider):
        processeditem = self._process_long_prereq(item)
        line = json.dumps(dict(processeditem)) + "\n"
        self.file.write(line)
        return processeditem


    def _process_long_prereq(self, item):

        reqGroups = {}
        andEitherDict = {}

        # REGEX patterns
        andPattern = '(?i)(?:and )'
        orPattern = '(?i)(?:or)'
        eitherorPattern = '(?i)(?:and )?Either'
        oneOfPattern = '(?i)(?:one of)'
        allOfPattern = '(?i)(?:all of)'
        coursePattern = '(\w{4}\s\d{3,4})'

        # returns processed string of prereqs from Course Item
        longprereqs = item.get('prereqs')

        # if there are no prereqs just return item
        if longprereqs is None:
            return item

        # EFFECTS: process string of prereqs by splitting string at 'and either'

        elif re.search(eitherorPattern, longprereqs[0]):

            afterEitherSplit = re.split(eitherorPattern, longprereqs[0], maxsplit=0, flags=0)
            requiredPrereqs = afterEitherSplit[0]
            otherPrereqs = afterEitherSplit[1]

            # EFFECTS: process required segment
            if re.search(andPattern, requiredPrereqs):
                requiredAndSplit = re.split(andPattern, requiredPrereqs)
                for r in requiredAndSplit:
                    LoO = []
                    if re.search(oneOfPattern, r):
                        oneofList = re.findall(coursePattern, r, flags=0)
                        LoO.append(oneofList)
                        if reqGroups.get('oneof'):
                            reqGroups['oneof'].append(oneofList)
                        else:
                            reqGroups['oneof'] = LoO

                    elif re.search(allOfPattern, r):
                        allofList = re.findall(coursePattern, r, flags=0)
                        LoO.append(allofList)
                        if reqGroups.get('allof'):
                            reqGroups['allof'].append(allofList)
                        else:
                            reqGroups['allof'] = LoO
                    else:
                        allofList = re.findall(coursePattern, r, flags=0)
                        LoO.append(allofList)
                        if reqGroups.get('allof'):
                            reqGroups['allof'].append(allofList)
                        else:
                            reqGroups['allof'] = LoO

                    reqGroups['oneof'] = LoO

                item['required'] = reqGroups


            # EFFECTS: process other prereqs
            if re.search(orPattern, otherPrereqs):
                otherPrereqsOrSplit = re.split(orPattern, otherPrereqs)

                firstOtherPrereq = otherPrereqsOrSplit[0]
                secondOtherPrereq = otherPrereqsOrSplit[1]

                childA = {}
                childB = {}

                if re.search(andPattern, firstOtherPrereq):
                    andSplit = re.split(andPattern,
                                        firstOtherPrereq)  # list of strings: ['(b) all of CPSC 260, EECE 320', 'one of CPSC 210, EECE 210, EECE 309.'
                    for s in andSplit:
                        if re.search(oneOfPattern, s):
                            oneofList = re.findall(coursePattern, s, flags=0)
                            childA['oneof'] = oneofList
                            andEitherDict['a'] = childA
                        elif re.search(allOfPattern, s):
                            allofList = re.findall(coursePattern, s, flags=0)
                            childA['allof'] = allofList
                            andEitherDict['a'] = childA
                        else:
                            allofList = re.findall(coursePattern, s, flags=0)
                            childA['allof'] = allofList
                            andEitherDict['a'] = childA

                    item['andEither'] = andEitherDict

                # (a) CPSC 221
                # else has no and pattern. Does not get split, only processed.
                else:
                    if re.search(oneOfPattern, firstOtherPrereq):
                        oneofList = re.findall(coursePattern, firstOtherPrereq, flags=0)
                        childA['oneof'] = oneofList
                    elif re.search(allOfPattern, firstOtherPrereq):
                        allofList = re.findall(coursePattern, firstOtherPrereq, flags=0)
                        childA['allof'] = allofList
                    else:
                        allofList = re.findall(coursePattern, firstOtherPrereq, flags=0)
                        childA['allof'] = allofList

                    andEitherDict['a'] = childA

                if re.search(andPattern, secondOtherPrereq):
                    andSplit = re.split(andPattern,
                                        secondOtherPrereq)  # list of strings: ['(b) all of CPSC 260, EECE 320', 'one of CPSC 210, EECE 210, EECE 309.'
                    for s in andSplit:
                        if re.search(oneOfPattern, s):
                            oneofList = re.findall(coursePattern, s, flags=0)
                            childB['oneof'] = oneofList

                        elif re.search(allOfPattern, s):
                            allofList = re.findall(coursePattern, s, flags=0)
                            childB['allof'] = allofList

                        else:
                            allofList = re.findall(coursePattern, s, flags=0)
                            childB['allof'] = allofList
                        andEitherDict['b'] = childB

                    item['andEither'] = andEitherDict



                # (a) CPSC 221 
                # (a) CPSC 221
                # (b) all of CPSC 260, EECE 320.
                else:
                    if re.search(oneOfPattern, secondOtherPrereq):
                        oneofList = re.findall(coursePattern, secondOtherPrereq, flags=0)
                        childB['oneof'] = oneofList
                    elif re.search(allOfPattern, secondOtherPrereq):
                        allofList = re.findall(coursePattern, secondOtherPrereq, flags=0)
                        childB['allof'] = allofList
                    else:
                        allofList = re.findall(coursePattern, secondOtherPrereq, flags=0)
                        childB['allof'] = allofList

                    andEitherDict['b'] = childB
                    item['andEither'] = andEitherDict

            #item['required'] = reqGroups
            #item['andEither'] = andEitherDict
            return item

        elif re.search(andPattern, longprereqs[0]):

            afterAndSplit = re.split(andPattern, longprereqs[0], maxsplit=0, flags=0)

            for c in afterAndSplit:
                LoO = []

                if re.search(oneOfPattern, c):
                    oneofList = re.findall(coursePattern, c, flags=0)
                    LoO.append(oneofList)
                    if reqGroups.get('oneof'):
                        reqGroups['oneof'].append(oneofList)
                    else:
                        reqGroups['oneof'] = LoO

                elif re.search(allOfPattern, c):
                    allofList = re.findall(coursePattern, c, flags=0)
                    LoO.append(allofList)
                    if reqGroups.get('allof'):
                        reqGroups['allof'].append(allofList)
                    else:
                        reqGroups['allof'] = LoO
                else:
                    allofList = re.findall(coursePattern, c, flags=0)
                    LoO.append(allofList)
                    if reqGroups.get('allof'):
                        reqGroups['allof'].append(allofList)
                    else:
                        reqGroups['allof'] = LoO

                item['required'] = reqGroups
            # item['andEither'] = andEitherDict

            return item


        else:
            LoO = []

            if re.search(oneOfPattern, longprereqs[0]):
                oneofList = re.findall(coursePattern, longprereqs[0], flags=0)
                LoO.append(oneofList)
                reqGroups['oneof'] = LoO
            elif re.search(allOfPattern, longprereqs[0]):
                allofList = re.findall(coursePattern, longprereqs[0], flags=0)
                LoO.append(allofList)
                reqGroups['allof'] = LoO
            else:
                allofList = re.findall(coursePattern, longprereqs[0], flags=0)
                LoO.append(allofList)
                reqGroups['allof'] = LoO

            item['required'] = reqGroups
            # item['andEither'] = andEitherDict

            return item




