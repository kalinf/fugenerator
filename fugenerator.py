import music21 as music
import copy

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

def tempo_change(melody, k):
    notes = notes_of_melody(melody)
    for note in notes:
        note.duration = music.duration.Duration(note.duration.quarterLength * k)
    return melody_of_notes(notes)

def notes_of_melody(melody):
    return list(melody.notesAndRests)

def melody_of_notes(notes):
    melody = music.stream.Stream()
    for note in notes:
        melody.append(note)
    return melody

def inversion(melody):
    inverted_melody = music.stream.Stream()
    notes = notes_of_melody(melody)
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

def transposition(melody, interval):
    transposed_melody = music.stream.Stream()
    notes = notes_of_melody(melody)
    for note in notes:
        transposed_melody.append(note.transpose(interval))
    return transposed_melody

def retrogradation(melody):
    notes = notes_of_melody(melody)
    notes.reverse()
    return melody_of_notes(notes)

def augmentation(melody, k):
    return tempo_change(melody, k)
    
def diminution(melody, k):
    return tempo_change(melody, 1/k)

# transformations - list of unary transforming funcktions
def generate_variants(melody, transformations, iterations):
    variants = [melody]
    old_variants = variants
    for i in range(iterations):
        new_variants = []
        for transformation in transformations:
            new_variants += [transformation(m) for m in old_variants]
        variants += new_variants # chyba chcę usuwać powtórzenia
        old_variants = new_variants
    return variants         
        
def instantiate_binary_transformation(transformation, k):
    return lambda m: transformation(m, k)

def get_transformations(unary_transformations, binary_transformations):
    transformations = copy.deepcopy(unary_transformations)
    for transformation in binary_transformations:
        for j in range(transformation[1], transformation[2]):
            transformations.append(instantiate_binary_transformation(transformation[0], j))
    return transformations
        
UNARY_TRANSFORMATIONS = [inversion, retrogradation]
BINARY_TRANSFORMATIONS = [(transposition, -12, 13),
                          (augmentation, 2, 5), 
                          (diminution, 2, 9)]

def main():
    kurki = make_kurki_trzy()
    # new_kurki = transposition(kurki, 2)
    # new_kurki.show('midi')
    # new_kurki.show()
    transformations = get_transformations(UNARY_TRANSFORMATIONS, BINARY_TRANSFORMATIONS)
    variants = generate_variants(kurki, transformations, 3)
    print(len(variants))
    # for variant in variants:
    #     print(variant)

main()