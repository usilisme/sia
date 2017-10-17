import json, requests
import urllib2

data = {  
   "clientUUID":"AnyUniqueStringToIdentifyTheRequest",
   "request":{  
      "itineraryDetails":[  
         {  
            "originAirportCode":"FCO",
            "destinationAirportCode":"SIN",
            "departureDate":"2017-11-01"
         }
      ],
      "cabinClass":"Y",
      "adultCount":1
   }
}

req = urllib2.Request('https://apidev.singaporeair.com/appchallenge/flight/search')
req.add_header('Content-Type','application/json')
req.add_header('x-api-key','du1yO8KLZm9PfFeg6OHQW8CFcpK1RMym3JXp78Uk')

response = urllib2.urlopen(req, json.dumps(data))

result = json.load(response)

print result['response']['flights'][0]['segments'][0]['legs'][0]['flightNumber']


