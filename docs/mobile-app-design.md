# CheckMate Mobile App: Enhanced Problem Statement & Three-Factor Authentication Design

## 1. Introduction

In today’s world, traditional phone calls are no longer enough to guarantee secure, genuine communication. With the advent of deepfake technology, AI-generated voice and video impersonations, and sophisticated device compromises, it is increasingly challenging to know for sure who is on the other end of the line. 

CheckMate is designed to ensure that when you communicate with a loved one, such as a father in India and his daughter in the USA, you can be confident that the person you are speaking with is genuine. We achieve this through a multi-layered, three-factor authentication process that builds on the principles of "what you know, who you are, and what you have."

---

## 2. Enhanced Problem Statement

### Traditional Phone Call Vulnerabilities

- **What Traditional Phone Calls Provide:**  
  Traditional phone calls verify that a phone number is active, but they do not verify the identity of the caller. Caller ID can be spoofed, and phone numbers can be recycled or hijacked.

- **Threats in the Modern Era:**  
  - **Deepfakes & AI Impersonation:** Advanced deepfake technology can convincingly mimic voices and even create realistic video calls, making it nearly impossible to rely on audio or visual cues alone.
  - **Device Compromise:** Even if the phone number is authentic, a compromised device (e.g., through malware or physical theft) can be controlled by an unauthorized party, who might mimic the genuine user's behavior.
  - **Lack of Human Verification:** Automated systems can only verify device consistency or SIM ownership. They cannot ensure that the actual human user is in control.

### The Need for a Robust, Multi-Factor Approach

To address these challenges, CheckMate introduces three-factor authentication that combines:
- **What You Have:** The registered device, proven through a zero-knowledge proof (ZKP) protocol that verifies the device’s cryptographic identity.
- **Who You Are:** Biometrics (such as fingerprint or facial recognition) that confirm the physical presence and identity of the user.
- **What You Know:** A unique, pair-specific visual passcode (e.g., a sequence of symbols and colors) that only the genuine user would know, with an under-duress option that triggers an emergency response.

---

## 3. Three-Factor Authentication in CheckMate

### Factor 1: Device Verification ("What You Have")

- **Zero-Knowledge Proof (ZKP) Protocol:**  
  Each registered device generates cryptographic credentials during the initial registration phase. During a call, both devices run a ZKP protocol that verifies the device’s identity without revealing any sensitive data.
- **What It Proves:**  
  Confirms that the device currently in use is the same device that was registered. This protects against device replacement or unauthorized device tampering.

### Factor 2: Biometric Verification ("Who You Are")

- **Biometric Authentication:**  
  Immediately after the device verification, the app prompts the user to authenticate using biometrics (fingerprint or facial recognition). This step ensures that the person holding the device matches the registered biometric profile.
- **What It Proves:**  
  Provides real-time confirmation that the genuine user is present, preventing remote impersonation or the use of cloned devices.

### Factor 3: Pair-Specific Visual Passcode ("What You Know")

- **Unique Visual Passcode:**  
  During registration between two users (for example, between the father and his daughter), the initiating user (e.g., the father) sets a unique passcode composed of 4 symbols (triangles, circles, squares, spades) in a specific order, each chosen from a palette of 16 colors. This passcode is known only to him.
- **Interactive Challenge:**  
  During a verification session, after the device and biometric checks have passed, the father must enter the unique passcode.
  - **Standard Passcode:** A correct entry confirms that the device remains in the hands of someone who knows the pre-arranged secret.
  - **Under-Duress Option:** An alternative passcode can be configured which, if entered, discreetly triggers the phone to send its GPS location (including historical data) to the authorities, indicating that the user is under duress or the device is compromised.
- **What It Proves:**  
  Ensures that even if a device is stolen or compromised, the attacker is unlikely to know the pre-set visual challenge, thereby adding a strong layer of human knowledge to the authentication process.

---

## 4. Why This Approach is Superior to Traditional Phone Calls

- **Traditional Phone Calls:**  
  - Verify only phone number ownership.
  - Are susceptible to spoofing, deepfake impersonation, and device compromise.
  - Rely on static caller ID information, which does not confirm the actual identity of the user.

- **CheckMate's Three-Factor Authentication:**  
  - **Device Verification (What You Have):**  
    Confirms that the call is originating from the registered, uncompromised device.
  - **Biometric Verification (Who You Are):**  
    Ensures that the person using the device is indeed the legitimate user.
  - **Visual Passcode (What You Know):**  
    Provides a personalized, unique challenge that only the genuine user could answer, with an additional emergency mechanism (under-duress passcode) if needed.
  - **Combined Assurance:**  
    Even if a device is compromised, an attacker must overcome all three barriers to successfully impersonate the genuine user.

---

## 5. User Experience: A Real-World Scenario

Imagine a father on a call with his daughter:
- **Initial State:**  
  The father sees a clean interface with a “Verify Identity” button.
- **Upon Initiation:**  
  The app silently runs the ZKP protocol. A progress bar indicates that the device is being verified.
- **Biometric Prompt:**  
  The father is then asked to scan his fingerprint or use facial recognition. This step confirms that the person interacting is him.
- **Passcode Challenge:**  
  After a successful biometric scan, he is prompted to enter a unique visual passcode (4 symbols with colors) that he previously set for this family pair.
  - If the correct passcode is entered, his screen shows a bright green “Verified” badge.
  - If the under-duress passcode is entered (or the challenge fails), the app shows an alert and discreetly sends location data to the authorities.
- **Outcome:**  
  This layered process reassures the father that his device—and by extension, the daughter’s device—has not been compromised. It gives him the confidence to continue the call, knowing that even if the phone number is correct, the verification process confirms the genuine presence of his daughter.

---

## 6. Conclusion

CheckMate’s multi-factor authentication—combining device verification, biometric confirmation, and a unique visual passcode—provides robust protection against modern threats such as deepfakes, device compromises, and unauthorized impersonation. This approach offers a level of trust and security that traditional phone calls simply cannot match, ensuring that family connections remain secure even in the face of advanced technological threats.

---

This document encapsulates the enhanced problem statement and the design rationale for our three-factor authentication system, specifically tailored for protecting family communications. Let me know if you need any further adjustments or additional details!
