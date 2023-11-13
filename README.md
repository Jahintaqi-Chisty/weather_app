**Instructions**

 1. Create a virtual environment 
 2. Install requirements.txt
> cd strtive_weather 		
> pip install -r  requirements.txt

3. Then run the django server from project .

> python manage.py runserver

4. I have added swagger for better view.
		
>http://127.0.0.1:8000/swagger/

**API Details and answers**
1. API for the coolest 10 districts based on the average temperature at 2pm for the next 7 days.

> URL: http://127.0.0.1:8000/weather/coolest-districts/
First time it takes around 3 seconds and caching implemented for 1hour .So,for next request it takes 420ms appx.
2. Now as we got the list, where do you want to travel and why?
> According to my running coolest place is Panchagarh and I love cold so I will choose that place.
3.  Let's say your friend wants to travel as well and needs your help. Let's create an API where you take your friend's location, their destination, and the date of travel. Compare the temperature of those two locations at 2 PM on that day and return a response deciding if they should travel there or not.
> Created API for compare temperature
> URL: http://127.0.0.1:8000/compare-temperatures/
> body:{
>"friend_location":"Dhaka",
>"destination_location":"Faridpur",
>"travel_date": "2023-11-14"
>}
Response:
> {
> 
> "friend_location": {
> 
> "district": "Dhaka",
> 
> "latitude": 23.7115253,
> 
> "longitude": 90.4111451,
> 
> "temperature_2pm": 25.5
> 
> },
> 
> "destination_location": {
> 
> "district": "Faridpur",
> 
> "latitude": 23.6070822,
> 
> "longitude": 89.8429406,
> 
> "temperature_2pm": 24.8
> 
> },
> 
> "date": "2023-11-14",
> 
> "travel_recommendation": "Recommended"
> 
> }
>
>Logic for recommendation if temperature is less or equal friend place temperature then it's suitable for travel.