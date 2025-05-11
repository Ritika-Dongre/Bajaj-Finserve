import requests


payload = {
    "name": "Ritika Dongre",
    "regNo": "0827CI221117",  
    "email": "ritikadongre220750@acropolis.in"
}


response = requests.post("https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON", json=payload)

if response.status_code == 200:
    data = response.json()
    webhook_url = data.get("webhook")
    access_token = data.get("accessToken")

    print("Webhook URL:", webhook_url)
    print("Access Token:", access_token)

    final_sql = """
SELECT 
  p.AMOUNT AS SALARY,
  CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
  FLOOR(DATEDIFF('2025-03-05', e.DOB) / 365) AS AGE,
  d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE DAY(p.PAYMENT_TIME) != 1
ORDER BY p.AMOUNT DESC
LIMIT 1;
"""

   
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }

    submit_payload = {
        "finalQuery": final_sql.strip()
    }

    submit_response = requests.post(webhook_url, headers=headers, json=submit_payload)

    if submit_response.status_code == 200:
        print("Successfully submitted the SQL query!")
    else:
        print("Submission failed:", submit_response.text)

else:
    print(" Webhook generation failed:", response.text)
