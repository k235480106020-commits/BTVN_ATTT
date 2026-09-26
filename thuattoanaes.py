from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


def aes_encrypt(plaintext: str, key: bytes) -> dict:
    """
    Mã hóa văn bản với AES-256 ở chế độ CBC.
    key: 32 byte (256 bit)
    """
    iv = get_random_bytes(16)                      # Vector khởi tạo (IV) ngẫu nhiên 16 byte
    cipher = AES.new(key, AES.MODE_CBC, iv)         # Khởi tạo bộ mã hóa AES chế độ CBC
    data = plaintext.encode("utf-8")
    padded_data = pad(data, AES.block_size)         # Đệm dữ liệu cho đủ bội số của 16 byte
    ciphertext = cipher.encrypt(padded_data)        # Thực hiện mã hóa

    return {
        "iv": base64.b64encode(iv).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
    }


def aes_decrypt(iv_b64: str, ciphertext_b64: str, key: bytes) -> str:
    """
    Giải mã bản mã AES-256-CBC, trả về văn bản gốc.
    """
    iv = base64.b64decode(iv_b64)
    ciphertext = base64.b64decode(ciphertext_b64)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = cipher.decrypt(ciphertext)        # Giải mã
    data = unpad(padded_data, AES.block_size)       # Loại bỏ phần đệm

    return data.decode("utf-8")


if __name__ == "__main__":
    # Sinh khóa bí mật 256 bit (32 byte) dùng chung cho mã hóa và giải mã
    secret_key = get_random_bytes(32)

    message = "An toan va bao mat thong tin - AES demo"
    print("Ban ro (plaintext):", message)

    # Mã hóa
    result = aes_encrypt(message, secret_key)
    print("IV (base64):        ", result["iv"])
    print("Ban ma (base64):    ", result["ciphertext"])

    # Giải mã
    decrypted_message = aes_decrypt(result["iv"], result["ciphertext"], secret_key)
    print("Ban giai ma:        ", decrypted_message)

    assert message == decrypted_message
    print("\n=> Ma hoa va giai ma thanh cong, du lieu khop 100%.")