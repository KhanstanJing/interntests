import numpy
from numpy import savez

import os
import matplotlib.pyplot as plt

import paddle
import paddle_quantum
from paddle import matmul
from paddle_quantum.ansatz import Circuit
from paddle_quantum.qinfo import pauli_str_to_matrix
from paddle_quantum.linalg import dagger
from paddle_quantum.state import zero_state

N = 3  # 量子比特数/量子神经网络的宽度
SEED = 50  # 固定随机种子

# 定义哈密顿量的项
pauli_str = [(1, 'I0, X1, X2'),
             (0.5, 'I0, X1, Z2'),
             (-0.2, 'Z0, X1, X2'),
             (1.2, 'Z0, Z1, I2')]

# 生成 Hamilton 量的矩阵信息
complex_dtype = paddle_quantum.get_dtype()
H = pauli_str_to_matrix(pauli_str, N).astype(complex_dtype)


def U_theta(num_qubits: int) -> Circuit:
    """
    U_theta
    """
    # 按照量子比特数量/网络宽度初始化量子神经网络
    cir = Circuit(num_qubits)

    cir.universal_three_qubits([0, 1, 2])

    # 返回量子神经网络的电路
    return cir


class Net(paddle.nn.Layer):
    def __init__(self, num_qubits: int):
        super(Net, self).__init__()

        # 构造量子神经网络
        self.cir = U_theta(num_qubits)

    # 定义损失函数和前向传播机制
    def forward(self, H):

        # 计算损失函数
        U = self.cir.unitary_matrix()
        loss_struct = paddle.real(matmul(matmul(dagger(U), H), U))

        # 输入计算基去计算每个子期望值，相当于取 U^dagger*H*U 的对角元
        loss_components = []
        for i in range(len(loss_struct)):
            loss_components.append(loss_struct[i][i])

        # 最终加权求和后的损失函数
        loss = 0
        for i in range(len(loss_components)):
            weight = i
            # weight = 8 - i
            loss += weight * loss_components[i]
        print('the unitary matrix is ', U)
        return loss, loss_components, self.cir


ITR = 300  # 设置训练的总迭代次数
LR = 0.3  # 设置学习速率

paddle.seed(SEED)

# 我们需要将 numpy.ndarray 转换成 PaddlePaddle 支持的 Tensor
hamiltonian = paddle.to_tensor(H)
# print(H)
# 确定网络的参数维度
net = Net(N)

# Adam 优化器来获得相对好的收敛，
# 当然你可以改成 SGD 或者是 RMS prop.
opt = paddle.optimizer.Adam(learning_rate=LR, parameters=net.parameters())
# opt = paddle.optimizer.SGD(learning_rate=LR, parameters=net.parameters())
# opt = paddle.optimizer.RMSProp(learning_rate=LR, parameters=net.parameters())

# 定义初始态
init_state = zero_state(N)

# 记录优化结果
summary_iter, summary_loss = [], []
summary_loss_components = []

# 优化循环
for itr in range(1, ITR + 1):

    # 前向传播计算损失函数并返回估计的能谱
    loss, loss_components, cir = net(hamiltonian)

    # 在动态图机制下，反向传播极小化损失函数
    loss.backward()
    opt.minimize(loss)
    opt.clear_grad()

    # 更新优化结果
    summary_loss.append(loss.numpy())
    summary_loss_components.append(min(loss_components).numpy())
    summary_iter.append(itr)

    # 打印训练结果
    if itr % 10 == 0:
        print('iter:', itr, 'loss:', '%.4f' % loss.numpy()[0])

def output_ordinalvalue(num):
    r"""
    Convert to ordinal value

    Args:
        num (int): input number

    Return:
        (str): output ordinal value
    """
    if num == 1:
        return str(num) + "st"
    elif num == 2:
        return str(num) + "nd"
    elif num == 3:
        return str(num) + "rd"
    else:
        return str(num) + 'th'


for i in range(len(loss_components)):
    if i == 0:
        print('The estimated ground state energy is: ', loss_components[i].numpy())
        print('The theoretical ground state energy is: ', numpy.linalg.eigh(H)[0][i])
    else:
        print('The estimated {} excited state energy is: {}'.format(
            output_ordinalvalue(i), loss_components[i].numpy())
        )
        print('The theoretical {} excited state energy is: {}'.format(
            output_ordinalvalue(i), numpy.linalg.eigh(H)[0][i])
        )

# 储存训练结果到 output 文件夹
os.makedirs("output_with_uni3", exist_ok=True)
savez("./output/summary_data_with_uni3", iter = summary_iter, energy=summary_loss_components)

cir.plot(
    save_path=r"D:\pythonstarter\baiduquantumnotbroken\circuit_with_uni3.png",  # 保存图像的路径
    dpi=300,  # 分辨率
    show=False,  # 是否显示图像
    output=True,  # 是否返回 Figure 实例
    scale=1.0,  # 缩放系数
    tex=False  # 是否使用 LaTeX 字体
)

result = numpy.load('./output/summary_data_with_uni3.npz')

eig_val, eig_state = numpy.linalg.eig(H)
min_eig_H = numpy.min(eig_val.real)
min_loss = numpy.ones([len(result['iter'])]) * min_eig_H

plt.figure(2)
func1, = plt.plot(result['iter'], result['energy'],
                  alpha=0.7, marker='', linestyle="-", color='r')
func_min, = plt.plot(result['iter'], min_loss,
                  alpha=0.7, marker='', linestyle=":", color='b')
plt.xlabel('Number of iteration')
plt.ylabel('Energy (Ha)')

plt.legend(handles=[func1, func_min],
    labels=[
        r'$\left\langle {\psi \left( {\theta } \right)} '
        r'\right|H\left| {\psi \left( {\theta } \right)} \right\rangle $',
        'Ground-state energy',
    ], loc='best')
#标记基态能量大小
plt.text(-5, -1.75, f'{min_eig_H:.5f}', fontsize=10, color='b')
plt.savefig(r"D:\pythonstarter\baiduquantumnotbroken\ground_energy_with_uni3.png")