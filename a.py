import random
d=random.randint(0,4)
que=('A','B','C','D','E')
ans=(1,2,3,4,5)
correct=('F','G','H','I','J')


def kbc(a,b):
    
    c=0
    for i in range(5):
        d = random.randint(0,4)
        print(que[d])
        print(ans[d])
        lock=input('Lock Answer-')
        if lock in correct:
            print('SHII JAVAB \n')
            print("--"*10)
            print('Agla Padav')
            c+=1
            
        else:
            print('Galat Javaab')
            print("--"*10)
            break
        
    print(f"Your score is {c} and u earn ${c*100}")
    
        


kbc(que,ans)
    
