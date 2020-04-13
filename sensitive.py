import math
import copy
def network(P,W1,W2):
 A=matrixMul(W1, P)
 for i in range(len(A)):
     for j in range(len(A[i])):
         if A[i][j]<0:
             A[i][j]=0.0
 Z=matrixMul(W2,A)
 Y=softmax(Z)
 return Y

def softmax(x):
   p = x.index(max(x))
   zmax=x[p][0]
   sum=0
   for i in range(len(x)):
       x[i]=math.exp(x[i][0]-zmax)
       sum=sum+x[i]
   for i in range(len(x)):
       x[i]=x[i]/sum
   return x

def matrixMul(A, B):
  res = [[0] * len(B[0]) for i in range(len(A))]
  for i in range(len(A)):
    for j in range(len(B[0])):
     for k in range(len(B)):
       res[i][j] =res[i][j]+A[i][k] * B[k][j]
  return res

def matrixMul2(A, B):
  return [[sum(a * b for a, b in zip(a, b)) for b in zip(*B)] for a in A]

N,M=map(int,input().split())
W1=[]
W2=[]
X=list(map(int,input().split()))
W1=list(map(float,input().split()))
W2= list(map(float, input().split()))


X_temp=[]
for data in X:
    X_temp1 = []
    X_temp1.append(data)
    X_temp.append( X_temp1)
X=X_temp

W1_temp=[]
for i in range(M):
     temp=W1[i*N:(i+1)*N]
     W1_temp.append(temp)
W1= W1_temp

W2_temp=[]
for i in range(10):
     temp=W2[i*M:(i+1)*M]
     W2_temp.append(temp)
W2=W2_temp



Y=0

d=0
label=0 #0 means without change #1 means change
f_noise=0
a=(network(X,W1,W2))
result=a.index(max(a))

for i in range(N):
    for noise in range(-128,128):
      myX=[]
      for data in X:
        myX.append(copy.deepcopy(data))
      myX[i][0]=noise
      new_Y=network(myX,W1,W2)
      new_result= new_Y.index(max(new_Y))
      if new_result!=result and new_Y[new_result]>Y:
             d=i
             label=1
             Y=new_Y[new_result]
             f_noise=noise

if label==0:
      Y=a[result]
      for i in range(N):
          for noise in range(-128, 128):
              myX=[]
              for data in X:
                  myX.append(copy.deepcopy(data))
              myX[i][0] = noise
              new_Y = network(myX, W1, W2)
              new_result = new_Y.index(max(new_Y))
              if new_result ==result and new_Y[new_result] <Y:
                  d = i
                  label = 1
                  Y = new_Y[new_result]
                  f_noise = noise

print(d+1,f_noise)








