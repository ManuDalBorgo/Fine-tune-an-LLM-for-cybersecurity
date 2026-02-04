# Specialist Machine Learning Researcher - Interview Prep Roadmap

Welcome to your interview preparation workspace. This folder contains a comprehensive set of **12 Python scripts** tailored to the specific requirements of the Specialist ML Researcher role. 

The scripts are organized by domain to specifically target the job description's key areas: LLMs, Agentic AI, Cyber Defence, Cloud Deployment, and Rigorous Evaluation.

## 🗺️ Practice Roadmap

### 1. Large Language Models & Agentic AI
*Focus: Fine-tuning, RAG, and Agentic workflows.*

- **`01_llm_finetuning_lora.py`**  
  **Concept**: Parameter-Efficient Fine-Tuning (PEFT) with LoRA.  
  **Key Libs**: `transformers`, `peft`  
  **Goal**: Understand how to adapt large models efficiently without retraining fully.

- **`02_rag_agent_vector_db.py`**  
  **Concept**: Retrieval Augmented Generation (RAG).  
  **Key Libs**: `sentence-transformers`, `numpy` (custom vector search)  
  **Goal**: Build a system that retrieves context to verify claims or answer questions grounded in data.

- **`03_agentic_workflow_langgraph.py`**  
  **Concept**: Stateful Agentic Workflows (Planning, Researching, Reviewing).  
  **Key Libs**: Pure Python (Mocking LangGraph state machines)  
  **Goal**: Demonstrate how to build agents that can plan and execute multi-step tasks.

### 2. Core ML & Deep Learning Architectures
*Focus: Deep theoretical understanding of modern and classical methods.*

- **`09_custom_attention_layer.py`**  
  **Concept**: Transformer Multi-Head Attention from scratch.  
  **Key Libs**: `torch`  
  **Goal**: Prove deep understanding of the "Attention is All You Need" mechanism beyond just calling APIs.

- **`12_graph_neural_network_intro.py`**  
  **Concept**: Graph Convolutional Networks (GCN) from scratch.  
  **Key Libs**: `torch`  
  **Goal**: Understand message passing on graphs (spectral convolution), relevant for complex relational data.

- **`06_anomaly_detection_cyber.py`**  
  **Concept**: Unsupervised Anomaly Detection for Cyber Security.  
  **Key Libs**: `sklearn` (Isolation Forest)  
  **Goal**: Detect malicious patterns in network traffic without labeled data.

### 3. Optimization, Deployment & Cloud
*Focus: Deploying efficient models to Edge and Cloud environments.*

- **`04_model_quantization_edge.py`**  
  **Concept**: Post-Training Quantization (FP32 -> INT8).  
  **Key Libs**: `torch.quantization`  
  **Goal**: Optimize models for edge devices (latency vs precision trade-off).

- **`10_scalable_deployment_api.py`**  
  **Concept**: High-concurrency Model Serving.  
  **Key Libs**: `fastapi`  
  **Goal**: Create a scalable API service that can handle concurrent inference requests.

- **`11_azure_ai_foundry_demo.py`**  
  **Concept**: Cloud AI Operations (Azure AI Foundry / Azure ML).  
  **Key Libs**: `azure-ai-ml` (Mocked for demo)  
  **Goal**: Demonstrate familiarity with cloud SDKs for Model Registration, Endpoints, and Job Submission.

### 4. Security, Evaluation & Statistics
*Focus: Reliability, Robustness and Scientific Rigour.*

- **`05_evaluation_framework.py`**  
  **Concept**: Robust Evaluation Frameworks & Sliced Analysis.  
  **Key Libs**: `sklearn.metrics`  
  **Goal**: Go beyond accuracy; evaluate bias and performance across specific data slices.

- **`07_adversarial_security.py`**  
  **Concept**: Adversarial Attacks (FGSM).  
  **Key Libs**: `torch`  
  **Goal**: Demonstrate awareness of AI-specific security threats and how to generate adversarial examples.

- **`08_statistical_hypothesis_testing.py`**  
  **Concept**: Rigorous Statistical Comparison.  
  **Key Libs**: `scipy.stats`  
  **Goal**: Use T-tests and Bootstrapping to verify if model improvements are statistically significant.

---

### 5. Mini-Project: LANL Auth "AI for Triage" (Path B)
*Focus: Full "Darktrace-style" pipeline from raw logs to SOC alerts.*
*Location*: `LANL_Auth_Triage_Project/`

- **`download_real_data.sh`**: Download script for the real LANL dataset (~10GB).
- **`01_data_ingestion_preprocessing.py`**: Parses real LANL logs (`auth.txt.gz`).
- **`Synthetic_Utils/generate_synthetic_lanl.py`**: (Optional) Generates synthetic data if real data is unavailable.
- **`02_anomaly_scoring_baselining.py`**: Probabilistic baselining (P(Computer|User)) and Time-of-Day anomaly scoring.
- **`03_graph_features_lateral_movement.py`**: Extracts graph features (PageRank, Out-Degree) to detect lateral movement.
- **`04_incident_ranking_evaluation.py`**: Evaluation using SOC-relevant metrics (Precision@K, Recall@Low-FPR).

---

## 🚀 How to Use
Each file is a standalone executable script. You can run them in any order, but the recommended order is to start with the domain you feel least confident in.

```bash
# Example
python 01_llm_finetuning_lora.py
```

Good luck with the interview prep!
