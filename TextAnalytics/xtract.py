import glob
import re


def extract_defects(filename):
	row_defects = ['seat','carpet','tray','recliner']
	toilet_defects = ['flush', 'lock', 'mirror']

	f = open(filename)


	lines = f.read().lower().split('\n')
	
	#Assume first line is the aircraft number
	m = re.search('\w+-\w+',lines[0])
	AirCraftNo = m.group(0)
	
	#Assume second line is the header of the message
	#DO NOTHING

	#Assume the remaining lines are the issues.
	#Assume there is only two category, Row_Defects, Toilet_Defects
	for line in lines[2:]:
		print line
		isRowDefect = False
		seatNo = ''
		isToiletDefect = False
		isAirConUnit = False
		defect = 'Unknown'

		if 'ACU'in line:
			isAirConUnit = True
			defect = 'AirConditioner'
			break

		for term in row_defects:
			if term in line:
				isRowDefect = True
				defect = term
				seatNo = re.search('\d+\w', line).group(0)
				break
		for term in toilet_defects:
			if term in line:
				isToiletDefect = True
				defect = term
				break

		print isRowDefect
		print seatNo
		print isToiletDefect
		print isAirConUnit
		print defect

def main():
	
	for f in glob.glob('*.txt'):
		extract_defects(f)

main()

