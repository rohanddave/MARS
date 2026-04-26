# MARS-1 HPC Deployment (NEU Explorer)

> **What this document covers:** Step-by-step runbook for deploying MARS-1 on the NEU Explorer HPC cluster — first-time setup, returning after a timeout, pulling results, and stopping. Copy-paste commands for SSH, srun, conda, vLLM serving, and background result syncing.

---

## First Time Setup

1. **Login node** — clean old state:
```bash
ssh <your-username>@login.explorer.northeastern.edu
rm -rf ~/mars1_staging /tmp/<your-username>* ~/.cache ~/.conda ~/.nv ~/.triton
```

2. **Local machine** — push code:
```bash
cd ~/Desktop/Code\ Projects/MARS-1
rsync -avz --exclude '.venv' --exclude 'venv' --exclude '.git' --exclude '__pycache__' ./ <your-username>@login.explorer.northeastern.edu:~/mars1_staging/
```

3. **Login node** — get a GPU:
```bash
srun --partition=sharing --gres=gpu:h100:1 --mem=64G --time=01:00:00 --pty bash
```

4. **Compute node** — setup environment (copy-paste this whole block):
```bash
export PROJECT_DIR="/tmp/<your-username>_mars_final"
mkdir -p $PROJECT_DIR && cd $PROJECT_DIR

# Sync fresh code (--delete removes files no longer in source)
rsync -avz --delete --exclude 'env_final' --exclude 'hf_cache' --exclude 'res' ~/mars1_staging/ $PROJECT_DIR/
mkdir -p res hf_cache data

# Create conda env and install deps
source /shared/centos7/anaconda3/2021.11/etc/profile.d/conda.sh
conda create --prefix $PROJECT_DIR/env_final python=3.10 -y
conda activate $PROJECT_DIR/env_final
pip install --upgrade pip
pip install vllm==0.19.1
pip install "transformers>=5.5.0" --no-deps
pip install "numpy<2" "torch>=2.4.0" huggingface_hub
pip install -r requirements.txt
```

5. **Same terminal** — serve model and run:
```bash
export HF_HOME="$PROJECT_DIR/hf_cache"
export HF_TOKEN="<your-token>"
vllm serve google/gemma-4-26B-A4B-it --max-model-len 32768 --gpu-memory-utilization 0.90 --port 8000 &
```
Wait for `Uvicorn running on http://0.0.0.0:8000`, then:
```bash
export no_proxy="localhost,127.0.0.1"
export NO_PROXY="localhost,127.0.0.1"
export OPENAI_API_KEY="not-needed"
export OPENAI_BASE_URL="http://localhost:8000/v1"
# Background sync results to home every 5 min
while true; do rsync -az $PROJECT_DIR/res/ ~/mars1_staging/res/ 2>/dev/null; sleep 300; done &

python3 main.py
```

## Returning After Timeout

1. **Local machine** — push latest code:
```bash
cd ~/Desktop/Code\ Projects/MARS-1
rsync -avz --exclude '.venv' --exclude 'venv' --exclude '.git' --exclude '__pycache__' ./ <your-username>@login.explorer.northeastern.edu:~/mars1_staging/
```

2. **Login node** — get a new GPU:
```bash
srun --partition=sharing --gres=gpu:h100:1 --mem=64G --time=01:00:00 --pty bash
```

3. **Compute node** — check if /tmp survived:
```bash
ls /tmp/<your-username>_mars_final/env_final/bin/python
```

3a. **If it exists** — clean stale files and restart:
```bash
export PROJECT_DIR="/tmp/<your-username>_mars_final"
cd $PROJECT_DIR

# Sync fresh code (--delete removes files no longer in source)
rsync -avz --delete --exclude 'env_final' --exclude 'hf_cache' --exclude 'res' ~/mars1_staging/ $PROJECT_DIR/

source /shared/centos7/anaconda3/2021.11/etc/profile.d/conda.sh
conda activate $PROJECT_DIR/env_final
```
Then serve model and run (same as step 5 above):
```bash
export HF_HOME="$PROJECT_DIR/hf_cache"
export HF_TOKEN="<your-token>"
vllm serve google/gemma-4-26B-A4B-it --max-model-len 32768 --gpu-memory-utilization 0.90 --port 8000 &
```
Wait for `Uvicorn running on http://0.0.0.0:8000`, then:
```bash
export no_proxy="localhost,127.0.0.1"
export NO_PROXY="localhost,127.0.0.1"
export OPENAI_API_KEY="not-needed"
export OPENAI_BASE_URL="http://localhost:8000/v1"
# Background sync results to home every 5 min
while true; do rsync -az $PROJECT_DIR/res/ ~/mars1_staging/res/ 2>/dev/null; sleep 300; done &

python3 main.py
```

3b. **If it doesn't exist** — redo step 4 and 5 from First Time Setup.

## Pulling Results (from local machine)

```bash
rsync -avz <your-username>@login.explorer.northeastern.edu:~/mars1_staging/res/ ./res/
```

Background sync copies results to `~/mars1_staging/res/` every 5 minutes, so this works even after the allocation ends. Checkpointing skips completed experiments on re-run.

## Stopping

```bash
kill %1
exit
exit
```
