import random
#sources: looked up eval at
    #source https://www.w3schools.com/python/ref_func_eval.asp#:~:text=The%20eval()%20function%20evaluates,statement%2C%20it%20will%20be%20executed.
    #source https://realpython.com/python-eval-function/ 


#talked/brainstormed with Petros Emmanouilidis and Gongwei Wang for some ways to implement function, but most of implementation is done by myself
#generates a basic arithmetic equation
def getSimpleArithmetic():
    nums=[0,1,2,3,4,5,6,7,8,9]
    operations=["+","-","/","*","%"]
    #gets a random operation and numbers 
    operation=operations[random.randint(0,len(operations)-1)]
    num1=nums[random.randint(0,len(nums)-1)]
    num2=nums[random.randint(0,len(nums)-1)]
    #ensure no division by 0
    while (operation=="%" or operation=="/") and num2==0:
        print("yes")
        num2=nums[random.randint(1,len(nums)-1)]


    #ensure no fraction
    if operation=="/" and num1%num2!=0:
        num1=nums[random.randint(0,len(nums)-1)]*num2

    question=str(num1)+operation+str(num2)
    answer=eval(question)

    #if answer is negative, regenerate equation
    #low recursion depth because it is unlikely to get negative numbers in a row

    return question,int(answer)

def getHarderArithmetic():
    nums=[-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9]
    operations=["+","-","/","*","%","**"]
    #gets a random operation and numbers 
    operation1=operations[random.randint(0,len(operations)-1)]
    operation2=operations[random.randint(0,len(operations)-1)]

    num1=nums[random.randint(0,len(nums)-1)]
    num2=nums[random.randint(0,len(nums)-1)]
    num3=nums[random.randint(0,len(nums)-1)]
    #ensure no division by 0
    while (operation1 in "%/" and num2==0): 
        print("yes")
        num2=nums[random.randint(1,len(nums)-1)]
    
    
    while (operation2 in "%/" and num3==0):
        print("yes")
        num3=nums[random.randint(1,len(nums)-1)]
    
    #ensure that you don't mod by negative numbers
    while (operation1=="%") and num2<0:
        num2=nums[random.randint(10,len(nums)-1)]

    while (operation2=="%") and num3<0:
        num3=nums[random.randint(10,len(nums)-1)]
    #if it is exponenet, make sure the power is not too big
    if operation1=="**":
        num2=random.randint(0,3)
    if operation2=="**":
        num3=random.randint(0,3)

    #ensure no fraction
    question=str(num1)+operation1+str(num2)+operation2+str(num3)
    answer=eval(question)
    #if answer is negative, regenerate equation
    #low recursion depth because it is unlikely to get negative numbers in a row
    if answer>500:
        print("too much")
        return getHarderArithmetic()
    return question,answer

def getHardestArithmetic():
    nums=[-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9]
    operations=["+","-","/","*","%","**"]
    #gets a random operation and numbers 
    operation1=operations[random.randint(0,len(operations)-1)]
    operation2=operations[random.randint(0,len(operations)-1)]
    operation3=operations[random.randint(0,len(operations)-1)]
    

    num1=nums[random.randint(0,len(nums)-1)]
    num2=nums[random.randint(0,len(nums)-1)]
    num3=nums[random.randint(0,len(nums)-1)]
    num4=nums[random.randint(0,len(nums)-1)]
    #ensure no division by 0
    while (operation1 in "%/" and num2==0): 
        print("yes")
        num2=nums[random.randint(1,len(nums)-1)]
    while (operation2 in "%/" and num3==0):
        print("yes")
        num3=nums[random.randint(1,len(nums)-1)]
    while (operation3 in "%/" and num4==0):
        print("yes")
        num4=nums[random.randint(1,len(nums)-1)]
    
     #ensure that you don't mod by negative numbers
    while (operation1=="%") and num2<0:
        num2=nums[random.randint(10,len(nums)-1)]
    while (operation2=="%") and num3<0:
        num3=nums[random.randint(10,len(nums)-1)]
    while (operation3=="%") and num4<0:
        num4=nums[random.randint(10,len(nums)-1)]
    
    #if it is exponenet, make sure the power is not too big
    if operation1=="**":
        num2=random.randint(0,3)
    if operation2=="**":
        num3=random.randint(0,3)
    if operation3=="**":
        num4=random.randint(0,3)

    question=str(num1)+operation1+str(num2)+operation2+str(num3)+operation3+str(num4)
    answer=eval(question)
    #if answer is negative, regenerate equation
    #low recursion depth because it is unlikely to get negative numbers in a row
    if answer>1000:
        print("too much")
        return getHardestArithmetic()
    return question,answer


#disregard it is my attempt at diversifying questions
def getSimpleFraction():
    denominators=[1,2,3,4,5,6,7,8,9]
    neumerators=[-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9]
    numerator1=neumerators[random.randint(0,len(neumerators)-1)]
    numerator2=neumerators[random.randint(0,len(neumerators)-1)]
    demoninator1=denominators[random.randint(0,len(denominators)-1)]
    demoninator2=denominators[random.randint(0,len(denominators)-1)]
    operations=["+","-","/","*"]
    operation=operations[random.randint(0,len(operations)-1)]
    while operation=="/" and numerator2==0:
        numerator2=neumerators[random.randint(0,len(neumerators)-1)]

        

    question=f"({numerator1}/{demoninator1}){operation}({numerator2}/{demoninator2})"
    return question,eval(question)

def getHarderFraction():
    denominators=[1,2,3,4,5,6,7,8,9]
    neumerators=[-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9]
    numerator1=neumerators[random.randint(0,len(neumerators)-1)]
    numerator2=neumerators[random.randint(0,len(neumerators)-1)]
    numerator3=neumerators[random.randint(0,len(neumerators)-1)]

    demoninator1=denominators[random.randint(0,len(denominators)-1)]
    demoninator2=denominators[random.randint(0,len(denominators)-1)]
    demoninator3=denominators[random.randint(0,len(denominators)-1)]

    operations=["+","-","/","*"]
    operation1=operations[random.randint(0,len(operations)-1)]
    operation2=operations[random.randint(0,len(operations)-1)]

    while operation1=="/" and numerator2==0:
        numerator2=neumerators[random.randint(0,len(neumerators)-1)]
    
    while operation2=="/" and numerator3==0:
        numerator3=neumerators[random.randint(0,len(neumerators)-1)]

    question=f"({numerator1}/{demoninator1}){operation1}({numerator2}/{demoninator2}){operation2}({numerator3}/{demoninator3})"
    return question,eval(question)

def getHardestFraction():
    denominators=[1,2,3,4,5,6,7,8,9]
    neumerators=[-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9]
    numerator1=neumerators[random.randint(0,len(neumerators)-1)]
    numerator2=neumerators[random.randint(0,len(neumerators)-1)]
    numerator3=neumerators[random.randint(0,len(neumerators)-1)]
    numerator4=neumerators[random.randint(0,len(neumerators)-1)]
    demoninator1=denominators[random.randint(0,len(denominators)-1)]
    demoninator2=denominators[random.randint(0,len(denominators)-1)]
    demoninator3=denominators[random.randint(0,len(denominators)-1)]
    demoninator4=denominators[random.randint(0,len(denominators)-1)]
    operations=["+","-","/","*"]
    operation1=operations[random.randint(0,len(operations)-1)]
    operation2=operations[random.randint(0,len(operations)-1)]
    operation3=operations[random.randint(0,len(operations)-1)]


    while operation1=="/" and numerator2==0:
        numerator2=neumerators[random.randint(0,len(neumerators)-1)]
    
    while operation2=="/" and numerator3==0:
        numerator3=neumerators[random.randint(0,len(neumerators)-1)]
    
    while operation3=="/" and numerator4==0:
        numerator4=neumerators[random.randint(0,len(neumerators)-1)]

    question=f"({numerator1}/{demoninator1}){operation1}({numerator2}/{demoninator2}){operation2}({numerator3}/{demoninator3}){operation3}({numerator4}/{demoninator4})"
    

    
    return question,eval(question)



print(getHardestFraction())


'''print(getSimpleArithmetic())
print(getHarderArithmetic())
print(getHardestArithmetic())'''

