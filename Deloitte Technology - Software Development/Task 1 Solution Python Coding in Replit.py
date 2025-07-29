#Import the necessary modules(Libraries)
import json, unittest, datetime 

#Use the open function to open the file and read the data

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)

#Define the funtion to convert the data from the first format to the second format

def convertFromFormat1 (jsonObject): 
#split the location string into a list of strings using the "/" character as the delemeter and store it in a variable called location using the split method. 
    location = jsonObject["location"].split("/")
    #create a new dictionary with the location date

    location_dict = {
        "country": location[0],
        "city": location[1],
        "area": location[2],
        "factory": location[3],
        "section": location[4]
    }
#create a new dictionary with the date data and store it in a varibale called data_dict 
    data_dict = { "status": jsonObject["operationStatus"], 
                 "temperature": jsonObject["temp"] 
    } 
    result={
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": location_dict, 
#add the location dictionary to the result dictionary using the key location and the value loaction dict
        "data": data_dict 
#add the data dictionary to the result dictionry using the key data and the value data_dict and return the result dictionary using the return staetment at the end of the function to convert the data from the first format to the second format and return the result dicionary.
    } 
    return result 


def convertFromFormat2(jsonObject):
    #convert the ISO timestamp to milliseconds since epoch and store it in a variable called timestamp
    date = datetime.datetime.strptime(jsonObject["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
    timestamp = int(date.timestamp() * 1000) #millisecond conversion

    #create a new dictionary with the location data and store it in a variable called location_dict
    location_dict = {
        "country": jsonObject["country"],
        "city": jsonObject["city"],
        "area": jsonObject["area"],
        "factory": jsonObject["factory"],
        "section": jsonObject["section"]
    }

    #create a new dictionary with the data and store it in a data_dict
    data_dict = jsonObject["data"]

    result = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp,
        "location": location_dict,
        "data": data_dict
    }

    return result

def main (jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()