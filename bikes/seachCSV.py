import pandas as pd

def main():

    bikeDF=pd.read_csv('clistchicago310.csv')
    print(bikeDF.head())
    print(len(bikeDF))


if __name__ == "__main__":
    main()

