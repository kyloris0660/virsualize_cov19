import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


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


def process(T, E, I, R, S, N=1400000000, r=2, sigma=1/14):
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


if __name__ == '__main__':
    S1, E1, I1, R1 = process(74, r=18, E=0, I=1, R=0, S=1399999999, sigma=1/14)
    S2, E2, I2, R2 = process(150 - 74, r=2, E=E1[74], I=I1[74], R=R1[74], S=S1[74], sigma=1/4)
    # 显示日期
    plt.figure(figsize=(10, 6))
    import pandas as pd

    xs = pd.date_range(start='20191124', periods=74 + 1, freq='1D')  # 生成2020-02-11类型的日期数组（）
    # print(xs)
    xs2 = pd.date_range(start='20200206', periods=150 - 74 + 1, freq='1D')

    # plt.plot(S_t, color='blue', label='Susceptibles')#, marker='.')
    plt.plot(xs, E1, color='grey', label='Exposed', marker='.')
    plt.plot(xs2, E2, color='grey', label='Exposed Prediction')
    plt.plot(xs, I1, color='red', label='Infected', marker='.')
    plt.plot(xs2, I2, color='red', label='Infected Prediction')
    plt.plot(xs, I1 + R1, color='green', label='Infected + Removed', marker='.')
    plt.plot(xs2, I2 + R2, color='green', label='Cumulative Infections Prediction')
    plt.legend()
    plt.show()
