import streamlit as st
from PIL import Image
from aes_utils import encrypt_bytes, decrypt_bytes
from encode import embed_data
from decode import extract_data
import io

st.set_page_config(page_title="Steganography App", layout="centered")
st.title("🕵️ Steganography with AES Encryption")

mode = st.radio("Choose mode:", ["Encode", "Decode"],index=None)

if mode == "Encode":
    image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    data_type = st.selectbox("Choose what to hide:", ["Text", "File"],index=None)
    password = st.text_input("Enter secret key (min 6 characters)", type="password")

    if data_type == "Text":
        message = st.text_area("Enter your secret message:")
        file_data = None
    else:
        file_data = st.file_uploader("Upload the file to hide")
        message = None

    if st.button("🔐 Encode"):
        if not image or not password or (not message and not file_data):
            st.error("Please provide all inputs.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            image = Image.open(image)
            data = message.encode() if message else file_data.read()
            encrypted = encrypt_bytes(data, password)
            stego_image = embed_data(image, encrypted)

            output = io.BytesIO()
            stego_image.save(output, format="PNG")
            st.success("Message successfully embedded!")
            st.download_button("📥 Download Stego Image", data=output.getvalue(),
                               file_name="stego_image.png", mime="image/png")

elif mode == "Decode":
    stego_image = st.file_uploader("Upload the stego image", type=["png", "jpg", "jpeg"])
    password = st.text_input("Enter the password used for encryption", type="password")

    if st.button("🕵️ Decode"):
        if not stego_image or not password:
            st.error("Please upload a stego image and enter the password.")
        else:
            try:
                image = Image.open(stego_image)
                encrypted = extract_data(image)
                decrypted = decrypt_bytes(encrypted, password)

                try:
                    text = decrypted.decode()
                    st.success("Hidden message:")
                    st.code(text)
                except UnicodeDecodeError:
                    st.success("Hidden file recovered!")
                    st.download_button("📁 Download File", decrypted, file_name="hidden_file", mime="application/octet-stream")
            except Exception as e:
                st.error(f"Failed to decode: {e}")
