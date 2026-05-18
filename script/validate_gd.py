"""
Validate the SGD setup from scene11/scene12.

Runs the exact same math and reports loss per epoch.  If this doesn't
converge to a small loss, neither will the animation.
"""

import numpy as np

# ── Same constants as scene11 ─────────────────────────────────────
# Break points spread across [-1.5, 1.5], activations point AWAY from origin
# so b2 stays small and the basis is well-conditioned.
# break_point_j = -B1[j] / W1[j]
N_HIDDEN = 6
W1 = np.array([ 1.0,  1.0,  1.0, -1.0, -1.0, -1.0])
B1 = np.array([-0.5, -1.0, -1.5, -0.5, -1.0, -1.5])
# → break points: +0.5, +1.0, +1.5, -0.5, -1.0, -1.5
# At x=0 all ReLUs are off → b2 ≈ target(0)


def true_fn(x):
    return 0.6 * float(x) ** 2 - 1.0


def relu(x):
    return np.maximum(0.0, x)


def forward(x, W2, b2):
    h = relu(W1 * float(x) + B1)
    return float(np.dot(W2, h) + b2)


def grad_step(x, y_true, W2, b2, lr):
    h = relu(W1 * float(x) + B1)
    y_pred = float(np.dot(W2, h) + b2)
    error = y_pred - y_true
    return W2 - lr * 2.0 * error * h, b2 - lr * 2.0 * error


def mean_loss(W2, b2, xs):
    return float(np.mean([(forward(x, W2, b2) - true_fn(x)) ** 2 for x in xs]))


def main():
    rng = np.random.default_rng(7)
    W2 = rng.normal(0, 0.4, N_HIDDEN)
    b2 = float(rng.normal(0, 0.3))

    train_xs = np.linspace(-1.6, 1.6, 8)

    print(f"Initial W2: {W2}")
    print(f"Initial b2: {b2:.4f}")
    print(f"Initial loss: {mean_loss(W2, b2, train_xs):.4f}")
    print()

    # ── Reference: closed-form least-squares solution ──
    H_aug = np.column_stack(
        [relu(W1[j] * train_xs + B1[j]) for j in range(N_HIDDEN)]
        + [np.ones(len(train_xs))]
    )
    y_target = np.array([true_fn(x) for x in train_xs])
    w_opt, _, _, _ = np.linalg.lstsq(H_aug, y_target, rcond=None)
    W2_opt = w_opt[:N_HIDDEN]
    b2_opt = float(w_opt[N_HIDDEN])
    opt_loss = mean_loss(W2_opt, b2_opt, train_xs)
    print(f"Least-squares-optimal loss: {opt_loss:.6f}")
    print(f"Optimal W2: {W2_opt}")
    print(f"Optimal b2: {b2_opt:.4f}")
    print()

    # ── SGD ──
    for lr in [0.03, 0.05, 0.08, 0.12, 0.20]:
        W2 = rng.normal(0, 0.4, N_HIDDEN)
        b2 = float(rng.normal(0, 0.3))
        # Re-seed deterministically per lr trial so each starts from same init
        rng2 = np.random.default_rng(7)
        W2 = rng2.normal(0, 0.4, N_HIDDEN)
        b2 = float(rng2.normal(0, 0.3))

        print(f"=== lr = {lr} ===")
        print(f"epoch 0  loss = {mean_loss(W2, b2, train_xs):.4f}")
        for epoch in range(1, 11):
            for x in train_xs:
                W2, b2 = grad_step(x, true_fn(x), W2, b2, lr)
            print(f"epoch {epoch}  loss = {mean_loss(W2, b2, train_xs):.4f}")
        print()


if __name__ == "__main__":
    main()
