from soil import get_data_JSON, loaded_model, chain1, chain2
import random
import json
import time

# Load sensor data
with open('assets/sensor_data.json', 'r') as infile:
    sensor_data = json.load(infile)

def info_response(input_sensor, language="English"):
    """Generate analysis response for sensor data"""
    data_json = get_data_JSON(input_sensor, loaded_model)
    explanation = chain1.predict(data_JSON=json.dumps(data_json, indent=2), language=language)
    return explanation, data_json

def chat_response(history, message, language="English"):
    """Generate chat response based on history and message"""
    # Format history for the prompt
    formatted_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
    explanation = chain2.predict(user_history=formatted_history, user_message=message, language=language)
    return explanation

def get_sensor_data():
    """Get random sensor data from the JSON file"""
    keys = [
        "N - Ratio of Nitrogen (NH4+) content in soil",
        "P - Ratio of Phosphorous (P) content in soil",
        "K - Ratio of Potassium (K) content in soil",
        "pH - Soil acidity (pH)",
        "ec - Electrical conductivity",
        "oc - Organic carbon",
        "S - Sulfur (S)",
        "zn - Zinc (Zn)",
        "fe - Iron (Fe)",
        "cu - Copper (Cu)",
        "Mn - Manganese (Mn)",
        "B - Boron (B)"
    ]
    
    # Get random sensor reading
    timestamp = random.choice(list(sensor_data.keys()))
    input_sensor = sensor_data[timestamp]
    
    # Create formatted dictionary
    data_dict = {k: v for k, v in zip(keys, input_sensor)}
    
    return data_dict, input_sensor, timestamp

def get_multiple_sensor_samples(n=2):
    """Get multiple unique sensor samples"""
    samples = []
    used_timestamps = []
    
    available_timestamps = list(sensor_data.keys())
    
    for i in range(min(n, len(available_timestamps))):
        # Get unused timestamp
        remaining = [t for t in available_timestamps if t not in used_timestamps]
        if not remaining:
            break
            
        timestamp = random.choice(remaining)
        used_timestamps.append(timestamp)
        
        data_dict, input_sensor, _ = get_sensor_data_by_timestamp(timestamp)
        samples.append({
            "data_dict": data_dict,
            "input_sensor": input_sensor,
            "timestamp": timestamp,
            "sample_id": f"Sample {i+1}"
        })
    
    return samples

def get_sensor_data_by_timestamp(timestamp):
    """Get specific sensor data by timestamp"""
    keys = [
        "N - Ratio of Nitrogen (NH4+) content in soil",
        "P - Ratio of Phosphorous (P) content in soil",
        "K - Ratio of Potassium (K) content in soil",
        "pH - Soil acidity (pH)",
        "ec - Electrical conductivity",
        "oc - Organic carbon",
        "S - Sulfur (S)",
        "zn - Zinc (Zn)",
        "fe - Iron (Fe)",
        "cu - Copper (Cu)",
        "Mn - Manganese (Mn)",
        "B - Boron (B)"
    ]
    
    input_sensor = sensor_data[timestamp]
    data_dict = {k: v for k, v in zip(keys, input_sensor)}
    
    return data_dict, input_sensor, timestamp
