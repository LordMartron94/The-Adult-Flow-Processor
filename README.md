# Adult Flow Processor

- [Purpose](#purpose)
- [Installtion](#installation)
- [Features](#features)

## Purpose
The purpose of this project is to aid me with my porn workflow. Most of the "software" functions as a middleman between other applications, automating much of what I need for my adult content flow.

At the moment of writing this, my workflow is as follows:
- *CTBREC* (https://mastodon.cloud/@ctbrec) records the streams of models I like on several sites (Stripchat, Cam4, Chaturbate, etc.)
- *The Adult Flow Processor* (thiso project) remuxes those streams from `.ts` into `.mp4`, renames it according to a configurable naming scheme and merges stream segments (based on a configurable time between segments) together into streams before moving them into a specifiable location. A NAS in my case.
- *Stash* (https://stashapp.cc/) serves as a variant of Plex for my porn. It is my private private Netflix. Stash scans the contents of my porn locations (on my NAS) and displays them in a web interface so I can watch them. Really worth looking into.

Eventually, I probably want to replace Stash with my own software, but that is for into the future.

## Installation
Download the source code for your desired platform and configure the options in `constants.py`. 
Eventually I will make executables for the platforms. (Most likely, the Linux edition will also work on Windows).

Editing the code to better suit your workflow is allowed, however, if you upload it somewhere, it would be nice if you could credit me as the original author.

### Requirements
Python is needed for this to work, obviously, so it must be installed on your system, either as a virtual environment or globally.

## Features
### Workflow Optimization Features:
1. **Consolidation and Transfer:**
   - Consolidates stream segments from each model into complete streams.
   - Transfers consolidated streams to a designated location, with customizable locations.
2. **Segment Renaming:**
   - Allows renaming of individual segments to a specified format, enhancing organization.
3. **Contact Sheet Generation:**
   - Generates contact sheets for both streams and individual segments, upon request.
4. **Segment Management:**
   - Transfers loose segments to a specified location, facilitating organization.

### User-Friendly Interface Features:
5. **Progress and Command Display:**
   - Displays merge progress and commands for better user understanding.

### Advanced Configuration Features:
6. **Segment Age Control:**
   - Sets the minimal age of a segment before merging, preventing premature consolidation based on age (in days).
7. **Automated Cleanup:**
   - Deletes original segments after merging, streamlining the workflow if specified.
8. **Sheet Regeneration:**
   - Regenerates contact sheets for moved videos if specified, ensuring up-to-date picture overviews.
9. **Corruption Handling:**
   - Deletes videos identified as corrupt by ffmpeg if specified, maintaining data integrity.