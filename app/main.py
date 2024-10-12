from ipaddress import IPv4Address
import socket
from .dns_message import ARecord, Message, Question, RecordType, RecordClass
def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
    print("Listening on port 2053...")
    while True:
        try:
            recvd_bytes, source = udp_socket.recvfrom(512)
            print("Received request")
            # id = int.from_bytes(recvd_bytes[:2], "big")
            id = int.from_bytes(recvd_bytes[:2], "big")
            reply_message = Message.build_reply(
                id=id,
                questions=[
                    Question(
                        name="codecrafters.io",
                        type=RecordType.A,
                        klass=RecordClass.IN,
                    )
                ],
                resource_records=[
                    ARecord("codecrafters.io", 60, IPv4Address("192.168.1.1"))
                ],
            )
            print(reply_message.to_bytes())
            print(len(reply_message.to_bytes()))
            udp_socket.sendto(reply_message.to_bytes(), source)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break
if __name__ == "__main__":
    main()