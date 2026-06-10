根据 Week 4 课程记录与课件 09 的卷积原理，以下为您演示一个 $3 \times 3$ 输入通过 $2 \times 2$ 卷积核（步长=1，无填充）得到输出特征图的完整手算过程。

### 1. 设定初始数值
为了计算清晰，我们设定简单的整数矩阵：

*   **输入图像 ($I$)**：
    $$\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}$$
*   **卷积核 ($K$)**：
    $$\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$$
*   **参数配置**：步长 $S=1$，填充 $P=0$。

### 2. 确定输出尺寸
根据尺寸公式 $O = \lfloor \frac{I - K + 2P}{S} \rfloor + 1$ [1]：
*   宽度/高度 $O = \lfloor \frac{3 - 2 + 0}{1} \rfloor + 1 = \mathbf{2}$
*   因此，输出特征图是一个 **$2 \times 2$** 的矩阵。

### 3. 逐步计算过程
卷积操作（在深度学习实现中通常指互相关计算）即卷积核在输入上滑动，将重叠区域的元素相乘并求和 [2, 3]。

*   **左上角位置（窗口 1）**：
    输入覆盖区域：$\begin{bmatrix} 1 & 2 \\ 4 & 5 \end{bmatrix}$
    计算：$(1 \times 1) + (2 \times 0) + (4 \times 0) + (5 \times 1) = 1 + 0 + 0 + 5 = \mathbf{6}$

*   **右上角位置（向右滑动 1 步，窗口 2）**：
    输入覆盖区域：$\begin{bmatrix} 2 & 3 \\ 5 & 6 \end{bmatrix}$
    计算：$(2 \times 1) + (3 \times 0) + (5 \times 0) + (6 \times 1) = 2 + 0 + 0 + 6 = \mathbf{8}$

*   **左下角位置（向下滑动 1 步，窗口 3）**：
    输入覆盖区域：$\begin{bmatrix} 4 & 5 \\ 7 & 8 \end{bmatrix}$
    计算：$(4 \times 1) + (5 \times 0) + (7 \times 0) + (8 \times 1) = 4 + 0 + 0 + 8 = \mathbf{12}$

*   **右下角位置（向右滑动 1 步，窗口 4）**：
    输入覆盖区域：$\begin{bmatrix} 5 & 6 \\ 8 & 9 \end{bmatrix}$
    计算：$(5 \times 1) + (6 \times 0) + (8 \times 0) + (9 \times 1) = 5 + 0 + 0 + 9 = \mathbf{14}$

### 4. 最终输出特征图
$$\begin{bmatrix} 6 & 8 \\ 12 & 14 \end{bmatrix}$$

**来源说明：**
*   **计算公式与参数定义**：笔记-week04-周五-AI [1]、09Deep learning.pdf (第 761-764 页)。
*   **卷积操作逻辑（无翻转）**：参考书-Deep Learning (Goodfellow) 第 9.1 节 [2, 3]。