from adapter import create_connection
import atexit
from datetime import datetime
from time import sleep

#Planner Program Refresh Interval in seconds
interval = 10

##BEGINING OF THE MAIN PROGRAM
def main():
	print ('Defect Planning STARTED...')
	
	#Collecting Datasets and Produce Queue.
	InitQueue()

	#Re-Collecting Statistical Data from Past Defect List
	Init_TechnicianStatistics()
	
	while True:
		LastRefreshed = datetime.now()
		print('LastRefreshed: '+str(LastRefreshed))
		sleep(interval)
		
		#Listening whether there is a new incoming Defect
		Listen(LastRefreshed)

		#Update the Task Queue based on the latest defect Status
		UpdateQueue(LastRefreshed)
			
		#Filter only defects that requires attention. No Fixer or No Parts
		#Order is determined by priority defined.
		sql_pre = '''
			select
				q.id, 
				q.TimeSlot_Id , 
				q.ProblemArea, 
				q.Defect_Id, 
				q.Status,
				q.ServicingPort,
				q.Airplane_Id,
				q.DeadlineTime
			from cases_qDefect q
			INNER JOIN cases_CaseHeader cc
				ON q.Defect_id = cc.id
			WHERE q.Fixer_Id is null
			OR isPartAvailable = 0
			OR q.Status != 'TRANSFERRED'
			ORDER BY cc.Priority;
		'''
		conn = create_connection()
		cur = conn.cursor()
		defects = cur.execute(sql_pre)

		#Main Section: Processing each Defects in the working queue.		
		for defect in defects:
			TimeLeft = datetime.strptime(str(defect[7]),'%H:%M:%S') - datetime.strptime(LastRefreshed.strftime('%H:%M:%S'),'%H:%M:%S')

			#Find the fixer, first check any specialist available. if not anyone.
			fixer_id = AssignSpecialist(conn,defect[1], defect[2])
			if fixer_id == None:
				fixer_id = AssignAny(conn,defect[0], defect[1])

			#Check if part is available.
			isPartAvailable = CheckPart(conn,defect[0],defect[3])

			#Check if it is neccessary to transfer problem elsewhere
			#e.g. if there is no part or if there is not enought time left.			
			nextPort = defect[5]
			print defect[4]
			if defect[4] == 'TRANSFERRED' or TimeLeft < 30:
				nextPort = Transfer(conn,defect[5],defect[6])
				print(nextPort)
				if nextPort == None:
					nextPort = defect[5]


			sql_upd = '''
				UPDATE cases_qDefect
				SET isPartAvailable = :isPartAvailable
					,fixer_id = :fixer_id
					,ServicingPort = :nextPort
				WHERE id = :qid
			'''
			conn.execute(sql_upd,{
					'qid': defect[0],
					'isPartAvailable': isPartAvailable,
					'fixer_id':fixer_id,
					'nextPort':nextPort,
				}
			)
			conn.commit()
		#Loop till there is not more tasks require attention.
		conn.close()
##ENDING OF THE MAIN PROGRAM

#Initialize Queue if it is empty
def InitQueue():
	conn = create_connection()
	sql_init = '''
		insert into cases_qdefect( TimeSlot_Id, Airplane_Id, Defect_Id, 
		ProblemArea ,Status, ServicingPort, DeadlineTime
		)
		select  tt.id, f.airplane_id, c.id, 
		c.ProblemArea , 'SCHEDULED', PortTo, time(f.DateTimeTo)
		FROM cases_timeslot tt
		INNER JOIN flights_parking f ON time(f.DateTimeFr) BETWEEN tt.TimeSlotFr AND tt.TimeSlotTo
		INNER JOIN cases_caseHeader c ON f.airplane_id = c.Airplane_id
		WHERE PortTo = 'SIN';
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
def Listen(LastRefreshed):	
	conn = create_connection()
	sql_get = '''
		insert into cases_qDefect( TimeSlot_Id, Airplane_Id, Defect_Id, 
		ProblemArea, Status , ServicingPort, DeadlineTime
		)
		select  tt.id, f.airplane_id, c.id, 
		c.ProblemArea , 'SCHEDULED', PortTo, time(f.DateTimeTo)
		FROM cases_timeslot tt
		INNER JOIN flights_parking f ON time(f.DateTimeFr) BETWEEN tt.TimeSlotFr AND tt.TimeSlotTo
		INNER JOIN cases_caseHeader c ON f.airplane_id = c.Airplane_id
		WHERE PortTo = 'SIN'
		AND c.CreatedOn > :LastRefreshed;
	'''
	conn.execute(sql_get,{'LastRefreshed':LastRefreshed})
	conn.commit()
	conn.close()
	return None

#Update the Task Queue based on the latest defect Status
def UpdateQueue(LastRefreshed):
	#Removed Closed Cases 
	conn = create_connection()
	sql_del = '''
		DELETE FROM cases_qDefect 
		WHERE defect_id IN (
			SELECT id
			FROM cases_CaseHeader 
			WHERE Status = 'CLOSED'
		);
	'''
	conn.execute(sql_del)
	conn.commit()

	conn.close()
	return None

#Assign Fixer to Defect based on their speciality.
def AssignSpecialist(conn,TimeSlot,ProblemArea):
	sql_sel = '''
			select Technician_id
			FROM cases_TechnicianStatistic
			LEFT JOIN (
				select Fixer_Id 
				FROM cases_qDefect 
				WHERE TimeSlot_Id = :TimeSlot
			) t on t.Fixer_Id != Technician_Id 
			where ProblemArea = :ProblemArea
			ORDER BY CountSolved,MeanServiceDuration  
			limit 1;
	'''
	c = conn.cursor()
	c.execute(sql_sel,{'TimeSlot':TimeSlot,'ProblemArea':ProblemArea})
	r = c.fetchone()
	if r==None:
		return None
	else:
		return r[0]

#Assign Any available fixer to the defects.
def AssignAny(conn,qId,TimeSlot):
	sql_sel = '''
			select Technician_id
			FROM cases_TechnicianStatistic
			LEFT JOIN (
				select Fixer_Id 
				FROM cases_qDefect 
				WHERE TimeSlot_Id = :TimeSlot
			) t on t.Fixer_Id != Technician_Id
			ORDER BY CountSolved,MeanServiceDuration  
			limit 1;
	'''
	c = conn.cursor()
	c.execute(sql_sel,{'TimeSlot':TimeSlot,})
	r = c.fetchone()
	if r==None:
		return None
	else:
		return r[0]

#Determine availability based on the Part_ID and StockQty
def CheckPart(conn,qid,Defect_Id):
	sql_check = '''
		SELECT StockQty
		FROM cases_Part p
		INNER JOIN cases_CaseHeader_Part cp ON p.id = cp.Part_Id 
		WHERE cp.CaseHeader_Id = :Defect_Id
	'''
	c = conn.cursor()
	r = c.execute(sql_check,{'Defect_Id':Defect_Id}).fetchone()
	if(r[0]>0):
		return True
	else:
		return False

#Handle interruptions by Supervisor, in case part not available for example
#When Technician missed the deadline, the task queue will be reassigned to the next Port
def Transfer(conn,PortFr,Airplane_Id):
	sql_sel = '''
		SELECT PortTo
		FROM flights_Parking
		WHERE PortFr = :PortFr
		AND Airplane_Id = :Airplane_Id
		ORDER BY DateTimeFr
		LIMIT 1;
	'''
	cur = conn.cursor()
	r = cur.execute(sql_sel,{'PortFr':PortFr,'Airplane_Id':Airplane_Id}).fetchone()
	
	if r==None:
		return None
	else:
		return r[0]
	return None


	


#Remove from Queue if it is completed
def CloseQueueItem():
	print('hi')
	return None

#Empty the Queue when the program is off
#@atexit.register
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