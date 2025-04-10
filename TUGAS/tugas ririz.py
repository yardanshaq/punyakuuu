boroughs = ("Manhatten", "Bron", "Brooklyn", "Queens", "Staten Island")
minLetters = 100
for borough in boroughs:
    if len(borough) < minLetters:
        minLetters = len(borough)
print("The shortest word has length", minLetters)