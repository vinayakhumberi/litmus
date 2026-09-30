# Encryption Fundamentals: Symmetric vs Asymmetric, Hashing, and TLS/HTTPS

## 🎯 Executive Summary

Every "how does HTTPS work," "how would you store passwords," and "explain how JWT signing works" question a frontend lead gets asked traces back to the same three primitives: encryption (reversible, with a secret), hashing (one-way, no secret), and the symmetric/asymmetric split that decides which one is fast versus which one solves the "we've never met, how do we share a secret" problem. Most candidates have absorbed the vocabulary — "AES," "RSA," "TLS" — without being able to say precisely what each one is actually *for*, which is exactly where an interviewer's follow-up question is aimed.

This is a must-know topic at Lead level because it's the load-bearing foundation under three things a frontend lead is expected to reason about directly: whether a given piece of data needs to be hashed or encrypted (getting this backwards, e.g. "encrypting" a password so it can be "decrypted" later, is a real, disqualifying security bug), how token-based auth actually gets forged-proofed (this is the entire mechanism behind JWT, covered in this repo's [Authentication: JWT vs Sessions](/topic-detail.html?id=authentication-jwt-sessions) topic), and why the padlock icon in a browser means less than most engineers assume.

## 📖 What Is It? (Plain-English Definition)

**In plain terms:** encryption scrambles data so that only someone holding the right secret can unscramble it back to the original — it's a two-way operation. Hashing is different in kind, not degree: it turns data into a fixed-length fingerprint that can never be turned back into the original, on purpose — it's a one-way operation, useful for proving data hasn't changed or proving you know a password without ever storing the password itself.

The symmetric-vs-asymmetric split is about *how many keys* are involved. Symmetric encryption uses the exact same key to lock and unlock — fast, but it means both sides need to already share that secret safely, which is a real chicken-and-egg problem if they've never met. Asymmetric encryption uses a *pair* of mathematically-linked keys — one public, one private — where anything locked with one can only be unlocked with the other. That solves the chicken-and-egg problem (you can publish your public key to the entire internet) at the cost of being much slower, which is exactly why real systems — TLS included — use asymmetric crypto only briefly, to safely hand off a symmetric key, then switch to fast symmetric encryption for everything else.

---

## 🧠 Core Technical Deep Dive

### Encoding, encryption, and hashing are three different things

These get conflated constantly, and the distinction is a genuine interview trap:

| | Reversible? | Needs a secret? | Purpose |
|---|---|---|---|
| **Encoding** (Base64, URL-encoding) | Yes, by anyone | No | Represent data in a different format — zero security value |
| **Encryption** (AES, RSA) | Yes, with the key | Yes | Keep data confidential from anyone without the key |
| **Hashing** (SHA-256, bcrypt) | No, by design | No | Verify integrity, or prove knowledge of a value without storing it |

Base64-"encoding" a password and calling it secured is a real, recurring junior mistake — it's fully reversible by anyone, with no key required at all.

### Symmetric encryption: one key, fast, but a distribution problem

AES (Advanced Encryption Standard) is the standard symmetric cipher: the same key encrypts and decrypts, it's computationally cheap, and it's what actually protects the bulk of data in any encrypted connection. Its entire weakness is key distribution — if two parties have never securely met, how does one hand the other this shared secret without an eavesdropper on the wire copying it too?

### Asymmetric encryption: a key pair solves the distribution problem, at a speed cost

RSA and elliptic-curve cryptography (ECC) generate a mathematically linked *pair*: a public key (safe to publish anywhere) and a private key (never shared). Data encrypted with the public key can only be decrypted with the paired private key — so anyone can encrypt a message to you using your published public key, and only you can read it. This is 100-1000x slower than symmetric encryption for the same data size, which is why it's essentially never used to encrypt bulk data directly in practice — it's used to safely establish a symmetric key, then gets out of the way.

### Digital signatures: asymmetric crypto used in reverse

Encryption uses the public key to lock, private key to unlock. A **signature** flips that: you encrypt (sign) a hash of the data with your *private* key, and anyone can verify it using your *public* key. Since only you hold the private key, a valid signature is proof the data really came from you and hasn't been altered — this exact mechanism is what RS256-signed JWTs and HTTPS certificates both rely on.

### Hashing: fixed-length, one-way, and why passwords get hashed, never encrypted

A cryptographic hash function takes input of any size and produces a fixed-length output, deterministically (the same input always produces the same hash), with an "avalanche effect" (changing one character of input produces a completely different output). This is why passwords are **hashed, never encrypted**: encryption implies a key that can reverse it — if that key ever leaks, every password it protected is exposed at once. A hash has no key to leak; even the server operator cannot recover the original password from a stored hash, only verify a login attempt by hashing the submitted password and comparing.

**Salting** adds a unique random value to each password before hashing, so two users with the identical password get different stored hashes, and precomputed "rainbow table" lookups become useless. **Modern password hashing deliberately uses slow, memory-hard algorithms** (bcrypt, scrypt, Argon2) instead of fast general-purpose hashes like SHA-256 — a fast hash lets an attacker with a leaked hash database try billions of guesses per second; a deliberately slow one caps that at a few thousand, which is the entire point.

### TLS/HTTPS: the hybrid model, end to end

TLS is the concrete, real-world application of everything above, in sequence:

1. Client connects; server presents its **certificate**, containing its public key, signed by a trusted Certificate Authority (CA).
2. Client validates the certificate against a built-in list of trusted root CAs — this is what the padlock icon actually verifies.
3. Client and server perform a key exchange (modern TLS uses Diffie-Hellman/ECDHE, giving **forward secrecy** — even if the server's long-term private key is compromised later, past recorded sessions still can't be decrypted, since each session's symmetric key was never transmitted anywhere) to agree on a shared symmetric session key, using asymmetric crypto briefly to set it up.
4. All subsequent traffic in that session uses fast symmetric encryption (AES) with that negotiated key.

**The detail that separates a working answer from a correct one:** HTTPS's padlock certifies that the *connection* is encrypted and the certificate chain is valid — it says **nothing** about whether the site itself is trustworthy. A phishing site can, and routinely does, have a perfectly valid HTTPS certificate. Confusing "encrypted" with "safe" is a common, and testable, misconception.

---

## 📊 Visual Architecture & Logic

### Diagram 1: Choosing an Approach — and Why Real Systems Use Both

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor":"#334155","primaryTextColor":"#f1f5f9","primaryBorderColor":"#64748b","lineColor":"#94a3b8","edgeLabelBackground":"#1e293b","textColor":"#f1f5f9","fontSize":"16px"}}}%%
flowchart TD
    A["Need to protect data in transit"] --> B{"Shared secret already exists?"}
    B -- "No" --> C["Use asymmetric crypto to safely exchange one"]
    C --> D["Now a shared symmetric key exists"]
    B -- "Yes" --> D
    D --> E["Switch to fast symmetric encryption"]
    E --> F["Encrypt all bulk data with AES"]

    classDef start fill:#0369a1,stroke:#7dd3fc,color:#f0f9ff,stroke-width:1.5px
    classDef decision fill:#4338ca,stroke:#c4b5fd,color:#f5f3ff,stroke-width:1.5px
    classDef neutral fill:#334155,stroke:#94a3b8,color:#f1f5f9,stroke-width:1.5px
    classDef result fill:#047857,stroke:#6ee7b7,color:#ecfdf5,stroke-width:1.5px

    class A start
    class B decision
    class C,D neutral
    class E,F result
```

### Diagram 2: The TLS Handshake, Simplified

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor":"#334155","primaryTextColor":"#f1f5f9","primaryBorderColor":"#64748b","lineColor":"#94a3b8","edgeLabelBackground":"#1e293b","textColor":"#f1f5f9","fontSize":"16px"}}}%%
flowchart TD
    A["Client connects to server"] --> B["Server presents its certificate"]
    B --> C{"Certificate signed by trusted CA?"}
    C -- "No" --> D["Browser blocks — connection untrusted"]
    C -- "Yes" --> E["Client and server negotiate a key"]
    E --> F["Shared symmetric session key established"]
    F --> G["All traffic encrypted with AES from here on"]

    classDef start fill:#0369a1,stroke:#7dd3fc,color:#f0f9ff,stroke-width:1.5px
    classDef decision fill:#4338ca,stroke:#c4b5fd,color:#f5f3ff,stroke-width:1.5px
    classDef warn fill:#b91c1c,stroke:#fca5a5,color:#fef2f2,stroke-width:1.5px
    classDef result fill:#047857,stroke:#6ee7b7,color:#ecfdf5,stroke-width:1.5px

    class A start
    class C decision
    class D warn
    class B,E,F,G result
```

---

## 🏢 Interview Context & FAANG Signals

| Interview Stage | Format |
|---|---|
| **Security/Backend-aware round** | "How would you securely store user passwords" or "explain how HTTPS actually works" |
| **System Design** | A follow-up on any auth-adjacent design question — "how is this token verified without a database lookup" |
| **Debugging/Trivia** | "Can someone read the contents of a JWT without the secret" — tests the encryption-vs-signing distinction directly |

**Lead signals interviewers listen for:**

1. **Never conflating encryption and hashing** — stating precisely why passwords are hashed, not encrypted, unprompted.
2. **Correctly identifying the symmetric/asymmetric trade-off** as a speed-vs-key-distribution trade-off, not just naming algorithms.
3. **Explaining TLS as a hybrid system**, not "it's just encrypted" — naming the handshake's actual purpose (safely negotiating a symmetric key).
4. **Knowing HTTPS validates the connection, not the site's legitimacy** — a subtle but common gap.
5. **Connecting signatures to verification without a shared secret** — the exact mechanism JWT's RS256 depends on.

## ⚔️ Lead Level vs Senior Level

**Question:** "Our login endpoint currently stores passwords using AES so we can 'decrypt them if a user forgets.' What's your read on this?"

**Senior Response:**
> That should probably use a stronger encryption algorithm, or rotate the key more often.

Treats it as an implementation-strength problem, missing that the architecture itself is fundamentally wrong.

---

**Staff/Lead Response:**
> The problem isn't the algorithm, it's that we're using encryption at all here — encryption is reversible by design, which means anyone who obtains that AES key, including an attacker who breaches the database and the app server, can recover every user's real password at once. Passwords need to be hashed with a slow, memory-hard algorithm like bcrypt or Argon2, with a per-user salt, so there's no key anywhere that reverses it — "forgot password" should always be a reset flow, never a "decrypt and show it to you" flow.
>
> I'd treat this as a P0 security fix, not a backlog item, and I'd also want to know whether we've ever displayed a decrypted password anywhere, since that's a real breach-disclosure question, not just a code-quality one.

The Lead answer identifies the category error (encryption vs. hashing) immediately and treats it with the urgency an actual security defect warrants.

## ⚠️ Common Pitfalls & Anti-Patterns

> ### ✕ "Encrypting" Passwords Instead of Hashing Them
> **Why it's wrong:** Encryption is reversible with a key — if that key ever leaks, every password it protects is exposed simultaneously. There should be no mechanism, anywhere, to recover a user's original password.
> **✓ Correct Lead Approach:** Hash passwords with a slow, memory-hard algorithm (bcrypt/Argon2) plus a per-user salt. "Forgot password" is always a reset, never a retrieval.

---

> ### ✕ Using a Fast General-Purpose Hash (MD5, SHA-256) for Passwords
> **Why it's wrong:** Fast hashes are fast for attackers too — a leaked hash database becomes brute-forceable at billions of guesses per second on modern hardware.
> **✓ Correct Lead Approach:** Use a purpose-built, deliberately slow password hashing algorithm (bcrypt, scrypt, Argon2) — speed is the vulnerability here, not a feature.

---

> ### ✕ Assuming the Padlock Icon Means "This Site Is Safe"
> **Why it's wrong:** HTTPS certifies the connection is encrypted and the certificate chain validates — it says nothing about the legitimacy of the site itself. Phishing sites routinely have valid HTTPS.
> **✓ Correct Lead Approach:** Treat HTTPS as a baseline transport requirement, not a trust signal about content or identity — those need separate verification (domain reputation, user education, allow-listing for sensitive flows).

---

> ### ✕ Encrypting Bulk Data Directly With Asymmetric Crypto
> **Why it's wrong:** Asymmetric encryption is 100-1000x slower than symmetric for equivalent data sizes — using RSA/ECC to encrypt an entire payload directly is a real, measurable performance mistake.
> **✓ Correct Lead Approach:** Use asymmetric crypto only to exchange a symmetric key (exactly what TLS does), then encrypt the actual bulk data with AES.

---

> ### ✕ Treating a JWT's Payload as Confidential
> **Why it's wrong:** A JWT's header and payload are Base64URL-*encoded*, not encrypted — anyone holding the token can decode and read every claim inside it, whether or not they can forge a new valid token.
> **✓ Correct Lead Approach:** Never place secrets or sensitive PII directly in a JWT payload. Treat it as signed, not confidential — see this repo's [Authentication: JWT vs Sessions](/topic-detail.html?id=authentication-jwt-sessions) topic for the full mechanism.

## 🛠️ Practice Scenarios

### Scenario 1: The Reversible Password Store

**Problem:**
```javascript
const crypto = require('crypto');

function storePassword(password, secretKey) {
  const cipher = crypto.createCipheriv('aes-256-cbc', secretKey, iv);
  let encrypted = cipher.update(password, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return encrypted; // stored directly in the users table
}
```

A teammate has written this to store user passwords, reasoning "it's encrypted, so it's secure." Diagnose the flaw and propose the fix.

<details>
<summary>Staff-Level Solution</summary>

**The flaw:** this is reversible by design — anyone who obtains `secretKey` (a config file leak, a compromised server, an insider) can decrypt every stored password instantly. Encryption is the wrong primitive entirely for this use case; the goal here isn't "recoverable with a secret," it's "never recoverable by anyone, ever, including us."

**Fix:**
```javascript
const bcrypt = require('bcrypt');

async function storePassword(password) {
  const saltRounds = 12; // deliberately slow
  return bcrypt.hash(password, saltRounds); // salt is generated and embedded automatically
}

async function verifyLogin(password, storedHash) {
  return bcrypt.compare(password, storedHash);
}
```

**Lead framing:** "The fix isn't a stronger key or a better cipher — it's recognizing this was never an encryption problem. Hashing removes the key from the equation entirely, which is the actual security property we need here."

</details>

---

### Scenario 2: Explaining a Decoded JWT to a Worried Teammate

**Problem:**
```javascript
const token = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiI0MjIiLCJyb2xlIjoiYWRtaW4ifQ.dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk";
const payload = JSON.parse(atob(token.split('.')[1]));
console.log(payload); // { userId: "422", role: "admin" }
```

A teammate is alarmed that pasting any user's JWT into a browser console reveals their `userId` and `role` in plain readable JSON. Are they right to be alarmed?

<details>
<summary>Staff-Level Solution</summary>

**Partially — but for the wrong reason.** The payload being readable is expected and by design; a JWT is signed, not encrypted, so anyone holding a token can always decode its claims with nothing more than `atob`. This is not itself a vulnerability.

**What would actually be a vulnerability:** if the signing algorithm is HS256 (a shared secret) and that secret is weak or has leaked, someone could *forge* a new token with `role: "admin"` and a valid signature — that's the real risk this pattern should be evaluated for, not the payload being human-readable.

**Lead framing:** "The alarm is pointed at the wrong thing. The question isn't 'can someone read this,' the answer is always yes — the question is 'can someone produce a *different*, still-valid token,' which depends entirely on whether the signing key is well-protected and which algorithm is in use. I'd also flag that `role: admin` sitting directly in a long-lived token, readable by anyone who intercepts it, is worth reconsidering regardless — even non-forgeable, that's more information exposure than most tokens need."

</details>
