import tensorflow as tf

def custom_simclr_loss(x1, x2, temperature=0.13):
    # Normalize the input vectors
    x1_normalized = tf.math.l2_normalize(x1, axis=1)
    x2_normalized = tf.math.l2_normalize(x2, axis=1)

    # Calculate cosine similarity matrix
    similarity_matrix = tf.matmul(x1_normalized, x2_normalized, transpose_b=True)

    # Calculate logits with temperature scaling
    logits = similarity_matrix / temperature

    # Create labels for positive pairs (diagonal elements)
    batch_size = tf.shape(x1)[0]
    # Create labels for positive pairs (diagonal elements)
    labels = tf.eye(batch_size * 2)
    labels = tf.linalg.set_diag(labels, tf.eye(batch_size * 2))

    # Calculate NT-Xent loss
    loss = tf.losses.categorical_crossentropy(labels, logits, from_logits=True)

    # Take the mean over the batch
    loss = tf.reduce_mean(loss)

    return loss

# Example usage:
x11 = [float(x) for x in range(10)]
x12 = [float(x) for x in range(10, 20)]
x13 = [float(x) for x in range(20, 30)]
x14 = [float(x) for x in range(30, 40)]
x1 = [x11, x12, x13, x14]
print(x1)
x1 = tf.convert_to_tensor(x1)
print(x1)

x21 = [float(x) for x in range(20, 30)]
x22 = [float(x) for x in range(30, 40)]
x23 = [float(x) for x in range(40, 50)]
x24 = [float(x) for x in range(50, 60)]
x2 = [x21, x22, x23, x24]
print(x2)
x2 = tf.convert_to_tensor(x2)
print(x2)
loss_value = custom_simclr_loss(x1, x2)
print("SimCLR Loss:", loss_value.numpy())
