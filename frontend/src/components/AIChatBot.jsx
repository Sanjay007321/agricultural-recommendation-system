import { useState, useRef, useEffect } from "react";

const AIChatBot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Vanakkam! 🙏 I'm your Agricultural Assistant. How can I help you today?",
      sender: "bot",
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState("en"); // 'en' for English, 'ta' for Tamil
  const [isListening, setIsListening] = useState(false);
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);

  const translations = {
    en: {
      title: "Agricultural Assistant",
      placeholder: "Ask about crops, weather, diseases...",
      send: "Send",
      voice: "Voice Input",
      stopVoice: "Stop",
      lang: "தமிழ்",
      welcome: "Welcome! I'm your Agricultural Assistant. How can I help you today?",
      listening: "Listening...",
    },
    ta: {
      title: "வேளாண்மை உதவியாளர்",
      placeholder: "பயிர்கள், வானிலை, நோய்கள் பற்றி கேட்கவும்...",
      send: "அனுப்பு",
      voice: "குரல் உள்ளீடு",
      stopVoice: "நிறுத்து",
      lang: "English",
      welcome: "வணக்கம்! நான் உங்கள் வேளாண்மை உதவியாளர். நான் உங்களுக்கு எப்படி உதவ முடியும்?",
      listening: "செவிமடுக்கிறது...",
    },
  };

  const agriculturalKnowledge = {
    crops: {
      en: [
        "Rice: Requires warm climate, plenty of water, alluvial soil",
        "Wheat: Cool climate, moderate water, well-drained loamy soil",
        "Cotton: Warm climate, less water, black soil ideal",
        "Sugarcane: Hot climate, heavy irrigation, fertile soil",
        "Groundnut: Warm climate, light rainfall, sandy loam soil",
      ],
      ta: [
        "நெல்: சூடு காலநிலை, அதிக தண்ணீர், வண்டல் மண்",
        "கோதுமை: குளிர் காலநிலை, மிதமான தண்ணீர், களிமண் மண்",
        "பருத்தி: சூடு காலநிலை, குறைந்த தண்ணீர், கரிசல் மண்",
        "கரும்பு: சூடு காலநிலை, அதிக பாசனம், வளமான மண்",
        "வேர்க்கடலை: சூடு காலநிலை, லேசான மழை, மணல் கலந்த மண்",
      ],
    },
    diseases: {
      en: [
        "Blast (Rice): Use resistant varieties, proper drainage",
        "Rust (Wheat): Spray fungicides, crop rotation",
        "Bollworm (Cotton): Use pheromone traps, biopesticides",
        "Red Rot (Sugarcane): Remove affected plants, hot water treatment",
      ],
      ta: [
        "வெடிப்பு நோய் (நெல்): நோய் எதிர்ப்பு ரகங்கள், சரியான வடிகால்",
        "துரு நோய் (கோதுமை): பூஞ்சை மருந்துகள், பயிர் சுழற்சி",
        "இளம்புழு (பருத்தி): பாலூமோன் பொறிகள், உயிரி பூச்சிக்கொல்லிகள்",
        "சிவப்பு அழுகல் (கரும்பு): பாதிக்கப்பட்ட பயிர்களை அகற்று",
      ],
    },
    schemes: {
      en: [
        "PM-KISAN: ₹6000/year income support",
        "KCC: Kisan Credit Card for loans",
        "Soil Health Card: Free soil testing",
        "Namami Gange: Organic farming support",
      ],
      ta: [
        "பிஎம்-கிசான்: ₹6000/ஆண்டு வருமான ஆதரவு",
        "கேசிசி: விவசாய கடன் அட்டை",
        "மண் ஆரோக்கிய அட்டை: இலவச மண் பரிசோதனை",
        "நமமி கங்கை: இயற்கை விவசாய ஆதரவு",
      ],
    },
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Initialize Speech Recognition
    const initSpeechRecognition = () => {
      if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
        try {
          const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;
          recognitionRef.current = new SpeechRecognition();
          recognitionRef.current.continuous = false;
          recognitionRef.current.interimResults = false;
          recognitionRef.current.lang = language === "en" ? "en-US" : "ta-IN";
          recognitionRef.current.maxAlternatives = 1;

          recognitionRef.current.onstart = () => {
            console.log("Speech recognition started");
            setIsListening(true);
          };

          recognitionRef.current.onresult = (event) => {
            console.log("Speech recognition result:", event);
            const transcript = event.results[0][0].transcript;
            setInputText(transcript);
            setIsListening(false);
            
            // Auto-send after voice input
            setTimeout(() => {
              handleSendMessage();
            }, 500);
          };

          recognitionRef.current.onerror = (event) => {
            console.error("Speech recognition error:", event.error);
            setIsListening(false);
            
            let errorMessage = "Voice input failed. ";
            if (event.error === "not-allowed") {
              errorMessage += "Please allow microphone access.";
            } else if (event.error === "no-speech") {
              errorMessage += "No speech detected. Please try again.";
            } else if (event.error === "audio-capture") {
              errorMessage += "No microphone found.";
            }
            
            alert(errorMessage);
          };

          recognitionRef.current.onend = () => {
            console.log("Speech recognition ended");
            setIsListening(false);
          };
          
          console.log("Speech recognition initialized successfully");
        } catch (error) {
          console.error("Error initializing speech recognition:", error);
          alert("Voice input is not supported in this browser. Please use Chrome or Edge.");
        }
      } else {
        console.warn("Speech Recognition API not supported");
        alert("Your browser does not support voice input. Please use Google Chrome or Microsoft Edge.");
      }
    };

    initSpeechRecognition();
  }, [language]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const toggleLanguage = () => {
    setLanguage(language === "en" ? "ta" : "en");
    // Add system message for language change
    const langMsg =
      language === "en"
        ? "Language changed to Tamil"
        : "மொழி ஆங்கிலத்திற்கு மாற்றப்பட்டது";
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now(),
        text: langMsg,
        sender: "system",
        timestamp: new Date(),
      },
    ]);
  };

  const startListening = () => {
    if (!recognitionRef.current) {
      alert("Voice input is not available. Please use Chrome or Edge browser.");
      return;
    }
    
    if (isListening) {
      try {
        recognitionRef.current.stop();
        setIsListening(false);
      } catch (error) {
        console.error("Error stopping recognition:", error);
      }
    } else {
      try {
        // Request microphone permission first
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          navigator.mediaDevices.getUserMedia({ audio: true })
            .then(() => {
              recognitionRef.current.start();
              setIsListening(true);
            })
            .catch((err) => {
              console.error("Microphone permission error:", err);
              alert("Please allow microphone access to use voice input.");
            });
        } else {
          recognitionRef.current.start();
          setIsListening(true);
        }
      } catch (error) {
        console.error("Error starting recognition:", error);
        alert("Failed to start voice input. Please try again.");
        setIsListening(false);
      }
    }
  };

  const generateResponse = (userMessage) => {
    const lowerMsg = userMessage.toLowerCase();
    let response = "";

    // Crop-related queries
    if (
      lowerMsg.includes("rice") ||
      lowerMsg.includes("paddy") ||
      lowerMsg.includes("நெல்")
    ) {
      response =
        language === "en"
          ? agriculturalKnowledge.crops.en[0] +
            "\n\nFor rice cultivation, ensure proper water management and use quality seeds."
          : agriculturalKnowledge.crops.ta[0] +
            "\n\nநெல் சாகுபடிக்கு சரியான நீர் மேலாண்மை மற்றும் தரமான விதைகளை பயன்படுத்தவும்.";
    }
    // Disease-related queries
    else if (
      lowerMsg.includes("disease") ||
      lowerMsg.includes("pest") ||
      lowerMsg.includes("நோய்") ||
      lowerMsg.includes("பூச்சி")
    ) {
      response =
        language === "en"
          ? agriculturalKnowledge.diseases.en[0] +
            "\n\nPlease specify which crop's disease you're asking about."
          : agriculturalKnowledge.diseases.ta[0] +
            "\n\nநீங்கள் கேட்கும் பயிரின் நோயை குறிப்பிடவும்.";
    }
    // Weather queries
    else if (
      lowerMsg.includes("weather") ||
      lowerMsg.includes("climate") ||
      lowerMsg.includes("வானிலை")
    ) {
      response =
        language === "en"
          ? "For weather information, please check the Climate Board on your dashboard. It provides real-time temperature, humidity, and rainfall data."
          : "வானிலை தகவலுக்கு, உங்கள் டாشبோர்டில் உள்ள காலநிலை பலகையைப் பார்க்கவும். இது உண்மை நேர வெப்பநிலை, ஈரப்பதம் மற்றும் மழைப்பொழிவு தரவை வழங்குகிறது.";
    }
    // Scheme-related queries
    else if (
      lowerMsg.includes("scheme") ||
      lowerMsg.includes("loan") ||
      lowerMsg.includes("subsidy") ||
      lowerMsg.includes("திட்டம்") ||
      lowerMsg.includes("கடன்")
    ) {
      response =
        language === "en"
          ? agriculturalKnowledge.schemes.en[0] +
            "\n\nYou can apply for these schemes through your local agriculture office."
          : agriculturalKnowledge.schemes.ta[0] +
            "\n\nஉங்கள் உள்ளூர் வேளாண்மை அலுவலகம் மூலம் இந்த திட்டங்களுக்கு விண்ணப்பிக்கலாம்.";
    }
    // Greeting
    else if (
      lowerMsg.includes("hello") ||
      lowerMsg.includes("hi") ||
      lowerMsg.includes("வணக்கம்") ||
      lowerMsg.includes("வணக்கம்")
    ) {
      response =
        language === "en"
          ? "Hello! How can I assist you with farming today?"
          : "வணக்கம்! விவசாயத்தில் நான் உங்களுக்கு எப்படி உதவ முடியும்?";
    }
    // Default response
    else {
      response =
        language === "en"
          ? "Thank you for your question. I can help you with:\n• Crop selection and analysis\n• Disease identification\n• Weather information\n• Government schemes\n• Best farming practices\n\nPlease ask me anything related to agriculture!"
          : "உங்கள் கேள்விக்கு நன்றி. நான் உங்களுக்கு உதவ முடியும்:\n• பயிர் தேர்வு மற்றும் பகுப்பாய்வு\n• நோய் அடையாளம்\n• வானிலை தகவல்\n• அரசு திட்டங்கள்\n• சிறந்த விவசாய நடைமுறைகள்\n\nவேளாண்மை தொடர்பான எதையும் என்னிடம் கேட்கவும்!";
    }

    return response;
  };

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputText,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText("");
    setIsLoading(true);

    // Simulate bot response delay
    setTimeout(() => {
      const botResponse = {
        id: Date.now() + 1,
        text: generateResponse(inputText),
        sender: "bot",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botResponse]);
      setIsLoading(false);
    }, 800);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const t = translations[language];

  return (
    <>
      {/* Chat Toggle Button */}
      <button
        onClick={toggleChat}
        className={`fixed bottom-6 right-6 z-50 w-16 h-16 rounded-full shadow-2xl flex items-center justify-center transition-all duration-300 ${
          isOpen
            ? "bg-red-500 hover:bg-red-600"
            : "bg-green-600 hover:bg-green-700"
        }`}
      >
        {isOpen ? (
          <svg
            className="w-8 h-8 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        ) : (
          <svg
            className="w-8 h-8 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
        )}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 z-50 w-96 max-h-[600px] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-gray-200">
          {/* Header */}
          <div className="bg-gradient-to-r from-green-600 to-green-700 p-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
                <span className="text-2xl">🌾</span>
              </div>
              <div>
                <h3 className="text-white font-bold text-lg">{t.title}</h3>
                <p className="text-green-100 text-xs">
                  {language === "en" ? "Online" : "இணையத்தில்"}
                </p>
              </div>
            </div>
            <button
              onClick={toggleLanguage}
              className="px-3 py-1 bg-white/20 hover:bg-white/30 rounded-lg text-white text-sm font-semibold transition-colors"
            >
              {t.lang}
            </button>
          </div>

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 bg-gray-50 min-h-[400px] max-h-[500px]">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`mb-4 flex ${
                  message.sender === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                    message.sender === "user"
                      ? "bg-green-600 text-white"
                      : message.sender === "system"
                      ? "bg-gray-300 text-gray-700 text-center mx-auto"
                      : "bg-white text-gray-800 border border-gray-200"
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.text}</p>
                  {message.sender !== "system" && (
                    <p
                      className={`text-xs mt-1 ${
                        message.sender === "user"
                          ? "text-green-100"
                          : "text-gray-500"
                      }`}
                    >
                      {new Date(message.timestamp).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start mb-4">
                <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div
                      className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.2s" }}
                    ></div>
                    <div
                      className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.4s" }}
                    ></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 p-4 bg-white">
            <div className="flex items-center space-x-2">
              <button
                onClick={startListening}
                className={`p-2 rounded-lg transition-colors ${
                  isListening
                    ? "bg-red-500 text-white"
                    : "bg-gray-200 hover:bg-gray-300 text-gray-700"
                }`}
                title={t.voice}
              >
                {isListening ? (
                  <svg
                    className="w-5 h-5"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                    <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
                  </svg>
                ) : (
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                    />
                  </svg>
                )}
              </button>
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={isListening ? t.listening : t.placeholder}
                className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 text-sm"
                disabled={isListening}
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputText.trim() || isLoading}
                className="p-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 rounded-lg text-white transition-colors"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                  />
                </svg>
              </button>
            </div>
            {isListening && (
              <p className="text-xs text-red-500 mt-2 text-center animate-pulse">
                🔴 {t.listening}
              </p>
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default AIChatBot;
