# 无视警告
import warnings

warnings.filterwarnings("ignore")
import os

import paddle
import paddle_quantum

from numpy import savez
from paddle_quantum.loss import ExpecVal
from paddle_quantum import Hamiltonian
from paddle_quantum.state import zero_state
from paddle_quantum.ansatz import Circuit


def U_theta(num_qubits: int, depth: int) -> Circuit:
    """
    Quantum Neural Network
    """

    # 按照量子比特数量/网络宽度初始化量子神经网络
    cir = Circuit(num_qubits)

    # 内置的 {R_y + CNOT} 电路模板
    cir.real_entangled_layer(depth=depth)

    # 铺上最后一列 R_y 旋转门
    cir.ry()

    return cir


# 定义哈密顿量的项
pauli_str = [(1, 'I0, X1, X2'),
             (0.5, 'I0, X1, Z2'),
             (-0.2, 'Z0, X1, X2'),
             (1.2, 'Z0, Z1, I2')]

# 构建哈密顿量
hamiltonian = Hamiltonian(pauli_str)

# 打印哈密顿量
#print("Constructed Hamiltonian:")
#print(hamiltonian)

# 定义损失函数
loss_func = ExpecVal(hamiltonian)

ITR = 80  # 设置训练的总迭代次数
LR = 0.4  # 设置学习速率
D = 2  # 设置量子神经网络中重复计算模块的深度 Depth
N = hamiltonian.n_qubits  # 设置参与计算的量子比特数

# 确定网络的参数维度
cir = U_theta(N, D)
#print(cir)
# 一般来说，我们利用Adam优化器来获得相对好的收敛，
# 当然你可以改成SGD或者是RMS prop.
opt = paddle.optimizer.Adam(learning_rate=LR, parameters=cir.parameters())

# 定义初始态
init_state = zero_state(N)

# 记录优化结果
summary_iter, summary_loss = [], []
# 优化循环
for itr in range(1, ITR + 1):
    #print("", hamiltonian.sites)
    #print("before state itr=", itr)
    #print(cir)
    # 前向传播计算损失函数
    #print('1')
    state = (init_state)
    #print(cir)
    #print("after state before loss itr=", itr)
    #print('2')
    loss = loss_func(state)
    #print('3')
    # 在动态图机制下，反向传播极小化损失函数
    loss.backward()
    opt.minimize(loss)
    opt.clear_grad()

    # 更新优化结果
    summary_loss.append(loss.numpy())
    summary_iter.append(itr)

    # 打印结果
    if itr % 20 == 0:
        print("iter:", itr, "loss:", "%.4f" % loss.numpy())
        print("iter:", itr, "Ground state energy:", "%.4f Ha"
              % loss.numpy())
    if itr == ITR:
        print("\n训练后的电路：")
        print(cir)

# 储存训练结果到 output 文件夹
os.makedirs("output", exist_ok=True)
savez("./output/summary_data", iter=summary_iter,
      energy=summary_loss)

r'''
D:\anaconda\envs\paddle_quantum_env\python.exe D:\pythonstarter\baiduquantum\qnncir.py 
D:\anaconda\envs\paddle_quantum_env\lib\site-packages\setuptools\sandbox.py:13: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
  import pkg_resources
D:\anaconda\envs\paddle_quantum_env\lib\site-packages\pkg_resources\__init__.py:2871: DeprecationWarning: Deprecated call to `pkg_resources.declare_namespace('mpl_toolkits')`.
Implementing implicit namespace packages (as specified in PEP 420) is preferred to `pkg_resources.declare_namespace`. See https://setuptools.pypa.io/en/latest/references/keywords.html#keyword-namespace-packages
  declare_namespace(pkg)
D:\anaconda\envs\paddle_quantum_env\lib\site-packages\pkg_resources\__init__.py:2871: DeprecationWarning: Deprecated call to `pkg_resources.declare_namespace('google')`.
Implementing implicit namespace packages (as specified in PEP 420) is preferred to `pkg_resources.declare_namespace`. See https://setuptools.pypa.io/en/latest/references/keywords.html#keyword-namespace-packages
  declare_namespace(pkg)
D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle\tensor\creation.py:125: FutureWarning: In the future `np.object` will be defined as the corresponding NumPy scalar.
  if data.dtype == np.object:
Traceback (most recent call last):
  File "D:\pythonstarter\baiduquantum\qnncir.py", line 1, in <module>
    from paddle_quantum.ansatz import Circuit
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle_quantum\__init__.py", line 37, in <module>
    from .ansatz import Circuit
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle_quantum\ansatz\__init__.py", line 21, in <module>
    from .circuit import Circuit
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle_quantum\ansatz\circuit.py", line 23, in <module>
    from .layer import Layer, SuperpositionLayer, WeakSuperpositionLayer, LinearEntangledLayer
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle_quantum\ansatz\layer.py", line 25, in <module>
    from ..gate import H, RX, RY, RZ, U3, CNOT
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle_quantum\gate\__init__.py", line 24, in <module>
    from .encoding import BasisEncoding
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle_quantum\gate\encoding.py", line 29, in <module>
    class BasisEncoding(Operator):
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle_quantum\gate\encoding.py", line 41, in BasisEncoding
    __x = x_gate('complex128')
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle_quantum\gate\matrix.py", line 198, in x_gate
    return paddle.to_tensor(gate_matrix, dtype=dtype)
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\decorator.py", line 232, in fun
    return caller(func, *(extras + args), **kw)
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle\fluid\wrapped_decorator.py", line 25, in __impl__
    return wrapped_func(*args, **kwargs)
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle\fluid\framework.py", line 434, in __impl__
    return func(*args, **kwargs)
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle\tensor\creation.py", line 125, in to_tensor
    if data.dtype == np.object:
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\numpy\__init__.py", line 305, in __getattr__
    raise AttributeError(__former_attrs__[attr])
AttributeError: module 'numpy' has no attribute 'object'.
`np.object` was a deprecated alias for the builtin `object`. To avoid this error in existing code, use `object` by itself. Doing this will not modify any behavior and is safe. 
The aliases was originally deprecated in NumPy 1.20; for more details and guidance see the original release note at:
    https://numpy.org/devdocs/release/1.20.0-notes.html#deprecations这些报错是什么意思
ChatGPT
这个报错涉及到 NumPy 库的一个变化。具体而言，这是因为 np.object 这个别名在 NumPy 1.20 版本中被废弃。在新版本的 NumPy 中，应该直接使用 object，而不再使用 np.object。

在你的情况中，这个警告是由 Paddle Quantum 库内部的代码触发的，因为它引用了即将被弃用的 np.object。这个问题通常是由于库内部使用了过时的 NumPy 语法导致的。

解决方法是更新 Paddle Quantum 或者相关的依赖库，以使用与 NumPy 1.20 版本兼容的版本。你可以尝试升级 Paddle Quantum 到最新版本，或者查看 Paddle Quantum 的文档，看看是否有关于兼容性的说明或已知问题。

此外，你也可以考虑在报告问题的同时联系 Paddle Quantum 社区，以获取更详细的支持和解决方案。

'''

r'''
Traceback (most recent call last):
  File "D:\pythonstarter\baiduquantum\qnncir.py", line 69, in <module>
    loss = loss_func(state)
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle\fluid\dygraph\layers.py", line 930, in __call__
    return self._dygraph_call_func(*inputs, **kwargs)
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle\fluid\dygraph\layers.py", line 915, in _dygraph_call_func
    outputs = self.forward(*inputs, **kwargs)
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle_quantum\loss\measure.py", line 95, in forward
    output_state, seq_for_acted = state_vector.unitary_transformation_without_swapback(
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle_quantum\backend\state_vector.py", line 122, in unitary_transformation_without_swapback
    perm_map = pq.intrinsic._perm_of_list(qubit_sequence, seq_for_acted)
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle_quantum\intrinsic.py", line 321, in _perm_of_list
    return [perm_map[val] for val in targ_list]
  File "D:\anaconda\envs\paddle_quantum_env\lib\site-packages\paddle_quantum\intrinsic.py", line 321, in <listcomp>
    return [perm_map[val] for val in targ_list]
KeyError: ''
'''


