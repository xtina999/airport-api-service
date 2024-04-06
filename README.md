# Airport api service
>The "Airport API Service" repository contains the software implementation of a service designed for viewing routes, airports, airplanes, and providing the ability to book tickets. It also allows you to create city, airplane_type, airport, airplane, route, crew, flight, order, ticket for system management. 


### Features
***

- JWT authenticated
- Admin panel /admin/
- Documentation is located at /api/doc/swagger/
- Managing orders and tickets
  - "ticket": "http://127.0.0.1:8000/api/airport/ticket/"
  - "order": "http://127.0.0.1:8000/api/airport/order/"
- Creating airport with city
  - "airport": "http://127.0.0.1:8000/api/airport/airport/"
  - "city": "http://127.0.0.1:8000/api/airport/city/"
- Create flight with route, airplane, crew
  - "airport": "http://127.0.0.1:8000/api/airport/airport/"
  - "route": "http://127.0.0.1:8000/api/airport/route/"
  - "flight": "http://127.0.0.1:8000/api/airport/flight/"
  - "airplane": "http://127.0.0.1:8000/api/airport/airplane/"
  - "crew": "http://127.0.0.1:8000/api/airport/crew/"
- Creating airplane_type
  - "airplanetypes": "http://127.0.0.1:8000/api/airport/airplanetypes"
- Filtering airport, flight, route
  - Example: /airport/?closest_big_city=1, /flight/?source=1&destination=2, /routes/?source=1&destination=2
- Adding tickets available and count taken seats for flight
 

### Installing using GitHub
***
Install PostgresSQL and create db



### Run with docker
***
Docker should be installed

```shell
docker-compose build
docker-compose up
```

### Getting access
***

- create user via /api/user/register/
- get access token via /api/user/token
***
##### DB structure:
