import music21 as music

music.environment.set('midiPath', '/usr/bin/timidity')

def make_kurki_trzy():
    melody = music.stream.Stream()
    melody = music.converter.parse('tinyNotation: 4/4 C4 C4 G4 G4 A4 A4 G2 F4 F4 E4 E4 D4 D4 C2')
    return melody

def flatten(lst):
    res = []
    for elem in lst:
        res += elem
    return res

def notes_from_melody(melody):
    res = []
    for measure in melody:
        res += measure.notesAndRests.stream()
    return res

def inversion(melody):
    inverted_melody = music.stream.Stream()
    notes = notes_from_melody(melody)
    for i, note in enumerate(notes):
        if i == 0: 
            inverted_melody.append(note)
        else:
            interval = music.interval.Interval(notes[i-1], notes[i])
            previous_note = inverted_melody[i-1]
            transposed_note = previous_note.transpose(-interval.semitones)
            transposed_note.duration = note.duration
            inverted_melody.append(transposed_note)

    return inverted_melody

def main():
    kurki = make_kurki_trzy()
    inverted_kurki = inversion(kurki)
    inverted_kurki.show('midi')
    # inverted_kurki.show()

main()