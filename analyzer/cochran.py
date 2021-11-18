from . import util
import os
import numpy
import math

def cochran(path):
    z_score = 1.96**2
    moe = 0.05**2
    bm_cochran={}
    for _d in os.listdir(path):
        data = util.parse_input(f"{path}/{_d}")[f"{path}/{_d}"]
        results={}
        for file in data:
            last4 = file.rows[-4:len(file.rows)]
            for row in last4:
                if row.zone not in results:
                    results[row.zone]=[]
                results[row.zone].append(float(row.power_j))
        zcochran=[]
        for zone,values in results.items():
            mean = numpy.mean(values)
            std = numpy.std(values)
            #top = 1.96 * std
            #error = mean * 0.005
            #temp_cochran = (top/error)**2
            #zcochran.append(math.ceil(temp_cochran))

            print(std)
            temp_cochran = (z_score * std * (1-std)) / moe
            zcochran.append(math.ceil(temp_cochran))
            print(temp_cochran)
        bm_cochran[_d] = max(zcochran)
    print(bm_cochran)