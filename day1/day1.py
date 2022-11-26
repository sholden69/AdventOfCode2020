import pandas as pd 

def find_two_product(lines) :
  cp=[ (x,y) for x in lines for y in lines]
  print ("searching...",len(cp), "entries")
  for x,y in cp:
    if (int(x)+int(y)==2020):
      print("answer:",x,y,' product:',int(x)*int(y))
  
def find_three_product(lines) :
  cp=[ (x,y,z) for x in lines for y in lines for z in lines]
  print ("searching...",len(cp), "entries")
  for x,y,z in cp:
    if (int(x)+int(y)+int(z)==2020):
      print("answer:",x,y,z,"product:",int(x)*int(y)*int(z))


def main():
  f = open("input.txt")
  lines = f.read().splitlines()
  print(len(lines))
  find_three_product(lines)

if __name__ == "__main__":
  main()