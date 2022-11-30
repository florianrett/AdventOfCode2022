import requests
import days

day = 1
bUseTestInput = True

if bUseTestInput:
    print("Loading test input from file")
    f = open("testinput.txt", "r")
    input = f.read().splitlines()
    f.close()
else:    
    url = 'https://adventofcode.com/2022/day/' + str(day) + '/input'
    print("Loading input from AoC: " + url)

    f = open("sessioncookie.txt", "r")
    aocsession = {'session' : f.read().splitlines()[0]}
    f.close()    
    
    response = requests.get(url, cookies = aocsession)
    if response.status_code == 200:
        input = response.text.split('\n')
        input.pop()
    else:
        print("Web request failed! Check if session cookie is valid")
        print(response.status_code)
        print(response.text)

funcname1 = 'day' + str(day) + 'a'
funcname2 = 'day' + str(day) + 'b'
result = getattr(days, funcname1)(input)
print("Puzzle 1 result:", result)
result = getattr(days, funcname2)(input)
print("Puzzle 2 result:", result)
