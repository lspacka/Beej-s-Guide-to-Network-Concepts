| Feature         | **TCP (Stream)**                                       | **UDP (Datagram)**                                                  |
| --------------- | ------------------------------------------------------ | ------------------------------------------------------------------- |
| **Socket type** | `socket.SOCK_STREAM`                                   | `socket.SOCK_DGRAM`                                                 |
| **Connection**  | Requires `connect()` / `listen()` / `accept()`         | No real connection (optional `connect()` just sets a default peer)  |
| **Reliability** | Reliable: guarantees delivery, order, no duplicates    | Unreliable: packets may be lost, duplicated, or arrive out of order |
| **Data**        | Continuous byte stream (no message boundaries)         | Message-based, each `sendto()` → one `recvfrom()`                   |
| **Overhead**    | Higher (handshake, retransmission, congestion control) | Lower (lightweight, no handshake)                                   |
| **Use cases**   | Web (HTTP/HTTPS), SSH, FTP, Email (SMTP, IMAP)         | DNS, VoIP, online games, streaming                                  |
