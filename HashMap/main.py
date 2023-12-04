
from hash.app_hashmap import HashDictionary

if __name__ == '__main__':

    d = HashDictionary()
    d["value1"] = 1
    d["value2"] = 2
    d["value3"] = 3
    d["1"] = 10
    d["2"] = 20
    d["3"] = 30
    d["1, 5"] = 100
    d["5, 5"] = 200
    d["10, 5"] = 300

    print(d.iloc[0])  # >>> 10
    print(d.iloc[2])  # >>> 300
    print(d.iloc[5])  # >>> 200
    print(d.iloc[8])  # >>> 3


    d1 = HashDictionary()
    d1["value1"] = 1
    d1["value2"] = 2
    d1["value3"] = 3
    d1["1"] = 10
    d1["2"] = 20
    d1["3"] = 30
    d1["(1, 5)"] = 100
    d1["(5, 5)"] = 200
    d1["(10, 5)"] = 300
    d1["(1, 5, 3)"] = 400
    d1["(5, 5, 4)"] = 500
    d1["(10, 5, 5)"] = 600

    print(d1.ploc[">=1"])  # {1=10, 2=20, 3=30}
    print(d1.ploc["<3"])  # >>> {1=10, 2=20}
    print(d1.ploc[">0, >0"])  # >>> {(1, 5)=100, (5, 5)=200, (10, 5)=300}
    print(d1.ploc[">=10,     >0"])  # >>> {(10, 5)=300}
    print(d1.ploc["<5, >=5, >=3"])  # >>> {(1, 5, 3)=400}


