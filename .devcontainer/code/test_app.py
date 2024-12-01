from prediction import predict_aqi

# testing if the output of the model has the expected shape
def test_prediction():
    # pm25, pm10, no2, so2, co, o3, temperature, rainfall, traffic!!, industry
    output = predict_aqi(30, 25, 10, 12, 35, 15, 30, 5, 2, 100)
    assert output == 1, f"Expected output was 1 but got {output}"