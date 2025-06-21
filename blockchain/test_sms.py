from blockchain.send_sms import send_alert

# Dummy data for testing
reason = "Test Failure: ΔT too low"
delta_t = 1.3

send_alert(reason, delta_t)
