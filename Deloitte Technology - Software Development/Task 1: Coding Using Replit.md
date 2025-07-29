Task 1: Coding

Task overview - 
What you'll learn - How to help a client reconcile different data sources?
What you'll do - Combine code into a unified format using Python?

----------------------------------------------------------------------------------------------
Here is the background information on your task
We have signed a new account: Daikibo Industrials, a global leader in the manufacturing of heavy machinery, founded and headquartered in Tokyo, Japan. They needed assistance with a variety of problems and were impressed to find out Deloitte could help in all verticals.

Daikibo is in the process of integrating IIoT (industrial internet of things) devices to monitor, measure and analyse their manufacturing processes. Half of their infrastructure uses devices streaming telemetry data in one format, and the other half in another. They need your help to combine the two.
-------------------------------------------**************--------------------------------------------------------

Here is your task - 
Take the following steps to complete the task:

Create an account at repl.it.
Fork this project into your workspace.
After navigating to the project, find the Fork button on the page and press it.
Get acquainted with the 2 data formats by exploring the files (hint: it's the same message, represented in 2 different formats):
data-1.json
data-2.json
Explore the target unified format by looking at the file data-result.json. This is the format you should aim to output in your solution.
Complete the solution located in the file main.py.
The project is set up in a way to test your solution automatically as you run it.

Find the 2 functions in need of implementation and finish them (look for comment lines starting with "IMPLEMENT:").

Use repl.it to run your project and test your solution (look for a big Run button, currently located at the top).

Don't mind the red colour of the console output and the message on failed repl process when you run the project - the important thing is to see no failures in the tests.

Please use comments in main.py, if you need to leave notes on your solution.

Hint: notice the timestamps of the 2 telemetry formats are different, but the target format is exactly like one of them (milliseconds). You will need to convert the other format (ISO) to it. Check the resources for a link to a SO post that can help.

***********************************************************************************************************************
Convert ISO Dates to Milliseconds in Python -

example :
datetime.datetime(2020,2,25,0,2,43).timestamp()
or
import datetime
time = "2020-02-25T00:02:43.000Z"
date = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
timestamp = str((date - datetime.datetime(1970, 1, 1)).total_seconds()*1000)
print(timestamp[:-2])

Python 3: Convert ISO 8601 to milliseconds
--->> @stackoverflow - https://stackoverflow.com/questions/60442518/python-3-convert-iso-8601-to-milliseconds/60443033#60443033

--->> @Replit Overview - https://docs.replit.com/getting-started/intro-replit

