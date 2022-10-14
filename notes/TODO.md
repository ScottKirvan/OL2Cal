OL2Cal - TODO
====
Just a spot to keep track of what's being worked on, what may get worked on next, and  what's been done.  

This is not a formal roadmap, or even a prioritized list, just a shorthand I like to use.

TODO
----
- [ ] error reporting  
- [ ] option:  change assumed hrs in day  
- [ ] default config file location?  
- [ ] add support for ical format
- [ ] instead of config file, move each format specific parts to their own modules and use a conditional to use the correct implementation
- [ ] document README.md

In Progress
-----------

Done ✓
------
- [x] add command line parser  
- [x] open specified filename rather than hardcoded one  
- [x] optionally write to file, insted of stdout [default]  
- [x] handle output to file as well as stdout
- [x] get a second format importing (FAM2)

Not Gonna Do ✓
------
- [x] use pattern matching / rules specified in a config file  - the problem is the changes required to parse certain filetypes - I'm thinking this might be abstractable to a certain degree
    - replaced with the idea of using specific module implementations for each format 