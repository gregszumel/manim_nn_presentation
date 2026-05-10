# Slides Outline

## Section 1: Intro (~3 min)

> In this L&L I'd like to get across a few things:
> 1. Neural networks are just math, we can reason about them, and they have some interesting properties
> 2. Evaluations become extremely important to evaluate these models well
> 3. Prompting / agent orchestration is pseudo-finetuning, so we need to think carefully about evaluations
> 4. We're also planning on doing an ML summer series that will go in way more detail than I'll go into today. We want to go from zero to your-own-LLM in about 12 weeks - so if you're interested we'll go over that in more detail at the end

**Slide 1 — Title + Goals**
- Static slide, 4 bullet goals appear one at a time
- *~2 min talking through goals, teasing the arc*

---

## Section 2: Neural Networks (~25 min)

**Slide 2 — The Basic Neural Network (~2 min)**
- Animation: nodes fade in layer by layer (input → hidden → output), then edges draw in connecting them
- Labels appear: "activations" on nodes, "weights" on edges
- Brief note that the bio analogy ends here

> This is a neural network that we've all seen -- the 'neurons' or 'activations' are the circles between the lines, and lines are the 'synapses' or 'weights'. I'll prefer activations and weights, since the similarity between human/animal neurons and synapses kinda ceases after our initial outline.

**Slide 3 — How one neuron computes (~3 min)**
- Animation: highlight two input nodes + their edges to a single hidden node
- Numbers appear on each input node (e.g. 0.5, 0.8)
- Numbers appear on edges (weights)
- Show multiplication happening inline: `0.5 × w₀`, `0.8 × w₁`
- Values sum into the hidden node, result appears inside it
- Bias term is added at the end
- Activation function applied to value inside of the neuron

> The model works by taking input activations, multiplying the input activation by its corresponding weight, and summing it with all other activation/weight pairs for that output neuron. We can have any number of input -> output activation counts, we just need to also scale up the amount of corresponding weights, and repeating the process. You may also know of bias terms here and elsewhere. We basically just add a bias to every activation output.
>
> We also usually have 'non-linearity' or 'activation-functions'. Intuitively, we can think of these as similar to human biological networks "threshold" -- they only fire after a certain threshold value is exceeded. But mathematically, they're really important. Let's see why.

**Slide 4 — Writing it as equations (~2 min)**
- Animation: equations materialize next to the diagram
  - `h₀ = i₀·w₀₀ + i₁·w₁₀`
  - `h₁ = i₀·w₀₁ + i₁·w₁₁`
- Show both hidden neurons computed in sequence

> So let's be a little more formal here. We can write this out in equation format -- where the top index is the layer we're in, the first index is our starting neuron index, and the last index is the ending neuron index. We can write h_{0,0} = i_0 * w_{0,0} + i_1 * w_{1,0}. We can also write the same for our other hidden neuron.

**Slide 5 — This is just matrix multiplication (~3 min)**
- Animation: equations from slide 4 rearrange and group into matrix form
- `h = W·i` appears, matrix brackets draw around the weight terms
- Visual: the network diagram on one side, the matrix equation on the other, with a `=` between them

> Then we can show visually that this is just matrix multiplying. Hopefully you're convinced that a layer of a neural network is equivalent to a matrix multiplication!

**Slide 6 — Two layers without activation functions (~3 min)**
- Animation: second layer of weights + output node appears on the network
- Equations: `h = W₀·i`, then `o = W₁·h`
- Substitution animation: `h` replaced inline → `o = W₁(W₀·i)`
- Key step: `W₁W₀` collapses into a single matrix `W*`
- Punchline: "no matter how many layers, without activation functions, it's still just one matrix — one linear transformation"

> Now suppose we added another layer, without an activation function. We know that we basically now do another matrix multiplication. If we substitute in h, we get o = W₁(W₀i). We can re-order the way we multiply them together, so we get o = (W₁W₀)i. But we can just multiply these two matrices together, and we get a new matrix.

**Slide 7 — Activation functions (~2 min)**
- Animation: σ symbol appears wrapping the inner computation in the equations
- `h = σ(W₀·i)`, `o = W₁·σ(W₀·i)`
- Show that substitution no longer collapses — the σ blocks it
- Brief: ReLU curve appears, label "fires past a threshold"

> How on earth are we going to add a layer? Well you guessed it, an activation function. As long as it is non-linear we can separate layers into chunks that cannot be re-ordered. The equations become h = σ(W₀i), and o = W₁h -> o = W₁σ(W₀i).

**Slide 8 — The XOR Problem (~4 min)**
- Animation: 4 XOR points plot on a 2D grid, colored by class (e.g. red/blue)
  - (0,0)→0, (1,1)→0, (0,1)→1, (1,0)→1
- A line tries to separate them, visibly fails no matter the angle
- Then: hidden layer + activation added to the network diagram
- New coordinate space appears — points are now linearly separable
- Line successfully separates them

> This gives us a huge amount of representational power that we didn't have before. Let's look at a classic example, called the XOR problem. XOR is unsolvable without activation functions - because 2 inputs -> 1 output always boils down to a 2x1 matrix, no matter how many hidden layers you have. The 2x1 matrix is a linear transformation, and there is no line that can separate all these points. But if we add activations, now we can represent more complex functions, including XOR!

**Slide 9 — Universal Function Approximators (~3 min)**
- Animation: four small subplots appear side by side
  - Linear, quadratic, exponential, random scatter
- For each: a neural network approximation curve draws in over the true function
- Punchline text fades in: "NNs can approximate any function"

> In fact, neural networks are called universal function approximators -- meaning they can approximate any function. What's crazy is that this means we can approximate any function -- linear, exponential, quadratics, and even random outputs.

**Slide 10 — Universal Function Approximators: Real World (~3 min)**
- Animation: A picture of a cat flattens out into individual pixels and arranges itself as a line as input to a neural network. The output says "cat". Another picture of a dog flattens out and plays into the neural network and the output says "not cat"
- Animation: A visual of an audio waveform flattens out into numbers and also goes into the network, and the output says "Ten-four"

> There's no need to stick to 2D classification/regression problems! These functions are universal after all. Images and audio are both fundamentally just numbers. Neural networks can approximate some function that maps pixel values to whether there's a cat. In the language model case, there's some function that can take in an entire mystery novel before the last word and accurately predict "And the killer was...". These are all just functions -- insanely complicated, but functions. Neural networks can approximate them.

---

## Section 3: Backprop Intuition (~4 min)

**Slide 11 — How do we train? (~2 min)**
- Animation: a simple loss landscape (hyperbola) appears
- A dot (current weights) sits somewhere on the curve
- Arrow appears pointing downhill ("-derivative")
- Dot takes a step in that direction, loss decreases

> Okay this is great and all, but how do we find these universal functions? The primary way is by gradient descent! Jesse covered it earlier in more technical rigor, but here's a quick recap of the basic idea. We have some function that we'd like to minimize. We take small steps using the gradient to get to a lower loss. In this case we're minimizing the hyperbola.

**Slide 12 — Gradient descent loop (~2 min)**
- Animation: small loop diagram
  - "Show example" → "Compute error" → "Nudge weights toward correct output" → repeat
- Highlight: "we push weights to match what we saw — so given enough time, it will memorize"

> So we step through our dataset, and for every input, we encourage the model to produce an output that is close to our target output. We try to minimize the difference between the label of the output and the actual prediction we made -- that's the function! Just abs(output - prediction). We just take steps and teach the model example by example.

---

## Section 4: Memorization vs. Generalization (~13 min)

**Slide 13 — Back to the random function (~2 min)**
- Recall slide 9's random scatter subplot
- Animation: zoom in, NN curve fits the points *perfectly*
- Pause. "Wait… it's approximating randomness?"

> I want to go back to one of our examples here -- the randomness. It's approximating randomness? No, that can't be, the definition of randomness means there's no function that can be learned. WHAT THE HECK. I'm a liar? Not exactly -- Then what's happening?

**Slide 14 — Memorization (~3 min)**
- Animation: show the 5 training points explicitly labeled
- New point appears outside the range — NN output is wild/wrong
- Contrast: linear function subpanel from slide 9, new point added — NN extrapolates correctly
- Label: "memorized" vs "learned the function"

> Memorization. Our neural network has memorized the inputs. In other words - it has certainly learned to approximate a function! Just not one that's particularly interesting. It's learned to map these 5 points to 5 other points. That's not the case with these other models. Show how one example can extrapolate a linear or quadratic, while the memorizing neural network cannot extrapolate. Why is that?
>
> It comes down to how we train them. We can carefully set parameters of our neural network to produce some desired output -- this is what early attempts at neural networks tried to do (i.e., for the XOR problem). But by training via gradient descent, we are essentially encouraging the model to memorize input and output pairs. We give an input and tell the model: change your parameters to better match this output. How on earth do we not memorize everything?! We, in fact, do memorize everything, if we train for long enough.

**Slide 15 — Overfitting (~4 min)**
- Animation: ~12 points that roughly follow a line, with noise
- First: simple line drawn through them, small residuals shown, label "some error, good generalization"
- Then: complex squiggly curve that hits every point exactly
- Label: "zero training error, terrible generalization" — this is overfitting

> If we train for long enough (and naively), the model will always learn to map the inputs it sees directly to the outputs. This is called overfitting. The model has overfit to our data and has essentially memorized it, or learned meaningless associations that aren't actually relevant (e.g., if a pixel in the top left corner of images is always lit up on a positive example, ignore the rest of the image and just focus on that pixel). The same thing is definitely true for cat-classifiers -- it might have memorized the cats it's seen and actually not fully grasped the 'concept of a cat'. How can we possibly tell?
>
> What? If our learning task is memorization, by definition, how do we generalize at all? How do LLMs generalize to new inputs? This is a fantastic question, and it's one of the biggest unsolved mysteries about how LLMs and other large models work.

**Slide 16 — Train / Val / Test (~4 min)**
- Animation: a pool of data points splits into three buckets: train, val, test
- Two loss curves plot over training time
  - Training loss: monotonically decreasing
  - Validation loss: decreases, then inflects upward
- Vertical line marks the inflection: "stop here"
- Test set appears separately: "used once, for final comparison"

> A way we get around this is through training -- specifically training by constantly watching for overfitting. We'll usually start with a 'training dataset'. This is the data the model actually learns from. We also have a validation set, which the model never sees. We periodically will check the model's performance on the evaluation set. What we typically see is that as the model trains, training loss goes down (by definition), and validation loss also goes down. But at a certain point, the model begins to memorize/overfit data, and validation loss actually goes up. Then we might also have another dataset that the model has never seen before, called the 'test' dataset. We can use this to compare different models' performance against each other in a fair way.
>
> This is how we evaluate the model, examining the development and test set. It's also why it's so important - we need to determine if the LLM memorized the information or if it is actually generalized inputs. LLM evaluations are just the same - however, they don't release their training data. We literally have no way of knowing if their training data contains the information they're evaluating on. In fact, some studies have shown that it's really difficult to prevent information leakage from the development set into the training set. So the field has moved to using closed-source evaluations -- but even OpenAI was also caught asking for test-set data from a provider. We can be better!

---

## Section 5: Prompting as Fine-tuning (~9 min)

> Now why does this matter? I'd like to try to convince you that if you're doing any LLM prompting, you're basically finetuning it, and you should at least construct a small train/dev/test set so you can be a more effective LM programmer.

**Slide 17 — Simplified LLM diagram (~3 min)**
- Animation: neural network appears with tokens as input nodes (words, labeled)
- Ungenerated positions labeled `<PAD>`
- Causal mask shown as a triangle: lower-index nodes connect forward, not backward
- "Each output is influenced by everything before it"

> We can think of a simplified LLM as a neural network. Each word is fed in at an input activation, and if the model hasn't generated the word yet, it says <PAD> and we ignore it. Current/older inputs can affect future/newer outputs, but future outputs cannot affect past inputs.

**Slide 18 — Prompt as bias term (~2 min)**
- Animation: show a single output activation being computed
- Prompt tokens highlighted — their contribution adds to the activation like a bias
- "Change the prompt → change the bias → change the output"
- Numbers optionally shown for concreteness

> By prompting, we effectively update the activation for the next output by adding a bias term. By changing our prompt, we also change our bias term, and also the output value at that position.

**Slide 19 — The two loops side by side (~3 min)**
- Animation: two columns appear simultaneously
  ```
  Training loop          Prompting loop
  ─────────────          ──────────────
  Run input              Run input
  Check vs expected      Check vs expected
  Update weights         Update prompt
  Repeat                 Repeat
  ```
- Lines draw connecting the parallel steps

> If we do this in a loop (update the prompt, try on new output, run again), we're effectively finetuning the model. We're basically finetuning on one example, and not using gradient descent but instead more of a random walk looking for better performance.

**Slide 20 — Evaluate your prompts (~1 min)**
- Recall the train/val/test diagram from slide 16
- Relabel: "prompt dev set", "held-out eval set"
- "If you're tuning a prompt, you need a holdout — or you're just overfitting to your examples"

> I hope that convinces you that prompting an LLM is similar to finetuning it, albeit not as strongly. But if you're tuning the model, you better be sure you didn't find some sharp corner that the LLM has overfit to. Make sure you keep a holdout set that you can verify against as you're building your perfect prompt.

---

## Section 6: Wrap-up (~2 min)

> Thanks! If this was interesting to you and you want to know more than just hand-wavey explanations, please think about our summer series!

**Slide 21 — Summary + ML Summer Series**
- Static: recap the 4 goals from slide 1, each checked off
- Teaser for the summer series

---

## Timing Summary

| Section | Slides | Est. time |
|---|---|---|
| Intro | 1 | 3 min |
| Neural networks | 2–10 | 25 min |
| Backprop | 11–12 | 4 min |
| Memorization | 13–16 | 13 min |
| Prompting | 17–20 | 9 min |
| Wrap-up | 21 | 2 min |
| **Total** | **21** | **~56 min** |
