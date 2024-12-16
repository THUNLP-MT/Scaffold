# Scaffold: 通过框架化坐标促进多模态大模型的视觉-语言协同 (COLING 2025)

此仓库包含我们的论文 通过框架化坐标促进多模态大模型的视觉-语言协同 的相关介绍、数据和代码。

## 🔥 更新动态

[2024.12.9] 我们的工作被 COLING 2025 会议接收！

[2024.08] 我们的工作在 ACL 2024 的 Wordplay Workshop 上展示！

[2024.02.22] 我们发布了代码，将 Scaffold 提示应用于视觉-语言任务。

## 📍 简介

最先进的大规模多模态模型（LMMs）在视觉-语言任务中展现了卓越的能力。然而，在需要多层次视觉信息复杂推理的挑战场景下，LMMs 的性能仍然受到限制。现有的提示技术主要集中于改进文本推理或利用工具进行图像预处理，但缺乏一种简单且通用的视觉提示方法来促进 LMMs 的视觉-语言协同。在本工作中，我们提出了 Scaffold 视觉提示方法，该方法通过框架化坐标促进视觉-语言协同。具体而言，Scaffold 在图像上叠加点矩阵作为视觉信息锚点，并利用多维坐标作为文本中的位置参考。针对一系列具有挑战性的视觉-语言任务的广泛实验表明，Scaffold 比纯文本链式推理（CoT）提示方法具有显著优势。

![overall](../../assets/overall.jpg)

上图展示了 Scaffold 的整体框架，说明其如何促进视觉-语言协同。

有关 Scaffold 的详细描述，请参考论文：[Scaffold](https://arxiv.org/abs/2402.12058)

---

## 📦 快速开始

以下是将 Scaffold 提示应用于 GPT-4V 的视觉-语言任务的快速指南。示例问题和答案存放在 `data/examples/example.jsonl` 文件中，对应的图像在 `data/examples/imgs` 文件夹中。

**步骤 0** 准备工作。

运行以下命令安装所需模块：

```bash
pip install -r requirements.txt
```

如果您希望将 Scaffold 提示应用于自己的数据，需将数据组织成与 `data/examples/example.jsonl` 中示例一致的格式。有效样本的示例如下：

```python
{
  "question_id": 1, 
  "image_path": "data/examples/imgs/1.jpg", 
  "question": "以下陈述是否正确：这个人正面向香蕉。", 
  "answer": 1
}
```

同时，需将图像放置在 `image_path` 指定的路径下。

**步骤 1** 处理图像。

运行以下命令在原始图像上叠加点矩阵和坐标：

```bash
python image_processor.py
```

注意：我们在实现中采用了默认的超参数设置，例如点矩阵的大小设为 $6 \times 6$。如果需要自定义超参数或探索新方法，请检查并修改 `image_processor.py` 文件。

**步骤 2** 调用 GPT-4V API。

首先，在 `call-api.py` 中的 `API_KEY` 位置（标记为 TODO）填写您的 OpenAI API 密钥。然后运行以下命令运行示例：

```bash
python call-api.py \
	--data-file data/examples/example.jsonl \
	--mode scaffold \
	--parallel 1
```

最终结果将存储在 `log` 目录下。

---

## ⚙️ 方法

![wino_example_1](../assets/wino_example_1.jpg)

Scaffold 提示旨在增强 LMMs 的视觉-语言协同。该方法包括图像叠加和文本引导两部分。因此，我们将从视觉和文本的角度介绍方法的实现。

**视觉层面，** 我们在每张输入图像上叠加一个均匀分布的矩形点矩阵，其中每个点都标注有多维笛卡尔坐标。这些点作为视觉位置锚点，其坐标则作为文本响应中的位置参考。

**文本层面，** 我们在任务指令前添加文本指导，包括点矩阵和坐标的简要描述，并附上一些关于其有效使用的通用指南。

---

## 🚀 使用案例

以下是我们实验中的部分案例。

1. 增强的空间推理能力。

   <div align=center>
   <img src="../assets/vsr_example.jpg" alt="vsr_example" width="75%" style="zoom: 50%;" />
   </div>

2. 改善的组合推理能力。

   <div align=center>
   <img src="../assets/wino_example_2.jpg" alt="wino_example_2" width="75%" style="zoom:50%;" />
   </div>

3. 在高分辨率图像上激发的视觉搜索能力。

   <div align=center>
   <img src="../assets/vstar_example.jpg" alt="vstar_example" width="75%" style="zoom:50%;" />
   </div>

---

## 📂 结果

我们基于 GPT-4V 在 11 个具有挑战性的视觉-语言基准上进行了广泛实验，结果如下：

![results](../assets/results.jpg)

![active_perception](../assets/active_perception.jpg)

此外，我们将 Scaffold 与主动感知相结合，并在 V* Bench 的 direct_attributes 子集中进行了实验。结果如下所示，表明 Scaffold 可以作为一种有效的主动感知框架。

<div align=center>
<img src="../assets/results_active.jpg" alt="results_active" width="75%" style="zoom:33%;" />
</div>

## 👏 引用

```
@misc{lei2024scaffolding,
      title={Scaffolding Coordinates to Promote Vision-Language Coordination in Large Multi-Modal Models}, 
      author={Xuanyu Lei and Zonghan Yang and Xinrui Chen and Peng Li and Yang Liu},
      year={2024},
      eprint={2402.12058},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```