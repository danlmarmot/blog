Title: Creating a sunrise/sunset calendar in Python
Tags: python
Category: tech
comments: enabled
Slug: sunrise-sunset-calendar
Summary: A Python script to generate an HTML calendar of sunrise and sunset times

Every time daylight savings time ends I get a little sad... because I don't know when the sun will rise and set anymore.

Years ago as one of my first adventures in Python I wrote a small script to spit out an HTML calendar.  It was an ugly 
little script, in some commented out lines I even had *C:\Program\ Files\ (x86)\* blather, and I haven't used Windows for
five years now.  

Last week I had some free time, and I finally modernized the script and made it less embarrassing.

The new improved script:

- Runs on Python 3.5
- Accepts command line arguments for location, year, and timezone
- Follows the US Naval Observatory's guidelines for computing atmospheric refraction
- Factors in daylight savings time changes for the timezone
- Has been refactored into nice tidy functions (ready for unit testing, but I haven't added any yet)
- Produces decent and static HTML

I don't know if the script works for odd cases like polar regions where the sun doesn't rise or set, but the script is
fairly complete.

It's here on Github: [https://github.com/danlmarmot/sunrise-sunset-calendar](https://github.com/danlmarmot/sunrise-sunset-calendar)   

### Example output
And here's [an example of the calendar](https://htmlpreview.github.io/?https://github.com/danlmarmot/sunrise-sunset-calendar/blob/master/sun_calendar_example.html)

Check it out!