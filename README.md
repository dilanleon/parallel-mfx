# 15-112 - project2

<b>Parallel Bandpass Drum Dynamics, Harmonics, and Reverb Processor</b>

Inspired by this video: https://youtu.be/4hGBYs10ZAU?si=jQk2Dl15u7sJtUK1

TL:DW is that this is a technique to make drums sound awesome through dynamics and harmonics processing on a parallel bandpass filter applied to the fundemental frequency.
Equivalent signal chain in Pro Tools:

<img width="158" alt="image" src="https://github.com/dilanleon/project2/assets/92342633/0a0b2908-764c-4a6b-b9bb-fabe0e1648fa">


Uses Spotify's Pedalboard API: https://spotify.github.io/pedalboard/index.html

Ambiances by EchoThief: http://www.echothief.com/

Currently, displays a togleabble list of effects, with dry/wet fader knobs and a drive knob.
All (most) functionality is working as expected and the only thing left is object-based implementation (EZPZ)

TO DO in (more or less) order:
- UI layout and implementation (functions already made)
- Fix killing of audioThread
- Does it really need clipping? make a decision about that
- Make it look not like shit
- Hover effects (so satisfying)
- 'Switch' class capable of toggling between two plugins for a given spot in the signal chain
- Figure out how to access the data within the AudioStream
- VU meters?? Maybe impossible maybe very easy?? Haven't experimented
- Drop down menus (i.e. for IR select, filter select)
- Verify functionality on Windows/Linux
- Figure out VST/AAX support? might be a pipe dream (probably)
- Super duper pretty-fication (like a Universal Audio plugin)