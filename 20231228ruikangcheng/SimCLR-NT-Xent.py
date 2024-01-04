import torch
import torch.nn.functional as F

def NT_Xent(x1, x2, temperature=0.13):
    # 交叉拼接x1和x2
    stacked_tensors = torch.stack((x1, x2), dim=1)
    x = torch.reshape(stacked_tensors, (8, -1))

    # 余弦相似度的矩阵
    csmx = F.cosine_similarity(x[None, :, :], x[:, None, :], dim=-1)

    # 去掉样本和自身的相似度
    eye = torch.eye(8)
    eye = eye.bool()
    y = csmx.clone()
    # 将沿所有对余弦相似度矩阵的主对角线的值设置为-inf，这样当我们计算每行的softmax时，该值将不会产生任何影响
    y[eye] = float("-inf")

    # 设置真实标签
    target = torch.arange(8)
    target[0:: 2] += 1
    target[1:: 2] -= 1
    # print(target)
    # tensor([1, 0, 3, 2, 5, 4, 7, 6])

    loss = F.cross_entropy(y / temperature, target, reduction="mean")

    return loss.item()

'''
用于创建张量的循环
x10 = [float(x) for x in range(10)]
x11 = [float(x) for x in range(10, 20)]
x12 = [float(x) for x in range(20, 30)]
x13 = [float(x) for x in range(30, 40)]
x1 = [x10, x11, x12, x13]
x1 = torch.tensor(x1)

x20 = [float(x) for x in range(20, 30)]
x21 = [float(x) for x in range(30, 40)]
x22 = [float(x) for x in range(40, 50)]
x23 = [float(x) for x in range(50, 60)]
x2 = [x20, x21, x22, x23]
x2 = torch.tensor(x2)
'''
x10 = [0., 1., 2., 3., 4., 5., 6., 7., 8., 9.]
x11 = [10., 11., 12., 13., 14., 15., 16., 17., 18., 19.]
x12 = [20., 21., 22., 23., 24., 25., 26., 27., 28., 29.]
x13 = [30., 31., 32., 33., 34., 35., 36., 37., 38., 39.]
x1 = [x10, x11, x12, x13]
x1 = torch.tensor(x1)

x20 = [20., 21., 22., 23., 24., 25., 26., 27., 28., 29.]
x21 = [30., 31., 32., 33., 34., 35., 36., 37., 38., 39.]
x22 = [40., 41., 42., 43., 44., 45., 46., 47., 48., 49.]
x23 = [50., 51., 52., 53., 54., 55., 56., 57., 58., 59.]
x2 = [x20, x21, x22, x23]
x2 = torch.tensor(x2)

lossx1x2 = NT_Xent(x1, x2)
print(lossx1x2)
