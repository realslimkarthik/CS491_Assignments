import sqlite3

netid = "kharih2.result"

social_db = "./data/social.db"
matrix_db = "./data/matrix.db"
university_db = "./data/university.db"

################################## Queries ##################################


# Names of students in grade 9
query_1 = """select name from student where grade=9 order by name;"""


# Number of students in each grade
query_2 = "select grade, count(name) from student group by grade;"


# Name and grade of students who have more than 2 friends
query_3 = """select student.name, student.grade
from student, friend where student.id = friend.id1
group by student.id
having count(friend.id1) > 2
order by student.name, student.grade;
"""


# Name and grade of students liked by students in a higher grade
query_4 = """select student.name, student.grade
from student, likes
where student.id = likes.id2
and student.grade < (select grade from student where id = likes.id1)
order by student.name, student.grade;"""


# Name and grade of students who don't like anyone or only like their friends
query_5 = """select student.name, student.grade
from student, friend
where student.id = friend.id1 and
student.id not in (select id1 from likes)
or
student.id in (select f.id1
    from friend f, likes l
    where f.id1 = l.id1 and f.id2 = l.id2)
group by student.id
order by student.name, student.grade;
"""


# 
query_6 = """select distinct likes.id1, student.name, likes.id2, s.name
from likes, student, student s, friend
where likes.id1 = student.id and likes.id2 = s.id and likes.id1 = friend.id1 and 
likes.id1 in 
(select id1 from likes where id2 = likes.id2)
and likes.id1 not in
(select id1 from friend where id2 = likes.id2)
order by likes.id1, likes.id2;
"""


query_7 = """select distinct likes.id1 ID1, student.name name1, likes.id2 ID2, s.name name2, fr.id1 ID3, st.name name3
from likes, student, student s, student st, friend, friend fr
where likes.id1 = student.id and likes.id2 = s.id and likes.id1 = friend.id1 and fr.id1 = st.id and
likes.id1 in 
(select id1 from likes where id2 = likes.id2)
and likes.id1 not in
(select id1 from friend where id2 = likes.id2)
and fr.id1 in
(select id1 from friend where id2 = likes.id1 or id2 = likes.id2)
order by likes.id1, likes.id2, fr.id1;
"""


query_8 = """"""


# Average class scores for tenured and untenured professors
query_9 = """select p.tenured, avg(fce.class_score)
from fact_course_evaluation fce, dim_professor p
where fce.professor_id = p.id
group by p.tenured;"""


# Average class scores for all courses, grouped by area over the different years
query_10 = """select t.year, type.area, avg(fce.class_score)
from fact_course_evaluation fce, dim_term t, dim_type type
where fce.term_id = t.id and fce.type_id = type.id
group by t.year, type.area;"""


# Sparse Matrix Multiplication query
query_11 ="""select A.row_num, B.col_num, sum(A.value * B.value)
from A, B
where A.col_num = B.row_num
group by A.row_num, B.col_num;"""

################################################################################

def get_query_list():
    """
    Form a query list for all the queries above
    """
    query_list = []
    for index in range(1, 12):
        eval("query_list.append(query_" + str(index) + ")")
    return query_list
    pass

def output_result(index, result):
    """
    Output the result of query to facilitate autograding.
    Caution!! Do not change this method
    """
    with open(netid, 'a') as fout:
        fout.write("<"+str(index)+">\n")

    with open(netid, 'a') as fout:
        for item in result:
            fout.write(str(item))
            fout.write('\n')

    with open(netid, 'a') as fout:
        fout.write("</"+str(index) + ">\n")
    pass


def init_db(db):
    """
    Function to initialize the connection and cursor objects
    """
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    return connection, cursor


def run():
    ## get all the query list
    query_list = get_query_list()

    ## problem 1
    conn, cur = init_db(social_db)
    for index in range(0, 8):
        cur.execute(query_list[index])
        result = cur.fetchall()
        tag = "q" + str(index + 1)
        output_result(tag, result)
    
    ## problem 2
    conn, cur = init_db(university_db)
    for index in range(8, 10):
        cur.execute(query_list[index])
        result = cur.fetchall()
        tag = "q" + str(index + 1)
        output_result(tag, result)


    ## problem 3
    conn, cur = init_db(matrix_db)
    cur.execute(query_list[10])
    result = cur.fetchall()
    tag = "q" + str(index + 1)
    output_result(tag, result)


if __name__ == '__main__':
    run()
