#include <wiringPi.h>
#include <lcd.h>

#define LCD_RST_PIN         = 27
#define LCD_DC_PIN          = 25
#define LCD_CS_PIN          = 8
#define LCD_BL_PIN          = 24

int main()
{
    int lcd;
    wiringPiSetup();
    lcd = lcdInit (2, 16, 8, 27, 25, 8, 24, 0, 0, 0, 0);

    lcdPuts(lcd, "Hello, world!");
}
