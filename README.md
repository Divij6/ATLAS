# ATLAS - AI-Powered Threat Detection & Live Alert System

ATLAS is an intelligent security monitoring system that combines real-time AI-powered threat detection with automated emergency response capabilities. The system analyzes live camera feeds to detect weapons and crowd anomalies, automatically alerting security personnel through multiple communication channels.

## Features

- **Weapon Detection**: Real-time identification of weapons using YOLO deep learning models
- **Crowd Panic Analysis**: Detection of anomalous crowd behavior using SVM-based machine learning
- **Multi-Channel Alerting**: Automated WhatsApp and voice call notifications to security personnel
- **Priority Escalation**: Intelligent escalation system through ranked contact lists
- **Video Recording**: Automatic clip recording and snapshot capture during threat events
- **Web Dashboard**: Live monitoring interface with threat visualization and management
- **Encrypted Storage**: End-to-end encryption of sensitive security data
- **GridFS Integration**: Efficient storage and retrieval of video files and images

## Technologies Used

### Backend
- **Python 3.8+** - Core application logic
- **Flask** - Web framework and API development
- **OpenCV** - Computer vision and video processing
- **YOLO (Ultralytics)** - Weapon detection deep learning model
- **Scikit-learn** - Crowd panic detection SVM model
- **MongoDB** - NoSQL database for scalable data storage
- **GridFS** - Large file storage system
- **Twilio** - SMS/WhatsApp and voice communication API

### Frontend
- **HTML5/CSS3** - User interface structure and styling
- **Bootstrap 5** - Responsive UI framework
- **JavaScript (ES6+)** - Client-side interactivity
- **WebRTC** - Real-time camera access

### Security & Utilities
- **Cryptography (Fernet)** - AES-256 encryption for data protection
- **Threading** - Concurrent processing for real-time operations
- **JSON** - Configuration and data exchange format

## System Requirements

### Hardware
- Webcam or IP camera for video input
- Minimum 4GB RAM (8GB recommended)
- GPU support recommended for faster AI inference

### Software Dependencies
```
Python 3.8+
MongoDB 4.4+
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/atlas-security-system.git
cd atlas-security-system
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up MongoDB**
- Install MongoDB Community Edition
- Start MongoDB service
- Update connection string in `appv2.py`

4. **Configure AI Models**
- Place YOLO weights file: `runs/detect/train3/weights/best.pt`
- Place SVM model file: `panic_detector_svm(4).pkl`

5. **Set up Twilio Configuration**
- Create `my_twilio_config.py` with your Twilio credentials:
```python
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"
TWILIO_VOICE_NUMBER = "+your_twilio_number"
TWIML_BIN_URL = "your_twiml_bin_url"
```

6. **Configure Emergency Contacts**
- Update `contacts.json` with security personnel information:
```json
[
  {"priority": 1, "name": "Security Chief", "phone": "+1234567890"},
  {"priority": 2, "name": "Backup Security", "phone": "+0987654321"}
]
```

7. **Generate Encryption Key**
```bash
python Key_Generation.py
```
- Copy the generated key to `EncryptionConfig.py`

## Usage

1. **Start the application**
```bash
python appv2.py
```

2. **Access the web interface**
- Open browser and navigate to `http://localhost:5000`
- Click "Start AI Detection" to begin monitoring
- View live camera feed with AI overlay annotations

3. **Monitor threats**
- Navigate to `/live_threats` for active threat dashboard
- Check `/neutralized` for resolved incidents
- Review `/police_stations` for emergency contact information

## API Endpoints

- `POST /api/start_detection` - Start AI threat detection
- `POST /api/stop_detection` - Stop threat detection
- `GET /api/detection_status` - Check system status
- `GET /api/threats` - Retrieve active threats
- `GET /api/neutralized` - Get neutralized threats
- `POST /api/neutralize/<id>` - Mark threat as resolved
- `GET /video_feed` - Live video stream endpoint

## Configuration

### Database Configuration
Update MongoDB connection string in `appv2.py`:
```python
MONGO_CONNECTION_STRING = "your_mongodb_connection_string"
```

### AI Model Tuning
- Weapon detection confidence threshold: `conf=0.80`
- Panic detection confidence threshold: `confidence > 0.85`
- Frame analysis chunk size: `chunk_size=30`

### Alert System Settings
- Call timeout duration: `CALL_TIMEOUT_SECONDS = 20`
- Video clip duration: `clip_duration = 10`
- Detection frame rate: `~30 FPS`

## Project Structure

```
atlas-security-system/
├── appv2.py                 # Main Flask application
├── predictv12.py            # Standalone AI detection script
├── static/                 # Static assets (CSS, JS, videos)
    ├── js                  # Frontend JavaScript controller
        ├── livecam.js
    ├── css                 # Application styling
        ├── styles.css              
├── contacts.json           # Emergency contact configuration
├── my_twilio_config.py     # Twilio API configuration
├── EncryptionConfig.py     # Encryption key storage
├── Key_Generation.py       # Encryption key generator
├── templates/              # HTML templates                
├── detection_clips/        # Generated video recordings
└── requirements.txt        # Python dependencies
```

## Security Considerations

- All sensitive data is encrypted using AES-256 encryption
- Database connections use secure authentication
- API endpoints implement proper authentication (add as needed)
- Video streams are processed locally to maintain privacy
- Contact information and threat data are encrypted at rest

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation for troubleshooting guides

## Acknowledgments

- YOLO object detection framework by Ultralytics
- OpenCV community for computer vision tools
- MongoDB for scalable database solutions
- Twilio for reliable communication APIs
- Flask community for web framework support

---

**Disclaimer**: This system is designed for educational and research purposes. Ensure compliance with local privacy laws and regulations before deployment in production environments.
