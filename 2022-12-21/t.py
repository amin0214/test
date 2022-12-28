a = [1,2,3,4]   # list
b = (11,22,33,44)   # tuple

score = {
            '座號': 10,
            '國文': 20, 
            '英文': 30, 
            '數學': 40,
            '姓名': '李大仁'
        }  


(x,y) = list(score.values())[0:2]

print(x,y)
