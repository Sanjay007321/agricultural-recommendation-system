# 🎤 Voice Input Troubleshooting Guide

## ⚡ Quick Fixes

### Issue: Voice input not working at all

**Solution 1: Check Browser**
```
✅ Recommended Browsers:
- Google Chrome (Best support)
- Microsoft Edge (Good support)
- Firefox (Limited support)
❌ Safari, Internet Explorer - Not supported
```

**Solution 2: Allow Microphone Permission**
1. Click the microphone icon in the chatbot
2. When browser asks for permission, click **"Allow"**
3. If you previously blocked it:
   - Click the lock icon 🔒 in the address bar
   - Change microphone permission to "Allow"
   - Refresh the page

---

## 🔍 Diagnostic Steps

### Step 1: Run Voice Input Test
Open the diagnostic test page:
```
1. Open: frontend/VOICE_INPUT_TEST.html in your browser
2. Follow the on-screen tests
3. Check results for each section
```

### Step 2: Check Console for Errors
```
1. Press F12 to open Developer Tools
2. Go to "Console" tab
3. Look for error messages when clicking microphone
4. Common errors and solutions below:
```

---

## ❌ Common Errors & Solutions

### Error: "not-allowed"
**Problem:** Microphone permission denied  
**Solution:**
1. Click lock icon 🔒 in address bar
2. Set Microphone to "Allow"
3. Refresh page (Ctrl+R or F5)

### Error: "no-speech"
**Problem:** No speech detected  
**Solution:**
1. Speak clearly into microphone
2. Check if microphone is muted
3. Move closer to microphone
4. Try in a quieter environment

### Error: "audio-capture"
**Problem:** No microphone found  
**Solution:**
1. Check if microphone is connected
2. Try a different USB port
3. Test microphone in system settings
4. Use headphones with built-in mic

### Error: "SpeechRecognition is not defined"
**Problem:** Browser doesn't support speech API  
**Solution:**
1. **Download Google Chrome**: https://www.google.com/chrome/
2. Or use Microsoft Edge
3. Update to latest browser version

---

## 🛠️ Browser-Specific Setup

### Google Chrome
```
✓ Best browser for voice input
✓ Full speech recognition support
✓ Works out of the box

Setup:
1. Open Chrome
2. Go to Settings > Privacy and security
3. Site Settings > Microphone
4. Ensure microphone access is enabled
```

### Microsoft Edge
```
✓ Good speech recognition support
✓ Chromium-based (same as Chrome)

Setup:
1. Open Edge
2. Go to Settings > Cookies and site permissions
3. Microphone
4. Enable microphone access
```

### Firefox
```
⚠ Limited speech recognition support
⚠ May require additional configuration

Note: Chrome or Edge recommended for best experience
```

---

## 🔧 Manual Testing

### Test 1: Check Browser Support
Open browser console (F12) and run:
```javascript
console.log('Speech API:', 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window);
console.log('Microphone API:', navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
```

**Expected Output:** Both should be `true`

### Test 2: Test Microphone
```javascript
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(() => console.log('✓ Microphone works!'))
  .catch(err => console.error('✗ Microphone error:', err));
```

**Expected Output:** "✓ Microphone works!"

---

## 📱 Windows/Mac Microphone Settings

### Windows 10/11
```
1. Settings > Privacy > Microphone
2. Enable "Allow apps to access your microphone"
3. Enable desktop apps access
4. Test microphone in Sound settings
```

### macOS
```
1. System Preferences > Security & Privacy > Privacy
2. Select Microphone
3. Ensure your browser is checked
4. Test microphone in Sound preferences
```

---

## 🌐 HTTPS Requirement

**Important:** Speech recognition requires a secure context

### Local Development (Works fine):
- ✅ `http://localhost:5173`
- ✅ `http://127.0.0.1:5173`

### Production (Requires HTTPS):
- ✅ `https://yourdomain.com`
- ❌ `http://yourdomain.com` (won't work)

**Solution for production:** Install SSL certificate

---

## 🔊 Microphone Volume Check

### Windows:
```
1. Right-click speaker icon
2. Sounds > Recording tab
3. Select your microphone
4. Properties > Levels
5. Set to 80-100%
```

### Mac:
```
1. System Preferences > Sound > Input
2. Select microphone
3. Adjust input volume to 80-100%
```

---

## 🧪 Testing Checklist

Test each component:

- [ ] Browser is Chrome or Edge
- [ ] Microphone is connected and working
- [ ] Browser has microphone permission
- [ ] VOICE_INPUT_TEST.html passes all tests
- [ ] No console errors
- [ ] Microphone volume is adequate
- [ ] Using HTTPS (for production)
- [ ] Latest browser version

---

## 💡 Tips for Better Recognition

1. **Speak clearly** - Enunciate words properly
2. **Reduce noise** - Minimize background noise
3. **Close to mic** - Stay 6-12 inches from microphone
4. **One sentence** - Speak in short phrases
5. **Good connection** - Ensure stable internet
6. **Update browser** - Keep browser up to date

---

## 🆘 Still Not Working?

### Last Resort Solutions:

1. **Reinstall Chrome:**
   - Uninstall current browser
   - Download fresh copy from google.com/chrome
   - Install and try again

2. **Try Different Computer:**
   - Test on another machine
   - Helps identify if it's hardware issue

3. **Use External Microphone:**
   - Built-in mics can fail
   - Try USB or Bluetooth microphone

4. **Check Firewall/Antivirus:**
   - Some security software blocks microphone
   - Temporarily disable to test

---

## 📞 Contact Support

If none of the above solutions work:

1. Run VOICE_INPUT_TEST.html
2. Take screenshot of results
3. Check browser console for errors
4. Note your browser name and version
5. Contact development team with this information

---

## ✅ Success Indicators

Voice input is working correctly when:

- ✓ Green microphone icon appears
- ✓ Clicking mic shows "Listening..." message
- ✓ Red pulse animation when active
- ✓ Speech transcribes to text automatically
- ✓ Message sends after speaking
- ✓ No error messages

---

**Quick Reference:**
- **Test Page:** `frontend/VOICE_INPUT_TEST.html`
- **Component:** `AIChatBot.jsx`
- **Browser:** Chrome or Edge recommended
- **Permission:** Microphone access required
- **Protocol:** HTTPS needed for production

**Status:** Ready to troubleshoot  
**Last Updated:** March 2026
