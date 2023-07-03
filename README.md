# indietour api

<!-- ## Contents
### Endpoints
- [Authentication](#authentication)
    - [Login](#login)
    - [Refresh JWT](#refresh-jwt)
    - [Update User](#update-user)
    - [Register New User](#register-new-user)
    - [Verify User Email](#verify-user-email)
    - [Change Password](#change-password)
- [Band](#band)
    - [Bands](#bands)
    - [Band Detail](#band-detail)
    - [Band Users](#band-users)
- [Tour](#tour)
    - [Tours](#tours)
    - [Tour Detail](#tour-detail)
    - [Tour Users](#tour-users)
- [Date](#date) 
    - [Dates](#dates) 
    - [Date Detail](#date-detail)  -->


&nbsp;
&nbsp;
# Authentication
All auth endpoints return a JWT with the User object encoded within:

JWT Response Body
```json
{
    "refresh": "<REFRESH TOKEN>",
    "access": "<ACCESS TOKEN>"
}
```

Decoded User object
```json
{
    "email": "example@site.com",
    "username": "Bob",
    "email_verified": true,
    "active_band_id": "5e54b079-4302-41e6-bc53-1cffb3a45545",
    "active_tour_id": "7cbf34ac-d750-4973-93a7-012433ced43b",
}
```

&nbsp;
## Login
**Path**  
```markdown
/auth/login
```
**POST**  

Request Body:
```json
{
    "email": "example@site.com",
    "password": "password1@"
}
```
&nbsp;
## Refresh JWT
**Path**  
```markdown
/auth/refresh
```
**POST**

Request Body:
```json
{
    "refresh": "<REFRESH TOKEN>"
}
```

&nbsp;
## Update User
**Path**  
```markdown
/auth/user
```
**PATCH**

Request Body:
```json
{
    "username": "Robert",
    "active_band_id": "aa32f727-82ea-470f-882b-4649aee2a36d",
    "active_tour_id": "aa32f727-82ea-470f-882b-4649aee2a36d",
}   
```

&nbsp;
## Register New User
**Path**  
```markdown
/auth/register
```
**POST**

Request Body:
```json
{
    "email": "bob@bob.com",
    "password": "password1@",
    "username": "Bobert"
}
```

&nbsp;
## Verify User Email
**Path**
```markdown
/auth/verify
```

**POST**

Request Body:
```json
{
    "verification_code": "592353"
}
```



**GET**

Response Body:
```json
{
    "detail": "An email with a new verification code has been sent to dan.stoffels@gmail.com. "
}
```

&nbsp;
## Change Password
**Path**
```markdown
/auth/password
```

**POST**

Request Body:
```json
{
    "old_password": "PxwbSaef6Eh1",
    "new_password": "Spades42!"
}
```

&nbsp;
&nbsp;
# Band
## Collection
    **Path** 
    ```markdown
    /bands
    ```

    **POST**

    Request Body
    ```json
    {
        "name": "Bob's Band"
    }
    ```
    Params
    ```markdown
    /bands?include=tours
    ```
    Returns the band resource with a nested array of its tours.
    ```markdown
    /bands?include=dates
    ```
    Returns the band resource with a nested array of its tours, each with a nested array of their tour dates.

    - params:
        - archives: Set true to include archived bands
    - GET -> [Band]

## Resource
# /bands/<band_id>
- GET -> Band
- PATCH -> Band
    - body: {name|is_archived}
- DELETE

# /bands/<band_id>/users
- POST -> Band
    - body: {email, is_admin}

# /bands/<band_id>/users/<banduser_id>
- PATCH -> Band
    - body {is_admin}
- DELETE -> Band

**TOURS**
Tour:
{
    id,
    name,
    is_archived,
    tour_users: [TourUser]
    *dates: [Date]
}

TourUser:
{
    id,
    banduser: BandUser
}

- params: (for all non-nested tour endpoints excl. /users)
    - include: Options for nesting depth. No nesting by default. 
        - options: all, dates
    - past-dates: Set true to include past dates.

# /bands/<band_id>/tours (filtered by band_id)
- params:
    - archived_tours: Set true to include archived tours
- POST -> [Tour]
    - body: {name}
- GET -> [Tour]

# /bands/<band_id>/tours/<tour_id>
- GET -> Tour
- PATCH -> Tour
    - body: {name, is_archived}
- DELETE

# /bands/<band_id>/tours/<tour_id>/users
- POST -> Tour
    - body: {email, is_admin}

# /bands/<band_id>/tours/<tour_id>/users/<touruser_id>
- DELETE -> Tour

**DATES**

Date:
{
    id,
    date: YYYY-MM-DD,
    notes,
    is_show_day,
    is_confirmed,
    title,
    tour_id,
    place: Place
    *timeslots: [Timeslot]
    *prospects: [Prospect]
    *contacts: [DateContact]
}
# /bands/<band_id>/tours/<tour_id>/dates (filtered by tour_id)
- params
    - past-dates: Set true to include past dates.
- POST -> Tour
    - body: {date}

# /bands/<band_id>/tours/<tour_id>/dates/<date_id>
- GET -> Date
- PATCH -> Date
    - body: {date|notes|is_show_day|is_confirmed|title|place_id}
- DELETE

**TIMESLOTS**

Timeslot:
{
    id,
    description,
    start_time: HH:MM:SS,
    starts_after_midnight: bool,
    origin: Place,
    end_time: HH:MM:SS,
    ends_after_midnight: bool,
    destination: Place,
    details,
    type_options: ['Event', 'Travel', 'Flight', 'Meeting']
    type: (type_option - default: 'Event')
}

# /bands/<band_id>/tours/<tour_id>/dates/<date_id>/timeslots
- POST -> Date
    - body: {description, start_time, starts_after_midnight|origin|end_time|ends_after_midnight|destination|details|type}
# /bands/<band_id>/tours/<tour_id>/dates/<date_id>/timeslots/<pk>
- PATCH -> Date
    - body: {description|start_time|starts_after_midnight|origin|end_time|ends_after_midnight|destination|details|type}
- DELETE -> Date
<!-- # /bands/<band_id>/tours/<tour_id>/dates/<date_id>/prospects -->
<!-- # /bands/<band_id>/tours/<tour_id>/dates/<date_id>/prospects/<prospect_id> -->
<!-- # /bands/<band_id>/tours/<tour_id>/dates/<date_id>/prospects/<prospect_id>/confirm -->
<!-- # /bands/<band_id>/tours/<tour_id>/dates/<date_id>/prospects/<prospect_id>/notes -->
<!-- # /bands/<band_id>/tours/<tour_id>/dates/<date_id>/prospects/<prospect_id>/notes/<prospectnote_id> --> -->
<!-- # /contacts -->
<!-- # <!-- /contacts/<contact_id> -->

**PLACES** 
Places are fetched directly from the Google Place API by place_id, formatted and stored in the database, when fetched for the first time.

Place:
{
    id,
    name,
    formatted_address,
    political_address,
    lat,
    lng,
}

# /places/<pk>
- GET -> Place
# <!-- /places/<place_id>/contacts -->
# <!-- /places/<place_id>/contacts/<contact_id> -->
# <!-- /places/<place_id>/commments -->
# <!-- /places/<place_id>/commments/<placecomment_id> -->
# /places/autocomplete (proxy)
- GET -> Google Places API predictions obj
# /places/directions (proxy)
- GET -> Google Directions API directions obj
