sample = [
    {'subject': 'PHYS',
     'catalog_number': '121',
     'units': 0.5,
     'title': 'Mechanics',
     'note': 'Choose TUT section for Related 1.',
     'class_number': 6998,
     'section': 'LEC 001',
     'campus': 'UW U',
     'associated_class': 1,
     'related_component_1': None,
     'related_component_2': None,
     'enrollment_capacity': 200,
     'enrollment_total': 185,
     'waiting_capacity': 0,
     'waiting_total': 0,
     'topic': None,
     'reserves': [],
     'classes': [
         {'date':
              {'start_time': '13:00',
               'end_time': '14:20',
               'weekdays': 'TTh',
               'start_date': None,
               'end_date': None,
               'is_tba': False,
               'is_cancelled': False,
               'is_closed': False},
          'location':
              {'building': 'AL'
                  , 'room': '113'},
          'instructors': ['Epp,Richard J']}
     ],
     'held_with': [],
     'term': 1199,
     'academic_level': 'undergraduate',
     'last_updated': '2019-08-02T15:07:30-04:00'}] ##One class ends here, and next one starts below it


#Useful info: prof name, timing, tutorial timing, enrolment capacity and enrolment total. Prequisites can be seen later or mentioned in side.
# Need prof rating but later.
#First just make a schedule.
#Ask for courses from the user, do not limit the user on the number of courses, make a timetable.
#          Monday
#    (8:30 AM to 9:20AM)
#        PHYS 122
#    ...................
#          .....

from uwaterlooapi import UWaterlooAPI
uw = UWaterlooAPI(api_key="120f4c218136a91d9f0f83d0ce79cca7")

def conv(obj):    ##Solves the problem of error of start-time and end-time being unavailable for any class
    try:
       return int(obj.replace(':',''))
    except Exception: return "N/A"

def oneinother(s1,s2):   #Returns True if s1 in s2 or s2 in s1 else false
                         #Also deals with the problem of section name being not available
   try:
        if len(s1) >= len(s2) and s2 in s1:
            return True
        elif s1 in s2:
            return True
        else: return False

   finally: return False

def sch_imp(subj,no,code):
    secs = []
    api_output = uw.course_schedule(subj, no, term = code)
    for section in api_output:
        en_cap = section['enrollment_capacity']
        en_tot = section['enrollment_total']
        cl_inf = \
            {'course' : section['subject'] + section['catalog_number'],
            'sec_name' : section['section'],
            'instructors' : section['classes'][0]['instructors'],
            'start_time' : conv(section['classes'][0]['date']['start_time']),
            'end_time' : conv(section['classes'][0]['date']['end_time']),
             'days' : section['classes'][0]['date']['weekdays'],
            'avai' : en_cap - en_tot} ##Gives no. of available seats
        secs.append(cl_inf)
    return secs
##this funtion outputs list of dictionaries giving subj name, course no, class no, section

timetable = []

def sch_grouper():
    imp_inf = []
    no_course = int(input("Enter no of Courses: "))
    term_inp = int(input("Input term code: "))
    for x in range(no_course):
        sub_inp = input("Input Subject : ")
        no_inp = int(input("Input Course No: "))
        imp_inf.append(sch_imp(sub_inp,no_inp,term_inp))
    return imp_inf  # Gives a list of lists (first list of highest priority), each containing dictionaries with section info
    #Now need to create a time table, which is basically a list, with first classes coming first,
    # each class represented as a dictionary with start time and end time. Having a tutorial in time table is necessary if
    # there is a tutorial.
    # assume courses are inputed according to priority
    # sch_make should give all the possible combinations in time table.!!!! ---> Should give a list of lists (possible timetables) containing
    # classes in a form of dictionaries. with {'course': -----, 'days' : -------, 'time':--------- , 'instructor' : -----------}



#section_valid(sec): produces a bool value: True if section is valid, False if invalid.
# This function compares sec and Class in timetable on basis of (same course name and same class type)
# or (same days and time conflict)
# or (no space available in class)
def section_valid(sec):
    final = True
    for Class in timetable:
        if (sec['course'] == Class['course'] and sec['sec_name'].split(' ')[0] in Class['sec_name']) or\
                oneinother(Class['days'], sec['days']) and (
                not(sec['end_time'] < Class['start_time'] or sec['start_time'] > Class['end_time'])):
            final = final and False
    return final and sec['avai'] > 0






#wrapper function to make the final timetable
#[[{},{},{}...],[{},{},{}...],...]
def sch_make(cours_inf):
    for course in cours_inf:
        for sec in course:
            if section_valid(sec):
                timetable.append(sec)
    return timetable








a = \
    [[{'course': 'PHYS236',
   'sec_name': 'LAB 001',
   'instructors': ['Taylor,James'],
   'start_time': 1430,
   'end_time': 1550,
   'days': 'MW',
   'avai': 18},
  {'course': 'PHYS236',
   'sec_name': 'LAB 002',
   'instructors': ['Lee,Brenda Yasie'],
   'start_time': 830,
   'end_time': 950,
   'days': 'TTh',
   'avai': 7},
  {'course': 'PHYS236',
   'sec_name': 'TUT 101',
   'instructors': ['Taylor,James'],
   'start_time': 1130,
   'end_time': 1250,
   'days': 'F',
   'avai': 25}],
 [{'course': 'MATH235',
   'sec_name': 'LEC 001',
   'instructors': ['Akash,Mukto'],
   'start_time': 1130,
   'end_time': 1220,
   'days': 'MWF',
   'avai': 0},
  {'course': 'MATH235',
   'sec_name': 'LEC 002',
   'instructors': ['Satriano,Matthew'],
   'start_time': 1530,
   'end_time': 1620,
   'days': 'MWF',
   'avai': 0},
  {'course': 'MATH235',
   'sec_name': 'LEC 003',
   'instructors': ['Webster,Ben'],
   'start_time': 930,
   'end_time': 1020,
   'days': 'MWF',
   'avai': 21},
  {'course': 'MATH235',
   'sec_name': 'LEC 004',
   'instructors': ['Satriano,Matthew'],
   'start_time': 1030,
   'end_time': 1120,
   'days': 'MWF',
   'avai': 1},
  {'course': 'MATH235',
   'sec_name': 'LEC 005',
   'instructors': ['Rubinstein,Michael'],
   'start_time': 1230,
   'end_time': 1320,
   'days': 'MWF',
   'avai': 16},
  {'course': 'MATH235',
   'sec_name': 'TUT 101',
   'instructors': [],
   'start_time': 1730,
   'end_time': 1820,
   'days': 'M',
   'avai': 0},
  {'course': 'MATH235',
   'sec_name': 'TUT 102',
   'instructors': [],
   'start_time': 1730,
   'end_time': 1820,
   'days': 'M',
   'avai': 38},
  {'course': 'MATH235',
   'sec_name': 'TST 201',
   'instructors': [],
   'start_time': 1630,
   'end_time': 1820,
   'days': 'T',
   'avai': 38},
  {'course': 'MATH235',
   'sec_name': 'LEC 081',
   'instructors': ['Vicente Colmenares,Alejandra'],
   'start_time': 'N/A',
   'end_time': 'N/A',
   'days': None,
   'avai': 0}],
 [{'course': 'MATH237',
   'sec_name': 'LEC 001',
   'instructors': ['West,Joseph John'],
   'start_time': 1030,
   'end_time': 1120,
   'days': 'MWF',
   'avai': 0},
  {'course': 'MATH237',
   'sec_name': 'LEC 002',
   'instructors': ['Krivodonova,Lilia'],
   'start_time': 930,
   'end_time': 1020,
   'days': 'MWF',
   'avai': 1},
  {'course': 'MATH237',
   'sec_name': 'LEC 003',
   'instructors': ['West,Joseph John'],
   'start_time': 1230,
   'end_time': 1320,
   'days': 'MWF',
   'avai': 1},
  {'course': 'MATH237',
   'sec_name': 'LEC 004',
   'instructors': ['Garbary,Robert'],
   'start_time': 1230,
   'end_time': 1320,
   'days': 'MWF',
   'avai': 0},
  {'course': 'MATH237',
   'sec_name': 'LEC 005',
   'instructors': ['Garbary,Robert'],
   'start_time': 1530,
   'end_time': 1620,
   'days': 'MWF',
   'avai': -2},
  {'course': 'MATH237',
   'sec_name': 'TUT 101',
   'instructors': [],
   'start_time': 1630,
   'end_time': 1720,
   'days': 'W',
   'avai': 1},
  {'course': 'MATH237',
   'sec_name': 'TUT 102',
   'instructors': [],
   'start_time': 1630,
   'end_time': 1720,
   'days': 'W',
   'avai': -1},
  {'course': 'MATH237',
   'sec_name': 'TST 201',
   'instructors': [],
   'start_time': 1630,
   'end_time': 1820,
   'days': 'T',
   'avai': 0}],
 [{'course': 'CS136',
   'sec_name': 'LEC 001',
   'instructors': ['Tompkins,Dave'],
   'start_time': 1000,
   'end_time': 1120,
   'days': 'TTh',
   'avai': 9},
  {'course': 'CS136',
   'sec_name': 'LEC 002',
   'instructors': ['Tompkins,Dave'],
   'start_time': 1130,
   'end_time': 1250,
   'days': 'TTh',
   'avai': 9},
  {'course': 'CS136',
   'sec_name': 'LEC 003',
   'instructors': ['Tompkins,Dave'],
   'start_time': 1430,
   'end_time': 1550,
   'days': 'TTh',
   'avai': -1},
  {'course': 'CS136',
   'sec_name': 'TUT 101',
   'instructors': [],
   'start_time': 1130,
   'end_time': 1220,
   'days': 'M',
   'avai': 17},
  {'course': 'CS136',
   'sec_name': 'TUT 102',
   'instructors': [],
   'start_time': 1330,
   'end_time': 1420,
   'days': 'M',
   'avai': 0},
  {'course': 'CS136',
   'sec_name': 'TUT 103',
   'instructors': [],
   'start_time': 1230,
   'end_time': 1320,
   'days': 'M',
   'avai': 13},
  {'course': 'CS136',
   'sec_name': 'TUT 104',
   'instructors': [],
   'start_time': 1630,
   'end_time': 1720,
   'days': 'M',
   'avai': 15},
  {'course': 'CS136',
   'sec_name': 'TUT 105',
   'instructors': [],
   'start_time': 830,
   'end_time': 920,
   'days': 'M',
   'avai': 11},
  {'course': 'CS136',
   'sec_name': 'TST 201',
   'instructors': [],
   'start_time': 1900,
   'end_time': 2050,
   'days': 'M',
   'avai': 56}],
 [{'course': 'AMATH251',
   'sec_name': 'LEC 001',
   'instructors': ['Lamb,Kevin G'],
   'start_time': 830,
   'end_time': 950,
   'days': 'TTh',
   'avai': 10},
  {'course': 'AMATH251',
   'sec_name': 'TUT 101',
   'instructors': [],
   'start_time': 1130,
   'end_time': 1220,
   'days': 'T',
   'avai': 10}],
 [{'course': 'STAT240',
   'sec_name': 'LEC 001',
   'instructors': ['Jagannath,Aukosh'],
   'start_time': 1430,
   'end_time': 1550,
   'days': 'TTh',
   'avai': 23},
  {'course': 'STAT240',
   'sec_name': 'TST 101',
   'instructors': ['Jagannath,Aukosh'],
   'start_time': 1630,
   'end_time': 1820,
   'days': 'Th',
   'avai': 23}]]



