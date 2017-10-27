from datetime import datetime

from rest_framework import serializers
 
from users.serializers import UserSerializer
from cases.models import (
	CaseHeader, CaseHistory
)
from flights.models import(
    Airplane, Parking,
)


class CaseHeaderSerializer(serializers.ModelSerializer):
    #case = serializers.ReadOnlyField(reporter='user.username')

    def create(self,validated_data):
    	case = CaseHeader()
    	hist = CaseHistory()
    	
    	aCaseHeaderKey =  datetime.today().strftime('SQ-%Y%m%d-%H%M%S')
    	aReporter = self.context['request'].user

    	case.CaseHeaderKey = aCaseHeaderKey
    	case.CreatedOn = datetime.today()
    	case.LastUpdOn = datetime.today()
        case.Status = 'OPENED'
        

        vFlightNo = validated_data.get('FlightNo',None)
    	case.FlightNo = vFlightNo
        oAirplane = Parking.objects.all().filter(FlightNoFr = vFlightNo).get().Airplane
        #vAirplane = Airplane.objects.all().filter(RegNo = '9V-SB1').get()
        case.Airplane = oAirplane

        case.Priority = validated_data.get('Priority',None)
    	case.ProblemArea = validated_data.get('ProblemArea',None)
    	case.Title = validated_data.get('Title',None)
    	case.SeatNo = validated_data.get('SeatNo','N.A.')
    	case.ToiletNo = validated_data.get('ToiletNo','N.A.')
    	case.Reporter = aReporter
    	case.save()

    	hist.CaseHeaderKey = aCaseHeaderKey
    	hist.CreatedOn = datetime.today()
    	hist.Description = 'Case '+ aCaseHeaderKey +' is created by '+aReporter.username
    	hist.save()

    	return case

    def update(self,instance,validated_data):
    	StatusFr = instance.Status
    	instance.Status = validated_data.get('Status', instance.Status)
    	StatusTo = instance.Status
    	instance.Feedback = validated_data.get('Feedback', instance.Feedback)
        instance.save()

    	hist = CaseHistory()
    	hist.CaseHeaderKey = instance.CaseHeaderKey
    	hist.CreatedOn = datetime.today()
    	hist.Description = 'Changing the status from '+ StatusFr + ' to ' + StatusTo
    	hist.save()
    	return instance

    class Meta:
        model = CaseHeader
        fields = ('url','id','CaseHeaderKey','CreatedOn'
        		,'LastUpdOn' , 'FlightNo'
        		,'Priority' , 'Status'
        		, 'ProblemArea'
        		,'Title','SeatNo','ToiletNo', 'Reporter'
        		, 'Reporter_Name'
        		, 'Feedback'
                , 'AirplaneNo'
      
        	)
        extra_kwargs = {
            'url': {
                'view_name': 'cases:case-detail',
            }
        }