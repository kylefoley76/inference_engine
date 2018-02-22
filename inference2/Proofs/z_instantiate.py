



str1 = input("enter sentence:")

#str1 = "(f=abstract) & ((b J f) ≡ ((b I z) ⊻ (b I y) ⊻ (b I x) ⊻ (b I g) ⊻ (b I h) ⊻ (b I j) ⊻ (b I k) ⊻ (b I m) ⊻ (b I w))) & (z=moment) & (y=number) & (x=point) & (g=property) & (h=relationship) & (j=whole) & (k=part) & (m=relation) & (w=symbol) | (b⇒g₁)"

l1 = "\u2081"
l2 = "\u2082"
subscripts = [l1, l2]
mini_c = chr(8658)

instantiations = str1[str1.find("|") + 1:]
str1 = str1[:str1.find("|")-1]

i = -1
while i < len(str1) - 1:
    i += 1
    if i < len(str1) - 2:
        if str1[i] == "=" and str1[i + 2].islower():
            k = str1.rfind("(", 0, i)
            m = str1.find(")",i , len(str1))
            first_half = str1[:k]
            second_half = str1[m + 4:]
            str1 = first_half + second_half
            i = k
            bb = 8

str1 = str1[:str1.rfind(")", 0, len(str1))]

dict1 = {}
for i, letter in enumerate(instantiations):
    if letter == mini_c:
        old_var = instantiations[i - 1]
        new_var = instantiations[i + 1]
        if i < len(instantiations) - 1:
            if instantiations[i+2] in subscripts:
                new_var += instantiations[i + 2]
            if instantiations[i-1] in subscripts:
                old_var = instantiations[i - 2] + instantiations[i - 1]
        if old_var == l1:
            bb = 8
        dict1.update({old_var: new_var})
        assert old_var != l1
        assert new_var != l1

i = -1
while i < len(str1) - 1:
    i += 1
    letter = str1[i]
    subscript = ""
    if i > 500:
        str1 = "error"
        break
    j = 0
    if i < len(str1) - 1:
        if str1[i + 1] == l1:
            letter += l1
            j = 1

    if letter in dict1.keys():
        first_half = str1[:i]
        second_half = str1[i + 1 + j:]
        new_var = dict1.get(letter)
        str1 = first_half + new_var + second_half
        i += j

print (str1)