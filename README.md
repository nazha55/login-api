## Firebase Setup
1. Download the Firebase private key from the Firebase Console.
2. Place the file in a secure location on your system (e.g., `/home/user/keys/private_key.json`).
3. Set the `FIREBASE_KEY_PATH` environment variable:
   ```bash
   export FIREBASE_KEY_PATH="/home/user/keys/private_key.json"
