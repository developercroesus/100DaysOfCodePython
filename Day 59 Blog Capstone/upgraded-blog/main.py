from flask import Flask, render_template, request
import requests
import smtplib
import os

GMAIL = "johnwesleydavisII@gmail.com"
GMAIL_SMTP = "smtp.gmail.com"
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")
print(GMAIL_PASSWORD)
YAHOO = "johnwesleydavis@yahoo.com"

url = "https://api.npoint.io/cc03a5956b41677ec7b6"
app = Flask(__name__)

response = requests.get(url)
datas = response.json()


@app.route('/')
def get_all_posts():
    return render_template("index.html", datas=datas)


@app.route("/about.html")
def about():
    return render_template("about.html")


@app.route("/contact.html", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        from_email = data["email"]
        name = data["name"]
        message = data["message"]

        send_email(email=YAHOO,
                   from_email = from_email,
                   subject = f"Contact Form from {name}",
                   message = message)
        return render_template("contact.html", header="Successfully sent your message")

    return render_template("contact.html", header="Contact Me")


@app.route("/post.html/<num>")
def post(num):
    post_data = datas[int(num) - 1]
    return render_template("post.html", post=post_data)


def send_email(email, from_email, subject, message):
    msg = f"Subject:{subject}\n\n{message}"
    with smtplib.SMTP(GMAIL_SMTP) as connection:
        connection.starttls()
        connection.login(user=GMAIL, password=GMAIL_PASSWORD)
        connection.sendmail(
            from_addr=from_email,
            to_addrs=email,
            msg=msg
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
