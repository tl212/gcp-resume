# LCD Display Wiring Guide for Arduino Uno

## 16x2 LCD Pin Connections

### Standard LCD (without I2C backpack)

| LCD Pin | LCD Function | Connect To Arduino | Wire Color (suggestion) |
|---------|--------------|-------------------|------------------------|
| 1 (VSS) | Ground | GND | Black |
| 2 (VDD) | Power +5V | 5V | Red |
| 3 (V0) | Contrast | Potentiometer center pin* | Orange |
| 4 (RS) | Register Select | Digital Pin 12 | Yellow |
| 5 (RW) | Read/Write | GND | Black |
| 6 (E) | Enable | Digital Pin 11 | Green |
| 7-10 | Data pins D0-D3 | Not connected | - |
| 11 (D4) | Data pin 4 | Digital Pin 5 | Blue |
| 12 (D5) | Data pin 5 | Digital Pin 4 | Purple |
| 13 (D6) | Data pin 6 | Digital Pin 3 | Gray |
| 14 (D7) | Data pin 7 | Digital Pin 2 | White |
| 15 (A) | Backlight Anode (+) | 5V (or through 220Ω resistor) | Red |
| 16 (K) | Backlight Cathode (-) | GND | Black |

*Potentiometer connections:
- Left pin → GND
- Center pin → LCD Pin 3 (V0)
- Right pin → 5V

## Step-by-Step Wiring Instructions

### Step 1: Power Connections
1. Connect LCD pin 1 (VSS) to Arduino GND
2. Connect LCD pin 2 (VDD) to Arduino 5V
3. Connect LCD pin 5 (RW) to Arduino GND

### Step 2: Contrast Control
1. Connect potentiometer left pin to GND
2. Connect potentiometer right pin to 5V
3. Connect potentiometer center pin to LCD pin 3 (V0)

### Step 3: Control Pins
1. Connect LCD pin 4 (RS) to Arduino pin 12
2. Connect LCD pin 6 (E) to Arduino pin 11

### Step 4: Data Pins (4-bit mode)
1. Connect LCD pin 11 (D4) to Arduino pin 5
2. Connect LCD pin 12 (D5) to Arduino pin 4
3. Connect LCD pin 13 (D6) to Arduino pin 3
4. Connect LCD pin 14 (D7) to Arduino pin 2

### Step 5: Backlight (Optional)
1. Connect LCD pin 15 (A) to 5V (use 220Ω resistor if too bright)
2. Connect LCD pin 16 (K) to GND

## Testing Your Connections

After wiring:
1. Power on the Arduino
2. Adjust the potentiometer until you see rectangles on the LCD
3. If you see rectangles, the wiring is correct!
4. Run the visitor_feeder.py script to display the count

## Troubleshooting

### Nothing appears on LCD:
- Check power connections (pins 1, 2)
- Adjust contrast potentiometer

### Only rectangles/blocks appear:
- Check data pin connections (pins 11-14 → Arduino pins 5,4,3,2)
- Check control pins (RS pin 4 → Arduino pin 12, E pin 6 → Arduino pin 11)

### Backlight not working:
- Check pins 15, 16 connections
- Add 220Ω resistor if backlight is too dim

### Garbled text:
- Verify all data pins are connected correctly
- Check that Arduino sketch matches pin configuration

## If You Have an I2C LCD (with backpack)

If your LCD has an I2C backpack (small board attached to back with 4 pins):

| I2C Pin | Connect To Arduino |
|---------|-------------------|
| VCC | 5V |
| GND | GND |
| SDA | A4 (Analog pin 4) |
| SCL | A5 (Analog pin 5) |
