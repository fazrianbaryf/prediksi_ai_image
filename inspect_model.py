import tensorflow as tf
import os

try:
    model_path = 'model.keras'
    if not os.path.exists(model_path):
        model_path = 'model.h5'
    
    print(f"Loading model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
    
    print("Model loaded successfully.")
    
    input_shape = model.input_shape
    print(f"Input Shape: {input_shape}")
    
    output_shape = model.output_shape
    print(f"Output Shape: {output_shape}")
    
    # Try to see config for more details if needed
    # print(model.get_config())

except Exception as e:
    print(f"Error: {e}")
