# -
对抗性分析机试题
在数学和计算机领域有很多重要的猜想，比如哥德巴赫猜想、黎曼猜想、ABC猜想，P&NP猜想等等，有些猜想是“简单的”，有些问题则已经困扰了全人类几百年。但是这些猜想里，大部分普通人都很难能看懂。

最近，有个新闻华裔数学家黄皓（Hao Huang）仅用两页纸就证明了一个近30年的计算机科学猜想——布尔函数敏感度猜想（Boolean Sensitivity ），同时这个证明是非常简洁可读的。其实关于敏感度，其实在深度学习里也有类似的考虑。虽然深度学习在大数据、强力GPU计算资源的加持下，在语音识别、图像分类、自然语言理解、强化学习等方向取得了巨大的进步，但研究人员发现，很多情况下，一个训练好，表现也非常优异的神经网络经常对于输入数据的扰动还是非常敏感的。

举个视觉的例子。假设我们训练好了一个目标分类的卷积神经网络模型M，它已经能够正确分类某一张图片为熊猫（哪怕置信度达到了99%），研究人员发现我们可以通过对这张图像进行人眼很难分辨的像素级别的微小修改，就可以使得模型M的预测结果发生改变，甚至变成任意指定的类别，比如苹果。

image

这些细微的不同可能是随机错误导致的，也可能是压缩带来的信息损失。当然伤害最大的可能还是hackers的定向hack，用来破解某些系统，例如语音识别和人脸识别等系统。为了预防hackers的破解，也为了深入理解一下相关内容，现请你针对一些神经网络进行分析，找出它们的薄弱点。

简单起见，我们弱化一个神经网络为最简单的两层全连接网络(不带偏置项)，不需要任何相关知识就可以理解。

假设网络的输入是X，输出是Y，那么公式表达就是

Y=Softmax(Z), Z=W2*ReLU(A)), A=W1*X

其中X是一个N维的向量，W1是一个MxN的矩阵，ReLU(A)=max(A,0), W2是一个10xM的矩阵, Z是一个10维的向量。Softmax的操作定义为：

image

可以看到这时候所有Yi的求和为1，因此Yi可以代表数据X被分类到第i类的概率。为了数值稳定性，建议大家用上面第2个公式进行计算。

接下来请找出输入向量中敏感度最高的位置，假设输入数据X的每一维度上都只能是[-128,127]范围的整数，以下操作都只考虑只修改X的某一维的情况，不能同时修改多个维度的值：

1 如果存在X的某一维度（假设是第i维），当它的值修改为[-128,127]范围的某个整数后，网络输出的类别（即softmax后概率最高的位置）跟原始X的分类结果相比发生了改变，且使得新类别的预测概率最大，则i为敏感度最高的位置。

2 如果对于X的任意一个位置，把它的值进行[-128,127]范围的任意修改，网络输出的类别都不会发生改变，那么我们把可以使得网络输出概率可以降到最低的那个修改所对应位置称为敏感度最高的位置。

3 测试样例中，原始网络的输出中只会有一个类别概率最高，不会出现多个类别概率同时最高的情况，X中也不会出现存在多个敏感度最高位置。

Input Format

输入4行。

第一行是两个整数N，M。代表输入向量的维度为N，第一个隐藏层的节点数为M。

第二行有N个整数，以空格隔开。即为输入的向量。

第三行有M*N个浮点数，以空格隔开。即第一个全连接层的网络参数W1。其中第(i-1)*N+1到第i*N个浮点数是第一个全连接层第i个节点的权重参数。

第四行有10*M个浮点数，以空格隔开。即第二个全连接层的网络参数W2。其中第(i-1)*M+1到第i*M个浮点数是第二个全连接层第i个节点的权重参数。

Constraints

60%的测试样例满足如下条件：

第一行是一个整数N，取值范围：1<= N<= 100, 1 <= M <100

第二行的N个整数Ni，取值范围：-128 <= Ni < 128

第三行的浮点数fi，取值范围：-8.0 <= fi <= 8.0

第四行的浮点数fj，取值范围:-8.0 <= fj <= 8.0

剩下40%的测试样例满足如下条件：

第一行是一个整数N，取值范围：1<= N<= 1000, 1 <= M <100

第二行的N个整数Ni，取值范围：-128 <= Ni < 128

第三行的浮点数fi，取值范围：-8.0 <= fi <= 8.0

第四行的浮点数fj，取值范围:-8.0 <= fj <= 8.0

Output Format

输出2个整数P,V，以空格隔开。 其中P是[1,N]的某个整数，代表输入向量X中敏感度最高的位置。 V表示X的敏感度最高的位置的数字应该被修改成[-128,127]中的哪个数字，使得网络受影响最大（即:如果预测类别被改变了，怎么样改会概率最高；如果预测类别不变，怎么样改使得当前类别的预测概率最小）。

Sample Input 0

8 4
-4 -71 -56 -41 85 -19 -56 -3
0.00719 0.01590 -0.01121 -0.02345 0.00777 0.01680 0.01642 -0.01437 0.04963 -0.02698 -0.03168 -0.02930 0.00784 -0.03372 -0.01824 0.01997 -0.01687 -0.02018 -0.00434 -0.00647 -0.01860 -0.01780 -0.01345 0.03369 0.00142 -0.00109 -0.02072 0.00518 -0.02600 -0.01217 -0.00510 -0.00254
-0.00372 0.06219 0.00260 0.06550 -0.02418 -0.02375 0.00115 0.00132 0.00280 -0.01428 0.02612 -0.03527 -0.02926 -0.02194 -0.04160 0.03126 0.01071 0.02239 0.00883 0.03610 0.00117 0.00429 -0.05671 0.00374 0.03496 0.03749 0.03426 0.01259 0.01202 -0.00021 -0.04738 -0.02131 0.02525 0.04419 -0.01626 0.04310 -0.01328 -0.00932 -0.03152 0.06103
Sample Output 0

1 -77
