name = str(input("Hello there! What is your name, I'm cody!: "))

print(f"Nice to meet you {name}!")

mood = input(f"How are you feeling today {name}? :").lower

if mood == "good" or mood == 'great' or mood == "fine":
    print("Oh glad to hear that")

elif mood == "bad" or mood == "not fine" or mood == "not so great":
    print("Oh, I'm sorry")

else:
    print("Sometimes it is difficult to put emotions in words.")

hobby = input("What is your hobby? ").lower()

if hobby != "coding":
    print(f"Okay, {hobby.upper()} is not bad.")
else:
    print(f"Wow even i like {hobby.upper()}")

print("It was nice chatting with you")