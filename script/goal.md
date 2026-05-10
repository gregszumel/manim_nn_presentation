
## Intro slide

In this L&L I'd like to get across a few things:

1) Neural networks are just math, we can reason about them, and they have some interesting properties
2) Evaluations become extremely important to evaluate these models well
3) Prompting / agent orchestration is pseudo-finetuning, so we need to think carefully about evaluations
4) We're also planning on doing an ML summer series that will go in way more detail than I'll go into today. We want to go from zero to your-own-LLM in about 12 weeks - so if you're interested we'll go over that in more detail at the end

## Neural networks - mathematical perspective

This is a neural network that we've all seen -- the 'neurons' or 'activations' are the circles between the lines, and lines are the 'synapses' or 'weights'. I'll prefer activations and weights, since the similarity between human/animal neurons and synapses kinda ceases after our initial outline

The model works by taking input activations, multiplying the input activation by it's corresponding weight, and summing it with all other activation/weight pairs for that output neuron. We can have any number of input -> output activation counts, we just need to also scale up the amount of corresponding weights, and repeating the process. You may also know of bias terms here and elsewhere. We basically just add a bias to every activation output.

We also usually have 'non-linearity' or 'activation-functions'. Intuitively, we can think of these as similar to human biological networks "threshold" -- they only fire after a certain threshold value is exceeded. But mathematically, they're really important. Let's see why.

So let's be a little more formal here. We can write this out in equation format ($x_{i, j}^l$)- where the top index is the layer we're in, the first index is our starting neuron index, and the last index in the ending neuron index. We can write $h_{0, 0} = i_{0} * w_{0, 0} + i_{1} * w_{1, 0}$. We can also write the same our other hidden neuron. Then we can show visually that this is just matrix multiplying. Hopefully you're convinced that a layer of a neural network is equivalent to a matrix multiplication!

Now suppose we added another layer, without an activation function. Well, we know that we basically now do another matrix multiplication (two equations, where $h = W_0a$, and $o = W_1h$). If we substitute in h in equation 2, we get $o = W_1(W_0i)$. Although matrix multiplication is a little weird, in that we can't re-order variables in a multiplicaiton, we can re-order the way we multiply them together. so we can do $o = (W_1W_0)i $. But we can just multiply these two matrices together, and we get a new matrix. Visually, TODO: what is this?

How on earth are we going to add a layer? Well you guessed it, an activation function. As long as it is non-linear (i.e., also called non-linearities) we can separate layers into chunks that cannot be re-ordered. The equations become $h = \sigma(W_0i)$, and $o = W_1h -> o = W_1\sigma(W_0i)$

This gives us a huge amount of representational power that we didn't have before. Let's look at a classic example, called the XOR problem
XOR is unsolvable without activation functions - because 2 inputs (x/y coordinates) -> 1 output (class label) always boils down to a 2x1 matrix, no matter how many hidden layers you have. The 2x1 matrix is a linear transformation, and there is no line that can separate all these points. But if we add activations, now we can represent more complex functions, including the xor!

In fact, neural networks are called universal function approximators -- meaning they can approximate (or mimic) any function (universal function).

What's crazy, is that this means we can approximate any function (show a handful of functions, their approximations, and weights: linear, exponential, quadratics, and random outputs).

There's no need for us to stick to stick to the 2d classification / regression problems! These functions are universal after all - we can represent anything. Images (cat detector), and audio are both also fundamentally just numbers. Neural networks can approximate some function (and there is some function out there) that maps these collection of pixel values to whether or not there's a cat! This audio to whether or not there is speech. In the language models case, there's some function that can take in an entire mystery novel before the last word, and can accurately predict the next word from: "And the killer was ...". it's kind of mind bending to think about, but these are all just functions, albeit insanely complicated, but these are functions! Neural networks can approximate them.

## Backprop

maybe

## Memorization vs generalization, and why we need evaluations

I want to go back to one of our examples here -- the randomness. It's approximating randomness? No, that can't be, the definition of randomness means there's no function that can be learned. WHAT THE HECK. I'm a liar? Not exactly -- Then what's happening?

Memorization. Our our neural network has memorized the inputs. In other words - it has certainly learned to approximate a function! Just not one that's particularly interesting. It's learned to map these 5 points to 5 other points. That's not the case with these other models. (Show how one example can extrapolate a linear or quadratic, while the memorizing neural network cannot extrapolate (obviously, it's a random function)) Why is that?

It comes down to how we train them. We can carefully set parameters of our neural network to produce some desired output -- why is what early attempts at neural networks tried to do (i.e., for the XOR problem). But by training via gradient descent, we are essentially encouraging the model to memorize input and output pairs. We give an input and tell the model, change your parameters to better match this output. How on earth do we not memorize everything?! We, in fact, do memorize everything, if we train for long enough.

If we train for long enough (and naively), the model will always learn to map the inputs it sees directly to the outputs. (Show a graph that we're fitting that is almost a line,and show a line with a little error, and iterate on reducing the error at the expense of increasing the complexity). This is called overfitting. The model has overfit to our data and has essentially memorized it, or learned meaningless associations that aren't actually relevant (e.g., if a pixel in the top left corner of images is always lit up on a positive example, ignore the rest of the image and just focus on that pixel). The same thing is definitely true for cat-classifiers -- it might have memorized the cats it's seen and actually not fully grasped the 'concept of a cat' to anthropomorphize with the neural network. How can we possibly tell?

What? If our learning task is memorization, by definition, how do we generalize at all? How do LLMs generalize to new inputs? This is a fantastic question, and it's one of the biggest unsolved mysteries about how LLMs and other large models work.

A way we get around this is through training -- specifically training by constantly watching for overfitting. We'll usually start with a 'training dataset'. This is the data the model actually learns from. We also have an validation set, which the model never sees. We periodically will check the model's performance on the evaluation set. What we typically see is that as the model trains, training loss goes down (by definition), and validation loss also goes down. But at a certain point, the model begins to memorize/overfit data, and validation loss actually goes up. Then we might also have another dataset that the model has never seen before, called the 'test' dataset. We can use this to compare different model's performance against each other in a fair way.

This is how we evaluate the model, examining the development and test set. It's also why it's so important - we need to determine if the LLM memorized the information or if it is actually generalized inputs. LLM evaluations are just the same - however, they don't release their training data. We literally have no way of knowing if their training data contains the information they're evaluating on. In fact, some studies have shown that it's really difficult to prevent information leakage from the development set into the training set. So the field has moved to using closed-source evaluations -- but even OpenAI was also caught asking for test-set data from a provider. We can be better!

## Prompting is akin to Fine-tuning

Now why does this matter? I'd like to try to convince you that if you're doing any llm-prompting, you're basically finetuning it, and you should at least construct a small train/dev/test set so you can be a more effective lm-programmer.

Let's go back to the visual here. We can think of a simplified LLM as a being a neural network. In this setup, each word is fed in at an input activation, and if the model hasn't generated the word yet, it just says <PAD> and we ignore it. Also, current/older inputs can affect future/newer outputs, but future outputs cannot affect past inputs. (visual showing the edge layout,  where activations with a higher index are not linked to ones with a lower one, but ones with lower activation indcies are linked to everything with a higher activation). By prompting, we effectively update the activation for the next output by adding a bias term. By changing our prompt, we also change our bias term, and also the output value at that position. This is effectively finetuning the model -- we're updating the bias term in this illustrative example.

The loops are also incredibly similar:

Training loop:               Prompting loop:
- Run input through model    - Run input through model
- Check output vs expected   - Check output vs expected
- Update weights to improve  - Update prompt to improve
- Repeat on more examples    - Repeat on more examples


I hope that convinces you that prompt an LLM is similar to finetuning it, albeit not as strongly. But if you're tuning the model, you better be sure you didn't find some sharp corner that the LLM has overfit to. Make sure you keep a holdout set that you can verify against as you're building your perfect prompt.


Thanks! If this was interesting to you and you want to know more than just hand-wavey explanations, please think about our summer series!




