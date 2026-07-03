import streamlit as st
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
def generate_key(password):
    password = password.encode()

    salt = b"secure_file_encryptor"

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def encrypt_file(file_data, password):
    key = generate_key(password)
    cipher = Fernet(key)
    return cipher.encrypt(file_data)


def decrypt_file(file_data, password):
    key = generate_key(password)
    cipher = Fernet(key)
    return cipher.decrypt(file_data)

st.set_page_config(
    page_title="Secure File Encryptor",
    page_icon="🔐",
    layout="centered"
)
st.markdown("""
<style>

.stButton > button{
    width:100%;
    height:50px;
    border-radius:12px;
    font-size:18px;
    font-weight:bold;
}

.stDownloadButton > button{
    width:100%;
    height:50px;
    border-radius:12px;
    font-size:18px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🔐 Secure File Encryptor")

    st.markdown("---")

    st.info("""


. Secure

. Fast

. Easy to Use
""")

   

    st.caption("Made with  using Python & Streamlit")

st.title("🔐 Secure File Encryptor")

st.markdown(
"""
Encrypt any file securely using **AES-based Fernet Encryption**.

Upload → Encrypt → Download

or

Upload → Decrypt → Download
"""
)



with st.container(border=True):

    mode = st.radio(
        "Choose Operation",
        ["Encrypt", "Decrypt"],
        horizontal=True
    )

    uploaded_file = st.file_uploader(
        "📂 Upload File"
    )
    if uploaded_file is not None:
        st.info(
            f"📄 **File:** {uploaded_file.name}\n\n"
            f"📦 **Size:** {uploaded_file.size:,} bytes"
        )


    password = st.text_input(
        "🔑 Password",
        type="password"
    )

col1, col2 = st.columns(2)



if st.button(mode):

    if uploaded_file is None:
        st.error("Please upload a file.")

    elif password == "":
        st.error("Please enter a password.")

    else:

        file_data = uploaded_file.read()

        with st.spinner("Processing..."):
            try:

                if mode == "Encrypt":

                    result = encrypt_file(file_data, password)

                    st.success("File Encrypted Successfully!")
                    st.balloons()

                    st.download_button(
                        "⬇ Download Encrypted File",
                        result,
                        file_name=uploaded_file.name + ".enc",
                        mime="application/octet-stream"
                    )

                else:

                    result = decrypt_file(file_data, password)

                    filename = uploaded_file.name.replace(".enc", "")

                    st.success("File Decrypted Successfully!")

                    st.download_button(
                        "⬇ Download Decrypted File",
                        result,
                        file_name=filename,
                        mime="application/octet-stream"
                    )

            except Exception:
                st.error("Wrong password or invalid encrypted file.")
                st.markdown("---")

st.caption("© 2026 Secure File Encryptor | Built with Streamlit")