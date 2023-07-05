/auth/register
/auth/login
<!-- /auth/logout -->
/auth/refresh
/auth/user
/auth/verify
/auth/password

<!-- /contacts -->
<!-- /contacts/<pk> -->
/places/<pk>
<!-- /places/<pk>/contacts -->
<!-- /places/<pk>/commments -->
<!-- /places/<pk>/commments/<pk> -->
/places/autocomplete (proxy)
/places/directions (proxy)

/bands
/bands/<band_id>
/bands/<band_id>/users
/bands/<band_id>/users/<banduser_id>
/bands/<band_id>/tours
/bands/<band_id>/tours/<tour_id>
/bands/<band_id>/tours/<tour_id>/users
/bands/<band_id>/tours/<tour_id>/users/<touruser_id>
/bands/<band_id>/tours/<tour_id>/prospects
/bands/<band_id>/tours/<tour_id>/prospects/<prospect_id>
/bands/<band_id>/tours/<tour_id>/prospects/<prospect_id>/logentries
/bands/<band_id>/tours/<tour_id>/prospects/<prospect_id>/logentries/<logentry_id>
/bands/<band_id>/tours/<tour_id>/dates
/bands/<band_id>/tours/<tour_id>/dates/<date_id>
/bands/<band_id>/tours/<tour_id>/dates/<date_id>/lodgings
/bands/<band_id>/tours/<tour_id>/dates/<date_id>/lodgings/<lodging_id>
/bands/<band_id>/tours/<tour_id>/dates/<date_id>/timeslots
/bands/<band_id>/tours/<tour_id>/dates/<date_id>/timeslots/types
/bands/<band_id>/tours/<tour_id>/dates/<date_id>/timeslots/<timeslot_id>
/venues
/venues/types
/venues/<venue_id>/notes
/venues/<venue_id>/notes/<venuenote_id>


How will I handle venues and places?
Does the confirmation process create a new venue for the place? (if none exists)
- venue can be marked public, but ONLY ONE can be public.

How will I contend w changing google data?
- cache expiration: attach a timestamp to every place and implement 

venue types
- Amphitheater
- Arena
- Bar
- Brewpub
- Club
- Coffeehouse
- Fair
- Festival
- House
- Listening Room
- Nightclub
- PAC
- Theater
- Winery
- Other