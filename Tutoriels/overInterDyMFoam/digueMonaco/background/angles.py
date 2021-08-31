#!/usr/bin/env python3

from pandas import read_csv, DataFrame
from numpy import pi, arccos, arcsin, arctan, cos, genfromtxt, arange

from scipy.interpolate import interp1d

if __name__ == "__main__":

    data = read_csv("orientation.csv")
    times = genfromtxt("times.csv")
            
    a2 = data["a2"].values
    a3 = data["a3"].values
    b2 = data["b2"].values
    c2 = data["c2"].values 

    beta = arcsin(-a2)*180/pi
    gamma = arctan(c2/b2)*180/pi
    alpha = arcsin(a3/cos(beta))*180/pi

    df = DataFrame(data = [times, alpha, beta, gamma]).transpose()
    df.columns = ["temps","alpha", "beta", "gamma"]
    df.to_csv("angles.csv", index = False)
