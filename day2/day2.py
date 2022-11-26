import pandas as pd 



def main():
# todays input file contains lo-hi letter: password 
  df=pd.read_csv("input.txt", sep='\s+',header=None)
  #print(df)
  
  
  for index, row in df.iterrows():
    mandate=row[0]
    letter=row[1]
    pwd=row[2]
    print(mandate,letter,row)
 
if __name__ == "__main__":
  main()