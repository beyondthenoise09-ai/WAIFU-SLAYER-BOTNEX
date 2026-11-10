import asyncio
from getpass import getpass
from pyrogram import Client

async def main():
    api_id = int(input("API_ID: ").strip())
    api_hash = getpass("API_HASH: ").strip()
    phone = input("Assistant phone number (+91...): ").strip()

    app = Client(
        "botnex_assistant",
        api_id=api_id,
        api_hash=api_hash,
        phone_number=phone,
        in_memory=True
    )

    await app.connect()

    try:
        sent = await app.send_code(phone)
        code = input("Telegram login code: ").strip()

        try:
            await app.sign_in(phone, sent.phone_code_hash, code)
        except Exception as e:
            if "SESSION_PASSWORD_NEEDED" in str(e):
                password = getpass("Two-step verification password: ")
                await app.check_password(password)
            else:
                raise

        print("\nSession generated successfully.")
        print(await app.export_session_string())
    finally:
        await app.disconnect()

asyncio.run(main())
