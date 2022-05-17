from unicodedata import name
from pandas import read_csv
from PIL import Image, ImageDraw, ImageFont
import pyqrcode
import mail
import create_pass

data = read_csv("pass.csv").values.tolist()
template = Image.open("templates/pass_template.png")
detailsFont = ImageFont.truetype("fonts/Poppins-Regular.ttf", 60)
allowedFont = ImageFont.truetype("fonts/Poppins-SemiBold.ttf", 65)


def makeCertificate(student):
    response = create_pass.create_pass(student[0], student[1], student[2], student[3])

    cert = template.copy()
    draw = ImageDraw.Draw(cert)
    # qrcodes
    size = makeQR(response["_id"])
    pos = ((842 - int(size / 2)), 160)
    cert.paste(Image.open("templates/qr_code.png"), pos)
    # unique number
    w, h = draw.textsize(response["_id"].upper(), detailsFont)
    draw.text(
        xy=((1684 - w) / 2, 1100),
        text=response["_id"].upper(),
        fill="#03045E",
        font=detailsFont,
    )
    # name
    nameFont = 150
    w, h = draw.textsize(
        student[1].upper(), ImageFont.truetype("fonts/Poppins-Bold.ttf", nameFont)
    )
    difference = w - (1682 - 440)
    if difference > 0 and difference <= 100:
        nameFont = 130
    elif difference > 100 and difference <= 250:
        nameFont = 110
    elif difference > 250 and difference <= 400:
        nameFont = 100
    elif difference > 400:
        nameFont = 80
    else:
        nameFont = 150
    draw.text(
        xy=(220, 1450),
        text=student[1].upper(),
        fill="white",
        font=ImageFont.truetype("fonts/Poppins-Bold.ttf", nameFont),
    )
    # email
    draw.text(xy=(220, 1650), text=student[0], fill="white", font=detailsFont)
    # roll
    draw.text(xy=(220, 1740), text=student[2].upper(), fill="white", font=detailsFont)
    # allowed
    allowText = "Single Entry Only"
    match student[3]:
        case 3:
            allowText = "+2 allowed"
        case 2:
            allowText = "+1 allowed"
    draw.text(xy=(360, 2330), text=allowText, fill="white", font=allowedFont)

    print(student[0])
    cert.save(str("img/" + student[0]) + "_pass.png")

    # send email
    mail.send_mail(student[0], student[1], response["_id"], str(response["allowed"]))


def makeQR(data):
    qr = pyqrcode.create(data)
    qr.png(
        "templates/qr_code.png", scale=30, module_color="#03045E", background="#538EFF"
    )
    return qr.get_png_size(30)


for i in data:
    makeCertificate(i)
