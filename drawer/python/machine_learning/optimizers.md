# Optimizers

### Optimizer reference <!-- tag:ml, sgd, adam, adamw, optimizer, training -->

| Optimizer | Key idea | Typical LR | When to reach for it |
|-----------|----------|------------|----------------------|
| SGD | plain gradient step | 0.1 – 0.01 | simple baselines; needs LR tuning |
| SGD + momentum | accumulates a velocity term | 0.1 – 0.01 | CNNs from scratch; often best final accuracy |
| Nesterov | momentum with a lookahead step | 0.1 – 0.01 | slightly better convergence than plain momentum |
| RMSprop | divides by running RMS of gradients | 1e-3 | RNNs; largely superseded by Adam |
| Adam | momentum + per-parameter scaling | 1e-3 | strong default when you don't want to tune |
| AdamW | Adam with decoupled weight decay | 1e-3 | transformers; the correct Adam for regularized training |
| Adagrad | accumulates all past squared grads | 1e-2 | sparse features; LR decays monotonically |

### Key hyperparameters <!-- tag:ml, hyperparameter, beta, weight decay, epsilon -->

| Parameter | Typical | What it controls |
|-----------|---------|------------------|
| `lr` | 1e-3 (Adam), 0.1 (SGD) | step size — the one that matters most |
| `momentum` | 0.9 | SGD velocity carried between steps |
| `betas` | (0.9, 0.999) | Adam's decay for 1st/2nd moment estimates |
| `eps` | 1e-8 | numerical floor in the denominator |
| `weight_decay` | 1e-2 (AdamW), 5e-4 (SGD) | L2 regularization strength |

### optimizer setup in PyTorch <!-- tag:pytorch, adam, adamw, sgd, optimizer -->
```python
import torch

# strong default for most things
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)

# SGD with momentum — often better final accuracy on vision, more tuning
optimizer = torch.optim.SGD(
    model.parameters(), lr=0.1, momentum=0.9, nesterov=True, weight_decay=5e-4
)
```

### learning rate schedulers <!-- tag:pytorch, scheduler, learning rate, warmup, cosine -->
```python
import torch

# cosine decay over the full run — common for transformers and modern vision
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)

# drop the LR when validation loss plateaus
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode="min", factor=0.1, patience=5
)

for epoch in range(num_epochs):
    train_one_epoch()
    scheduler.step()          # ReduceLROnPlateau takes a metric: scheduler.step(val_loss)
```

### AdamW vs Adam weight decay <!-- tag:pytorch, adamw, weight decay, regularization, l2 -->
```python
# Adam applies weight decay INSIDE the adaptive step, so it gets scaled by the
# per-parameter learning rate — not true L2 regularization.
torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-2)     # coupled

# AdamW decouples it: decay is applied directly to the weights, independent of
# the gradient scaling. This is what you want almost every time.
torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)    # decoupled
```
