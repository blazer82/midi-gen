from fractions import Fraction
from midiutil import MIDIFile

def decimal(fraction, n_digits):
    int_part = int(fraction)
    remaining_fraction = fraction - int_part
    digits = int(remaining_fraction*10**n_digits)
    result = ("{int}.{digits:0"+str(n_digits)+"d}").format(int=int_part, digits=digits)
    return result

def arctan(fraction, precision):
    result = fraction
    numerator = fraction
    denominator = 1
    for n in range(precision):
        numerator *= fraction**2
        denominator += 2
        result += (-1)**(n+1) * Fraction(numerator, denominator)
    return result

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

p = 768
feynmanPi = 16 * arctan(Fraction(1, 5), p) - 4 * arctan(Fraction(1, 239), p)
pi_digits = list(map(lambda c: int(c), list("{}".format(decimal(feynmanPi, p)).replace(".", ""))))

scale = major_scale(start=60) # C
harmony_scale = major_scale(start=36) # C

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
    pi_num = pi_digits[i]

    if i in range(24, 48):
        scale_index = pi_num % len(scale) - 2
        duration = duration_scale[pi_num % len(duration_scale)]
    else:
        scale_index = -1 * (pi_num % len(scale))
        duration = duration_scale[pi_num % len(duration_scale)]

    # melody
    if (i >= next_note):
        midi.addNote(0, channel, scale[scale_index], time + i, duration, volume)
        next_note = i + duration
    
    # harmony
    if i % 2 == 0:
        midi.addNote(1, channel, harmony_scale[scale_index], time + i, 1., volume)
        midi.addNote(1, channel, harmony_scale[(scale_index + 4) % len(harmony_scale)], time + i + 1., 1., volume)

with open("tune3.mid", "wb") as output_file:
    midi.writeFile(output_file)