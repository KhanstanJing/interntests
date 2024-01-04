import paddle

from paddle_quantum.ansatz import Circuit

# 确定网络的参数维度
cir = U_theta(N, D)

# 一般来说，我们利用Adam优化器来获得相对好的收敛，
# 当然你可以改成SGD或者是RMS prop.
opt = paddle.optimizer.Adam(learning_rate=LR, parameters=cir.parameters())

# 定义初始态
init_state = zero_state(N)

# 记录优化结果
summary_iter, summary_loss = [], []

# 优化循环
for itr in range(1, ITR + 1):

    # 前向传播计算损失函数
    state = cir(init_state)
    loss = loss_func(state)

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