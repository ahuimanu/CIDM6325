def calculate_eta_detailed(data):
    return "Estimated delivery in 2 hours"  # ✅ This is fine

# logistics_app/ai_engine.py

def calculate_eta_mock(order):              # ⛔ Overwrites the first one
    return "ETA: 3 hours (mock)"
