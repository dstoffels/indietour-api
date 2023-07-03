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
    band_users: [BandUser]
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
