# CUDA / ML

The commands I need rarely enough to forget between uses — mostly GPU status
checks and PyTorch/CUDA debugging.

## GPU status
- `nvidia-smi` — utilization, memory, running processes
- `watch -n 1 nvidia-smi` — live refresh every second
- `nvidia-smi --query-gpu=memory.used,memory.total --format=csv` — quick memory-only check
- `nvcc --version` — CUDA toolkit/compiler version (can differ from the driver's reported version)

## PyTorch + CUDA
- `python -c "import torch; print(torch.__version__, torch.version.cuda)"` — installed torch build + the CUDA version it was compiled against
- `python -c "import torch; print(torch.cuda.is_available())"` — sanity check before assuming GPU training
- `python -c "import torch; print(torch.cuda.get_device_name(0))"` — confirm which GPU torch actually sees
- `torch.cuda.memory_summary()` — detailed allocator breakdown, useful when chasing an OOM
- `torch.cuda.empty_cache()` — release cached (not active) memory back to the driver
- `CUDA_VISIBLE_DEVICES=0 python train.py` — restrict which GPU(s) a process can see

## conda + CUDA toolkit
- `conda install pytorch pytorch-cuda=12.1 -c pytorch -c nvidia` — install a CUDA-matched torch build
- `conda list | grep -i cuda` — see what CUDA-related packages are in the current env

## Ollama (local serving)
- `ollama list` — installed models
- `ollama run <model>` — pull (if needed) and start a model interactively
- `ollama ps` — currently loaded models
- `ollama rm <model>` — remove a downloaded model

## Common gotchas (16GB card)
- Driver vs. toolkit mismatch: check the CUDA version at the top of `nvidia-smi`
  (max version the driver supports) against `nvcc --version` / `torch.version.cuda`
  (what's actually installed) — they don't have to match exactly, but the installed
  version must be ≤ what the driver supports.
- OOM on 16GB: drop batch size first, then try `torch.cuda.amp.autocast()` for
  mixed precision, then gradient checkpointing if the model itself is the problem.
- Silent CPU fallback: always assert `torch.cuda.is_available()` at the top of a
  training script — don't assume the GPU got picked up.
