# Cloud Resume Challenge - Retro Gaming Theme 🎮

A serverless resume website with a retro 8-bit gaming aesthetic, built on Google Cloud Platform following the Cloud Resume Challenge.

## 🚀 Live Demo
[View the live site](https://7l33.dev)

## 🏗️ Architecture

This project implements a fully serverless architecture on Google Cloud Platform with an optional hardware display component.

### Tech Stack
- **Frontend**: Static HTML/CSS/JS with retro gaming theme
- **Backend**: Python Cloud Function for visitor counter
- **Database**: Firestore for visitor data
- **Infrastructure**: Terraform IaC
- **CI/CD**: GitHub Actions with automated testing
- **Hardware Display** (Optional): Arduino Uno with LCD for physical visitor counter

## 🎨 Features
- Retro 8-bit gaming design with pixel art aesthetic
- Interactive animations and effects
- Serverless visitor counter with optional physical LCD display
- Responsive mobile-friendly layout
- CDN distribution for global performance
- SSL/HTTPS secured
- Arduino integration for real-world visitor count display

## 📂 Project Structure
```
frontend/website/    - Static website files
backend/            - Cloud Function code
terraform/          - Infrastructure as Code
tests/              - Unit and integration tests
.github/workflows/  - CI/CD pipeline
arduino/            - Arduino visitor display code
```

## 🖥️ Arduino Visitor Display (Optional)

This project includes an optional hardware component that displays the visitor count on a physical LCD display using an Arduino Uno.

### Hardware Requirements
- Arduino Uno
- 16x2 LCD Display (I2C or standard)
- Jumper wires
- USB cable for Arduino connection

### Setup Instructions
1. Connect your LCD display to the Arduino Uno:
   - For I2C LCD: SDA to A4, SCL to A5, VCC to 5V, GND to GND
   - For standard LCD: Follow standard 16x2 LCD wiring diagram

2. Install Arduino IDE and required libraries:
   ```bash
   # Install the LiquidCrystal library through Arduino IDE Library Manager
   ```

3. Upload the sketch:
   ```bash
   # Open arduino/visitor_display/visitor_display.ino in Arduino IDE
   # Select your Arduino board and port
   # Upload the sketch
   ```

4. The display will automatically fetch and show the visitor count from your live website

### Features
- Real-time visitor count updates
- Retro-styled LCD display matching the website theme
- Auto-refresh every 30 seconds
- Connection status indicators

## 🧪 Testing
```bash
# Install dependencies
pip install -r tests/requirements_test.txt

# Run tests
pytest tests/ -v
```

## 📝 License
MIT License

## 📬 Contact
- Website: [7l33.dev](https://7l33.dev)
- LinkedIn: [linkedin.com/in/tl212](https://www.linkedin.com/in/tl212/)
- GitHub: [github.com/tl212](https://github.com/tl212)
