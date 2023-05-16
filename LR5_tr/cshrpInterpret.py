import clr
import os

pathDLLSort = os.getcwd() + "\\pythonCompile.dll"
pathDLLByte = os.getcwd() + "\\Bytes.dll"


clr.AddReference(pathDLLSort)
clr.AddReference(pathDLLByte)

# Bubble Sort Started

from pythonCompile import BubbleSort

import System

print(BubbleSort)


arr = [5, 2, 9, 1, 5, 6]
cs_arr = System.Array.CreateInstance(System.Int32, len(arr))
for i, x in enumerate(arr):
    cs_arr[i] = x
BubbleSort.Sort(cs_arr)
for i in range(len(arr)):
    arr[i] = cs_arr[i]

print(arr)

print(clr.GetClrType(System.Object).Assembly.ImageRuntimeVersion)
# Bubble Sort Ended



#Byte Code Strted

import Bytes

print(Bytes)

from Bytes import ByteCode

bytes_c = [104, 101, 108, 108, 111]
string = ByteCode.ConvertBytesToString(bytes_c)
print(string)  # "hello"

bytes_b = [77, 121, 32, 78, 97, 109, 101, 32, 105, 115, 32, 86, 108, 97, 100]
string_2 = ByteCode.ConvertBytesToString(bytes_b)

print(string_2) #My Name is Vlad ...