import tensorflow as tf


class GaussianInitializer(tf.keras.initializers.Initializer):
    def __init__(self):
        super().__init__()
        self.sigma = 2

    def _gaussian_kernel(kernel_size, sigma, n_channels, dtype):
    x = tf.range(-kernel_size // 2 + 1, kernel_size // 2 + 1, dtype=dtype)
    g = tf.math.exp(-(tf.pow(x, 2) / (2 * tf.pow(tf.cast(sigma, dtype), 2))))
    g_norm2d = tf.pow(tf.reduce_sum(g), 2)
    g_kernel = tf.tensordot(g, g, axes=0) / g_norm2d
    g_kernel = tf.expand_dims(g_kernel, axis=-1)
    return tf.expand_dims(tf.tile(g_kernel, (1, 1, n_channels)), axis=-1)


def apply_blur(img):
    blur = _gaussian_kernel(3, 2, 3, img.dtype)
    img = tf.nn.depthwise_conv2d(img[None], blur, [1,1,1,1], 'SAME')
    return img[0]

data = tf.data.Dataset.from_tensor_slices(
    (tf.pad(tf.ones((1, 1, 1, 2)), ((0, 0),(1, 1),(1, 1),(0,1))), tf.ones((1, 3, 3, 1)))
).map(lambda x, y: (apply_blur(x), y)).repeat().batch(10)


x = tf.keras.layers.Input((10, 10, 3))
y = tf.keras.layers.Conv2D(filters=1, kernel_size=1, activation=tf.keras.activations.relu)(x)

model = tf.keras.models.Model(inputs=[x], outputs=[y])
model.compile(loss=tf.losses.binary_crossentropy)
model.fit(data, steps_per_epoch=10, epochs=10)



