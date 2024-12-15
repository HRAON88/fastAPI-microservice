# from pyrogram import Client
# import asyncio
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
# API_ID = int(os.getenv('API_ID'))
# API_HASH = os.getenv('API_HASH')
#
# async def stringGenerate():
#     api_id = API_ID
#     api_hash = API_HASH
#     client = Client("my_session_for_parser", api_id, api_hash)
#     await client.connect()
#
#     phone_number = input("Insert your phone number: \nIncluding Country code. Example: +5357653423 \n")
#     print("Sending code to telegram... \n")
#     code = await client.send_code(phone_number)
#
#     phone_code_msg = input("Insert registration code: \n")
#
#     try:
#         print('Login in Telegram...')
#         await client.sign_in(phone_number, code.phone_code_hash, phone_code_msg)
#     except:
#         password = input('Insert your double factor:\n')
#         await client.check_password(password=password)
#     print("Session String: ")
#     string_session = await client.export_session_string()
#
#     print(f"Session String:\n{string_session}")
#
#
# if __name__ == "__main__":
#     asyncio.run(stringGenerate())