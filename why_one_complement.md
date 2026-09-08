## 🟢 What is One’s Complement?

One’s complement is just a way of representing negative numbers in binary.
To get the one’s complement of a binary number, you **flip every bit** (0 → 1, 1 → 0).

Example with 4 bits:

```
  0101   (decimal 5)
~ 1010   (this is the one’s complement of 5)
```

In a **one’s complement system**:

* Positive numbers are normal binary.
* Negative numbers are “all bits flipped” versions of the positive number.

So:

* +5 = `0101`
* -5 = `1010`

(Notice: in modern computers we use **two’s complement** instead, because it’s easier for hardware, but Internet checksums kept the older one’s complement idea.)

---

## 🟢 Why does the Internet checksum use one’s complement?

There are two main reasons:

1. **End-around carry matches one’s complement addition.**
   In one’s complement arithmetic, when you add two numbers and it overflows, you take the extra carry bit and add it back in.
   That’s exactly what this line does:

   ```c
   total = (total & 0xffff) + (total >> 16);
   ```

2. **Detects common errors better than plain modulo.**
   The checksum is designed to catch simple errors (like 1 bit flipping, or a burst of flipped bits).
   With one’s complement:

   * Every bit matters equally (if any bit changes, the sum changes).
   * Even if bits get swapped around (like network byte order issues), it often still catches the error.

---

## 🟢 Why not just use modulo (throw away the overflow)?

If we just used modulo 2¹⁶ (ignore overflow), some errors would **cancel out** and go undetected more often.

Example:

```
Word A: 1111111111111111 (0xFFFF)
Word B: 0000000000000001 (0x0001)
```

* With plain modulo, sum = 0 (bad — looks like nothing happened).
* With one’s complement addition, the carry “wraps around” and becomes part of the result, so the error shows up.

That’s why protocols like IP, TCP, UDP all use one’s complement checksums — they give better error detection with very cheap math (just adds and bit flips).

---

✅ So, in summary:

* **One’s complement** = flip all bits.
* **Internet checksum** = add words with “end-around carry” (one’s complement addition), then flip the final result.
* They chose it because it was **simple for 1970s hardware** and **detects transmission errors better** than plain modulo.

---

