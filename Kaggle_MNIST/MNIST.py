#Load the dataset
import pandas as pd
import math
import numpy as np

def series_trans(series1, n):
  tmp = []
  for x in series1:
    if x == n:
      tmp.append(1.0)
    else:
      tmp.append(0.0)
  series2 = pd.Series(tmp)
  return series2

train = pd.read_csv('train.csv')
train.drop(['label'], axis = 1, inplace = True)
train = train.values
train = np.float32(train)

label = pd.read_csv('train.csv',usecols = [0])
for x in range(10):
  label[str(x)] = series_trans(label['label'], x)
label.drop(['label'], axis = 1, inplace = True)
label = label.values
label = np.float32(label)

test = pd.read_csv('test.csv')
test = test.values
test = np.float32(test)

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

#Implementing the regression
import tensorflow as tf
x = tf.placeholder(tf.float32, shape=[None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.matmul(x, W) + b

#Training
y_ = tf.placeholder(tf.float32, shape=[None, 10])


W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
x_image = tf.reshape(x, [-1,28,28,1])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])
y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

sess = tf.InteractiveSession()

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
#train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
train_step = tf.train.RMSPropOptimizer(1e-3).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
result = tf.argmax(y_conv,1)
sess.run(tf.global_variables_initializer())

SampleNum = len(label)
Start = 0
Step = 100
for i in range(15000):
  batch_xs = train[Start:Start+Step]
  batch_ys = label[Start:Start+Step]
  if i%100 == 0:
    train_accuracy = accuracy.eval(feed_dict={
        x:batch_xs, y_: batch_ys, keep_prob: 1.0})
    print("step %d, training accuracy %g"%(i, train_accuracy))
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys, keep_prob: 0.5})
  if Start + Step < SampleNum:
    Start += Step
  else:
    Start = Start+Step-SampleNum

Output = []

for m in test:
  Output.append(sess.run(result, feed_dict={x: [m], keep_prob: 1.0})[0])
print (Output[0:5])
Output_File = open('Output.txt', 'w')
for x in Output:
  Output_File.write(str(x)+'\n')
Output_File.close()
