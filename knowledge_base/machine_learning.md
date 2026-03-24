# Machine Learning Basics

## What is Machine Learning?
Machine Learning (ML) is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. ML algorithms build mathematical models based on training data to make predictions or decisions. The three main types are supervised learning, unsupervised learning, and reinforcement learning.

## Supervised vs Unsupervised Learning
**Supervised Learning** uses labeled datasets to train algorithms. The model learns the mapping between inputs and known outputs. Common algorithms include Linear Regression, Decision Trees, Random Forests, and Support Vector Machines (SVM). It is used for classification and regression tasks.

**Unsupervised Learning** works with unlabeled data to discover hidden patterns or groupings. Common algorithms include K-Means Clustering, DBSCAN, Principal Component Analysis (PCA), and Autoencoders. It is used for clustering, dimensionality reduction, and anomaly detection.

## What is Overfitting?
Overfitting occurs when a model learns the training data too well, including its noise and outliers, resulting in poor performance on new, unseen data. Signs include very high training accuracy but low test/validation accuracy. Solutions include cross-validation, regularization (L1/L2), dropout (in neural networks), early stopping, and using more training data.

## What is a Neural Network?
A neural network is a computational model inspired by the human brain. It consists of layers of interconnected nodes (neurons): an input layer, one or more hidden layers, and an output layer. Each connection has a weight that is adjusted during training. Deep learning refers to neural networks with many hidden layers. Common architectures include CNNs (for images), RNNs/LSTMs (for sequences), and Transformers (for NLP).

## Model Evaluation Metrics
- **Accuracy**: Percentage of correct predictions overall.
- **Precision**: Of all positive predictions, how many were actually positive.
- **Recall**: Of all actual positives, how many were correctly predicted.
- **F1 Score**: Harmonic mean of precision and recall, balancing both metrics.
- **AUC-ROC**: Measures the model's ability to distinguish between classes across all thresholds.
