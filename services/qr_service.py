import qrcode
import io
import base64

def generate_qr(url):
    qr = qrcode.make(url)
    
     # 👇 MOSTRAR NA TELA
    qr.show()
    print("QR code gerado com sucesso!")
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode()

if __name__ == "__main__":
    url = "https://qr-code-avaluation.onrender.com/"
    qr_base64 = generate_qr(url)
    print("QR gerado com sucesso!")