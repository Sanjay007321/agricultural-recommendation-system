# AI Agricultural ChatBot Documentation

## Overview
The AI ChatBot is an intelligent agricultural assistant integrated into your crop management system. It provides real-time assistance to farmers in both **English** and **Tamil** languages with voice input capabilities.

## Features

### 1. **Bilingual Support** 🌐
- **English**: Full English language support
- **Tamil (தமிழ்)**: Complete Tamil language interface
- **Language Toggle**: Easy switch between languages with a single click

### 2. **Voice Input** 🎤
- Speech-to-text functionality for hands-free operation
- Supports both English and Tamil speech recognition
- Visual feedback when listening (red indicator)
- Compatible with modern browsers (Chrome, Edge, Firefox)

### 3. **Agricultural Knowledge Base** 🌾

#### Crop Information
- Rice/Paddy cultivation techniques
- Wheat growing conditions
- Cotton farming practices
- Sugarcane requirements
- Groundnut cultivation

#### Disease Management
- Crop disease identification
- Pest control measures
- Treatment recommendations
- Preventive measures

#### Government Schemes
- PM-KISAN scheme details
- Kisan Credit Card (KCC) information
- Soil Health Card program
- Various agricultural subsidies

#### Weather & Climate
- Real-time weather guidance
- Climate-specific recommendations
- Seasonal farming advice

### 4. **User Interface** 💻

#### Position
- Fixed at **bottom-right corner** of the screen
- Accessible from any page in the application
- Non-intrusive design

#### Chat Window
- Clean, modern interface
- Scrollable message history
- Timestamp for each message
- Loading indicators
- Responsive design

#### Controls
- **Green button**: Open chat
- **Red button**: Close chat
- **Microphone icon**: Voice input
- **Send button**: Submit message
- **Language button**: Toggle English/Tamil

## Usage Instructions

### Opening the ChatBot
1. Look for the green chat icon at the bottom-right corner
2. Click to open the chat window
3. The bot greets you with a welcome message

### Sending Messages
1. Type your question in the input field
2. Press Enter or click the send button
3. Wait for the bot's response (typically < 1 second)

### Using Voice Input
1. Click the microphone icon
2. Allow microphone access if prompted
3. Speak your question clearly
4. The bot will automatically transcribe your speech
5. Click send or press Enter

### Changing Language
1. Click the language button (shows "தமிழ்" or "English")
2. The interface switches immediately
3. Continue conversation in the new language

## Sample Questions

### In English:
- "What crops are suitable for warm climate?"
- "How to treat rice blast disease?"
- "Tell me about government schemes"
- "What is the ideal weather for wheat?"
- "How much loan can I get from KCC?"

### In Tamil:
- "நெல் சாகுபடிக்கு என்ன தேவை?" (What is needed for rice cultivation?)
- "பருத்தி நோய்களை எப்படி கட்டுப்படுத்துவது?" (How to control cotton diseases?)
- "அரசு திட்டங்கள் என்னென்ன?" (What are the government schemes?)
- "கோதுமைக்கு ஏற்ற காலநிலை என்ன?" (What is the suitable climate for wheat?)

## Technical Details

### Browser Compatibility
- ✅ Google Chrome (Recommended)
- ✅ Microsoft Edge
- ✅ Mozilla Firefox
- ⚠️ Safari (Limited voice support)

### Requirements
- Modern web browser with JavaScript enabled
- Microphone (for voice input)
- Internet connection

### Privacy
- Voice processing happens locally in the browser
- No audio recordings are stored or transmitted
- Chat history is session-based (cleared on refresh)

## Integration Points

### Current Implementation
- Integrated in `App.jsx` - available on all protected routes
- Appears on: Dashboard, Crop Analysis, History, Profile, Results pages
- Not shown on: Login, Register pages

### Customization Options

#### To modify agricultural knowledge:
Edit the `agriculturalKnowledge` object in `AIChatBot.jsx`:
```javascript
const agriculturalKnowledge = {
  crops: {
    en: ["Your crop information here"],
    ta: ["உங்கள் பயிர் தகவல் இங்கே"]
  }
};
```

#### To change position:
Modify the CSS classes in the chat button and window:
```jsx
className="fixed bottom-6 right-6 ..."  // Change these values
```

#### To adjust response logic:
Edit the `generateResponse()` function to add more intelligent responses.

## Future Enhancements

Potential improvements:
1. **API Integration**: Connect to real agricultural APIs
2. **ML Model**: Implement actual NLP for better understanding
3. **Image Recognition**: Allow users to upload diseased crop photos
4. **Location-based**: Provide district-specific recommendations
5. **Expert Connection**: Connect farmers with agricultural experts
6. **Chat History**: Save conversation history in database
7. **More Languages**: Add Hindi, Marathi, Punjabi, etc.

## Troubleshooting

### Voice input not working?
1. Check browser permissions for microphone
2. Ensure you're using a supported browser
3. Try Chrome or Edge for best compatibility

### Chat not appearing?
1. Clear browser cache
2. Check console for errors
3. Verify the component is imported correctly

### Tamil typing issues?
1. Use Unicode Tamil keyboard
2. Copy-paste from other sources works too
3. Consider using voice input instead

## Support

For technical issues or questions about the chatbot:
1. Check browser console for errors
2. Verify all dependencies are installed
3. Ensure proper internet connectivity
4. Contact development team for assistance

---

**Version**: 1.0  
**Last Updated**: March 2026  
**Author**: Agricultural AI Team
