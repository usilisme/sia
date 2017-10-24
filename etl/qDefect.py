from adapter import create_connection
import atexit
from datetime import datetime
from time import sleep

interval = 5

def main():
	print ('ETL STARTED...')
	InitQueue()
	Init_TechnicianStatistics()
	while True:
		LastRefreshed = datetime.now()
		print('LastRefreshed: '+str(LastRefreshed))
		sleep(interval)
		UpdateQueue(LastRefreshed)
		Assign()

#Initialize Queue if it is empty
def InitQueue():
	conn = create_connection()
	sql_init = '''
		insert into cases_qDefect( TimeSlot_Id, Airplane_Id, Defect_Id, ProblemArea )
		select  tt.id, f.airplane_id, c.id, c.ProblemArea
		FROM cases_timeslot tt
		INNER JOIN flights_parking f ON strftime('%H:%M:%S',f.DateTimeFr) BETWEEN tt.TimeSlotFr AND tt.TimeSlotTo
		INNER JOIN cases_caseHeader c ON f.airplane_id = c.Airplane_id;
	'''
	#WHERE c.Status != 'CLOSED'

	conn.execute(sql_init)
	conn.commit()
	conn.close()
	return None

#Initialize qProfile that shall compute the Stats of Technicians
def Init_TechnicianStatistics():
	conn = create_connection()
	sql_agg = '''
		insert into cases_technicianStatistic(technician_id, ProblemArea, CountSolved, MeanServiceDuration)
		select fixer_id,ProblemArea, count(1), avg(ServiceDuration) 
		from cases_caseheader 
		where status = 'CLOSED' 
		group by fixer_id,ProblemArea;
	'''
	conn.execute('delete from cases_technicianStatistic;')
	conn.commit()
	conn.execute(sql_agg)
	conn.commit()
	conn.close()
	return None

#Update the Queue Real Time depending on the interval if new Defect is registered in the List
def UpdateQueue(LastRefreshed):
	conn = create_connection()
	sql_get = '''
		insert into cases_qDefect( TimeSlot_Id, Airplane_Id, Defect_Id, ProblemArea )
		select  tt.id,f.airplane_id, c.id, c.ProblemArea
		FROM cases_timeslot tt
		INNER JOIN flights_parking f ON strftime('%H:%M:%S',f.DateTimeFr) BETWEEN tt.TimeSlotFr AND tt.TimeSlotTo 
		INNER JOIN cases_caseHeader c ON f.airplane_Id = c.Airplane_id
		WHERE c.CreatedOn > :LastRefreshed;
	'''
	conn.execute(sql_get,{'LastRefreshed':LastRefreshed})
	conn.commit()
	conn.close()
	return None

#Get any unassigned Defects and then allocate Fixer accordingly
def Assign():
	conn = create_connection()
	sql_pre = '''
		select id, TimeSlot_Id , ProblemArea
		from cases_qDefect
		WHERE Fixer_Id is null;
	'''
	cur = conn.cursor()
	defects = cur.execute(sql_pre)
	for defect in defects:
		count = AssignSpecialist(conn,defect[0], defect[1], defect[2])
		if count == 0:
			AssignAny(conn,defect[0], defect[1])
	conn.close()
def AssignSpecialist(conn,qId,TimeSlot,ProblemArea):
	sql_find = '''
		update cases_qDefect
		set fixer_id = (
			select Technician_id
			FROM cases_TechnicianStatistic
			LEFT JOIN (
				select Fixer_Id 
				FROM cases_qDefect 
				WHERE TimeSlot_Id = :TimeSlot
			) t on t.Fixer_Id != Technician_Id 
			where ProblemArea = :ProblemArea
			ORDER BY CountSolved,MeanServiceDuration  
			limit 1
			)
		where id = :qid;
	'''
	c = conn.cursor()
	c.execute(sql_find,{'qid':qId,'TimeSlot':TimeSlot,'ProblemArea':ProblemArea})
	conn.commit()
	return c.rowcount
def AssignAny(conn,qId,TimeSlot):
	sql_find = '''
		update cases_qDefect
		set fixer_id = (
			select Technician_id
			FROM cases_TechnicianStatistic
			LEFT JOIN (
				select Fixer_Id 
				FROM cases_qDefect 
				WHERE TimeSlot_Id = :TimeSlot
			) t on t.Fixer_Id != Technician_Id
			ORDER BY CountSolved,MeanServiceDuration  
			limit 1
			)
		where id = :qid;
	'''
	f = conn.execute(sql_find,{'qid':qId,'TimeSlot':TimeSlot})
	conn.commit()
	return None


#Remove from Queue if it is completed
def CloseQueueItem():
	print('hi')
	return None

#Empty the Queue when the program is off
@atexit.register
def EmptyQueue():
	print('ETL STOPPED...')
	conn = create_connection()
	conn.execute('delete from cases_qDefect;')
	conn.commit()
	conn.execute('delete from cases_qDefect;')
	conn.commit()
	conn.close()
	return None

main()