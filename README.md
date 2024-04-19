# 15-112 - project2

<b>MultiFX Processor</b>

Originally inspired by this video: https://youtu.be/4hGBYs10ZAU?si=jQk2Dl15u7sJtUK1

TL:DW is that this is a technique to make drums sound awesome through dynamics and harmonics processing on a parallel bandpass filter applied to the fundemental frequency.
Equivalent signal chain in Pro Tools:

<img width="158" alt="image" src="https://github.com/dilanleon/project2/assets/92342633/0a0b2908-764c-4a6b-b9bb-fabe0e1648fa">

Uses Spotify's Pedalboard API: https://spotify.github.io/pedalboard/index.html

Ambiances by EchoThief: http://www.echothief.com/

Displays a toggleable list of effects, dry/wet mutes, and effect parameters that update in realtime

TO DO in (more or less) order:
- Convolution select
- Finish adding other filter modes
- Compressor Makeup Gain
- LFOs capable of targeting any knob
- Figure out how to access the data within the AudioStream
- VU meters?? Maybe impossible maybe very easy?? Haven't experimented
- Verify functionality on Windows/Linux
