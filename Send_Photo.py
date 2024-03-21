# 连接服务器
import smtplib
import ssl
from email.message import EmailMessage
import base64
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def Send_Photo(picture_name):
    # 邮箱地址
    EMAIL_ADDRESS = '2231742813@qq.com'
    # SMTP的授权码(QQ邮箱设置里
    EMAIL_PASSWORD = 'ervlwvcemlkidifa'
    """
    在smtplib中，如果您将context设置为None，这意味着您的SMTP连接将不会使用SSL/TLS加密，即使目标SMTP服务器支持它。这可能会导致您发送的邮件的安全性受到威胁，因为它们可能会在网络传输过程中被拦截或篡改。
    如果您想确保SMTP连接的安全性，我建议您将context参数设置为一个有效的SSLContext对象，以便启用SSL/TLS加密。您也可以考虑使用其他方法（如STARTTLS命令）来启用SMTP连接的加密。
    """
    context = ssl.create_default_context()
    # 发件人邮箱
    # sender = '2231742813@qq.com'
    # 收件人邮箱
    receiver = '2508427602@qq.com'
    # 邮件的标题
    subject = '手机拍摄图片'

    # 读取图片数据并编码为 base64，以便在 HTML 中嵌入
    with open(r"\\192.168.30.65/yf1/wengzhichao/picture/{}".format(picture_name), 'rb') as f :
        image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')

    # 构造 HTML，其中使用嵌入式数据 URI 将图像添加到HTML中
    html = """
    <html>
        <body>
            <h2>{}</h2>
            <p>图片见下</p>
            <img src='data:image/png;base64,{}'>
        </body>
    </html>
    """.format(subject, encoded_image)

    # 创建 MIMEMultipart 对象并设置邮件内容
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver

    # 添加 HTML 和图像作为替代内容
    msg.attach(MIMEText(html, 'html'))
    msg_img = MIMEImage(image_data, name = os.path.basename(picture_name))
    msg.attach(msg_img)

    # 创建 SMTP 客户端对象并发送邮件
    with smtplib.SMTP_SSL("smtp.qq.com", 465, context = context) as smtp :
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_ADDRESS, receiver, msg.as_string())



    # msg = EmailMessage()
    # # 邮件主题
    # msg['subject'] = subject
    # # 发件人
    # msg['From'] = sender
    # # 收件人
    # msg['To'] = receiver
    # # 邮件内容
    # msg.set_content("图片见附件")
    # # 图片处理
    # file_name = r'\\192.168.30.65/yf1/wengzhichao/picture/{}'.format(picture_name)
    # with open(file_name, 'rb') as f :
    #     file_data = f.read()
    #     img_data = base64.b64encode(f.read()).decode('utf-8')
    # msg.add_attachment(file_data, maintype = 'image', subtype = 'jpg', filename = file_name)
    # # 创建SMTP服务器对象
    # smtp = smtplib.SMTP('smtp.qq.com', 25)
    # # 打招呼
    # smtp.ehlo()
    # with smtplib.SMTP_SSL("smtp.qq.com", 465, context = context) as smtp :
    #     smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    #     smtp.send_message(msg)