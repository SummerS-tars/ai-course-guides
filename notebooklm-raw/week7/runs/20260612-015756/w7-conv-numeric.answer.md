这是一个基于 **Week 7 课程记录**与**课件 09** 要求的 tiny 互相关（Cross-correlation）手算例子。

### 1. 设定输入与卷积核数值

*   **输入图像 (Input, $3 \times 3$):**
    $$X = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}$$
*   **卷积核 (Kernel, $2 \times 2$):**
    $$K = \begin{bmatrix} 1 & 0 \\ 2 & 1 \end{bmatrix}$$
*   **参数设置：** 步长 $stride=1$，无填充（Padding=0）。

### 2. 计算输出特征图尺寸
根据公式 $Output\_size = Input\_size - Kernel\_size + 1$ [1]：
*   输出宽度 = $3 - 2 + 1 = 2$
*   输出高度 = $3 - 2 + 1 = 2$
因此，输出特征图是一个 **$2 \times 2$** 的矩阵 [1]。

### 3. 完整计算过程（互相关，不翻转卷积核）

在卷积神经网络中，所谓的“卷积”操作实际上通常是 **互相关（Cross-correlation）**，即直接将卷积核与输入对应位置相乘并求和，**不进行数学定义中的卷积核翻转** [2, 3]。

*   **计算输出左上角值 $Y$：**
    卷积核覆盖输入左上角区域 $\begin{bmatrix} 1 & 2 \\ 4 & 5 \end{bmatrix}$。
    $$Y = (1 \times 1) + (2 \times 0) + (4 \times 2) + (5 \times 1) = 1 + 0 + 8 + 5 = \mathbf{14}$$

*   **计算输出右上角值 $Y[4]$：**
    卷积核向右滑动 1 个步长，覆盖区域 $\begin{bmatrix} 2 & 3 \\ 5 & 6 \end{bmatrix}$。
    $$Y[4] = (2 \times 1) + (3 \times 0) + (5 \times 2) + (6 \times 1) = 2 + 0 + 10 + 6 = \mathbf{18}$$

*   **计算输出左下角值 $Y[4]$：**
    卷积核向下滑动 1 个步长，覆盖区域 $\begin{bmatrix} 4 & 5 \\ 7 & 8 \end{bmatrix}$。
    $$Y[4] = (4 \times 1) + (5 \times 0) + (7 \times 2) + (8 \times 1) = 4 + 0 + 14 + 8 = \mathbf{26}$$

*   **计算输出右下角值 $Y[4]$：**
    卷积核向右、向下滑动 1 个步长，覆盖区域 $\begin{bmatrix} 5 & 6 \\ 8 & 9 \end{bmatrix}$。
    $$Y[4] = (5 \times 1) + (6 \times 0) + (8 \times 2) + (9 \times 1) = 5 + 0 + 16 + 9 = \mathbf{30}$$

### 4. 最终输出特征图
$$Y = \begin{bmatrix} 14 & 18 \\ 26 & 30 \end{bmatrix}$$

**说明：**
本例子遵循深度学习惯例，采用 **互相关（Cross-correlation）** 计算，即卷积核 $K$ 在滑动过程中 **不进行上下或左右翻转** [3]。

**依据来源：**
1.  **Week 7 课程记录 ("week7-周五-AI.md")**：明确指出 CNN 中的卷积实际上是互相关，不翻转卷积核 [3]；提供输出尺寸计算公式 [1]。
2.  **课件 09 ("09Deep learning.pdf")**：在信号处理术语中这被称为互相关而非卷积，但神经网络领域通用“卷积”一词来指代此操作 [5, 6]。