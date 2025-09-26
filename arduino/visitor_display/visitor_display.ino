/*
 * Website Visitor Counter LCD Display
 * Displays visitor count from GCP Resume website on 16x2 LCD
 * Hardware: Arduino Uno + 16x2 LCD Display
 * Communication: Serial from Python script
 */

#include <LiquidCrystal.h>

// LCD pin connections - working configuration
LiquidCrystal lcd(4, 6, 10, 11, 12, 7);

// variables
long currentCount = 0;
long previousCount = 0;
unsigned long lastUpdateTime = 0;
const unsigned long UPDATE_INTERVAL = 1000; // check for updates every second

void setup() {
  // initialize Serial communication at 9600 baud
  Serial.begin(9600);
  
  // initialize 16x2 LCD
  lcd.begin(16, 2);
  
  // display startup message
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Visitor Counter");
  lcd.setCursor(0, 1);
  lcd.print("Initializing...");
  
  delay(2000); // Show startup message for 2 seconds
  
  // clear and show waiting message
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Waiting for");
  lcd.setCursor(0, 1);
  lcd.print("connection...");
  
  // send ready signal to Python script
  Serial.println("READY");
}

void loop() {
  // check if data is available from Serial
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim(); // remove any whitespace
    
    // check if input is a valid number
    if (isValidNumber(input)) {
      long newCount = input.toInt();
      
      // update count if it changed
      if (newCount != currentCount) {
        previousCount = currentCount;
        currentCount = newCount;
        lastUpdateTime = millis();
        
        // update display with animation if count increased
        if (currentCount > previousCount) {
          animateCountIncrease();
        } else {
          updateDisplay();
        }
        
        // send confirmation back to Python
        Serial.print("OK:");
        Serial.println(currentCount);
      }
    }
    // handle special commands
    else if (input == "PING") {
      Serial.println("PONG");
    }
    else if (input == "CLEAR") {
      lcd.clear();
      Serial.println("CLEARED");
    }
    else if (input == "STATUS") {
      Serial.print("COUNT:");
      Serial.println(currentCount);
    }
  }
  
  // display connection status if no updates for a while
  if (millis() - lastUpdateTime > 30000 && lastUpdateTime > 0) {
    displayConnectionLost();
    lastUpdateTime = 0; // reset to prevent repeated updates
  }
}

void updateDisplay() {
  lcd.clear();
  
  // first line - title
  lcd.setCursor(0, 0);
  lcd.print("Website Visitors");
  
  // second line - centered count
  lcd.setCursor(0, 1);
  String countStr = formatNumber(currentCount);
  int padding = (16 - countStr.length()) / 2;
  
  for (int i = 0; i < padding; i++) {
    lcd.print(" ");
  }
  lcd.print(countStr);
}

void animateCountIncrease() {
  // flash effect for new visitor
  for (int i = 0; i < 2; i++) {
    lcd.noDisplay();
    delay(100);
    lcd.display();
    delay(100);
  }
  
  // update with new count
  updateDisplay();
  
  // show increment briefly
  lcd.setCursor(0, 1);
  lcd.print("+1 ");
  delay(500);
  
  // show final count
  updateDisplay();
}

void displayConnectionLost() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connection Lost");
  lcd.setCursor(0, 1);
  lcd.print("Last: ");
  lcd.print(currentCount);
}

String formatNumber(long num) {
  // format number with commas for readability
  String numStr = String(num);
  String formatted = "";
  int len = numStr.length();
  
  for (int i = 0; i < len; i++) {
    if (i > 0 && (len - i) % 3 == 0) {
      formatted += ",";
    }
    formatted += numStr[i];
  }
  
  return formatted;
}

bool isValidNumber(String str) {
  if (str.length() == 0) return false;
  
  for (unsigned int i = 0; i < str.length(); i++) {
    if (!isDigit(str[i])) {
      return false;
    }
  }
  
  return true;
}
