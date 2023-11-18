# Introduction
Conventional machine learning approaches often assume that the test data are well-represented by the training data, which is drawn from a target distribution. During the training phase, however, data from the target domains may be limited or altogether unknown in many practical cases. This leads to numerous degrees of heterogeneity between the test and training domains, resulting in test data that differs from training data in distribution. To address this challenge, the field of domain generalization has emerged. Domain generalization focuses on the development of models that can effectively generalize to new and even unseen populations that are not represented in the training domains [2].
Domain generalization has attracted significant attention from various disciplines, including Federated Learning (FL). More specifically, existing methods in FL mainly focus on solving the heterogeneity issue from the optimization perspective [1]. Works that focus on this can be mainly divided into two directions: local and global model adjustment. On the one hand, methods in the local direction conduct the adjustment on local model training at the client side, aiming at producing local models with smaller differences [3]. On the other hand, methods in the global direction conduct the adjustment on the global model on the server side, aiming at producing a global model with better performance [3].

# Methodology (FedDG [1])
The most important finding of FedDG [1] is that the dataset size is not the only factor for weighting the client updates in the aggregation step on the server side. Hence, FedDG shows that the ”Generalization Gap” between local and global models could be a beneficial and complementary indicator for determining aggregation weights. This gap represents the difference between the global model’s performance on a domain and the performance of the previous local model. Although existing methods try to address the issue by designing a training pipeline on the client side, authors in FedDG [1] believe that focusing only on an improved local training strategy cannot guarantee that the global model is generalizable enough to unseen domains. Therefore, they propose the FedDG that addresses the generalization issue on the server side by dynamically adjusting the aggregation weights of clients. More specifically, in FedDG [1], authors design a method called Generalization Adjustment that dynamically calibrates aggregation weights based on the observed generalization gaps during training to optimize the global objective. Authors claim that GA leads to a tighter generalization bound.

# Our Contribution
In this section, we present an overview of our potential contributions and a timeline for implementing the contributions. First, we aim to re-implement and evaluate the FedDG on a CovID-19 medical image classification task [4] and compare the results when a usual FedAVG method is used as in [5]. This is to both evaluate the FedDG in a real-world scenario and understand
better the idea used in FedDG. 

Second, as an extension of the FedDG and inspired by the idea of recently published the paper FedDisco [3], we plan to combine local adjustment methods (Ditto [6], MOON [7], and SCAFFOLD [8]) with global adjustment methods (General Adjustment (GA) presented in FedDG [1] and FedDisco [3]) in a centralized federated learning framework and analyze the effect of different local adjustment methods on the result of the FedDG algorithm. We hypothesize that this approach could potentially be a way to incorporate both personalization and generalization abilities in a centralized federated learning framework (like FedAVG). Moreover, we think it could give better results in terms of generalization because we consider both state-of-the-art methods in the local generalization and global generalization.

To elaborate on our idea, we will adopt Algorithm 1 from the FedDG paper [1], which focuses on reducing variations in generalization performance across diverse domains. The goal is to create a global model that is more capable of generalizing well across different scenarios by taking both local and global adjustment methods. More specifically, we face an optimization problem in which the optimization process is divided into two phases: 

### 1. Local Training Phase: 
In this phase, each client optimizes its local model parameters through gradient descent using its local dataset. However, this stage potentially differs from the one that is suggested in the FedDG [1] paper and it actually incorporates some local adjustment methods such as Ditto [6], MOON [7], and SCAFFOLD [8]. In this way, we would like to change the local objectives in a way that they tend to achieve more personalized and generalized results on their own specific data. 

### 2. Aggregation (global training) Phase:
After local training, the server performs a momentum update to compute the generalization weights by evaluating the generalization gaps on all domains. This step will be implemented in the same way the authors have done in [1]. These weights influence how much each client’s model contributes to the global model. Moreover, if we have enough time, we would like to implement the FedDisco [3] as another global adjustment strategy to improve the generalization and see how the results differ from FedDG, as these two have not been compared even in the FedDisco [3] paper which is published after FedDG [1].


# Conclusion
FedDG [1] is a way to adjust the aggregation weights to pursue better out-of-domain generalization in the centralized federated learning setting. Specifically, it proposes a new global optimization objective that encourages flatness and fairness by reducing the variance of generalization gaps. So, in this project, we plan to re-implement it and evaluate the method on an image classification task to understand the elements of FedDG. Moreover, we aim to combine the FedDG, as an adjustment technique on the global objective of the federated learning problem, with some state-of-the-art local adjustment techniques, to see how the results differ from the FedDG. We hypothesize that this approach could potentially be a way to incorporate both personalization and generalization abilities and give better results in terms of generalization.


# Datasets
### 1. PACS: [https://sketchx.eecs.qmul.ac.uk](https://drive.google.com/drive/folders/0B6x7gtvErXgfUU1WcGY5SzdwZVk?resourcekey=0-2fvpQY_QSyJf2uIECzqPuQ)

# References
[1] Ruipeng Zhang, Qinwei Xu, Jiangchao Yao, Ya Zhang, Qi Tian, and Yanfeng Wang. Federated domain generalization with generalization adjustment. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 3954–3963, 2023.

[2] Sai Li and Linjun Zhang. Multi-dimensional domain generalization with low-rank structures. arXiv preprint arXiv:2309.09555, 2023.

[3] Rui Ye, Mingkai Xu, Jianyu Wang, Chenxin Xu, Siheng Chen, and Yan-feng Wang. Feddisco: Federated learning with discrepancy-aware collaboration. arXiv preprint arXiv:2305.19229, 2023.

[4] Joseph Paul Cohen, Paul Morrison, and Lan Dao. Covid-19 image data collection. arXiv 2003.11597, 2020.

[5] Ines Feki, Sourour Ammar, Yousri Kessentini, and Khan Muhammad. Federated learning for covid-19 screening from chest x-ray images. Applied Soft Computing, 106:107330, 2021.

[6] Tian Li, Shengyuan Hu, Ahmad Beirami, and Virginia Smith. Ditto: Fair and robust federated learning through personalization. In International Conference on Machine Learning, pages 6357 6368. PMLR, 2021.

[7] March 30) Li, Q. et.al (2021. Model-contrastive federated learning (moon). arXiv.org, 2021.

[8] Sai Praneeth Karimireddy, Satyen Kale, Mehryar Mohri, Sashank Reddi, Sebastian Stich, and Ananda Theertha Suresh. Scaffold: Stochastic controlled averaging for federated learning. In International conference on machine learning, pages 5132–5143. PMLR, 2020.

[9] Mohammad Norouzi Ting Chen, Simon Kornblith and Geoffrey Hinton. A simple framework for contrastive learning of visual representations. arXiv.org, 2020.

