import music21 as music
import copy
import itertools
import random

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
    return list(melody.recurse().notesAndRests)

def melody_of_notes(notes):
    melody = music.stream.Stream()
    for note in notes:
        melody.append(note)
    return melody

def merge_melodies(melodies):
    melody = music.stream.Stream()
    for m in melodies:
        for n in m.recurse().notes:
            melody.append(copy.deepcopy(n))
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

# transformations - pair of unary and binary transforming functions
def generate_variants(melody, transformations):
    variants = set()
    variants.add(melody)
    
    unary_transformations, binary_transformations = transformations
    for i, transformation in enumerate(unary_transformations):
        new_variants = [transformation(m) for m in variants]
        variants |= set(new_variants)
    for i, transformation in enumerate(binary_transformations):
        new_variants = []
        print(i)
        for j in transformation[1]:
            print(j)
            new_variants += [instantiate_binary_transformation(transformation[0], j)(copy.deepcopy(m)) for m in variants]
        variants |= set(new_variants)
    return variants         
        
def instantiate_binary_transformation(transformation, k):
    return lambda m: transformation(m, k)

def get_transformations(unary_transformations, binary_transformations):
    transformations = copy.deepcopy(unary_transformations)
    for transformation in binary_transformations:
        for j in transformation[1]:
            transformations.append(instantiate_binary_transformation(transformation[0], j))
    return transformations
        
UNARY_TRANSFORMATIONS = [inversion, retrogradation]
BINARY_TRANSFORMATIONS = [(tempo_change, [2, 4, 8, 1/2, 1/4, 1/8]),
                          (transposition, list(range(-12, 12)))]
TRANSFORMATIONS = (UNARY_TRANSFORMATIONS, BINARY_TRANSFORMATIONS)

SAMPLES = 500
LENGTH = 40

# r == length // len(melody)
def gen_domain(variants, r):
    domain = []
    domain += list(itertools.combinations(variants, r))
    return domain

def main():
    kurki = make_kurki_trzy()

    variants = list(generate_variants(kurki, TRANSFORMATIONS))
    # print(len(variants))
    # print('variants:')
    # for i, variant in enumerate(variants):
    #     print(i)
    #     variant.show('text')
    #     print()
        
    # domain = gen_domain(variants, 8)
    
    domain = []
    r = LENGTH // len(kurki)
    for _ in range(SAMPLES):
        domain += [random.sample(variants, r)]
    
    print('number of combinations:')
    print(len(domain))
    # for i in range(SAMPLES):
    #     print(i)
    #     melody = merge_melodies(domain[i])
    #     # melody.show('midi')
    #     print('domain merged to melody:')
    #     melody.show('text')
        # melody.show()
    merge_melodies(domain[0]).show()

main()