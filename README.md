# BTVN_ATTT
Bài tập về nhà an toàn thông tin
# MÔN: AN TOÀN VÀ BẢO MẬT THÔNG TIN


## 1. THUẬT TOÁN MÃ HÓA HIỆN ĐẠI DES, AES

### 1.1. Tổng quan về mã hóa đối xứng

Mã hóa đối xứng (Symmetric Encryption) là phương pháp mã hóa trong đó **cùng một khóa** được sử dụng cho cả quá trình mã hóa (encryption) và giải mã (decryption).

Đặc điểm chính:

- Tốc độ xử lý nhanh, phù hợp mã hóa dữ liệu lớn.

- Yêu cầu bài toán trao đổi khóa bí mật an toàn giữa hai bên trước khi truyền dữ liệu.

- Hai đại diện tiêu biểu: **DES** (Data Encryption Standard) và **AES** (Advanced Encryption Standard).

---

### 1.2. Thuật toán DES (Data Encryption Standard)

#### 1.2.1. Giới thiệu

DES được NIST (Mỹ) công bố làm chuẩn mã hóa vào năm 1977, dựa trên thuật toán Lucifer của IBM.

- Kích thước khối dữ liệu (block size): **64 bit**.

- Kích thước khóa: **64 bit**, nhưng chỉ có **56 bit** thực sự được sử dụng (8 bit còn lại dùng làm bit kiểm tra chẵn lẻ - parity bit).

- Số vòng lặp (round): **16 vòng**.

- Cấu trúc nền tảng: **Mạng Feistel (Feistel Network)**.

Do độ dài khóa 56 bit quá ngắn so với khả năng tính toán hiện đại, DES hiện nay được xem là **không an toàn**, dễ bị tấn công brute-force, và đã được thay thế bởi AES.

#### 1.2.2. Cấu trúc mạng Feistel của DES

Ý tưởng cốt lõi: chia khối dữ liệu 64 bit thành 2 nửa trái/phải (L, R) mỗi nửa 32 bit, sau đó thực hiện 16 vòng biến đổi giống nhau, mỗi vòng dùng một khóa con (subkey) khác nhau.

Công thức một vòng Feistel thứ *i*:

```
L(i) = R(i-1)
R(i) = L(i-1) XOR f(R(i-1), K(i))
```

Trong đó `f` là hàm mã hóa vòng (round function) kết hợp phép hoán vị mở rộng (Expansion), XOR với khóa con, thay thế qua các hộp S-box, và hoán vị P-box.

#### 1.2.3. Quy trình mã hóa DES

1. **Hoán vị khởi tạo (Initial Permutation - IP):** sắp xếp lại 64 bit đầu vào theo bảng hoán vị cố định.

2. **Sinh khóa con:** từ khóa 64 bit, loại bỏ 8 bit parity còn 56 bit, qua phép hoán vị PC-1, chia thành 2 nửa 28 bit, dịch vòng (left shift) và hoán vị PC-2 để sinh ra 16 khóa con K1...K16 (mỗi khóa con 48 bit).

3. **16 vòng Feistel:** với mỗi vòng, nửa phải R được:
   - Mở rộng từ 32 bit lên 48 bit (Expansion permutation E).
   - XOR với khóa con Ki (48 bit).
   - Đưa qua 8 hộp S-box để nén trở về 32 bit (đây là bước duy nhất phi tuyến, tạo tính bảo mật).
   - Hoán vị P-box.
   - Kết quả XOR với nửa trái L để tạo R mới; L mới = R cũ.

4. **Hoán vị cuối (Final Permutation - IP⁻¹):** sau 16 vòng, ghép (R16, L16) và áp dụng hoán vị nghịch đảo của IP để ra bản mã 64 bit.

#### 1.2.4. Quy trình giải mã DES

Giải mã DES sử dụng **chính cấu trúc thuật toán mã hóa**, chỉ khác là các khóa con được sử dụng theo **thứ tự ngược lại**: K16, K15, ..., K1. Đây là ưu điểm đặc trưng của mạng Feistel — không cần thuật toán đảo ngược riêng.

#### 1.2.5. Hạn chế của DES

- Không gian khóa 56 bit (2^56 khả năng) có thể bị dò brute-force trong thời gian hợp lý với phần cứng hiện đại (đã được chứng minh từ năm 1998 với máy "Deep Crack").

- Từ đó, biến thể **3DES (Triple DES)** ra đời (mã hóa 3 lần với 2 hoặc 3 khóa) để tăng độ an toàn tạm thời, nhưng tốc độ chậm hơn nhiều so với AES.

---

### 1.3. Thuật toán AES (Advanced Encryption Standard)

#### 1.3.1. Giới thiệu

AES được NIST chọn làm chuẩn mã hóa mới vào năm 2001, dựa trên thuật toán **Rijndael** do hai nhà mật mã học người Bỉ (Joan Daemen và Vincent Rijmen) thiết kế, nhằm thay thế DES.

- Kích thước khối dữ liệu: **128 bit** (cố định).

- Kích thước khóa: **128, 192, hoặc 256 bit** (tương ứng AES-128, AES-192, AES-256).

- Số vòng lặp: 10 vòng (AES-128), 12 vòng (AES-192), 14 vòng (AES-256).

- Cấu trúc nền tảng: **Mạng thay thế - hoán vị (Substitution - Permutation Network - SPN)**, khác với Feistel của DES.

#### 1.3.2. Biểu diễn dữ liệu - State Matrix

Khối dữ liệu 128 bit (16 byte) được sắp xếp thành ma trận **4x4 byte** gọi là **State**, xử lý theo cột.

#### 1.3.3. Các phép biến đổi cơ bản trong mỗi vòng AES

1. **SubBytes:** thay thế từng byte trong State bằng giá trị tương ứng tra trong bảng **S-box** (dựa trên phép nghịch đảo trong trường hữu hạn GF(2^8) kết hợp biến đổi affine). Đây là bước tạo tính phi tuyến, chống lại phân tích tuyến tính/vi phân.

2. **ShiftRows:** dịch vòng (trái) các hàng của State: hàng 0 giữ nguyên, hàng 1 dịch 1 byte, hàng 2 dịch 2 byte, hàng 3 dịch 3 byte. Bước này tạo hiệu ứng khuếch tán (diffusion) giữa các cột.

3. **MixColumns:** nhân mỗi cột của State (xem như đa thức trên GF(2^8)) với một ma trận cố định, làm trộn dữ liệu giữa các byte trong cùng một cột. Bước này bị **bỏ qua ở vòng cuối cùng**.

4. **AddRoundKey:** thực hiện phép XOR giữa State hiện tại với khóa con (round key) tương ứng của vòng đó, được sinh ra từ quá trình mở rộng khóa (Key Expansion/Key Schedule).

#### 1.3.4. Quy trình mã hóa AES

```
Bước 1: AddRoundKey (dùng khóa gốc K0)

Bước 2: Lặp (Nr - 1) vòng chính, mỗi vòng gồm:
        SubBytes -> ShiftRows -> MixColumns -> AddRoundKey

Bước 3: Vòng cuối cùng (không có MixColumns):
        SubBytes -> ShiftRows -> AddRoundKey
```

Trong đó Nr = 10/12/14 tùy độ dài khóa 128/192/256 bit.

#### 1.3.5. Quy trình giải mã AES

Giải mã thực hiện các phép biến đổi **nghịch đảo** theo thứ tự ngược lại, sử dụng các khóa con theo thứ tự ngược:

```
AddRoundKey (khóa cuối cùng)

Lặp (Nr - 1) vòng: InvShiftRows -> InvSubBytes -> AddRoundKey -> InvMixColumns

Vòng cuối: InvShiftRows -> InvSubBytes -> AddRoundKey
```

#### 1.3.6. Sinh khóa mở rộng (Key Expansion)

Từ khóa gốc (128/192/256 bit), thuật toán sinh ra Nr+1 khóa con 128 bit bằng cách sử dụng các hàm **RotWord** (xoay byte), **SubWord** (thay thế qua S-box) và hằng số vòng **Rcon**, kết hợp XOR liên tiếp giữa các từ (word) 32 bit.

#### 1.3.7. Vì sao AES an toàn và nhanh hơn DES

| Tiêu chí | DES | AES |
|---|---|---|
| Kích thước khối | 64 bit | 128 bit |
| Độ dài khóa | 56 bit | 128/192/256 bit |
| Cấu trúc | Feistel | SPN (thay thế - hoán vị) |
| Số vòng | 16 | 10/12/14 |
| Tốc độ | Chậm hơn | Nhanh hơn (tối ưu tốt trên phần cứng, có tập lệnh AES-NI) |
| Độ an toàn hiện nay | Không an toàn | An toàn (chưa có tấn công thực tế khả thi) |

---

### 1.4. Cài đặt thuật toán AES bằng ngôn ngữ Python

Bên dưới là chương trình minh họa mã hóa/giải mã AES-256 ở chế độ **CBC (Cipher Block Chaining)**, sử dụng thư viện `pycryptodome` (thư viện triển khai chuẩn AES theo đúng đặc tả NIST FIPS-197).

#### 1.4.1. Cài đặt thư viện

```bash
pip install pycryptodome
```

#### 1.4.2. Mã nguồn: `aes_demo.py`

```python
"""
Chương trình minh họa mã hóa / giải mã AES-256-CBC
Môn: An toàn và bảo mật thông tin
"""

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
```

#### 1.4.3. Giải thích chương trình

- `get_random_bytes(32)`: sinh khóa bí mật ngẫu nhiên 256 bit dùng chung cho cả hai chiều mã hóa/giải mã (đúng bản chất **đối xứng**).

- `AES.MODE_CBC`: chế độ CBC yêu cầu một **IV (Initialization Vector)** ngẫu nhiên để đảm bảo cùng một bản rõ mã hóa nhiều lần sẽ cho ra bản mã khác nhau.

- `pad()` / `unpad()`: AES là mã khối (block cipher) làm việc trên khối 16 byte cố định, nên dữ liệu đầu vào cần được đệm (padding theo chuẩn PKCS#7) cho đủ bội số của 16.

- Kết quả IV và ciphertext được mã hóa Base64 để tiện lưu trữ/truyền dưới dạng văn bản.

- Chương trình minh họa đầy đủ: sinh khóa → mã hóa → giải mã → kiểm tra kết quả khớp với bản rõ ban đầu.

---

## 2. THUẬT TOÁN MÃ HÓA BẤT ĐỐI XỨNG RSA

### 2.1. Giới thiệu

RSA (đặt theo tên 3 tác giả **Rivest, Shamir, Adleman**, công bố năm 1977) là thuật toán mã hóa **bất đối xứng (asymmetric)** đầu tiên được ứng dụng rộng rãi, sử dụng **hai khóa khác nhau**:

- **Khóa công khai (Public Key):** dùng để mã hóa, được công bố công khai.

- **Khóa bí mật (Private Key):** dùng để giải mã, chỉ chủ sở hữu nắm giữ.

Độ an toàn của RSA dựa trên độ khó của bài toán **phân tích một số nguyên rất lớn thành tích của hai số nguyên tố** (bài toán phân tích thừa số nguyên tố).

### 2.2. Nguyên lý sinh cặp khóa bí mật - công khai

Quá trình sinh khóa RSA gồm các bước sau:

**Bước 1:** Chọn ngẫu nhiên hai số nguyên tố lớn, phân biệt: `p` và `q` (trong thực tế mỗi số có độ dài hàng trăm/nghìn bit).

**Bước 2:** Tính tích:

```
n = p * q
```

`n` được gọi là **modulus**, có mặt trong cả khóa công khai lẫn khóa bí mật, và độ dài của `n` (tính theo bit) chính là độ dài khóa RSA (vd: RSA-2048).

**Bước 3:** Tính giá trị hàm Euler (phi):

```
phi(n) = (p - 1) * (q - 1)
```

**Bước 4:** Chọn số mũ công khai `e` sao cho:

```
1 < e < phi(n)   và   gcd(e, phi(n)) = 1  (e nguyên tố cùng nhau với phi(n))
```

Trong thực tế, `e` thường được chọn là **65537** (2^16 + 1) vì vừa đảm bảo an toàn vừa tính toán nhanh.

**Bước 5:** Tính số mũ bí mật `d` là nghịch đảo modulo của `e`:

```
d = e^(-1) mod phi(n)
```

nghĩa là `d` thỏa mãn: `(e * d) mod phi(n) = 1`. Việc tính `d` dựa trên **thuật toán Euclid mở rộng (Extended Euclidean Algorithm)**.

**Kết quả:**

- **Khóa công khai (Public Key):** cặp số `(e, n)` — công bố cho mọi người.

- **Khóa bí mật (Private Key):** cặp số `(d, n)` — giữ bí mật tuyệt đối.

- Sau khi sinh khóa xong, `p`, `q`, và `phi(n)` phải được **hủy bỏ hoàn toàn**, vì nếu lộ ra, kẻ tấn công có thể tính lại `d` từ `e` và `n`.

### 2.3. Quy trình mã hóa / giải mã RSA

**Mã hóa** (dùng khóa công khai bên nhận `(e, n)`):

```
C = M^e mod n
```

Trong đó `M` là bản rõ (đã chuyển thành số nguyên `0 <= M < n`), `C` là bản mã.

**Giải mã** (dùng khóa bí mật `(d, n)`):

```
M = C^d mod n
```

Tính đúng đắn của thuật toán được đảm bảo bởi **Định lý Euler** trong lý thuyết số, do cách chọn `e` và `d` là nghịch đảo của nhau theo modulo `phi(n)`.

### 2.4. Ví dụ minh họa với số nhỏ

```
Chọn: p = 61, q = 53
=> n = p * q = 3233
=> phi(n) = (61-1)*(53-1) = 3120

Chọn e = 17 (thỏa gcd(17, 3120) = 1)
Tính d = 2753 (vì 17 * 2753 mod 3120 = 1)

Khóa công khai: (e=17, n=3233)
Khóa bí mật:   (d=2753, n=3233)

Mã hóa M = 65:
C = 65^17 mod 3233 = 2790

Giải mã C = 2790:
M = 2790^2753 mod 3233 = 65  (khôi phục đúng bản rõ)
```

*(Ví dụ dùng số nhỏ chỉ nhằm minh họa nguyên lý toán học; RSA thực tế dùng số nguyên tố có độ dài 1024-4096 bit để đảm bảo an toàn.)*

---

## 3. CÁC MÔ HÌNH ÁP DỤNG THUẬT TOÁN RSA

Vì RSA có 2 khóa tách biệt (công khai/bí mật), tùy theo **ai giữ khóa nào** và **ai dùng khóa nào để mã hóa**, ta có 3 mô hình ứng dụng chính.

### 3.1. Mô hình xác thực người gửi (chữ ký số - Digital Signature)

**Mục tiêu:** Người nhận xác minh được thông điệp đúng là do người gửi tạo ra (chống giả mạo danh tính, chống chối bỏ - non-repudiation), nhưng **không đảm bảo bí mật nội dung**.

Quy trình:

1. Người gửi (A) dùng **khóa bí mật của chính mình** để mã hóa (ký) thông điệp (thường ký trên giá trị băm - hash - của thông điệp để tăng hiệu năng):

```
Chữ ký S = Hash(M)^d_A mod n_A
```

2. Người gửi gửi `(M, S)` cho người nhận.

3. Người nhận (B) dùng **khóa công khai của A** để giải mã chữ ký và so sánh với hash của thông điệp nhận được:

```
Hash'(M) = S^e_A mod n_A
```

Nếu `Hash'(M) = Hash(M)` thì xác nhận thông điệp đúng là do A gửi và chưa bị chỉnh sửa.

**Ứng dụng thực tế:** chữ ký số trong hợp đồng điện tử, xác thực phần mềm, email đã ký (S/MIME).

### 3.2. Mô hình xác thực người nhận (mã hóa bảo mật nội dung)

**Mục tiêu:** Đảm bảo chỉ đúng người nhận hợp lệ mới đọc được nội dung (bảo mật/confidentiality), nhưng **không xác thực được ai là người gửi thật sự**.

Quy trình:

1. Người gửi (A) dùng **khóa công khai của người nhận B** để mã hóa thông điệp:

```
C = M^e_B mod n_B
```

2. Gửi `C` cho B.

3. Chỉ B mới có **khóa bí mật tương ứng** `(d_B, n_B)` để giải mã:

```
M = C^d_B mod n_B
```

**Ứng dụng thực tế:** gửi dữ liệu nhạy cảm (mật khẩu, khóa phiên) đến đúng một máy chủ/người nhận cụ thể.

### 3.3. Mô hình xác thực cả người gửi và người nhận (kết hợp)

**Mục tiêu:** Đảm bảo đồng thời cả **tính bí mật** (chỉ người nhận đọc được) lẫn **tính xác thực** (người nhận biết chắc ai đã gửi) — kết hợp cả hai mô hình trên.

Quy trình (A gửi cho B):

1. **Ký** thông điệp bằng khóa bí mật của A: `S = Hash(M)^d_A mod n_A`

2. **Mã hóa** cả thông điệp và chữ ký bằng khóa công khai của B: `C = (M, S)^e_B mod n_B`

3. Gửi `C` cho B.

4. B dùng khóa bí mật của mình `d_B` để giải mã, lấy lại `(M, S)`.

5. B dùng khóa công khai của A `(e_A, n_A)` để kiểm tra chữ ký `S`, xác nhận người gửi và tính toàn vẹn dữ liệu.

Mô hình này đạt được đồng thời: **bảo mật (confidentiality) + xác thực (authentication) + toàn vẹn (integrity) + chống chối bỏ (non-repudiation)** — là mô hình an toàn nhất trong 3 mô hình, thường dùng làm nền tảng cho các giao thức bảo mật thực tế như TLS/SSL, PGP.

### 3.4. So sánh thời gian mã hóa / giải mã giữa RSA và AES

| Tiêu chí | AES (đối xứng) | RSA (bất đối xứng) |
|---|---|---|
| Tốc độ mã hóa/giải mã | Rất nhanh (xử lý theo khối byte, phép toán đơn giản: XOR, hoán vị, tra bảng) | Chậm hơn nhiều (phép lũy thừa modulo số lớn, có độ phức tạp cao) |
| Độ phức tạp tính toán | Thấp | Cao (do làm việc với số nguyên hàng trăm/nghìn bit) |
| Kích thước khóa an toàn tương đương | 128 bit AES ~ tương đương RSA 3072 bit | RSA cần khóa dài hơn nhiều lần để đạt cùng mức an toàn |
| Khả năng mã hóa dữ liệu lớn | Phù hợp (file, luồng dữ liệu lớn) | Không phù hợp (thường chỉ mã hóa dữ liệu rất nhỏ, nhỏ hơn kích thước modulus n) |
| Vấn đề trao đổi khóa | Khó khăn: cần kênh an toàn để chia sẻ khóa bí mật dùng chung | Thuận lợi: khóa công khai chia sẻ tự do, không cần kênh bí mật |
| Ứng dụng phù hợp | Mã hóa nội dung/dữ liệu số lượng lớn | Trao đổi khóa, chữ ký số, xác thực |

**Nhận xét:** Trong cùng điều kiện thử nghiệm (ví dụ: mã hóa lần lượt các khối dữ liệu bằng AES-256 và RSA-2048), thời gian mã hóa và giải mã của RSA thường chậm hơn AES từ **hàng chục đến hàng trăm lần**, do bản chất phép toán lũy thừa modulo trên số nguyên lớn tốn nhiều chi phí CPU hơn nhiều so với các phép XOR/hoán vị/tra bảng đơn giản của AES. Đây chính là lý do RSA hiếm khi được dùng để mã hóa trực tiếp toàn bộ dữ liệu, mà chủ yếu dùng để mã hóa/trao đổi một khóa đối xứng ngắn (session key).

### 3.5. Kết hợp sức mạnh của RSA và AES (Mã hóa lai - Hybrid Encryption)

Vì mỗi thuật toán có ưu/nhược điểm bổ sung cho nhau:

- **AES:** nhanh, phù hợp mã hóa dữ liệu lớn, nhưng khó trao đổi khóa bí mật an toàn.

- **RSA:** trao đổi khóa công khai dễ dàng, an toàn, nhưng chậm và không phù hợp mã hóa dữ liệu lớn.

=> Giải pháp thực tế phổ biến nhất là **mô hình mã hóa lai (Hybrid Cryptosystem)**, kết hợp cả hai:

**Quy trình mô hình lai:**

1. Bên gửi (A) sinh ngẫu nhiên một **khóa phiên (session key)** đối xứng, ví dụ khóa AES-256.

2. A dùng khóa AES đó để mã hóa **toàn bộ dữ liệu/thông điệp thực sự** (nhanh, hiệu quả với dữ liệu lớn).

3. A dùng **khóa công khai RSA của người nhận (B)** để mã hóa **khóa AES vừa sinh** (vì khóa AES rất ngắn, chỉ 16/32 byte, nên RSA xử lý nhanh dù bản chất chậm).

4. A gửi cho B gói tin gồm: `{Dữ liệu đã mã hóa bằng AES, Khóa AES đã mã hóa bằng RSA}`.

5. B nhận được, dùng **khóa bí mật RSA của mình** để giải mã ra khóa AES gốc.

6. B dùng khóa AES vừa khôi phục để giải mã toàn bộ dữ liệu còn lại.

**Sơ đồ tóm tắt:**

```
[Khóa AES ngẫu nhiên] --mã hóa bằng--> [RSA Public Key của B] --> Gói khóa đã mã hóa

[Dữ liệu gốc] --mã hóa bằng--> [Khóa AES] --> Dữ liệu đã mã hóa

Gửi đi: (Gói khóa đã mã hóa + Dữ liệu đã mã hóa)

Bên nhận B:
Gói khóa đã mã hóa --giải mã bằng--> [RSA Private Key của B] --> Khóa AES gốc
Dữ liệu đã mã hóa --giải mã bằng--> [Khóa AES gốc] --> Dữ liệu gốc
```

**Ưu điểm của mô hình lai:**

- Tận dụng **tốc độ cao của AES** để xử lý toàn bộ dữ liệu thực tế, dù dữ liệu lớn đến đâu.

- Tận dụng khả năng **trao đổi khóa an toàn, không cần kênh bí mật trước** của RSA, giải quyết triệt để bài toán phân phối khóa của mã hóa đối xứng.

- Có thể kết hợp thêm chữ ký số (RSA) để đồng thời đảm bảo xác thực người gửi như mô hình ở mục 3.3.

**Ứng dụng thực tế của mô hình lai:** Đây chính là nguyên lý nền tảng của hầu hết các giao thức bảo mật hiện đại như **TLS/SSL (HTTPS)**, **PGP/GPG** (mã hóa email), **SSH**, VPN...: giai đoạn "bắt tay" (handshake) dùng RSA (hoặc Diffie-Hellman/ECC) để trao đổi khóa phiên, sau đó toàn bộ phiên làm việc dùng AES để mã hóa dữ liệu truyền đi.
