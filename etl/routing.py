import sqlite3
from sqlite3 import Error

def assign_H_cases(conn):
    sql = ''' 
        SELECT id, priority, CaseHeaderKey , ParkingTimeMinute, isHandledBy
        FROM cases_caseheader 
        WHERE priority = 'H' 
        ORDER BY ParkingTimeMinute ASC
        '''

    assign = '''
        UPDATE cases_caseheader
        SET isHandledBy = :StaffId
        WHERE id = :CaseHeaderId
    '''

    cur = conn.cursor()
    try:
        cases = cur.execute(sql)
    except Error as e:
        print (e)


    for case in cases:
        AssignedStaffId = get_someone(conn,case[0], case[2])

def get_someone(conn, CaseNo, CaseHeaderKey):
    sql = '''
        SELECT id, MainHandPhoneNo
        FROM users_user
        WHERE Role = 'T'
        AND isAvailable = 1
        AND Rating >= 4
        ORDER BY CurrentCaseCount ASC, Rating
        LIMIT 1
        '''

    assignTask = '''
        UPDATE cases_caseheader
        SET isHandledBy = :StaffId
        WHERE id = :CaseHeaderId
    '''

    cur = conn.cursor()
    cur.execute(sql)

    AssignedStaff = cur.fetchone()
    AssignedStaffId = AssignedStaff[0]
    Contact = AssignedStaff[1]


    assign = '''
        UPDATE users_user
        SET CurrentCaseCount = CurrentCaseCount + 1
        WHERE  id = :StaffId
    '''
    c2 = conn.cursor()
    c2.execute(assign, {'StaffId': AssignedStaffId} )
    
    c3 = conn.cursor()
    c3.execute(assignTask,{'StaffId':AssignedStaffId,'CaseHeaderId':CaseNo})

    #SMS
    print (Contact + " , You have been assigned a task " + str(CaseHeaderKey) +". Please Login to opono for more details.")

    return (Contact)

def update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET priority = ? ,
                  begin_date = ? ,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def main():
    database = "C:\\Users\usilisme\OneDrive\Projects\sia\db.sqlite3"

    # create a database connection
    conn = create_connection(database)
    with conn:
        assign_H_cases(conn)


if __name__ == '__main__':
    main()

