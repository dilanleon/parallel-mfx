# 15-112 - project2

Parallel Bandpass Drum Dynamics, Harmonics, and Reverb Processor

Inspired by this video: https://youtu.be/4hGBYs10ZAU?si=jQk2Dl15u7sJtUK1

TL:DW is that this is a technique to make drums sound awesome through dynamics and harmonics processing on a parallel bandpass filter applied to the fundemental frequency.

Uses Spotify's Pedalboard API: https://spotify.github.io/pedalboard/index.html

and impulse response(s) from Chris Warren's EchoThief: http://www.echothief.com/
- more IRs to be included; currently testing functionality

In its current state, only asks the user to select I/O drivers and then begins to play audio. 

TO DO in (more or less) order:
- Implementation of 'knob' and 'fader' classes
- User interactible enabling/disabling of plugins
- Decide on wether to use reverb or convolution, or toggle between them
    - No point in having both at once, as they do the same thing in different ways.
- Decide wether to include clipping or just distortion
- UI layout
- Tying a bunch of knobs to AudioHandler class parameters/functions
- Drop down menus (i.e. for IR select, filter select)
- VU meters?? Maybe impossible maybe very easy?? Haven't experimented
- Verify functionality on Windows/Linux
- Verify functionality through Pro Tools Audio Bridge/other virtual sound drivers
- Figure out VST/AAX support? might be a pipe dream (probably)
- License the IR library for non-private distribution (if vst works)
    - I have sent email to the guy who made the library. We'll see.
- Super duper pretty-fication (like a Universal Audio plugin)
