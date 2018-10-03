from midiutil import MIDIFile

def major_scale(start):
    return list([
        start + 0,
        start + 2,
        start + 4,
        start + 5,
        start + 7,
        start + 9,
        start + 11,
        start + 12
    ])

def fib(n):
    old, new = 0, 1
    if n == 0:
        return 0
    for i in range(n-1):
        old, new = new, old + new
    return new

scale = major_scale(start=58) # A
harmony_scale = major_scale(start=34) # A

duration_scale = list([.5, 1., 1.5, 2.])

channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 140   # In BPM
volume   = 90  # 0-127, as per the MIDI standard

midi = MIDIFile(numTracks=2)
#midi.addTempo(0, time, tempo)

next_note = 0.

for i in range(72):
    fib_num = fib(i)

    if i in range(24, 48):
        scale_index = fib_num % len(scale) - 2
        duration = duration_scale[fib_num % len(duration_scale)]
    else:
        scale_index = -1 * (fib_num % len(scale))
        duration = duration_scale[fib_num % len(duration_scale)]

    # melody
    if (i >= next_note):
        midi.addNote(0, channel, scale[scale_index], time + i, duration, volume)
        next_note = i + duration
    
    # harmony
    if i % 2 == 0:
        midi.addNote(1, channel, harmony_scale[scale_index], time + i, 1., volume)
        midi.addNote(1, channel, harmony_scale[(scale_index + 4) % len(harmony_scale)], time + i + 1., 1., volume)

with open("tune2.mid", "wb") as output_file:
    midi.writeFile(output_file)