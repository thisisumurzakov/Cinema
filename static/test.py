h,m=int(input()),int(input())
r,k=12-h,60-m
if r==0:r=12
if k==60:k=0
print(r,k)