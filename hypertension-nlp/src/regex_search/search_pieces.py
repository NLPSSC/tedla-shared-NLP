import re

note_group_to_term_data = """
heart failure with reduced ejection fraction
hfref
heart failure with preserved ejection fraction
hfpef
hyponatremia
low sodium
low na
hypokalemia
lower k
hypo k
low k
hyperkalemia
hyper k
hyperuricemia
ua high
hyper ua
uric acid elevated
hypercalcemia
hyper ca
high ca
high calcium
gout
gouty flare
impotence
ed
erectile disfunction
dry cough
nonproductive cough
angioedema
lip swelling
tongue swelling
face swelling
pregnancy
positive hgc
pregnant
flushing
facial erythema
gingival hypertrophy
gum swelling
tachycardia
increased heart rate
inc hr
elevated hr
bradycardia
low hr
decreased heart rate
headache
h/a
ha
constipation
parasomnia
vivid dreams
nightmare
insomnia
poor sleep
hallucinations
fatigue
tired
dizziness
light headedness
nausea
vomiting
n/v
weight gain
increased weight
inc. wt.
shortness of breath
sob
doe
dyspnea on exertion
sick sinus syndrome
decreased libido
dec. libido
sexual side effect
sexual se
gynecomastia
breast enlargement
mastodynia
breast pain
orthostatic hypotension
low bp
low blood pressure
syncope
passed out
falling out
somnolence
drowsiness
excessive sleepiness
dryness of the mouth
dry mouth
parkinsonian symptoms
parkinsonism
symptoms of parkinson
hyperprolactinemia
increased prolactin
hepatotoxicity
liver toxicity
increased lfts
increased liver function tests
lupus-like syndrome
positive ana
lupus symptom
lupus sx
hirsutism
excessive facial hair
urinary urgency
urgency
medication adherence
weight reduction
weight loss
increase in exercise
physical activity
low salt intake
low sodium
low alcohol intake
ascvd score
"""

pieces = [x for x in note_group_to_term_data.split("\n") if x.strip() != ""]
pieces.sort(key=lambda x: len(x), reverse=False)
# pieces = [x for x in pieces if "wt" in x]

regex_pattern = r"|".join(re.escape(piece) for piece in pieces)
regex_pattern = r"(?:\b" + regex_pattern + r")(?![a-zA-Z0-9])"

pattern = re.compile(regex_pattern, flags=re.IGNORECASE)

# should match
for piece in pieces:
    assert pattern.match(piece) is not None, f"Pattern should match '{piece}'"

# should not match
for extra in ["x", "1"]:
    for piece in pieces:
        should_not_match = piece[0:2] + extra + piece[2:]
        assert (
            pattern.match(should_not_match) is None
        ), f"Pattern should not match '{should_not_match}'"

print("")
print("")
print(pattern.pattern)
print("")
print("")
