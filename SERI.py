import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from sbsk import *


def SEIR(inivalue, _, beta1, beta2, gamma, sigma, r, N):
    X = inivalue
    Y = np.zeros(4)
    # S数量
    Y[0] = - (r * beta1 * X[0] * X[2]) / N - (r * beta2 * X[0] * X[1]) / N
    # E数量
    Y[1] = (r * beta1 * X[0] * X[2]) / N + (r * beta2 * X[0] * X[1]) / N - sigma * X[1]
    # I数量
    Y[2] = sigma * X[1] - gamma * X[2]
    # R数量
    Y[3] = gamma * X[2]
    return Y


def process(T, E, I, R, N=1400000000, r=2, sigma=1 / 14):
    S = N - I - R
    beta1 = 0.02  # 真实数据拟合得出
    beta2 = 0.021 / 3  # 0.007
    # r2 * beta2 = 2
    # sigma = 1 / 14  # 1/14, 潜伏期的倒数
    gamma = 1 / 7  # 1/7, 感染期的倒数
    prem = [S, E, I, R]
    Res = odeint(SEIR, prem, np.arange(0, T + 1), args=(beta1, beta2, gamma, sigma, r, N))
    S = Res[:, 0]
    E = Res[:, 1]
    I = Res[:, 2]
    R = Res[:, 3]
    return S, E, I, R


def draw_little_elephant(r1, r2, population, inflect=1):
    start_date = 23
    S1, E1, I1, R1 = process(start_date, r=r1, N=population, E=0, I=inflect, R=0, sigma=1 / 14)
    S2, E2, I2, R2 = process(167, r=r2, N=population, E=E1[start_date], I=I1[start_date], R=R1[start_date], sigma=1 / 4)
    temp1 = [R1[i] + I1[i] for i in range(len(R1))]
    temp2 = [R2[i] + I2[i] for i in range(len(R2))]
    return temp1 + temp2[1:]



# def draw_elephant(regulation_date, vaccine_date, population, r):



if __name__ == '__main__':
    #
    # S1, E1, I1, R1 = process(74, r=18, E=0, I=1, R=0, sigma=1 / 14)
    # S2, E2, I2, R2 = process(167, r=2, E=E1[74], I=I1[74], R=R1[74], sigma=1 / 4)
    # S3, E3, I3, R3 = process(300, r=9, E=0, I=1, R=0, sigma=1 / 14)
    # # 显示日期
    # plt.figure(figsize=(10, 6))
    # import pandas as pd
    #
    # xs = pd.date_range(start='20191124', periods=74 + 1, freq='1D')  # 生成2020-02-11类型的日期数组（）
    # # print(xs)
    # xs2 = pd.date_range(start='20200206', periods=167 + 1, freq='1D')
    # xs3 = pd.date_range(start='20200206', periods=148, freq='1D')
    # xs4 = pd.date_range(start='20190624', periods=300 + 1, freq='1D')
    #
    # # plt.plot(S_t, color='blue', label='Susceptibles')#, marker='.')
    # plt.plot(xs, E1, color='grey', label='Exposed', marker='.')
    # plt.plot(xs2, E2, color='grey', label='Exposed Prediction')
    # # plt.plot(xs4, E3, color='yellow', label='Without intervention')
    # plt.plot(xs, I1, color='red', label='Infected', marker='.')
    # plt.plot(xs2, I2, color='red', label='Infected Prediction')
    # # plt.plot(xs4, I3, color='yellow', label='Without intervention')
    # plt.plot(xs, I1 + R1, color='green', label='Infected + Removed', marker='.')
    # plt.plot(xs2, I2 + R2, color='green', label='Cumulative Infections Prediction')
    # # plt.plot(xs4, I3 + R3, color='coral', label='Without intervention')
    #
    # plt.plot(xs[48::], realData[:27:], color='blue', label='Real')
    # plt.plot(xs3, realData[26::], color='blue')
    #
    # plt.legend()
    # plt.show()
    print(draw_little_elephant(18, 2, 1400000000, 1))
