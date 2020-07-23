import numpy as np
from scipy.integrate import odeint
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from sbsk import *


def dict2list(dist):
    df = pd.DataFrame(dist).fillna('null')
    return df.values.tolist()


def SEIR(inivalue, _, beta1, beta2, gamma, sigma, r, N):
    """
    simple SEIR model.
    :param inivalue: X
    :param _: any
    :param beta1: 感染者传染给易感者的概率
    :param beta2: 潜伏者感染易感者的概率
    :param gamma: 康复概率
    :param sigma: 潜伏者转化为感染者的概率
    :param r: 每天接触的人数
    :param N: 总人口
    :return: S(易感人群) E(潜伏期) R(康复者) I(患者) 数量
    """
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


def process(T, E, I, R, N=1400000000, r=2, sigma=1 / 14, immune_people=0):
    """
    :param T: 传染时间
    :param E: 潜伏期
    :param I: 患者
    :param R: 康复者
    :param N: 总人口
    :param r: 每天接触的人数
    :param sigma: 潜伏者转化为感染者的概率
    :param immune_people: 接收疫苗人数
    :return: S(易感人群) E(潜伏期) R(康复者) I(患者) 数量
    """
    S = N - I - R - immune_people
    R = R + immune_people
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
    """
    各城市接触人数测试函数
    """
    t0_range = 23
    S1, E1, I1, R1 = process(t0_range, r=r1, N=population, E=0, I=inflect, R=0, sigma=1 / 14)
    S2, E2, I2, R2 = process(165, r=r2, N=population, E=E1[t0_range], I=I1[t0_range], R=R1[t0_range], sigma=1 / 4)
    temp1 = [R1[i] + I1[i] for i in range(len(R1))]
    temp2 = [R2[i] + I2[i] for i in range(len(R2))]
    return temp1 + temp2[1:]


def draw_mid_elephant(r1, r2, r3, population, inflect=1):
    t0_range = 23
    t1_range = 10
    t2_range = 154
    S1, E1, I1, R1 = process(t0_range, r=r1, N=population, E=0, I=inflect, R=0, sigma=1 / 14)
    S2, E2, I2, R2 = process(t1_range, r=r2, N=population, E=E1[t0_range], I=I1[t0_range], R=R1[t0_range], sigma=1 / 4)
    S3, E3, I3, R3 = process(t2_range, r=r3, N=population, E=E2[t1_range], I=I2[t1_range], R=R2[t1_range], sigma=1 / 4)
    temp1 = [R1[i] + I1[i] for i in range(len(R1))]
    temp2 = [R2[i] + I2[i] for i in range(len(R2))]
    temp3 = [R3[i] + I3[i] for i in range(len(R3))]
    print(len(temp1), len(temp2), len(temp3))
    return temp1 + temp2[1:] + temp3[1:]


def draw_elephant(regulation_vaccine, population, r0):
    """
    :param regulation_vaccine: [[开始时间, 结束时间, r, num_vaccine], ...]
    :param population: 区域总人口
    :param r0: 初始接触人数
    :return: 传染人数队列
    """
    S_ = [0 for i in range(len(regulation_vaccine) + 1)]
    E_ = [0 for i in range(len(regulation_vaccine) + 1)]
    I_ = [0 for i in range(len(regulation_vaccine) + 1)]
    R_ = [0 for i in range(len(regulation_vaccine) + 1)]

    t0 = datetime(int(regulation_vaccine[0][0].split('-')[0]), int(regulation_vaccine[0][0].split('-')[1]),
                  int(regulation_vaccine[0][0].split('-')[2])) - datetime(2020, 1, 5)
    t0 = abs(t0.days)
    S_[0], E_[0], I_[0], R_[0] = process(t0, r=r0, E=0, I=1, R=0, sigma=1 / 14, N=population)
    # num_regulation = len(regulation)
    # date_list = []
    N = population
    cnt = 0
    for i in regulation_vaccine:
        delta_time = datetime(int(i[0].split('-')[0]), int(i[0].split('-')[1]),
                              int(i[0].split('-')[2])) - datetime(
            int(i[1].split('-')[0]),
            int(i[1].split('-')[1]),
            int(i[1].split('-')[2]))
        delta_time = abs(delta_time.days)
        r = r0 * float(i[2])
        N = N - float(i[3])

        S_[cnt + 1], E_[cnt + 1], I_[cnt + 1], R_[cnt + 1] = process(delta_time, r=r, E=E_[cnt][-1], I=I_[cnt][-1],
                                                                     R=R_[cnt][-1], sigma=1 / 4, N=N)
        cnt = cnt + 1

    result = []
    for i in range(len(S_)):
        result.append(I_[i] + R_[i])
    # for i in result:
    #     print(i.shape[0])
    result_seq = []

    for i in range(len(result)):
        if i == 0:
            result_seq += [k for k in result[i]]
        else:
            result_seq += [k for k in result[i][1:]]

    assert len(result_seq) == 189
    # print(len(result_seq))
    return result_seq


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
    # print(draw_little_elephant(18, 2, 1400000000, 1))
    # print(draw_mid_elephant(18, 9, 2, 1400000000))
    print((draw_elephant([['2020-02-5', '2020-02-07', 1, 0], ['2020-02-07', '2020-07-11', 2 / 18, 200000],
                          ], 1400000000,
                         18)))
    print((draw_elephant([['2020-02-02', '2020-07-11', 2 / 50, 0]], 1400000000,
                         50)))
    print((draw_elephant([['2020-01-15', '2020-01-17', 1, 0], ['2020-01-17', '2020-02-11', 2 / 18, 0],
                          ['2020-02-11', '2020-07-11', 2 / 18, 0]], 1400000000,
                         18)))
    # 6 30 150
    print((draw_elephant([['2020-01-28', '2020-02-07', 0.5, 0], ['2020-02-08', '2020-02-11', 0.1111111111111111, 0],
                          ['2020-02-12', '2020-07-11', 0.1111111111111111, 0]], 1400000000,
                         18)))
