import streamlit as st
import random
import string
import qrcode
import io

st.set_page_config(
    page_title="Password Generator",
    page_icon=":keyboard:",
    initial_sidebar_state="expanded"
)


def generate_password(length, use_numbers, use_lowercase, use_uppercase, use_symbols, exclude_similar,
                      exclude_sequential, exclude_repeated, start_with_letter):
    characters = ''
    if use_numbers:
        characters += string.digits
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_symbols:
        characters += string.punctuation

    if exclude_similar:
        characters = characters.translate(str.maketrans('', '', 'o0Oi1lL'))

    password = ''
    for _ in range(length):
        char = random.choice(characters)
        password += char

    if exclude_sequential:
        while any([password[i:i + 3] in string.ascii_letters or password[i:i + 3] in string.digits for i in
                   range(length - 2)]):
            password = generate_password(length, use_numbers, use_lowercase, use_uppercase, use_symbols,
                                         exclude_similar, exclude_sequential, exclude_repeated, start_with_letter)

    if exclude_repeated:
        while any([password[i] == password[i + 1] for i in range(length - 1)]):
            password = generate_password(length, use_numbers, use_lowercase, use_uppercase, use_symbols,
                                         exclude_similar, exclude_sequential, exclude_repeated, start_with_letter)

    if start_with_letter and password[0] in string.digits + "!@*$?&%_.-:,\"')(;=/>{}[]+|<#^`~":
        password = generate_password(length, use_numbers, use_lowercase, use_uppercase, use_symbols, exclude_similar,
                                     exclude_sequential, exclude_repeated, start_with_letter)

    return password


def main():
    st.markdown("<h1 style='text-align: center;'>Password Generator</h1>", unsafe_allow_html=True)

    numPasswords = st.number_input("Number of Password to Generate:", min_value=1, value=1)

    col1, col2 = st.columns([4, 5])

    with col1:
        allowNumber = st.checkbox("Allow Number", help="e.g. 123456789")
        allowLowerCase = st.checkbox("Allow Lowercase Letters", help="e.g. abcdefghijklmnopqrstuvwxyz")
        allowUpperCase = st.checkbox("Allow Uppercase Letters", help="e.g. ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        allowSymbol = st.checkbox("Allow Symbols", help="e.g !@#$%^()[]{}")

    with col2:
        excludeSimilarChar = st.checkbox("Exclude Similar Characters", help="e.g. !@#$%^")
        excludeSequentialChar = st.checkbox("Exclude Sequences", help="e.g. 123, abc")
        excludeDuplicateChar = st.checkbox("Exclude Duplicate Characters", help="e.g. No same character more than once")
        startWithLetter = st.checkbox("Start with a Letter", help="Not start with number/symbol")

    passwordLength = st.number_input("Password Length", min_value=8, max_value=50, value=8)
    generateButton = st.button("Generate Passwords", help="Click to generate passwords")

    if generateButton:
        passwords = [
            generate_password(passwordLength, allowNumber, allowLowerCase, allowUpperCase, allowSymbol,
                              excludeSimilarChar, excludeSequentialChar, excludeDuplicateChar, startWithLetter)
            for _ in range(numPasswords)
        ]

        for i, password in enumerate(passwords):
            st.write(f"Password {i + 1}")
            st.code(password)
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(password)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Convert the PIL Image to bytes using BytesIO
            img_byte_array = io.BytesIO()
            qr_img.save(img_byte_array, format="PNG")
            st.image(img_byte_array, caption=f"QR Code for Password {i + 1}", use_column_width=True)

            # Add a download button for QR code
            img_download = img_byte_array.getvalue()
            st.download_button(label=f"Download QR Code for Password {i + 1}", data=img_download,
                               file_name=f"qrcode_password_{i + 1}.png")


if __name__ == "__main__":
    main()