import random
d=random.randint(0,4)
que=('A','B','C','D','E')
ans=(1,2,3,4,5)
correct=('F','G','H','I','J')


def kbc(a,b):
    d = random.randint(0,4)
    print(que[d])
    print(ans[d])
    c=0
    lock=input('Lock Answer-')
    if lock in correct:
        print('SHII JAVAB')
        if lock in correct:
            print('Agla Padav')
            c+=1
            # kbc(que, ans)
    elif lock not in correct:
        print('Galat Javaab')
    
    

for i in range(5):
    
    kbc(que, ans)
    
