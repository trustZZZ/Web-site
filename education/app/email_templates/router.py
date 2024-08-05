import hashlib
from email.message import EmailMessage

from random import randbytes
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends

from jinja2 import Environment, select_autoescape, PackageLoader
from pydantic import EmailStr, BaseModel
from app.users.dao import UsersDAO
import smtplib

from app.config import settings

from fastapi_mail import ConnectionConfig

from app.users.dependencies import get_current_user
from app.users.schemas import SUserID

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


class Email:
    def __init__(self, url: str, email: List[EmailStr]):
        self.sender = 'Codevo <dogisocks@yandex.ru>'
        self.email = email
        self.url = url
        pass

    async def send_mail(self, subject, template):
        # Define the config
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.EMAIL_USERNAME,
            MAIL_PASSWORD=settings.EMAIL_PASSWORD,
            MAIL_FROM=settings.EMAIL_FROM,
            MAIL_PORT=settings.EMAIL_PORT,
            MAIL_SERVER=settings.EMAIL_HOST,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        # Generate the HTML template base on the template name
        template = env.get_template(f'{template}.html')

        html = template.render(
            url=self.url,
            subject=subject
        )

        # Define the message options
        # message = MessageSchema(
        #     subject=subject,
        #     recipients=self.email,
        #     body=html,
        #     subtype="html"
        # )
        message = EmailMessage()
        message["Subject"] = "Email Verification"
        message["From"] = settings.EMAIL_FROM
        message["To"] = self.email
        message.set_content(f"{html}", subtype='html')
        # Send the email_templates
        # fm = FastMail(conf)
        # await fm.send_message(message)

        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.login(settings.EMAIL_FROM, settings.EMAIL_PASSWORD)
            server.send_message(message)


router = APIRouter(
    prefix="/verification",
    tags=["Verification Email"]
)


@router.post("")
async def send_verification_code(user: SUserID = Depends(get_current_user)):
    if user.verified_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Your email has been already verified")
    try:
        token = randbytes(10)
        hashedCode = hashlib.sha256()
        hashedCode.update(token)
        verification_code = hashedCode.hexdigest()

        await UsersDAO.find_and_update({"verification_code": verification_code}, id=user.id)
        url = rf"http://127.0.0.1:3000/verification/verifyemail/{token.hex()}"
        await Email.send_mail(Email(url=url, email=[user.email]), 'Your verification code (Valid for 10min)',
                              'verification')

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=error)


@router.get('/verifyemail/{token}')
async def verify_me(token: str):
    hashedCode = hashlib.sha256()
    hashedCode.update(bytes.fromhex(token))
    verification_code = hashedCode.hexdigest()
    result = await UsersDAO.find_one_or_none(verification_code=verification_code)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid verification code or account already verified')

    await UsersDAO.find_and_update({"verification_code": None, "verified_email": True},
                                   verification_code=verification_code)
    return {
        "status": "success",
        "message": "Account verified successfully",
    }
