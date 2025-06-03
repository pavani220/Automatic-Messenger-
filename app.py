from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.parse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    numbers_raw = request.form['numbers']
    message = request.form['message']

    # Split numbers by line and clean them
    numbers = [num.strip() for num in numbers_raw.strip().split('\n') if num.strip()]

    # Start browser
    driver = webdriver.Chrome()  # Optional: specify path to ChromeDriver here
    driver.get("https://web.whatsapp.com")
    print("Please scan the QR code in the browser to continue.")
    time.sleep(20)  # Adjust if login takes longer

    for number in numbers:
        encoded_msg = urllib.parse.quote(message)
        url = f"https://web.whatsapp.com/send?phone={number}&text={encoded_msg}"
        driver.get(url)
        time.sleep(10)  # Load chat

        try:
            send_btn = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            send_btn.click()
            print(f"Message sent to {number}")
        except Exception as e:
            print(f"Failed to send to {number}: {e}")
        time.sleep(5)

    driver.quit()
    return "Messages sent successfully!"

if __name__ == '__main__':
    app.run(debug=True)




