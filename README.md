# indietour-api

**AUTH**

User: (encoded in JWT)
{
    email,
    username,
    email_verified: bool,
    active_band_id: uuid,
    active_tour_id: uuid,
}

# /auth/login
- POST -> JWT
    - body: {email, password}

# /auth/refresh
- POST -> JWT
    - body: {refresh: (JWT refresh)}

# /auth/user
- PATCH -> JWT
    - body: {username|active_band_id|active_tour_id}

<!-- /auth/logout -->

# /auth/register
- POST -> JWT
    - body: {email, password, username}

# /auth/verify
- POST -> JWT
    - body: {verification_code}
- GET -> str

# /auth/password
- POST -> JWT
    - body: {old_password, new_password}

**BANDS**
Band:
{
    id,
    name,
    is_archived,
    owner: User
    users: [BandUser]
    *tours: [Tour]
}

BandUser:
{
    id,
    is_admin,
    user: User,
}

- params: (for all non-nested band endpoints excl. /users)
    - include (optional): Options for nesting depth. No nesting by default. 
        - options: all|tours|dates

# /bands (filtered by owner_id)
- params:
    - archives: Set true to include archived bands
- POST -> [Band] 
    - body: {name}
- GET -> [Band]

# /bands/<pk>
- GET -> Band
- PATCH -> Band
    - body: {name|is_archived}
- DELETE

# /bands/<pk>/users
- POST -> Band
    - body: {email, is_admin}

# /bands/<pk>/users/<pk>
- PATCH -> Band
    - body {is_admin}
- DELETE -> Band

**TOURS**
Tour:
{
    id,
    name,
    is_archived,
    users: [TourUser]
    *dates: [Date]
}

TourUser:
{
    id,
    banduser: BandUser
}

- params: (for all non-nested tour endpoints excl. /users)
    - include: Options for nesting depth. No nesting by default. 
        - options: all, dates, contacts, prospects, timeslots

# /bands/<pk>/tours (filtered by band_id)
- params:
    - archives: Set true to include archived tours
- POST -> [Tour]
    - body: {name}
- GET -> [Tour]

# /bands/<pk>/tours/<pk>
- GET -> Tour
- PATCH -> Tour
    - body: {name, is_archived}
- DELETE

# /bands/<pk>/tours/<pk>/users
- POST -> Tour
    - body: {email, is_admin}

# /bands/<pk>/tours/<pk>/users/<pk>
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
# /bands/<pk>/tours/<pk>/dates (filtered by tour_id)
- params: 
    - include: Options for nesting depth. No nesting by default
        - options: all, contacts, prospects, timeslots
- POST -> [Date]
    - body: {date}
- GET -> [Date]

# /bands/<pk>/tours/<pk>/dates/<pk>
- GET -> Date (nested)
- PATCH -> Date (nested)
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

# /bands/<pk>/tours/<pk>/dates/<pk>/timeslots
- POST -> Date (nested)
    - body: {description, start_time, starts_after_midnight|origin|end_time|ends_after_midnight|destination|details|type}
# /bands/<pk>/tours/<pk>/dates/<pk>/timeslots/<pk>
- PATCH -> Date (nested)
    - body: {description|start_time|starts_after_midnight|origin|end_time|ends_after_midnight|destination|details|type}
- DELETE -> Date (nested)
# <!-- /bands/<pk>/tours/<pk>/dates/<pk>/prospects -->
# <!-- /bands/<pk>/tours/<pk>/dates/<pk>/prospects/<pk> -->
# <!-- /bands/<pk>/tours/<pk>/dates/<pk>/prospects/<pk>/notes -->
# <!-- /bands/<pk>/tours/<pk>/dates/<pk>/prospects/<pk>/notes/<pk> -->
# <!-- /bands/<pk>/tours/<pk>/dates/<pk>/contacts -->
# <!-- /bands/<pk>/tours/<pk>/dates/<pk>/contacts/<pk> -->
# <!-- /contacts -->
# <!-- /contacts/<pk> -->

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
# <!-- /places/<pk>/contacts -->
# <!-- /places/<pk>/commments -->
# <!-- /places/<pk>/commments/<pk> -->
# /places/autocomplete (proxy)
- GET -> Google Places API predictions obj
# /places/directions (proxy)
- GET -> Google Directions API directions obj
