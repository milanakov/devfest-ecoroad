EcoRoute Planner

EcoRoute Planner is a small web application that calculates how much CO2 a user saves by choosing a greener transport option instead of driving a car. The app takes a start point, an end point, and an eco-friendly transport mode, and then returns the route distance, estimated CO2 savings, and earned reward points.

Features:
Enter start and end locations as text or coordinates
Select an eco-friendly transport option
Backend geocodes the inputs and requests a route from OpenRouteService
Distance is used to calculate CO2 savings and points
Clean interface with several planned future features shown as placeholders

How it works:
The frontend sends a request to the backend with start, end and selected transport mode.
The Flask backend geocodes both locations using OpenRouteService.
ORS routing is requested with fallback through multiple profiles (cycling, walking, driving).
The returned distance is used to compute saved CO2.
Points are assigned as one point per gram of CO2 saved.
The result is returned to the frontend and displayed to the user.

Technology:
Python and Flask
JavaScript, HTML and CSS
OpenRouteService API for geocoding and routing

Setup:
Install required packages:
pip install flask flask-cors geopy openrouteservice
Insert your OpenRouteService API key into app.py:
ORS_API_KEY = “eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjgyOGYxNGQ4YzE1YzQxN2Q4ZWQyNTg2MjE3ZjVjODA4IiwiaCI6Im11cm11cjY0In0=”

Run the backend:
python app.py
Open index.html in a browser to use the frontend.

Emission factors used (kg CO2 per km)
Car 0.20–0.25

Bus 0.08

E-bike 0.004–0.01

E-scooter 0.015

Bicycle 0

Walking 0

These values are based on DEFRA, EEA and published LCA studies.

Future extensions planned:
Multi-city route planning
Public transport transfer routing
Detailed segment-level emissions
Combined reasonability scores
Eco-streaks and achievement rewards

Lovable interface:
https://id-preview--6a6a7ab5-037d-4210-a47f-7526a574ce1f.lovable.app/?__lovable_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiQ201ZzAwVUg1Uk4wNFozemNaUlNzekZuT2NpMSIsInByb2plY3RfaWQiOiI2YTZhN2FiNS0wMzdkLTQyMTAtYTQ3Zi03NTI2YTU3NGNlMWYiLCJub25jZSI6ImM4NTViNjljMWY4NDBmYTJjODc2ODVlNDFjYWU3Y2M1IiwiaXNzIjoibG92YWJsZS1hcGkiLCJzdWIiOiI2YTZhN2FiNS0wMzdkLTQyMTAtYTQ3Zi03NTI2YTU3NGNlMWYiLCJhdWQiOlsibG92YWJsZS1hcHAiXSwiZXhwIjoxNzY1NjQwMTA0LCJuYmYiOjE3NjUwMzUzMDQsImlhdCI6MTc2NTAzNTMwNH0.fJdUZr-ikUhWKE29fmKUnHsGCHlU44Ck_iYTWEI2BUY
