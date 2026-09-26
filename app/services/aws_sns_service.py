import boto3
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger("sira.aws_sns")

class AwsSnsService:
    """
    Service d'envoi de SMS Transactionnels et Notifications Push via AWS SNS / Pinpoint SMS-Voice.
    Sender ID enregistre : SIRA (Cote d'Ivoire - CI)
    Topic ARN : arn:aws:sns:us-east-1:868962733015:SIRA:802d6db5-74b7-425e-8d37-98170f78bbb1
    """

    @classmethod
    def get_sns_client(cls):
        params = {
            "region_name": settings.AWS_REGION or "us-east-1"
        }
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            params["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
            params["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
            if settings.AWS_SESSION_TOKEN:
                params["aws_session_token"] = settings.AWS_SESSION_TOKEN
        return boto3.client("sns", **params)

    @classmethod
    def get_sms_voice_client(cls):
        params = {
            "region_name": settings.AWS_REGION or "us-east-1"
        }
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            params["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
            params["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
            if settings.AWS_SESSION_TOKEN:
                params["aws_session_token"] = settings.AWS_SESSION_TOKEN
        return boto3.client("pinpoint-sms-voice-v2", **params)

    @classmethod
    def send_sms_otp(cls, phone_number: str, code: str) -> bool:
        clean_phone = phone_number.replace(" ", "").strip()
        message = f"Votre code de verification SIRA est : {code}. Valable 10 minutes."

        # 1. Tentative via AWS Pinpoint SMS Voice v2 (avec Sender ID SIRA)
        try:
            print(f"[AWS SMS-Voice] Envoi du SMS avec Sender ID 'SIRA' vers {clean_phone}...")
            sms_voice = cls.get_sms_voice_client()
            response = sms_voice.send_text_message(
                DestinationPhoneNumber=clean_phone,
                OriginationIdentity=settings.AWS_SMS_SENDER_ID or "SIRA",
                MessageBody=message,
                MessageType="TRANSACTIONAL"
            )
            message_id = response.get("MessageId")
            print(f"[AWS SMS-Voice SUCCESS] SMS delivre MessageId={message_id}")
            return True
        except Exception as e:
            print(f"[AWS SMS-Voice Info] {e}. Tentative via AWS SNS Direct Publish...")

        # 2. Tentative via AWS SNS Direct SMS (Transactional)
        try:
            sns = cls.get_sns_client()
            response = sns.publish(
                PhoneNumber=clean_phone,
                Message=message,
                MessageAttributes={
                    "AWS.SNS.SMS.SenderID": {
                        "DataType": "String",
                        "StringValue": settings.AWS_SMS_SENDER_ID or "SIRA"
                    },
                    "AWS.SNS.SMS.SMSType": {
                        "DataType": "String",
                        "StringValue": "Transactional"
                    }
                }
            )
            message_id = response.get("MessageId")
            print(f"[AWS SNS SUCCESS] SMS envoye au {clean_phone} via AWS SNS (MessageId: {message_id})")
            return True
        except Exception as e:
            print(f"[AWS SNS Error] {e}")
            return False

    @classmethod
    def publish_push_notification(cls, message: str, subject: str = "Alerte SIRA") -> bool:
        """Publie une notification push / alerte sur le Topic SNS SIRA"""
        if not settings.AWS_SNS_TOPIC_ARN:
            return False
        try:
            sns = cls.get_sns_client()
            response = sns.publish(
                TopicArn=settings.AWS_SNS_TOPIC_ARN,
                Message=message,
                Subject=subject
            )
            print(f"[AWS SNS Push SUCCESS] Notification publiee sur le Topic SIRA (MessageId: {response.get('MessageId')})")
            return True
        except Exception as e:
            print(f"[AWS SNS Push Error] {e}")
            return False
